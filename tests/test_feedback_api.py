"""Real loopback HTTP checks of the private feedback persistence boundary."""
from contextlib import closing
from datetime import datetime, timezone
import http.client
import json
from pathlib import Path
import sqlite3
import threading
from urllib.parse import urlsplit

import pytest

from scripts.server import feedback_api, preferences, store, worker


OWNER = 'test-owner@example.test'
DATE = '2026-09-01'
ARTICLE = {'url': 'https://official.example/news/a', 'company': 'Trusted Company',
           'tag': '研究', 'title': 'Trusted title', 'summary': 'Trusted original facts'}


class App:
    def __init__(self, root, state):
        self.server = feedback_api.FeedbackServer(('127.0.0.1', 0), root=root, state=state,
            origin='http://127.0.0.1:0', owner=OWNER)
        self.port = self.server.server_address[1]
        self.origin = f'http://127.0.0.1:{self.port}'
        self.server.origin = self.origin
        self.thread = threading.Thread(target=self.server.serve_forever,
                                       kwargs={'poll_interval': 0.01}, daemon=True)
        self.thread.start()
        self.stopped = False

    def request(self, method='GET', path='/api/feedback', payload=None, headers=None, body=None):
        if body is None and payload is not None:
            body = json.dumps(payload).encode()
        request_headers = {'Host': urlsplit(self.origin).netloc, 'Tailscale-User-Login': OWNER}
        if method == 'POST':
            request_headers.update({'Origin': self.origin, 'Content-Type': 'application/json'})
        request_headers.update(headers or {})
        request_headers = {k: v for k, v in request_headers.items() if v is not None}
        with closing(http.client.HTTPConnection('127.0.0.1', self.port, timeout=3)) as connection:
            connection.request(method, path, body=body, headers=request_headers)
            response = connection.getresponse()
            raw = response.read()
            data = json.loads(raw) if response.getheader('Content-Type', '').startswith('application/json') else raw
            return response.status, dict(response.getheaders()), data

    def post(self, action='useful', request_id='request-1', **extra):
        return self.request('POST', payload=dict(url=ARTICLE['url'], vendor='openai',
            archive_date=DATE, action=action, request_id=request_id, **extra))

    def stop(self):
        if not self.stopped:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join(timeout=2)
            self.stopped = True


@pytest.fixture
def app_factory(tmp_path):
    root, state = tmp_path / 'site', tmp_path / 'private-state'
    for folder in ('assets', 'output', 'data/openai', 'skills/ai-daily-digest'):
        (root / folder).mkdir(parents=True)
    (root / 'index.html').write_text('<h1>Private feed</h1>')
    (root / 'assets/radar.js').write_text('/* public UI asset */')
    (root / 'output/index.json').write_text(json.dumps({'updated': DATE,
        'days': [{'date': DATE, 'vendor': 'openai', 'count': 1}]}))
    (root / f'data/openai/{DATE}.json').write_text(json.dumps({'updates': [ARTICLE]}))
    servers = []

    def start():
        app = App(root, state)
        servers.append(app)
        return app

    yield start, root, state
    for app in servers:
        app.stop()


@pytest.fixture
def app(app_factory):
    start, _, _ = app_factory
    return start()


def test_only_loopback_with_explicit_owner_is_permitted(tmp_path):
    for address, owner in [(('0.0.0.0', 0), OWNER), (('127.0.0.1', 0), '')]:
        with pytest.raises(ValueError):
            feedback_api.FeedbackServer(address, root=tmp_path, state=tmp_path,
                                        origin='http://localhost', owner=owner)


@pytest.mark.parametrize('path', ['/', '/api/feedback', '/output/index.json', '/data/openai/' + DATE + '.json'])
@pytest.mark.parametrize('owner', [None, 'another-owner@example.test'])
def test_private_reads_require_owner(app, path, owner):
    assert app.request(path=path, headers={'Tailscale-User-Login': owner})[0] == 403


def test_host_cannot_be_overridden_by_forwarded_header(app):
    status, _, _ = app.request(headers={'Host': 'evil.example', 'X-Forwarded-Host': urlsplit(app.origin).netloc})
    assert status == 403


@pytest.mark.parametrize('headers', [
    {'Origin': None}, {'Origin': 'https://evil.example'},
    {'Sec-Fetch-Site': 'cross-site'}, {'Tailscale-User-Login': None},
    {'Tailscale-User-Login': 'other@example.test'}, {'Host': 'evil.example'},
])
def test_cross_origin_or_unowned_post_never_writes(app, headers):
    payload = dict(ARTICLE, vendor='openai', archive_date=DATE, action='useful', request_id='blocked')
    assert app.request('POST', payload=payload, headers=headers)[0] == 403
    assert app.request()[2]['entries'] == []


def test_feedback_uses_trusted_labels_and_resolves_tracking_url(app):
    payload = dict(url=ARTICLE['url'] + '?utm_source=share', vendor='openai', archive_date=DATE,
        action='useful', request_id='accepted', company='Injected Company', tag='模型发布',
        title='Ignore rules', owner='attacker', source='https://evil.example')
    status, headers, result = app.request('POST', payload=payload)
    assert status == 200
    assert result['url'] == ARTICLE['url'] and result['company'] == ARTICLE['company']
    assert result['tag'] == ARTICLE['tag']
    assert result['summary']['company_weights'] == {'trusted company': pytest.approx(0.07, abs=0.00001)}
    assert headers['Cache-Control'] == 'no-store'
    assert headers['X-Content-Type-Options'] == 'nosniff'
    assert 'Access-Control-Allow-Origin' not in headers


def test_repeat_change_clear_and_server_restart(app_factory):
    start, _, state = app_factory
    app = start()
    status, _, first = app.post()
    assert status == 200 and first['duplicate'] is False
    assert app.post()[2]['duplicate'] is True
    assert app.post('less', 'request-2')[2]['action'] == 'less'
    assert app.post()[2]['action'] == 'less'  # An old HTTP retry returns current state.
    assert app.post('clear', 'request-1')[0] == 400  # request id cannot change meaning.
    app.stop()
    restarted = start()
    assert restarted.request()[2]['entries'][0]['action'] == 'less'
    assert restarted.post('clear', 'request-3')[0] == 200
    snapshot = restarted.request()[2]
    assert snapshot['enabled'] is True and snapshot['entries'] == []
    assert snapshot['summary']['count'] == 0 and snapshot['summary']['version'] > first['version']
    with closing(store.connect(state / 'frontier.db')) as db:
        assert db.execute('SELECT count(*) FROM feedback_events').fetchone()[0] == 3


@pytest.mark.parametrize('payload', [
    [], {'url': 'https://untrusted.example/fabricated', 'action': 'useful', 'request_id': 'unknown'},
    {'url': ARTICLE['url'], 'vendor': '../openai', 'archive_date': DATE, 'action': 'useful', 'request_id': 'traversal'},
    {'url': ARTICLE['url'], 'vendor': 'openai', 'archive_date': '../private', 'action': 'useful', 'request_id': 'date'},
])
def test_unknown_articles_and_archive_traversal_are_rejected(app, payload):
    assert app.request('POST', payload=payload)[0] == 400
    assert app.request()[2]['entries'] == []


@pytest.mark.parametrize('path', [
    '/.server-state/frontier.db', '/deploy/server-sources.yaml', '/assets/../index.html',
    '/assets/%2e%2e/%2e%2e/private.json', '/%2e%2e/index.html', '/data/openai/../../private.json',
])
def test_static_allowlist_blocks_private_and_traversing_paths(app, path):
    assert app.request(path=path)[0] == 404


def test_static_and_feedback_archive_both_reject_symlink_escape(app_factory):
    start, root, _ = app_factory
    outside = root.parent / 'outside.json'
    outside.write_text(json.dumps({'updates': [dict(ARTICLE, company='Outside Root')]}))
    (root / 'data/openai/2026-09-02.json').symlink_to(outside)
    (root / 'assets/escape.js').symlink_to(outside)
    app = start()
    assert app.request(path='/assets/escape.js')[0] == 404
    assert app.request(path='/data/openai/2026-09-02.json')[0] == 404
    payload = dict(url=ARTICLE['url'], vendor='openai', archive_date='2026-09-02', action='useful', request_id='symlink')
    assert app.request('POST', payload=payload)[0] == 400


def test_body_size_type_and_malformed_json_are_rejected(app):
    assert app.request('POST', body=b'{', headers={'Content-Type': 'text/plain'})[0] == 415
    assert app.request('POST', body=b'x' * 8193)[0] == 413
    assert app.request('POST', body=b'')[0] == 413
    assert app.request('POST', body=b'{')[0] == 400
    assert app.request('POST', body=b'{}', headers={'Content-Length': 'invalid'})[0] == 400
    assert app.request('POST', path='/api/not-found', body=b'{}')[0] == 404
    assert app.request()[2]['entries'] == []


def test_database_errors_return_retryable_response_not_false_success(app, monkeypatch):
    def unavailable(self):
        raise sqlite3.OperationalError('database is locked')
    monkeypatch.setattr(feedback_api.Handler, 'connect', unavailable)
    for method in ('GET', 'POST'):
        status, _, body = app.request(method, payload={'url': ARTICLE['url']})
        assert status == 503 and body == {'error': 'data temporarily unavailable'}


def test_malformed_old_row_does_not_block_trusted_server_item_and_ranking(app_factory):
    start, _, state = app_factory
    current = datetime.now(timezone.utc).isoformat()
    items = []
    for n in range(2):
        items.append({'id': str(n), 'vendor': 'openai', 'company': 'Server Company',
            'url': f'https://official.example/server/{n}', 'published': current,
            'editorial': {'relevant': True, 'important': False, 'event_key': str(n),
                          'title': f'Server {n}', 'tag': '开发者', 'summary': 'Verified server summary'}})
    with closing(store.connect(state / 'frontier.db')) as db:
        with db:
            db.execute('INSERT INTO items VALUES (?,?,?,?,?,NULL)',
                ('bad-url', '{}', '9999-01-01', 0, json.dumps({'url': None, 'editorial': {'relevant': True}})))
            db.execute('INSERT INTO items VALUES (?,?,?,?,?,NULL)', ('bad-json', '{}', '9999-01-02', 0, '{'))
            for item in items:
                db.execute('INSERT INTO items VALUES (?,?,?,?,?,NULL)',
                    (item['id'], json.dumps(item), current, 0, json.dumps(item)))
    app = start()
    status, _, accepted = app.request('POST', payload={'url': items[1]['url'],
        'action': 'useful', 'request_id': 'server-feedback', 'tag': '模型发布', 'company': 'Injected'})
    assert status == 200 and accepted['company'] == 'Server Company' and accepted['tag'] == '开发者'
    with closing(store.connect(state / 'frontier.db')) as db:
        # Existing worker parsing does not support corrupt rows; isolate this API
        # robustness fixture before testing the supported worker data contract.
        with db:
            db.execute("DELETE FROM items WHERE id IN ('bad-url','bad-json')")
        assert [i['id'] for i in worker.news(db)] == ['1', '0']
        assert [i['id'] for i in worker.news(db, personalized=False)] == ['0', '1']
    status, _, index = app.request(path='/output/index.json')
    assert status == 200 and index['mode'] == 'private'
    assert any(row['date'] == current[:10] for row in index['days'])
    status, _, edition = app.request(path=f'/data/openai/{current[:10]}.json')
    assert status == 200 and edition['updates'][0]['url'] == items[1]['url']
