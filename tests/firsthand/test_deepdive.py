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


from scripts.firsthand.deepdive import build_skeleton


def test_build_skeleton_structure():
    cluster = [
        _it("Introducing Claude Tag", "anthropic-news",
            "https://www.anthropic.com/news/introducing-claude-tag", "2026-06-24T07:49:00+08:00",
            summary="Claude 作为团队成员加入 Slack。"),
        _it("Agent identity in Claude Tag", "claude-blog",
            "https://claude.com/blog/agent-identity-access-model", "2026-06-24T07:49:00+08:00",
            summary="agent 独立身份访问模型。"),
    ]
    md = build_skeleton(cluster, fetch_text_fn=lambda u: f"正文@{u}", feature_available=False)
    assert "type: reference" in md
    assert "https://www.anthropic.com/news/introducing-claude-tag" in md
    assert "https://claude.com/blog/agent-identity-access-model" in md
    for sec in ["① 这是什么", "② 功能详解", "③ 官方案例", "④ 实操截图", "⑤ 作者点评"]:
        assert sec in md
    assert "暂不可体验" in md
    assert "正文@https://www.anthropic.com/news/introducing-claude-tag" in md
    assert "Claude 作为团队成员加入 Slack。" in md


def test_build_skeleton_feature_available_marks_todo_screenshot():
    cluster = [_it("X feature", "claude-blog", "https://claude.com/blog/x",
                   "2026-06-24T00:00:00+08:00")]
    md = build_skeleton(cluster, fetch_text_fn=lambda u: "t", feature_available=True)
    assert "待补截图" in md
    assert "暂不可体验" not in md


from scripts.firsthand.deepdive import write_draft


def test_write_draft_path_and_content(tmp_path):
    cluster = [_it("Introducing Claude Tag", "anthropic-news",
                   "https://www.anthropic.com/news/introducing-claude-tag",
                   "2026-06-24T07:49:00+08:00")]
    path = write_draft(tmp_path, cluster, today="2026-06-24",
                       fetch_text_fn=lambda u: "正文", feature_available=False)
    assert path.parent.name == "2026-06-24_introducing-claude-tag"
    assert path.name == "draft.md"
    assert path.exists()
    assert "## ① 这是什么" in path.read_text(encoding="utf-8")
