"""Feedback must survive restarts and change ranking without changing facts."""
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import pytest

from scripts.server import preferences, store, worker


NOW = datetime(2026, 9, 7, 1, 0, tzinfo=timezone.utc)


def story(name, *, company="OpenAI", tag="研究", important=False, published=None):
    return {"id": name, "url": "https://example.com/news/" + name,
            "company": company, "vendor": "openai", "published": published or NOW.isoformat(),
            "editorial": {"tag": tag, "relevant": True, "important": important,
                          "event_key": name, "title": name, "summary": "verified facts"}}


def feedback(db, item, action="useful", request_id="one", **kwargs):
    return preferences.record_feedback(db, item, action, request_id, now=NOW, **kwargs)


def test_url_identity_keeps_meaningful_queries_and_changelog_anchors():
    base = "https://example.com/news/one?a=1&b=2#date"
    assert preferences.canonical_url("HTTPS://EXAMPLE.COM:443/news/one/?b=2&utm_source=email&a=1#date") == base
    assert preferences.content_key(base) == preferences.content_key(base + "")
    assert preferences.content_key(base) != preferences.content_key(base.replace("a=1", "a=2"))
    assert preferences.content_key(base) != preferences.content_key(base.replace("#date", "#other"))
    for url in ("javascript:alert(1)", "https://person:secret@example.com", "https://example.com\n/path", "/local"):
        with pytest.raises(ValueError):
            preferences.content_key(url)


def test_persistence_idempotency_replacement_clear_and_old_replay(tmp_path):
    path = tmp_path / "frontier.db"
    db = store.connect(path)
    item = story("one")
    first = feedback(db, item)
    replay = feedback(db, dict(item, url=item["url"] + "?utm_source=share"))
    assert replay["duplicate"] and replay["version"] == first["version"]
    second = feedback(db, item, "less", "two")
    assert second["action"] == "less"
    assert feedback(db, item)["action"] == "less"  # stale retry cannot overwrite.
    with pytest.raises(ValueError):
        feedback(db, item, "clear", "one")
    assert preferences.preference_summary(db, now=NOW)["count"] == 1
    db.close()
    db = store.connect(path)
    assert preferences.list_feedback(db)[0]["action"] == "less"
    feedback(db, item, "clear", "three")
    assert preferences.list_feedback(db) == []
    assert preferences.list_feedback(db, include_cleared=True)[0]["action"] == "clear"
    assert preferences.preference_summary(db, now=NOW)["company_weights"] == {}
    assert db.execute("SELECT count(*) FROM feedback_events").fetchone()[0] == 3


def test_one_url_is_one_signal_even_across_revisions_and_shared_urls(tmp_path):
    db = store.connect(tmp_path / "frontier.db")
    item = story("one")
    first = feedback(db, item)
    initial = preferences.preference_summary(db, now=NOW)
    for n in range(12):
        assert feedback(db, dict(item, id="revision-" + str(n)), request_id="req-" + str(n))["content_key"] == first["content_key"]
    summary = preferences.preference_summary(db, now=NOW)
    assert summary["count"] == 1
    assert summary["company_weights"] == initial["company_weights"]


def test_concurrent_network_retries_persist_only_one_audit_event(tmp_path):
    path = tmp_path / "frontier.db"
    store.connect(path).close()

    def send(_):
        db = store.connect(path)
        try:
            return feedback(db, story("one"))
        finally:
            db.close()

    with ThreadPoolExecutor(max_workers=4) as pool:
        responses = list(pool.map(send, range(8)))
    db = store.connect(path)
    assert sum(not r["duplicate"] for r in responses) == 1
    assert db.execute("SELECT count(*) FROM feedback_events").fetchone()[0] == 1
    assert preferences.preference_summary(db, now=NOW)["count"] == 1


def test_actor_isolation_and_validation(tmp_path):
    db = store.connect(tmp_path / "frontier.db")
    feedback(db, story("one"), actor="one-owner")
    assert preferences.list_feedback(db) == []
    assert preferences.list_feedback(db, actor="one-owner")
    for bad_action in ("clicked", "read", "publish", "LIKE"):
        with pytest.raises(ValueError):
            feedback(db, story("one"), bad_action)
    with pytest.raises(ValueError):
        feedback(db, story("one"), request_id="request\nheader")


def test_generalization_is_bounded_decays_and_does_not_penalize_vendor(tmp_path):
    db = store.connect(tmp_path / "frontier.db")
    feedback(db, story("old", company="Specific Company", tag="研究"), "less")
    summary = preferences.preference_summary(db, now=NOW)
    assert summary["company_weights"]["specific company"] == pytest.approx(-0.07)
    assert summary["tag_weights"]["研究"] == pytest.approx(-0.04)
    assert "vendor_weights" not in summary
    later = preferences.preference_summary(db, now=NOW + timedelta(days=90))
    assert abs(later["company_weights"]["specific company"]) < abs(summary["company_weights"]["specific company"]) / 4
    for n in range(30):
        feedback(db, story(str(n), company="Specific Company"), "less", "req-" + str(n))
    saturated = preferences.preference_summary(db, now=NOW)
    assert abs(saturated["company_weights"]["specific company"]) < 0.35
    assert abs(saturated["tag_weights"]["研究"]) < 0.20
    # Unrelated company + taxonomy in the same vendor gains no penalty.
    other = story("unrelated", company="Other Company", tag="开发者")
    assert other["company"].casefold() not in saturated["company_weights"]
    assert other["editorial"]["tag"] not in saturated["tag_weights"]


def test_next_ranking_uses_feedback_but_preserves_important_and_all_candidates(tmp_path):
    db = store.connect(tmp_path / "frontier.db")
    a, b = story("a", company="One", tag="企业"), story("b", company="Two", tag="开发者")
    launch = story("launch", company="One", tag="模型发布", important=True)
    original = [a, b, launch]
    feedback(db, b)
    feedback(db, launch, "less", "two")
    ranked = preferences.rank_items(db, original, now=NOW)
    assert [i["id"] for i in ranked] == ["launch", "b", "a"]
    assert original == [a, b, launch] and launch["editorial"]["important"] is True
    feedback(db, b, "clear", "three")
    feedback(db, launch, "clear", "four")
    assert [i["id"] for i in preferences.rank_items(db, original, now=NOW)] == ["launch", "a", "b"]


def test_feedback_cannot_overcome_large_freshness_gap(tmp_path):
    db = store.connect(tmp_path / "frontier.db")
    old = story("old", company="Old", tag="企业", published=(NOW - timedelta(hours=60)).isoformat())
    new = story("new", company="New", tag="开发者")
    feedback(db, old)
    assert preferences.rank_items(db, [old, new], now=NOW)[0]["id"] == "new"


def test_worker_applies_preference_before_edition_cap_and_alerts_can_bypass(tmp_path):
    db = store.connect(tmp_path / "frontier.db")
    current = datetime.now(timezone.utc).isoformat()
    items = [story(str(n), company="One", published=current) for n in range(7)]
    stale = story("stale", published="2000-01-01")
    irrelevant = story("irrelevant", published=current)
    irrelevant["editorial"]["relevant"] = False
    for i in [*items, stale, irrelevant]:
        with db:
            db.execute("INSERT INTO items VALUES (?,?,?,?,?,NULL)",
                       (i["id"], json.dumps(i), current, 0, json.dumps(i)))
    preferences.record_feedback(db, items[-1], "useful", "one")
    preferences.record_feedback(db, stale, "useful", "two")
    preferences.record_feedback(db, irrelevant, "useful", "three")
    assert worker.news(db)[0]["id"] == "6"
    assert worker.news(db, personalized=False)[0]["id"] == "0"
    assert {i["id"] for i in worker.news(db)} == {str(n) for n in range(7)}
    edition = worker.edition_items(db)
    assert len(edition) == 6 and edition[0]["id"] == "6"
