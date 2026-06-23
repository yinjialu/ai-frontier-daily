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

def test_state_roundtrip(tmp_path):
    state_file = tmp_path / "state.json"
    assert load_state(state_file) == {}
    save_state(state_file, {"claude-blog": {"last_fetch_ok": True}})
    assert load_state(state_file)["claude-blog"]["last_fetch_ok"] is True
