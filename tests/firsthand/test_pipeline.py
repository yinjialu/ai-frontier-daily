from scripts.firsthand.pipeline import diff_new_articles, render_pr_body, cluster_same_event
from scripts.firsthand.summarize import SUMMARY_FAILED


def _a(source, title, url, summary="s"):
    return {"source": source, "title": title, "url": url, "summary": summary}


def test_cluster_groups_cross_source_by_shared_bigram():
    arts = [
        _a("anthropic-news", "Introducing Claude Tag", "u1"),
        _a("claude-blog", "Agent identity in Claude Tag", "u2"),
        _a("openai-news", "OpenAI ships new voice model", "u3"),
    ]
    groups = cluster_same_event(arts)
    # Claude Tag 两篇(不同源,共享 bigram "claude tag")归一组；voice 单独
    multi = [g for g in groups if len(g) > 1]
    assert len(multi) == 1
    assert {a["url"] for a in multi[0]} == {"u1", "u2"}


def test_cluster_does_not_group_same_source():
    arts = [
        _a("claude-blog", "Claude Managed Agents memory", "u1"),
        _a("claude-blog", "Claude Managed Agents updates", "u2"),
    ]
    # 同源不归并(归并只针对跨源同事件)
    assert all(len(g) == 1 for g in cluster_same_event(arts))


def test_cluster_does_not_group_on_single_common_word():
    arts = [
        _a("claude-blog", "Claude Opus 4.8 released", "u1"),
        _a("anthropic-news", "Claude Code desktop redesign", "u2"),
    ]
    # 仅共享单词 "claude"(无共享 bigram)→ 不归并
    assert all(len(g) == 1 for g in cluster_same_event(arts))


def test_render_pr_body_shows_same_event_section():
    arts = [
        _a("anthropic-news", "Introducing Claude Tag", "u1", "新功能"),
        _a("claude-blog", "Agent identity in Claude Tag", "u2", "访问模型"),
    ]
    body = render_pr_body(arts)
    assert "🔗 疑似同一事件" in body
    assert "u1" in body and "u2" in body

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
