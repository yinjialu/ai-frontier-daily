import json
from pathlib import Path
from scripts import monitor_firsthand
from scripts.monitor_firsthand import _firsthand_pr_title, _source_counts_from_pr_files, run_once


def test_firsthand_pr_title_counts_all_pr_files():
    files = [
        {"path": "data/firsthand/openai-news/04-a.md"},
        {"path": "data/firsthand/openai-news/05-b.md"},
        {"path": "data/firsthand/google-gemini/03-a.md"},
        {"path": "data/firsthand/anthropic-news/14-a.md"},
        {"path": "data/firsthand/anthropic-news/14-b.md"},
        {"path": "README.md"},
    ]

    counts = _source_counts_from_pr_files(files)
    title = _firsthand_pr_title("firsthand/2026-07-01", counts)

    assert counts == {
        "anthropic-news": 2,
        "google-gemini": 1,
        "openai-news": 2,
    }
    assert title == (
        "📡 内参新动态 | 2026-07-01 "
        "(anthropic-news 2篇, openai-news 2篇, google-gemini 1篇)"
    )


def test_run_once_first_run_no_pr(tmp_path, monkeypatch):
    yaml_file = tmp_path / "sources.yaml"
    yaml_file.write_text(
        "sources:\n"
        "  - id: demo\n"
        "    name: Demo\n"
        "    url: https://demo/blog\n"
        "    type: html-links\n"
        "    link_prefix: /blog/\n"
        "    base_url: https://demo\n",
        encoding="utf-8",
    )
    okf_root = tmp_path / "firsthand"
    state_file = tmp_path / "state.json"

    fetched = [{"url": "https://demo/blog/a", "title": "A"},
               {"url": "https://demo/blog/b", "title": "B"}]
    calls = {"pr": 0}
    result = run_once(
        sources_path=yaml_file,
        okf_root=okf_root,
        state_file=state_file,
        now="2026-06-23T15:30:00+08:00",
        fetch_fn=lambda s: fetched,
        article_text_fn=lambda u: "body",
        summarize_fn=lambda t, b: {"summary": "摘要", "tags": ["x"]},
        open_pr_fn=lambda branch, articles: calls.__setitem__("pr", calls["pr"] + 1),
        commit_state_fn=lambda: None,
    )
    assert calls["pr"] == 0
    assert result["new_count"] == 0


def test_run_once_second_run_opens_pr(tmp_path):
    yaml_file = tmp_path / "sources.yaml"
    yaml_file.write_text(
        "sources:\n  - id: demo\n    name: Demo\n    url: https://demo/blog\n"
        "    type: html-links\n    link_prefix: /blog/\n    base_url: https://demo\n",
        encoding="utf-8",
    )
    okf_root = tmp_path / "firsthand"
    state_file = tmp_path / "state.json"
    (okf_root / "demo").mkdir(parents=True)
    (okf_root / "demo" / "01-a.md").write_text(
        "---\nresource: https://demo/blog/a\n---\n", encoding="utf-8")

    fetched = [{"url": "https://demo/blog/a", "title": "A"},
               {"url": "https://demo/blog/b", "title": "B"}]
    captured = {}
    run_once(
        sources_path=yaml_file, okf_root=okf_root, state_file=state_file,
        now="2026-06-23T15:30:00+08:00",
        fetch_fn=lambda s: fetched,
        article_text_fn=lambda u: "body",
        article_published_fn=lambda u: "2026-05-01",
        summarize_fn=lambda t, b: {"summary": "摘要", "tags": ["x"]},
        open_pr_fn=lambda branch, articles: captured.update(branch=branch, articles=articles),
        commit_state_fn=lambda: None,
    )
    assert captured["branch"].startswith("firsthand/")
    assert [a["url"] for a in captured["articles"]] == ["https://demo/blog/b"]
    # 文件名只用 slug（无探测日期）；frontmatter 记真实发布日期 + 探测时间
    okf = okf_root / "demo" / "02-b.md"
    assert okf.exists()
    txt = okf.read_text(encoding="utf-8")
    assert "published: 2026-05-01" in txt
    assert "detected: 2026-06-23T15:30:00+08:00" in txt


def test_run_once_heartbeat_separate_and_state_stable(tmp_path):
    """无新文章时连续两轮，state.json 应完全一致（last_checked 不进 state，
    避免每小时心跳把 main 刷屏）；last_checked 写入独立 heartbeat 文件并随时间更新。"""
    yaml_file = tmp_path / "sources.yaml"
    yaml_file.write_text(
        "sources:\n  - id: demo\n    name: Demo\n    url: https://demo/blog\n"
        "    type: html-links\n    link_prefix: /blog/\n    base_url: https://demo\n",
        encoding="utf-8",
    )
    okf_root = tmp_path / "firsthand"
    state_file = tmp_path / "state.json"
    (okf_root / "demo").mkdir(parents=True)
    (okf_root / "demo" / "01-a.md").write_text(
        "---\nresource: https://demo/blog/a\n---\n", encoding="utf-8")

    fetched = [{"url": "https://demo/blog/a", "title": "A"}]  # 已入库 → 无新文章
    common = dict(
        sources_path=yaml_file, okf_root=okf_root, state_file=state_file,
        fetch_fn=lambda s: fetched, article_text_fn=lambda u: "body",
        summarize_fn=lambda t, b: {"summary": "x", "tags": []},
        open_pr_fn=lambda b, a: None, commit_state_fn=lambda: None,
    )
    run_once(now="2026-06-23T10:00:00+08:00", **common)
    s1 = state_file.read_text(encoding="utf-8")
    run_once(now="2026-06-23T11:00:00+08:00", **common)
    s2 = state_file.read_text(encoding="utf-8")
    assert s1 == s2, "无新文章时 state.json 不应变（否则每小时 commit 刷屏）"
    assert "last_checked" not in json.loads(s2)["demo"]
    hb = json.loads((tmp_path / ".firsthand-heartbeat.json").read_text(encoding="utf-8"))
    assert hb["demo"] == "2026-06-23T11:00:00+08:00"


def test_run_once_fetches_title_when_missing(tmp_path):
    """html-links 抓到的条目 title=None 时，应调 article_title_fn 取文章页标题，
    而非回退成 URL。"""
    yaml_file = tmp_path / "sources.yaml"
    yaml_file.write_text(
        "sources:\n  - id: demo\n    name: Demo\n    url: https://demo/blog\n"
        "    type: html-links\n    link_prefix: /blog/\n    base_url: https://demo\n",
        encoding="utf-8",
    )
    okf_root = tmp_path / "firsthand"
    state_file = tmp_path / "state.json"
    (okf_root / "demo").mkdir(parents=True)
    (okf_root / "demo" / "01-a.md").write_text(
        "---\nresource: https://demo/blog/a\n---\n", encoding="utf-8")

    fetched = [{"url": "https://demo/blog/a", "title": None},
               {"url": "https://demo/blog/b", "title": None}]
    captured = {}
    run_once(
        sources_path=yaml_file, okf_root=okf_root, state_file=state_file,
        now="2026-06-23T15:30:00+08:00",
        fetch_fn=lambda s: fetched,
        article_text_fn=lambda u: "body",
        article_title_fn=lambda u: "真实标题 B",
        article_published_fn=lambda u: None,
        summarize_fn=lambda t, b: {"summary": "摘要", "tags": ["x"]},
        open_pr_fn=lambda branch, articles: captured.update(articles=articles),
        commit_state_fn=lambda: None,
    )
    # 新文章 b 的标题来自 article_title_fn，不是 URL
    assert captured["articles"][0]["title"] == "真实标题 B"
    assert (okf_root / "demo" / "02-b.md").exists()


def test_run_once_corrupt_state_open_pr_without_initialized_is_first_run(tmp_path):
    """state 部分损坏：有 open_pr_urls 但无 initialized、且无 OKF 文件，
    仍应当首刊静默处理（不开 PR），不误开全量历史 PR。"""
    yaml_file = tmp_path / "sources.yaml"
    yaml_file.write_text(
        "sources:\n  - id: demo\n    name: Demo\n    url: https://demo/blog\n"
        "    type: html-links\n    link_prefix: /blog/\n    base_url: https://demo\n",
        encoding="utf-8",
    )
    okf_root = tmp_path / "firsthand"
    state_file = tmp_path / "state.json"
    # 部分损坏 state：有 open_pr_urls 但缺 initialized，且无任何 OKF 文件
    state_file.write_text(
        json.dumps({"demo": {"open_pr_urls": ["https://demo/blog/old"]}}),
        encoding="utf-8",
    )

    fetched = [{"url": "https://demo/blog/a", "title": "A"},
               {"url": "https://demo/blog/b", "title": "B"}]
    calls = {"pr": 0}
    result = run_once(
        sources_path=yaml_file, okf_root=okf_root, state_file=state_file,
        now="2026-06-23T15:30:00+08:00",
        fetch_fn=lambda s: fetched,
        article_text_fn=lambda u: "body",
        summarize_fn=lambda t, b: {"summary": "摘要", "tags": ["x"]},
        open_pr_fn=lambda branch, articles: calls.__setitem__("pr", calls["pr"] + 1),
        commit_state_fn=lambda: None,
    )
    assert calls["pr"] == 0
    assert result["new_count"] == 0
    st = json.loads(state_file.read_text(encoding="utf-8"))["demo"]
    assert st.get("initialized") is True


def test_run_once_first_run_sets_initialized_flag(tmp_path):
    """首刊后 state 应写入 initialized=True，且不再有 total_articles_seen 旧字段。"""
    yaml_file = tmp_path / "sources.yaml"
    yaml_file.write_text(
        "sources:\n  - id: demo\n    name: Demo\n    url: https://demo/blog\n"
        "    type: html-links\n    link_prefix: /blog/\n    base_url: https://demo\n",
        encoding="utf-8",
    )
    okf_root = tmp_path / "firsthand"
    state_file = tmp_path / "state.json"
    fetched = [{"url": "https://demo/blog/a", "title": "A"}]
    run_once(
        sources_path=yaml_file, okf_root=okf_root, state_file=state_file,
        now="2026-06-23T15:30:00+08:00",
        fetch_fn=lambda s: fetched,
        article_text_fn=lambda u: "body",
        summarize_fn=lambda t, b: {"summary": "摘要", "tags": ["x"]},
        open_pr_fn=lambda branch, articles: None,
        commit_state_fn=lambda: None,
    )
    st = json.loads(state_file.read_text(encoding="utf-8"))["demo"]
    assert st["initialized"] is True
    assert "total_articles_seen" not in st


def test_run_once_second_run_records_known_urls_count(tmp_path):
    """非首刊分支应写 known_urls_count（旧字段名 total_articles_seen 不再出现）。"""
    yaml_file = tmp_path / "sources.yaml"
    yaml_file.write_text(
        "sources:\n  - id: demo\n    name: Demo\n    url: https://demo/blog\n"
        "    type: html-links\n    link_prefix: /blog/\n    base_url: https://demo\n",
        encoding="utf-8",
    )
    okf_root = tmp_path / "firsthand"
    state_file = tmp_path / "state.json"
    (okf_root / "demo").mkdir(parents=True)
    (okf_root / "demo" / "01-a.md").write_text(
        "---\nresource: https://demo/blog/a\n---\n", encoding="utf-8")

    fetched = [{"url": "https://demo/blog/a", "title": "A"}]
    run_once(
        sources_path=yaml_file, okf_root=okf_root, state_file=state_file,
        now="2026-06-23T15:30:00+08:00",
        fetch_fn=lambda s: fetched,
        article_text_fn=lambda u: "body",
        summarize_fn=lambda t, b: {"summary": "摘要", "tags": ["x"]},
        open_pr_fn=lambda branch, articles: None,
        commit_state_fn=lambda: None,
    )
    st = json.loads(state_file.read_text(encoding="utf-8"))["demo"]
    assert "known_urls_count" in st
    assert "total_articles_seen" not in st


def test_run_once_pr_failure_does_not_crash_or_mark_seen(tmp_path):
    """开 PR 失败时：run_once 不崩、不把文章标记已见（下轮可重试）。"""
    yaml_file = tmp_path / "sources.yaml"
    yaml_file.write_text(
        "sources:\n  - id: demo\n    name: Demo\n    url: https://demo/blog\n"
        "    type: html-links\n    link_prefix: /blog/\n    base_url: https://demo\n",
        encoding="utf-8",
    )
    okf_root = tmp_path / "firsthand"
    state_file = tmp_path / "state.json"
    (okf_root / "demo").mkdir(parents=True)
    (okf_root / "demo" / "01-a.md").write_text(
        "---\nresource: https://demo/blog/a\n---\n", encoding="utf-8")

    fetched = [{"url": "https://demo/blog/a", "title": "A"},
               {"url": "https://demo/blog/b", "title": "B"}]
    def boom(branch, articles):
        raise RuntimeError("gh failed")
    result = run_once(
        sources_path=yaml_file, okf_root=okf_root, state_file=state_file,
        now="2026-06-23T15:30:00+08:00",
        fetch_fn=lambda s: fetched, article_text_fn=lambda u: "body",
        article_published_fn=lambda u: None,
        summarize_fn=lambda t, b: {"summary": "x", "tags": []},
        open_pr_fn=boom, commit_state_fn=lambda: None,
    )
    # 不崩，new_count=0（PR 失败未计），b 未被标记已见
    assert result["new_count"] == 0
    import json
    st = json.loads(state_file.read_text(encoding="utf-8"))["demo"]
    assert "https://demo/blog/b" not in st.get("open_pr_urls", [])


def test_run_once_article_fetch_failure_skips_only_failed_article(tmp_path):
    """单篇正文抓取失败时，不应拖垮整轮；失败 URL 不标记已见，留待下轮重试。"""
    yaml_file = tmp_path / "sources.yaml"
    yaml_file.write_text(
        "sources:\n  - id: demo\n    name: Demo\n    url: https://demo/blog\n"
        "    type: html-links\n    link_prefix: /blog/\n    base_url: https://demo\n",
        encoding="utf-8",
    )
    okf_root = tmp_path / "firsthand"
    state_file = tmp_path / "state.json"
    (okf_root / "demo").mkdir(parents=True)
    (okf_root / "demo" / "01-a.md").write_text(
        "---\nresource: https://demo/blog/a\n---\n", encoding="utf-8")

    fetched = [
        {"url": "https://demo/blog/a", "title": "A"},
        {"url": "https://demo/blog/bad", "title": "Bad"},
        {"url": "https://demo/blog/good", "title": "Good"},
    ]

    def article_text(url):
        if url.endswith("/bad"):
            raise RuntimeError("404 Not Found")
        return "body"

    captured = {}
    result = run_once(
        sources_path=yaml_file, okf_root=okf_root, state_file=state_file,
        now="2026-06-23T15:30:00+08:00",
        fetch_fn=lambda s: fetched,
        article_text_fn=article_text,
        article_published_fn=lambda u: None,
        summarize_fn=lambda t, b: {"summary": "x", "tags": []},
        open_pr_fn=lambda branch, articles: captured.update(articles=articles),
        commit_state_fn=lambda: None,
    )

    assert result["new_count"] == 1
    assert result["fetch_failures"] == [{
        "source": "demo",
        "url": "https://demo/blog/bad",
        "error": "RuntimeError: 404 Not Found",
    }]
    assert [a["url"] for a in captured["articles"]] == ["https://demo/blog/good"]

    st = json.loads(state_file.read_text(encoding="utf-8"))["demo"]
    assert "https://demo/blog/good" in st.get("open_pr_urls", [])
    assert "https://demo/blog/bad" not in st.get("open_pr_urls", [])
    assert (okf_root / "demo" / "02-good.md").exists()


def test_real_open_pr_stages_only_current_article_paths(monkeypatch):
    """更新已有 PR 时只 stage 本轮写出的 OKF，避免扫入工作树遗留文件。"""
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        class Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return Result()

    monkeypatch.setattr(monitor_firsthand, "_existing_open_pr", lambda branch: "94")
    monkeypatch.setattr(monitor_firsthand, "_refresh_pr_title", lambda pr_num, branch: None)
    monkeypatch.setattr(monitor_firsthand.subprocess, "run", fake_run)

    monitor_firsthand._real_open_pr("firsthand/2026-07-02", [{
        "source": "demo",
        "title": "Demo article",
        "url": "https://demo/article",
        "summary": "摘要",
        "okf_path": "data/firsthand/demo/02-article.md",
    }])

    assert ["git", "add", "data/firsthand/demo/02-article.md"] in calls
    assert ["git", "add", "data/firsthand/"] not in calls
