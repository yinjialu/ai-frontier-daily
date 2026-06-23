from scripts.firsthand.adapters import extract_html_links, fetch_source, fetch_article_text

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
