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
