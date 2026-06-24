from pathlib import Path
from scripts.firsthand.index import parse_okf, build_index, write_outputs


SAMPLE = """---
type: Article
title: Artifacts in Claude Code
source: claude-blog
resource: https://claude.com/blog/artifacts
published: 2026-06-18
tags: [claude-code, artifacts]
detected: 2026-06-23T15:30:00+08:00
---

Claude Code 新增 artifacts 预览。
"""


def test_parse_okf():
    a = parse_okf(SAMPLE)
    assert a["title"] == "Artifacts in Claude Code"
    assert a["source"] == "claude-blog"
    assert a["resource"] == "https://claude.com/blog/artifacts"
    assert a["published"] == "2026-06-18"
    assert a["tags"] == ["claude-code", "artifacts"]
    assert a["summary"] == "Claude Code 新增 artifacts 预览。"


def _write(root, source, name, published, title="T"):
    d = root / source
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(
        f"---\ntype: Article\ntitle: {title}\nsource: {source}\n"
        f"resource: https://x/{name}\npublished: {published}\n"
        f"tags: [a]\ndetected: 2026-06-23T00:00:00+08:00\n---\n\n摘要\n",
        encoding="utf-8")


def test_build_index_sorted_by_published_desc(tmp_path):
    _write(tmp_path, "claude-blog", "01-a.md", "2026-01-01")
    _write(tmp_path, "anthropic-news", "01-b.md", "2026-06-01")
    _write(tmp_path, "claude-blog", "02-c.md", "2026-03-01")
    items = build_index(tmp_path)
    assert [a["published"] for a in items] == ["2026-06-01", "2026-03-01", "2026-01-01"]


def test_write_outputs_stable_when_unchanged(tmp_path):
    """内容不变时,重复生成 index.json 字节一致(updated 用 max detected,非当前时刻 → 不刷屏)。"""
    _write(tmp_path, "claude-blog", "01-a.md", "2026-01-01")
    j1, _ = write_outputs(tmp_path)
    s1 = (tmp_path / "index.json").read_text(encoding="utf-8")
    write_outputs(tmp_path)
    s2 = (tmp_path / "index.json").read_text(encoding="utf-8")
    assert s1 == s2
    assert (tmp_path / "feed.xml").exists()
    import json
    idx = json.loads(s1)
    assert idx["count"] == 1
    assert idx["items"][0]["resource"] == "https://x/01-a.md"
