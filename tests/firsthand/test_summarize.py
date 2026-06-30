import urllib.error

from scripts.firsthand.summarize import (
    LLMConfig,
    summarize,
    _anthropic_messages_runner,
    _load_llm_config,
    _parse_json,
)

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

def test_load_llm_config_reads_private_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / "firsthand.env"
    env_file.write_text(
        "\n".join([
            "FIRSTHAND_LLM_API_KEY=file-key",
            "FIRSTHAND_LLM_BASE_URL=https://api.deepseek.com/anthropic",
            "FIRSTHAND_LLM_MODEL=deepseek-v4-flash",
        ])
    )
    monkeypatch.delenv("FIRSTHAND_LLM_API_KEY", raising=False)
    monkeypatch.delenv("FIRSTHAND_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("FIRSTHAND_LLM_MODEL", raising=False)

    cfg = _load_llm_config(env_file)

    assert cfg.api_key == "file-key"
    assert cfg.base_url == "https://api.deepseek.com/anthropic"
    assert cfg.model == "deepseek-v4-flash"

def test_env_overrides_private_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / "firsthand.env"
    env_file.write_text("FIRSTHAND_LLM_API_KEY=file-key\nFIRSTHAND_LLM_MODEL=file-model\n")
    monkeypatch.setenv("FIRSTHAND_LLM_API_KEY", "env-key")
    monkeypatch.setenv("FIRSTHAND_LLM_MODEL", "env-model")

    cfg = _load_llm_config(env_file)

    assert cfg.api_key == "env-key"
    assert cfg.model == "env-model"

def test_anthropic_messages_runner_posts_to_configured_endpoint():
    captured = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return b'{"content":[{"type":"text","text":"{\\"summary\\":\\"ok\\",\\"tags\\":[\\"tag\\"]}"}]}'

    def fake_urlopen(req, timeout):
        captured["url"] = req.full_url
        captured["headers"] = dict(req.header_items())
        captured["data"] = req.data
        captured["timeout"] = timeout
        return FakeResponse()

    raw = _anthropic_messages_runner(
        "prompt",
        config=LLMConfig(
            api_key="test-key",
            base_url="https://api.deepseek.com/anthropic/",
            model="deepseek-v4-flash",
            timeout=7,
        ),
        urlopen=fake_urlopen,
    )

    assert captured["url"] == "https://api.deepseek.com/anthropic/v1/messages"
    assert captured["headers"]["X-api-key"] == "test-key"
    assert captured["headers"]["Anthropic-version"] == "2023-06-01"
    assert b'"model": "deepseek-v4-flash"' in captured["data"]
    assert captured["timeout"] == 7
    assert raw == '{"summary":"ok","tags":["tag"]}'

def test_anthropic_messages_runner_falls_back_to_curl_on_url_error():
    def failing_urlopen(req, timeout):
        raise urllib.error.URLError("certificate verify failed")

    def fake_curl(url, payload, config):
        assert url == "https://api.deepseek.com/anthropic/v1/messages"
        assert payload["model"] == "deepseek-v4-flash"
        assert config.api_key == "test-key"
        return '{"content":[{"type":"text","text":"{\\"summary\\":\\"curl\\",\\"tags\\":[]}"}]}'

    raw = _anthropic_messages_runner(
        "prompt",
        config=LLMConfig(api_key="test-key"),
        urlopen=failing_urlopen,
        curl_runner=fake_curl,
    )

    assert raw == '{"summary":"curl","tags":[]}'
