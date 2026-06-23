from scripts.firsthand.pipeline import diff_new_articles

def test_diff_excludes_ingested_and_open_pr():
    fetched = [
        {"url": "https://c/blog/a", "title": "A"},
        {"url": "https://c/blog/b", "title": "B"},
        {"url": "https://c/blog/c", "title": "C"},
    ]
    ingested = {"https://c/blog/a"}
    open_pr = {"https://c/blog/b"}
    new = diff_new_articles(fetched, ingested, open_pr)
    assert [a["url"] for a in new] == ["https://c/blog/c"]

def test_diff_first_run_all_new_when_nothing_known():
    fetched = [{"url": "https://c/blog/a", "title": "A"}]
    assert diff_new_articles(fetched, set(), set()) == fetched
