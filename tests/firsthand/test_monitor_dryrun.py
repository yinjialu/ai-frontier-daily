import json
from pathlib import Path
from scripts.monitor_firsthand import run_once


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
    (okf_root / "demo" / "2026-06-22-a.md").write_text(
        "---\nresource: https://demo/blog/a\n---\n", encoding="utf-8")

    fetched = [{"url": "https://demo/blog/a", "title": "A"},
               {"url": "https://demo/blog/b", "title": "B"}]
    captured = {}
    run_once(
        sources_path=yaml_file, okf_root=okf_root, state_file=state_file,
        now="2026-06-23T15:30:00+08:00",
        fetch_fn=lambda s: fetched,
        article_text_fn=lambda u: "body",
        summarize_fn=lambda t, b: {"summary": "摘要", "tags": ["x"]},
        open_pr_fn=lambda branch, articles: captured.update(branch=branch, articles=articles),
        commit_state_fn=lambda: None,
    )
    assert captured["branch"].startswith("firsthand/")
    assert [a["url"] for a in captured["articles"]] == ["https://demo/blog/b"]
    assert (okf_root / "demo" / "2026-06-23-b.md").exists()


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
    (okf_root / "demo" / "2026-06-22-a.md").write_text(
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
