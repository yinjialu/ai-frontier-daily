import re
import requests
import feedparser
from html.parser import HTMLParser
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .urls import canonical_url, make_absolute

_HREF_RE = re.compile(r'href="([^"]+)"')
_UA = {"User-Agent": "Mozilla/5.0 (firsthand-monitor)"}

# launchd may inherit a stale HTTP(S)_PROXY from the interactive session that
# installed or restarted it. Public firsthand sources are reachable directly
# on the host, so do not let requests silently route them through that proxy.
# Keep a small retry budget for transient CDN/connection failures.
_HTTP = requests.Session()
_HTTP.trust_env = False
_HTTP.headers.update(_UA)
_HTTP.mount("https://", HTTPAdapter(max_retries=Retry(
    total=3,
    connect=3,
    read=3,
    status=2,
    backoff_factor=0.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=frozenset({"GET"}),
    respect_retry_after_header=True,
)))
_HTTP.mount("http://", HTTPAdapter(max_retries=Retry(
    total=3,
    connect=3,
    read=3,
    status=2,
    backoff_factor=0.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=frozenset({"GET"}),
    respect_retry_after_header=True,
)))

_MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}
# "Apr 23, 2026" / "Jan 6, 2025"
_HUMAN_DATE_RE = re.compile(
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),?\s+(\d{4})")
# ISO 日期前缀（article:published_time / time datetime）
_ISO_DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
_JSONLD_DATE_RE = re.compile(r'"datePublished"\s*:\s*"([^"]+)"')
_META_PUBLISHED_RE = re.compile(
    r'article:published_time"[^>]*content="([^"]+)"')


def parse_human_date(text: str) -> str | None:
    """把 'Apr 23, 2026' 解析成 ISO 'YYYY-MM-DD'；无匹配返回 None。"""
    m = _HUMAN_DATE_RE.search(text or "")
    if not m:
        return None
    mon = _MONTHS[m.group(1)]
    return f"{int(m.group(3)):04d}-{mon:02d}-{int(m.group(2)):02d}"


def _http_get(url: str) -> str:
    resp = _HTTP.get(url, timeout=20)
    resp.raise_for_status()
    return resp.text


def _listing_dates(html: str, prefix: str, base: str) -> dict:
    """从 <a href="prefix...">...文本...</a> 块里提取每个 URL 的发布日期（若有）。
    engineering 列表把日期写在链接文本内；claude-blog 链接文本是 'Read more'（无日期）。"""
    block_re = re.compile(
        r'<a[^>]*href="(' + re.escape(prefix) + r'[^"]+)"[^>]*>(.*?)</a>',
        re.DOTALL | re.IGNORECASE)
    out = {}
    for href, inner in block_re.findall(html):
        d = parse_human_date(re.sub(r"<[^>]+>", " ", inner))
        if d:
            out[canonical_url(make_absolute(href, base))] = d
    return out


def extract_html_links(html: str, source: dict) -> list[dict]:
    prefix = source["link_prefix"]
    base = source["base_url"]
    dates = _listing_dates(html, prefix, base)
    seen, out = set(), []
    for href in _HREF_RE.findall(html):
        if not href.startswith(prefix):
            continue
        url = canonical_url(make_absolute(href, base))
        if url in seen:
            continue
        seen.add(url)
        out.append({"url": url, "title": None, "published": dates.get(url)})
    return out


def extract_published(html: str) -> str | None:
    """从文章页 HTML 提取真实发布日期 → ISO 'YYYY-MM-DD'。
    依次尝试 JSON-LD datePublished、article:published_time、首个 ISO 日期。"""
    m = _JSONLD_DATE_RE.search(html)
    if m:
        v = m.group(1)
        iso = _ISO_DATE_RE.search(v)
        if iso:
            return iso.group(0)
        return parse_human_date(v)
    m = _META_PUBLISHED_RE.search(html)
    if m:
        iso = _ISO_DATE_RE.search(m.group(1))
        if iso:
            return iso.group(0)
    return None


def fetch_article_published(url: str, fetcher=_http_get) -> str | None:
    return extract_published(fetcher(url))


def _fetch_html_links(source: dict, fetcher) -> list[dict]:
    return extract_html_links(fetcher(source["url"]), source)


def _fetch_rss(source: dict, fetcher) -> list[dict]:
    feed = feedparser.parse(fetcher(source["url"]))
    out = []
    for e in feed.entries:
        link = getattr(e, "link", None)
        if not link:
            continue
        # feed entry 自带发布时间 → 直接取 published（ISO 日期），免逐篇抓文章页
        published = None
        tm = getattr(e, "published_parsed", None) or getattr(e, "updated_parsed", None)
        if tm:
            published = f"{tm.tm_year:04d}-{tm.tm_mon:02d}-{tm.tm_mday:02d}"
        out.append({"url": canonical_url(link), "title": getattr(e, "title", None),
                    "published": published})
    return out


def _fetch_github_org(source: dict, fetcher) -> list[dict]:
    """调 GitHub API 列举 org 的公开仓库，按 created 时间倒序。
    每个仓库 → {url: github页面, title: repo名, published: 创建日期}。
    source 需包含 org 字段（GitHub org name）。"""
    import json
    org = source.get("org") or source["id"]
    url = f"https://api.github.com/orgs/{org}/repos?sort=created&direction=desc&per_page=50"
    data = json.loads(fetcher(url))
    out = []
    for repo in data:
        if repo.get("fork"):
            continue
        created = (repo.get("created_at") or "")[:10]  # YYYY-MM-DD
        out.append({
            "url": canonical_url(repo["html_url"]),
            "title": repo.get("full_name") or repo["name"],
            "published": created or None,
        })
    return out


_ADAPTERS = {"html-links": _fetch_html_links, "rss": _fetch_rss, "github-org": _fetch_github_org}


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


class _TitleExtractor(HTMLParser):
    """抓 <h1>（文章标题，最干净）与 <title>（兜底）。"""

    def __init__(self):
        super().__init__()
        self._in_title = False
        self._in_h1 = False
        self.title_tag = None
        self.h1 = None

    def handle_starttag(self, tag, attrs):
        if tag == "title" and self.title_tag is None:
            self._in_title = True
        elif tag == "h1" and self.h1 is None:
            self._in_h1 = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False

    def handle_data(self, data):
        if self._in_title:
            self.title_tag = (self.title_tag or "") + data
        if self._in_h1:
            self.h1 = (self.h1 or "") + data


# <title> 常带站点后缀，如 "标题 | Claude" / "标题 \ Anthropic" / "标题 - X"
_TITLE_SUFFIX_RE = re.compile(r"\s*[|\\\-–—]\s*[^|\\\-–—]+$")


def extract_title(html: str) -> str | None:
    """优先 <h1>；无则取 <title> 并剥掉站点名后缀。都没有返回 None。"""
    p = _TitleExtractor()
    p.feed(html)
    if p.h1 and p.h1.strip():
        return p.h1.strip()
    if p.title_tag and p.title_tag.strip():
        return _TITLE_SUFFIX_RE.sub("", p.title_tag.strip()).strip() or p.title_tag.strip()
    return None


def fetch_article_title(url: str, fetcher=_http_get) -> str | None:
    return extract_title(fetcher(url))
