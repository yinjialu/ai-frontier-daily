"""Private, same-origin reading and feedback service behind Tailscale Serve.

Never bind this service beyond loopback: Serve supplies the verified identity.
Only allowlisted static files are exposed; private state remains in SQLite.
"""
import argparse
from contextlib import closing
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
import os
from pathlib import Path
import re
import sqlite3
from urllib.parse import unquote, urlsplit
from zoneinfo import ZoneInfo

from . import preferences, store

ROOT = Path(__file__).resolve().parents[2]


def live_editions(db):
    from .worker import news
    groups = {}
    # The same factual/date gates and preference ordering as the next digest.
    for rank, original in enumerate(news(db, hours=168)):
        item = dict(original, feed_rank=rank)
        date = item['published'][:10]
        groups.setdefault((item['vendor'], date), []).append(item)
    result = {}
    for (vendor, date), items in groups.items():
        dt = datetime.fromisoformat(date)
        result[(vendor, date)] = {
            'vendor': vendor, 'date': date.replace('-', '.'), 'cnDate': f'{dt.month}月{dt.day}日',
            'edition': dt.strftime('VOL.%j'), 'brand': 'AI 前哨 · 待审核',
            'updates': [dict(url=i['url'], company=i['company'], feed_rank=i['feed_rank'], **{
                k: i['editorial'][k] for k in ('tag', 'title', 'summary')}) for i in items],
            'outroTitle': '官方一手动态', 'outroDesc': '人工审核后发布', 'outroCta': 'AI 前哨',
        }
    return result


def archive_item(root, vendor, date, url):
    if not re.fullmatch(r'[a-z0-9_-]{1,40}', str(vendor)) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(date)):
        return None
    path = (root / 'data' / vendor / f'{date}.json').resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        return None
    target = preferences.canonical_url(url)
    for item in json.loads(path.read_text()).get('updates', []):
        candidate = item.get('url') or item.get('source')
        try:
            if preferences.canonical_url(candidate) == target:
                return dict(item, vendor=vendor, url=candidate,
                            company=item.get('company') or vendor)
        except (ValueError, TypeError):
            continue
    return None


def trusted_item(db, root, payload):
    target = preferences.canonical_url(payload.get('url'))
    # Resolve current server items first, including changelog updates sharing URLs.
    for row in db.execute('SELECT curated FROM items WHERE curated IS NOT NULL ORDER BY detected DESC'):
        try:
            item = json.loads(row[0])
            if item.get('editorial', {}).get('relevant') is True and preferences.canonical_url(item['url']) == target:
                return item
        except (ValueError, TypeError, KeyError, AttributeError):
            # An old malformed row cannot prevent feedback on healthy content.
            continue
    item = archive_item(root, payload.get('vendor'), payload.get('archive_date'), target)
    if item is None:
        raise ValueError('unknown article')
    return item


class FeedbackServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address, *, root, state, origin, owner, dev=False):
        if address[0] != '127.0.0.1':
            raise ValueError('feedback service must bind to loopback')
        self.root, self.state = Path(root), Path(state)
        self.origin, self.owner, self.dev = origin.rstrip('/'), owner, dev
        if not owner and not dev:
            raise ValueError('Tailscale owner login is required')
        super().__init__(address, Handler)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Request paths are sufficient for diagnostics; never log POST payloads.
        super().log_message(format, *args)

    def connect(self):
        return store.connect(self.server.state / 'frontier.db')

    def authorized(self):
        if self.headers.get('Host') != urlsplit(self.server.origin).netloc:
            self.json_response(403, {'error': 'host not allowed'})
            return False
        if not self.server.dev and self.headers.get('Tailscale-User-Login') != self.server.owner:
            self.json_response(403, {'error': 'owner access required'})
            return False
        return True

    def json_response(self, status, body):
        data = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if path == '/healthz':
            return self.json_response(200, {'ok': True})
        if not self.authorized():
            return
        try:
            if path == '/api/feedback':
                with closing(self.connect()) as db:
                    return self.json_response(200, {'enabled': True,
                        'entries': preferences.list_feedback(db),
                        'summary': preferences.preference_summary(db)})
            if path == '/output/index.json':
                data = json.loads((self.server.root / 'output/index.json').read_text())
                with closing(self.connect()) as db:
                    live = live_editions(db)
                records = {(r.get('vendor', 'anthropic'), r['date']): r for r in data['days']}
                for (vendor, date), edition in live.items():
                    records[(vendor, date)] = {'vendor': vendor, 'date': date, 'count': len(edition['updates'])}
                data['days'] = sorted(records.values(), key=lambda r: (r['date'], r['vendor']))
                data['mode'] = 'private'
                data['updated'] = max(r['date'] for r in data['days'])
                data['checked_at'] = datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
                return self.json_response(200, data)
            match = re.fullmatch(r'/data/([a-z0-9_-]{1,40})/(\d{4}-\d{2}-\d{2})\.json', path)
            if match:
                with closing(self.connect()) as db:
                    data = live_editions(db).get(match.groups())
                if data is not None:
                    return self.json_response(200, data)
            return self.serve_static(path)
        except (ValueError, OSError, KeyError, sqlite3.Error):
            return self.json_response(503, {'error': 'data temporarily unavailable'})

    def serve_static(self, path):
        name = 'index.html' if path == '/' else path.lstrip('/')
        allowed = name == 'index.html' or bool(re.fullmatch(r'assets/[a-zA-Z0-9_.-]+\.(?:js|css)', name)) or name in {
            'skills/ai-daily-digest/cards.js', 'skills/ai-daily-digest/cards.css'} or bool(
            re.fullmatch(r'data/[a-z0-9_-]{1,40}/\d{4}-\d{2}-\d{2}\.json', name))
        full = (self.server.root / name).resolve()
        if not allowed or not full.is_relative_to(self.server.root.resolve()) or not full.is_file():
            return self.json_response(404, {'error': 'not found'})
        data = full.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', (mimetypes.guess_type(full.name)[0] or 'application/octet-stream') + '; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if not self.authorized():
            return
        if urlsplit(self.path).path != '/api/feedback':
            return self.json_response(404, {'error': 'not found'})
        if self.headers.get('Origin') != self.server.origin or self.headers.get('Sec-Fetch-Site', 'same-origin') not in {'same-origin', 'none'}:
            return self.json_response(403, {'error': 'same-origin required'})
        if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
            return self.json_response(415, {'error': 'JSON required'})
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if size < 1 or size > 8192:
                return self.json_response(413, {'error': 'invalid payload size'})
            payload = json.loads(self.rfile.read(size))
            if not isinstance(payload, dict):
                raise ValueError('invalid payload')
            with closing(self.connect()) as db:
                item = trusted_item(db, self.server.root, payload)
                result = preferences.record_feedback(db, item, payload.get('action'), payload.get('request_id'))
                result['summary'] = preferences.preference_summary(db)
                return self.json_response(200, result)
        except (ValueError, TypeError, KeyError):
            return self.json_response(400, {'error': 'invalid feedback or unknown article'})
        except (OSError, sqlite3.Error):
            return self.json_response(503, {'error': 'data temporarily unavailable'})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8791)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--state', type=Path, default=Path(os.getenv('FRONTIER_STATE_DIR', ROOT / '.server-state')))
    parser.add_argument('--origin', required=True)
    parser.add_argument('--owner', default=os.getenv('FRONTIER_OWNER_LOGIN', ''))
    parser.add_argument('--dev', action='store_true', help='local testing only; loopback and exact Origin still required')
    args = parser.parse_args()
    server = FeedbackServer(('127.0.0.1', args.port), root=args.root, state=args.state,
                            origin=args.origin, owner=args.owner, dev=args.dev)
    server.serve_forever()


if __name__ == '__main__':
    main()
