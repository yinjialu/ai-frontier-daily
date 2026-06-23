import re
import requests
import feedparser
from html.parser import HTMLParser
from .urls import canonical_url, make_absolute

_HREF_RE = re.compile(r'href="([^"]+)"')
_UA = {"User-Agent": "Mozilla/5.0 (firsthand-monitor)"}


def _http_get(url: str) -> str:
    resp = requests.get(url, timeout=20, headers=_UA)
    resp.raise_for_status()
    return resp.text


def extract_html_links(html: str, source: dict) -> list[dict]:
    prefix = source["link_prefix"]
    base = source["base_url"]
    seen, out = set(), []
    for href in _HREF_RE.findall(html):
        if not href.startswith(prefix):
            continue
        url = canonical_url(make_absolute(href, base))
        if url in seen:
            continue
        seen.add(url)
        out.append({"url": url, "title": None})
    return out


def _fetch_html_links(source: dict, fetcher) -> list[dict]:
    return extract_html_links(fetcher(source["url"]), source)


def _fetch_rss(source: dict, fetcher) -> list[dict]:
    feed = feedparser.parse(fetcher(source["url"]))
    out = []
    for e in feed.entries:
        link = getattr(e, "link", None)
        if not link:
            continue
        out.append({"url": canonical_url(link), "title": getattr(e, "title", None)})
    return out


_ADAPTERS = {"html-links": _fetch_html_links, "rss": _fetch_rss}


def fetch_source(source: dict, fetcher=_http_get) -> list[dict]:
    """按 type 分派到适配器。fetcher 可注入便于测试。返回 [{url,title}]。"""
    adapter = _ADAPTERS.get(source["type"])
    if adapter is None:
        raise ValueError(f"未知 source type: {source['type']}")
    return adapter(source, fetcher)


class _TextExtractor(HTMLParser):
    _SKIP = {"script", "style", "noscript"}

    def __init__(self):
        super().__init__()
        self._skip_depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if self._skip_depth == 0:
            t = data.strip()
            if t:
                self.parts.append(t)


def fetch_article_text(url: str, fetcher=_http_get) -> str:
    parser = _TextExtractor()
    parser.feed(fetcher(url))
    return "\n".join(parser.parts)
