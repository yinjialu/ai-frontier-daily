import json
from datetime import datetime, timezone

import pytest

from scripts.server import sources, store, curation, worker


SOURCE = {"id": "official", "name": "Official", "vendor": "openai",
          "url": "https://example.com/news", "domains": ["example.com"],
          "path_regex": "^/news/[^/]+"}


def item(id="one"):
    return dict(id=id, source_id="official", vendor="openai", company="OpenAI",
                title="Model launch", text="An official model announcement with supporting evidence.",
                url="https://example.com/news/one", signal="announcement",
                published=datetime.now(timezone.utc).isoformat())


def result(items, error=None):
    return {"source": SOURCE, "items": items, "error": error}


def test_baseline_failure_and_incremental_restart(tmp_path):
    path = tmp_path / "state.db"
    db = store.connect(path)
    store.ingest(db, [result([], "403")])
    assert db.execute("SELECT initialized FROM sources").fetchone()[0] == 0
    assert store.ingest(db, [result([item()])]) == 0
    assert store.pending(db) == []
    db.close()
    db = store.connect(path)
    assert store.ingest(db, [result([item(), item("two")])]) == 1
    assert [i["id"] for i in store.pending(db)] == ["two"]
    store.ingest(db, [result([item(), item("two")])])
    assert len(store.pending(db)) == 1


@pytest.mark.parametrize("raw", ["<html>Access denied</html>", "<rss version='2.0'><channel/></rss>"])
def test_empty_and_challenge_feeds_are_failures(raw):
    with pytest.raises(ValueError):
        sources.parse_feed(raw, SOURCE)


def test_atom_updated_is_not_publication():
    raw = '''<feed xmlns="http://www.w3.org/2005/Atom"><title>News</title><entry>
    <id>one</id><title>Model</title><link href="https://example.com/news/one"/>
    <updated>2026-09-06T00:00:00Z</updated><summary>Body</summary></entry></feed>'''
    assert sources.parse_feed(raw, SOURCE)[0]["published"] is None


def test_unofficial_links_rejected():
    with pytest.raises(ValueError):
        sources.entry(SOURCE, "https://example.com.evil.test/news/one", "Fake")


def test_link_dates_and_dedup():
    raw = '<a href="/news/one">Sep 6, 2026 Model</a><a href="/news/one">Read more</a>'
    items = sources.parse_links(raw, SOURCE)
    assert len(items) == 1
    assert items[0]["published"] == "2026-09-06"


def test_changelog_revisions_keep_anchor():
    a = sources.parse_changelog('<main><h2 id="sep6">Sep 6, 2026</h2><p>Model A</p></main>', SOURCE)[0]
    b = sources.parse_changelog('<main><h2 id="sep6">Sep 6, 2026</h2><p>Model A and B</p></main>', SOURCE)[0]
    assert a["url"].endswith("#sep6")
    assert a["id"] != b["id"]


def test_openai_markdown_dates_inherit_year():
    value = sources.parse_markdown_changelog('## September, 2026\n\n### Sep 3\n\nReleased model A.\n', dict(SOURCE, url="https://example.com/changelog.md"))[0]
    assert value["published"] == "2026-09-03"
    assert value["url"] == "https://example.com/changelog#2026-09-03"


def test_sitemap_lastmod_is_not_a_release_date():
    raw = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.com/news/one</loc><lastmod>2026-09-06</lastmod></url></urlset>'
    assert sources.parse_sitemap(raw, SOURCE)[0]["published"] is None


def test_changed_source_establishes_new_baseline(tmp_path):
    db = store.connect(tmp_path / "state.db")
    store.ingest(db, [result([item()])])
    changed = result([item(), item("old-history")])
    changed["source"] = dict(SOURCE, url="https://example.com/sitemap.xml")
    assert store.ingest(db, [changed]) == 0
    assert store.pending(db) == []


def editorial():
    return dict(id="one", relevant=True, important=True, event_key="model-launch", tag="模型发布",
                title="官方发布新模型", summary="官方发布新模型并提供相关能力说明，开发者可查阅原文了解实际可用范围。",
                evidence="An official model announcement")


def test_missing_or_fabricated_model_output_rejected():
    with pytest.raises(ValueError):
        curation.validate([item()], [])
    with pytest.raises(ValueError):
        curation.validate([item()], [dict(editorial(), evidence="made up supporting evidence")])


def test_weak_and_undated_sources_never_trigger_breaking_alerts():
    for change in ({"signal": "weak"}, {"published": None}, {"published": "2000-01-01"}):
        out = curation.validate([dict(item(), **change)], [editorial()])[0]
        assert out["editorial"]["important"] is False


def test_delivery_failure_is_retryable(tmp_path):
    db = store.connect(tmp_path / "state.db")
    class Client:
        def card(self, *args):
            raise RuntimeError("temporary failure")
    with pytest.raises(RuntimeError):
        worker.deliver(db, Client(), "test", "Title", "Body")
    assert not store.delivered(db, "test")
    class OK:
        calls = 0
        def card(self, *args):
            self.calls += 1
            return "message-id"
    ok = OK()
    worker.deliver(db, ok, "test", "Title", "Body")
    worker.deliver(db, ok, "test", "Title", "Body")
    assert ok.calls == 1


def test_news_deduplicates_events_and_excludes_baseline(tmp_path):
    db = store.connect(tmp_path / "state.db")
    store.ingest(db, [result([item("baseline")])])
    store.ingest(db, [result([item("a"), item("b")])])
    for id in ("a", "b", "baseline"):
        with db:
            db.execute("UPDATE items SET curated=? WHERE id=?", (json.dumps(dict(item(id), editorial=editorial())), id))
    assert len(worker.news(db)) == 1


def test_next_edition_does_not_repeat_previous_days_cards(tmp_path):
    db = store.connect(tmp_path / "state.db")
    store.ingest(db, [result([item("baseline")])])
    store.ingest(db, [result([item()])])
    curated = dict(item(), editorial=editorial())
    with db:
        db.execute("UPDATE items SET curated=? WHERE id=?", (json.dumps(curated), "one"))
    assert len(worker.edition_items(db)) == 1
    with db:
        db.execute("INSERT INTO editions VALUES (?,?)", ("2026-09-05", json.dumps([curated])))
    assert worker.edition_items(db) == []


def test_zai_dated_release_timeline():
    raw = '<main><div class="update-container" id="2026-08-26"><button>2026-08-26</button><p>GLM new release details</p></div></main>'
    value = sources.parse_changelog(raw, SOURCE)[0]
    assert value["published"] == "2026-08-26"
    assert "GLM new release details" in value["text"]
