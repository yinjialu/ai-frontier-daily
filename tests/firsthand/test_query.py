import json
from pathlib import Path
from scripts.firsthand.query import (
    filter_vendor,
    load_index,
    load_open_pr_items,
    merge_by_resource,
    okf_items_from_tree,
    recent,
    vendor_of,
    _local_firsthand_remote_branches,
)


def test_vendor_of_maps_sources():
    assert vendor_of("claude-blog") == "anthropic"
    assert vendor_of("anthropic-news") == "anthropic"
    assert vendor_of("transformer-circuits") == "anthropic"
    assert vendor_of("openai-news") == "openai"
    assert vendor_of("deepmind-blog") == "gemini"
    assert vendor_of("google-gemini") == "gemini"
    assert vendor_of("qwen-blog") == "cn"
    assert vendor_of("inclusionai-ling") == "cn"
    assert vendor_of("unknown-x") is None


def test_filter_vendor():
    items = [
        {"title": "a", "source": "claude-blog"},
        {"title": "b", "source": "openai-news"},
        {"title": "c", "source": "deepmind-blog"},
    ]
    assert [a["title"] for a in filter_vendor(items, "anthropic")] == ["a"]
    assert [a["title"] for a in filter_vendor(items, "gemini")] == ["c"]


def test_load_index_missing_returns_empty(tmp_path):
    assert load_index(tmp_path) == []


def test_recent_filters_by_detected_window():
    items = [
        {"title": "old", "detected": "2026-06-10T00:00:00+08:00"},
        {"title": "mid", "detected": "2026-06-20T00:00:00+08:00"},
        {"title": "new", "detected": "2026-06-23T00:00:00+08:00"},
    ]
    # 近 5 天(以 2026-06-23 为今天)→ 只剩 mid(06-20) + new(06-23),倒序
    out = recent(items, days=5, today="2026-06-23")
    assert [a["title"] for a in out] == ["new", "mid"]


def test_recent_empty_when_all_old():
    items = [{"title": "x", "detected": "2026-01-01T00:00:00+08:00"}]
    assert recent(items, days=7, today="2026-06-23") == []


def test_load_index_reads_items(tmp_path):
    (tmp_path / "index.json").write_text(
        json.dumps({"items": [{"title": "T", "detected": "2026-06-23T00:00:00+08:00"}]}),
        encoding="utf-8")
    items = load_index(tmp_path)
    assert items[0]["title"] == "T"
    assert items[0]["candidate_origin"] == "main"


def test_okf_items_from_tree_parses_only_firsthand_markdown():
    tree = {
        "data/firsthand/anthropic-news/14-claude-science.md": (
            "---\n"
            "title: Claude Science\n"
            "source: anthropic-news\n"
            "resource: https://www.anthropic.com/news/claude-science-ai-workbench\n"
            "published: 2026-06-30\n"
            "tags: [科学, Agent]\n"
            "detected: 2026-07-01T01:06:02+08:00\n"
            "---\n\n"
            "Anthropic 发布 Claude Science 工作台。"
        ),
        "README.md": "ignore",
        "data/firsthand/index.json": "{}",
        "data/anthropic/2026-07-01.json": "{}",
    }

    items = okf_items_from_tree(tree)

    assert len(items) == 1
    assert items[0]["title"] == "Claude Science"
    assert items[0]["source"] == "anthropic-news"
    assert items[0]["resource"] == "https://www.anthropic.com/news/claude-science-ai-workbench"
    assert items[0]["summary"] == "Anthropic 发布 Claude Science 工作台。"


def test_merge_by_resource_prefers_open_pr_items():
    main = [
        {
            "title": "Old",
            "resource": "https://example.com/a",
            "detected": "2026-07-01T01:00:00+08:00",
            "summary": "old",
        },
        {
            "title": "Main only",
            "resource": "https://example.com/b",
            "detected": "2026-07-01T02:00:00+08:00",
        },
    ]
    overlay = [
        {
            "title": "Fresh",
            "resource": "https://example.com/a",
            "detected": "2026-07-01T03:00:00+08:00",
            "summary": "fresh",
        },
        {
            "title": "PR only",
            "resource": "https://example.com/c",
            "detected": "2026-07-01T04:00:00+08:00",
        },
    ]

    merged = merge_by_resource(main, overlay)

    assert [a["title"] for a in merged] == ["PR only", "Fresh", "Main only"]
    assert next(a for a in merged if a["resource"] == "https://example.com/a")["summary"] == "fresh"


def test_local_firsthand_remote_branches_parses_origin_refs(monkeypatch):
    class Proc:
        returncode = 0
        stdout = "\n".join([
            "origin/firsthand/2026-07-01",
            "origin/main",
            "origin/firsthand/2026-06-30",
        ])

    monkeypatch.setattr("scripts.firsthand.query.subprocess.run", lambda *args, **kwargs: Proc())

    assert _local_firsthand_remote_branches() == [
        "firsthand/2026-06-30",
        "firsthand/2026-07-01",
    ]


def test_load_open_pr_items_marks_candidate_ref(monkeypatch):
    tree = {
        "data/firsthand/claude-blog/25-loops.md": (
            "---\n"
            "title: Getting started with loops\n"
            "source: claude-blog\n"
            "resource: https://claude.com/blog/getting-started-with-loops\n"
            "published: 2026-06-30\n"
            "detected: 2026-07-01T08:00:00+08:00\n"
            "---\n\n"
            "Loops summary."
        ),
    }
    monkeypatch.setattr("scripts.firsthand.query._git_tree_for_branch", lambda branch: tree)

    items = load_open_pr_items(["firsthand/2026-07-01"])

    assert len(items) == 1
    assert items[0]["candidate_origin"] == "open-pr"
    assert items[0]["candidate_ref"] == "firsthand/2026-07-01"
