from pathlib import Path
from scripts.firsthand.store import (
    ingested_urls, write_okf, slugify, load_state, save_state,
)

def test_write_and_read_okf_roundtrip(tmp_path):
    article = {
        "title": "Artifacts in Claude Code",
        "source": "claude-blog",
        "url": "https://claude.com/blog/artifacts-in-claude-code",
        "summary": "新增 artifacts 预览。",
        "tags": ["claude-code", "artifacts"],
        "timestamp": "2026-06-23T15:30:00+08:00",
    }
    path = write_okf(tmp_path, article)
    assert path.exists()
    assert path.parent.name == "claude-blog"
    text = path.read_text(encoding="utf-8")
    assert "title: Artifacts in Claude Code" in text
    assert "resource: https://claude.com/blog/artifacts-in-claude-code" in text
    assert "新增 artifacts 预览。" in text
    assert ingested_urls(tmp_path, "claude-blog") == {
        "https://claude.com/blog/artifacts-in-claude-code"
    }

def test_ingested_urls_empty_for_new_source(tmp_path):
    assert ingested_urls(tmp_path, "brand-new") == set()

def test_slugify():
    assert slugify("https://claude.com/blog/artifacts-in-claude-code") == "artifacts-in-claude-code"

def test_write_okf_same_slug_different_url_no_overwrite(tmp_path):
    """两条末段相同但完整 URL 不同的文章，同日 write_okf 两次，不可互相覆盖。"""
    a1 = {
        "title": "Release v1",
        "source": "demo",
        "url": "https://demo.com/v1/release",
        "summary": "v1 摘要",
        "tags": ["x"],
        "timestamp": "2026-06-23T15:30:00+08:00",
    }
    a2 = {
        "title": "Release v2",
        "source": "demo",
        "url": "https://demo.com/v2/release",
        "summary": "v2 摘要",
        "tags": ["y"],
        "timestamp": "2026-06-23T16:00:00+08:00",
    }
    p1 = write_okf(tmp_path, a1)
    p2 = write_okf(tmp_path, a2)
    assert p1 != p2
    assert p1.exists() and p2.exists()
    assert ingested_urls(tmp_path, "demo") == {
        "https://demo.com/v1/release",
        "https://demo.com/v2/release",
    }


def test_write_okf_idempotent_same_url(tmp_path):
    """重复写同一篇 URL（resource 相同）仍用原名，幂等覆盖自身。"""
    a = {
        "title": "Release v1",
        "source": "demo",
        "url": "https://demo.com/v1/release",
        "summary": "v1 摘要",
        "tags": ["x"],
        "timestamp": "2026-06-23T15:30:00+08:00",
    }
    p1 = write_okf(tmp_path, a)
    p2 = write_okf(tmp_path, a)
    assert p1 == p2
    assert len(list((tmp_path / "demo").glob("*.md"))) == 1


def test_state_roundtrip(tmp_path):
    state_file = tmp_path / "state.json"
    assert load_state(state_file) == {}
    save_state(state_file, {"claude-blog": {"last_fetch_ok": True}})
    assert load_state(state_file)["claude-blog"]["last_fetch_ok"] is True
