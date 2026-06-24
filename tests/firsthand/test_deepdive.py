from scripts.firsthand.deepdive import candidates


def _it(title, source, resource, detected, summary="s"):
    return {"title": title, "source": source, "resource": resource,
            "detected": detected, "summary": summary, "published": detected[:10]}


def test_candidates_clusters_same_event_recent():
    items = [
        _it("Introducing Claude Tag", "anthropic-news",
            "https://www.anthropic.com/news/introducing-claude-tag", "2026-06-24T07:49:00+08:00"),
        _it("Agent identity in Claude Tag", "claude-blog",
            "https://claude.com/blog/agent-identity-access-model", "2026-06-24T07:49:00+08:00"),
        _it("Old thing", "openai-news", "https://openai.com/news/old", "2026-01-01T00:00:00+08:00"),
    ]
    cands = candidates(items, days=7, today="2026-06-24")
    assert len(cands) == 1
    assert {a["resource"] for a in cands[0]} == {
        "https://www.anthropic.com/news/introducing-claude-tag",
        "https://claude.com/blog/agent-identity-access-model",
    }


def test_candidates_empty_when_all_old():
    items = [_it("x", "claude-blog", "u", "2026-01-01T00:00:00+08:00")]
    assert candidates(items, days=7, today="2026-06-24") == []
