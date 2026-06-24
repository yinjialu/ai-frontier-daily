import json
from pathlib import Path
from scripts.firsthand.query import load_index, recent


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
