from scripts.firsthand.adapters import (
    extract_html_links, fetch_source, fetch_article_text,
    extract_title, fetch_article_title,
    parse_human_date, extract_published, fetch_article_published,
)


def test_parse_human_date():
    assert parse_human_date("Apr 23, 2026") == "2026-04-23"
    assert parse_human_date("Jun 18, 2026") == "2026-06-18"
    assert parse_human_date("Jan 6, 2025") == "2025-01-06"
    assert parse_human_date("没有日期") is None


def test_extract_html_links_attaches_published_from_listing():
    # engineering 风格：日期在链接文本里
    html = '''
    <a href="/engineering/managed-agents">Managed Agents Apr 08, 2026</a>
    <a href="/engineering/no-date-post">Featured Post</a>
    '''
    source = {"link_prefix": "/engineering/", "base_url": "https://www.anthropic.com"}
    items = extract_html_links(html, source)
    by_url = {i["url"]: i for i in items}
    assert by_url["https://www.anthropic.com/engineering/managed-agents"]["published"] == "2026-04-08"
    assert by_url["https://www.anthropic.com/engineering/no-date-post"]["published"] is None


def test_extract_published_from_jsonld():
    html = '<html><script type="application/ld+json">{"@type":"BlogPosting","datePublished":"Jun 18, 2026"}</script></html>'
    assert extract_published(html) == "2026-06-18"


def test_extract_published_from_iso_meta():
    html = '<meta property="article:published_time" content="2026-03-24T10:00:00Z"/>'
    assert extract_published(html) == "2026-03-24"


def test_extract_published_none_when_absent():
    assert extract_published("<html><body>no date</body></html>") is None


def test_fetch_article_published_uses_fetcher():
    html = '<script type="application/ld+json">{"datePublished":"Feb 05, 2026"}</script>'
    assert fetch_article_published("http://x", fetcher=lambda u: html) == "2026-02-05"

SAMPLE_HTML = '''
<html><body>
<a href="/blog/post-a">Post A</a>
<a href="/blog/post-b/?utm=x">Post B</a>
<a href="/about">About</a>
<a href="/blog/post-a">Dup</a>
</body></html>
'''

def test_extract_html_links_filters_prefix_and_dedups():
    source = {"link_prefix": "/blog/", "base_url": "https://claude.com"}
    items = extract_html_links(SAMPLE_HTML, source)
    urls = {i["url"] for i in items}
    assert urls == {
        "https://claude.com/blog/post-a",
        "https://claude.com/blog/post-b",
    }

def test_fetch_source_unknown_type_raises():
    try:
        fetch_source({"id": "x", "type": "nope"}, fetcher=lambda u: "")
        assert False, "should raise"
    except ValueError:
        pass

def test_fetch_article_text_strips_tags():
    html = "<html><head><style>x{}</style></head><body><h1>Hi</h1><p>Hello world</p><script>bad()</script></body></html>"
    text = fetch_article_text("http://x", fetcher=lambda u: html)
    assert "Hi" in text
    assert "Hello world" in text
    assert "bad()" not in text
    assert "x{}" not in text

def test_extract_title_prefers_h1():
    html = "<html><head><title>Artifacts in Claude Code | Claude</title></head><body><h1>Artifacts in Claude Code</h1></body></html>"
    assert extract_title(html) == "Artifacts in Claude Code"

def test_extract_title_falls_back_to_cleaned_title_tag():
    html = "<html><head><title>Some Post \\ Anthropic</title></head><body><p>no h1 here</p></body></html>"
    assert extract_title(html) == "Some Post"

def test_extract_title_strips_pipe_site_suffix():
    html = "<html><head><title>Hello World | Claude</title></head><body></body></html>"
    assert extract_title(html) == "Hello World"

def test_extract_title_none_when_absent():
    assert extract_title("<html><body><p>x</p></body></html>") is None

def test_fetch_article_title_uses_fetcher():
    html = "<html><body><h1>My Headline</h1></body></html>"
    assert fetch_article_title("http://x", fetcher=lambda u: html) == "My Headline"
