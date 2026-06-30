from scripts.firsthand.repair_summaries import repair_failed_summaries
from scripts.firsthand.store import write_okf
from scripts.firsthand.summarize import SUMMARY_FAILED


def test_repair_failed_summaries_rewrites_okf_from_saved_full_text(tmp_path):
    path = write_okf(tmp_path, {
        "title": "Artifacts in Claude Code",
        "source": "claude-blog",
        "url": "https://claude.com/blog/artifacts-in-claude-code",
        "summary": SUMMARY_FAILED,
        "summary_error": "old failure",
        "tags": [],
        "published": "2026-06-18",
        "detected": "2026-06-23T15:30:00+08:00",
        "full_text": "Claude Code now supports inline web artifacts preview.",
    })

    def fake_summarize(title, body):
        assert title == "Artifacts in Claude Code"
        assert "inline web artifacts preview" in body
        return {"summary": "Claude Code 新增内联 artifacts 预览。", "tags": ["Claude Code"], "error": None}

    result = repair_failed_summaries(tmp_path, summarize_fn=fake_summarize)

    assert result == {"repaired": 1, "failed": 0, "skipped": 0}
    text = path.read_text(encoding="utf-8")
    assert "Claude Code 新增内联 artifacts 预览。" in text
    assert "tags: [Claude Code]" in text
    assert "published: 2026-06-18" in text
    assert "old failure" not in text


def test_repair_failed_summaries_skips_files_without_full_text(tmp_path):
    path = write_okf(tmp_path, {
        "title": "No full text",
        "source": "demo",
        "url": "https://example.com/no-full-text",
        "summary": SUMMARY_FAILED,
        "summary_error": "old failure",
        "tags": [],
        "detected": "2026-06-23T15:30:00+08:00",
    })

    result = repair_failed_summaries(tmp_path, summarize_fn=lambda title, body: {})

    assert result == {"repaired": 0, "failed": 0, "skipped": 1}
    assert "old failure" in path.read_text(encoding="utf-8")
