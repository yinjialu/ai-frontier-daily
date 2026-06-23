from scripts.firsthand.summarize import summarize, _parse_json

def test_parse_json_extracts_from_noise():
    raw = '好的，结果如下：\n{"summary": "摘要", "tags": ["a", "b"]}\n完成。'
    obj = _parse_json(raw)
    assert obj["summary"] == "摘要"
    assert obj["tags"] == ["a", "b"]

def test_summarize_uses_runner():
    fake = lambda prompt: '{"summary": "新增预览能力。", "tags": ["claude-code"]}'
    result = summarize("Artifacts", "全文……", runner=fake)
    assert result["summary"] == "新增预览能力。"
    assert result["tags"] == ["claude-code"]

def test_summarize_fallback_on_bad_output():
    fake = lambda prompt: "完全不是 JSON 的东西"
    result = summarize("Title", "body", runner=fake)
    assert result["summary"] == "(摘要生成失败)"
    assert result["tags"] == []
