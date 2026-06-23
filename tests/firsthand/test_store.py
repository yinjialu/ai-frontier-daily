from pathlib import Path
from scripts.firsthand.store import (
    ingested_urls, write_okf, slugify, load_state, save_state, renumber_source,
)

def _article(url, title="T", summary="s", tags=None, published=None,
             detected="2026-06-23T15:30:00+08:00", source="demo"):
    return {"title": title, "source": source, "url": url, "summary": summary,
            "tags": tags or [], "published": published, "detected": detected}


def test_write_okf_prefixes_sequence_number(tmp_path):
    a = _article("https://claude.com/blog/artifacts-in-claude-code",
                 title="Artifacts", source="claude-blog",
                 published="2026-06-18", summary="新增 artifacts 预览。",
                 tags=["claude-code"])
    path = write_okf(tmp_path, a)
    # 文件名带 2 位序号前缀 + slug
    assert path.name == "01-artifacts-in-claude-code.md"
    text = path.read_text(encoding="utf-8")
    assert "resource: https://claude.com/blog/artifacts-in-claude-code" in text
    assert "published: 2026-06-18" in text
    assert "detected: 2026-06-23T15:30:00+08:00" in text
    assert "timestamp:" not in text
    assert ingested_urls(tmp_path, "claude-blog") == {
        "https://claude.com/blog/artifacts-in-claude-code"}


def test_write_okf_sequence_increments_in_call_order(tmp_path):
    p1 = write_okf(tmp_path, _article("https://demo.com/a"))
    p2 = write_okf(tmp_path, _article("https://demo.com/b"))
    p3 = write_okf(tmp_path, _article("https://demo.com/c"))
    assert p1.name == "01-a.md"
    assert p2.name == "02-b.md"
    assert p3.name == "03-c.md"


def test_write_okf_idempotent_same_url_keeps_number(tmp_path):
    """同一 URL 重写：复用原文件名(含原序号)，不新增、不递增。"""
    p1 = write_okf(tmp_path, _article("https://demo.com/a", summary="v1"))
    p2 = write_okf(tmp_path, _article("https://demo.com/a", summary="v2"))
    assert p1 == p2
    assert p1.name == "01-a.md"
    assert len(list((tmp_path / "demo").glob("*.md"))) == 1
    assert "v2" in p1.read_text(encoding="utf-8")


def test_write_okf_same_slug_different_url_distinct_by_sequence(tmp_path):
    """末段相同但 URL 不同：序号前缀天然区分，不互相覆盖。"""
    p1 = write_okf(tmp_path, _article("https://demo.com/v1/release"))
    p2 = write_okf(tmp_path, _article("https://demo.com/v2/release"))
    assert p1.name == "01-release.md"
    assert p2.name == "02-release.md"
    assert ingested_urls(tmp_path, "demo") == {
        "https://demo.com/v1/release", "https://demo.com/v2/release"}


def test_write_okf_omits_published_when_unknown(tmp_path):
    text = write_okf(tmp_path, _article("https://demo.com/x", published=None)).read_text(encoding="utf-8")
    assert "published:" not in text
    assert "detected: 2026-06-23T15:30:00+08:00" in text


def test_renumber_source_orders_by_published(tmp_path):
    """renumber_source 按 published 升序重排序号；undated 排最后。"""
    # 乱序写入
    write_okf(tmp_path, _article("https://demo.com/mar", published="2026-03-01"))
    write_okf(tmp_path, _article("https://demo.com/jan", published="2026-01-01"))
    write_okf(tmp_path, _article("https://demo.com/none", published=None))
    write_okf(tmp_path, _article("https://demo.com/feb", published="2026-02-01"))
    renumber_source(tmp_path / "demo")
    names = sorted(p.name for p in (tmp_path / "demo").glob("*.md"))
    assert names == ["01-jan.md", "02-feb.md", "03-mar.md", "04-none.md"]
    # 去重真相不受重命名影响
    assert len(ingested_urls(tmp_path, "demo")) == 4


def test_ingested_urls_empty_for_new_source(tmp_path):
    assert ingested_urls(tmp_path, "brand-new") == set()


def test_slugify():
    assert slugify("https://claude.com/blog/artifacts-in-claude-code") == "artifacts-in-claude-code"


def test_state_roundtrip(tmp_path):
    state_file = tmp_path / "state.json"
    assert load_state(state_file) == {}
    save_state(state_file, {"claude-blog": {"last_fetch_ok": True}})
    assert load_state(state_file)["claude-blog"]["last_fetch_ok"] is True
