from scripts.firsthand.pipeline import diff_new_articles, render_pr_body
from scripts.firsthand.summarize import SUMMARY_FAILED

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

def test_render_pr_body_marks_failed_summary():
    articles = [
        {"source": "claude-blog", "title": "A", "url": "https://c/blog/a",
         "summary": "正常摘要。"},
        {"source": "claude-blog", "title": "B", "url": "https://c/blog/b",
         "summary": SUMMARY_FAILED},
    ]
    body = render_pr_body(articles)
    # 顶部有失败汇总提示
    assert "⚠️ 1 篇摘要生成失败" in body
    # 失败的那条标题带 ⚠️，正常的不带
    assert "[B](https://c/blog/b) ⚠️" in body
    assert "[A](https://c/blog/a)\n" in body
    assert " ⚠️\n  > 正常摘要。" not in body

def test_render_pr_body_no_warning_when_all_ok():
    articles = [
        {"source": "claude-blog", "title": "A", "url": "https://c/blog/a",
         "summary": "正常摘要。"},
    ]
    body = render_pr_body(articles)
    assert "⚠️" not in body
    assert "## claude-blog" in body
