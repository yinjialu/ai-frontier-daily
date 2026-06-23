from scripts.firsthand.adapters import extract_html_links, fetch_source

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
