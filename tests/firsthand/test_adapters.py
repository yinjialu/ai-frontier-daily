from scripts.firsthand.adapters import (
    extract_html_links, fetch_source, fetch_article_text,
    extract_title, fetch_article_title,
)

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
