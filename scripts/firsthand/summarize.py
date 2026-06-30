import json
import os
import subprocess
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

# 摘要生成失败时写入的占位文本（PR 正文据此打 ⚠️ 标记）
SUMMARY_FAILED = "(摘要生成失败)"
DEFAULT_ENV_FILE = Path.home() / ".config" / "ai-frontier-daily" / "firsthand.env"
DEFAULT_BASE_URL = "https://api.deepseek.com/anthropic"
DEFAULT_MODEL = "deepseek-v4-flash"

_PROMPT = """只返回 JSON，不要任何解释或代码块标记。
格式：{{"summary": "中文摘要，100字以内", "tags": ["标签1", "标签2"]}}
针对以下文章生成面向中文 AI 从业者的摘要与 2-4 个主题标签。

标题：{title}

正文：
{body}
"""

_CLAUDE_BIN = str(
    next((p for p in [
        Path.home() / ".local/bin/claude",
        Path("/usr/local/bin/claude"),
    ] if p.exists()), "claude")
)


@dataclass(frozen=True)
class LLMConfig:
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    model: str = DEFAULT_MODEL
    timeout: int = 120


def _read_env_file(path: Path) -> dict:
    """读取简单 KEY=VALUE 私密配置文件；不支持 shell 展开，避免意外执行。"""
    values = {}
    if not path.exists():
        return values
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key] = value
    return values


def _load_llm_config(env_file: Path = DEFAULT_ENV_FILE) -> LLMConfig:
    """环境变量优先，其次读取 ~/.config/ai-frontier-daily/firsthand.env。"""
    file_env = _read_env_file(env_file)

    def pick(name: str, default: str = "") -> str:
        return os.environ.get(name) or file_env.get(name) or default

    timeout_raw = pick("FIRSTHAND_LLM_TIMEOUT_SECONDS", "120")
    try:
        timeout = int(timeout_raw)
    except ValueError:
        timeout = 120
    return LLMConfig(
        api_key=pick("FIRSTHAND_LLM_API_KEY") or pick("DEEPSEEK_API_KEY"),
        base_url=pick("FIRSTHAND_LLM_BASE_URL", DEFAULT_BASE_URL).rstrip("/"),
        model=pick("FIRSTHAND_LLM_MODEL", DEFAULT_MODEL),
        timeout=timeout,
    )


def _claude_runner(prompt: str) -> str:
    # timeout 抛 TimeoutExpired；非零退出（限流/未登录/网络）时错误多在 stderr，
    # 显式抛出带 stderr 的异常 —— 否则空 stdout 会坍缩成无用的 "no json"。
    proc = subprocess.run(
        [_CLAUDE_BIN, "-p", prompt],
        capture_output=True, text=True, timeout=120,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"claude 退出码 {proc.returncode}: {detail or '无输出'}")
    return proc.stdout


def _anthropic_messages_runner(
    prompt: str,
    config: LLMConfig | None = None,
    urlopen=urllib.request.urlopen,
    curl_runner=None,
) -> str:
    """调用 Anthropic Messages API 兼容端点，返回模型文本输出。"""
    cfg = config or _load_llm_config()
    if not cfg.api_key:
        raise RuntimeError(f"未配置 FIRSTHAND_LLM_API_KEY（可写入 {DEFAULT_ENV_FILE}）")

    url = f"{cfg.base_url.rstrip('/')}/v1/messages"
    payload = {
        "model": cfg.model,
        "max_tokens": 1024,
        "temperature": 0.2,
        "messages": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "x-api-key": cfg.api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=cfg.timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.URLError:
        raw = (curl_runner or _curl_post_messages)(url, payload, cfg)
    return _extract_text_content(raw)


def _curl_post_messages(url: str, payload: dict, cfg: LLMConfig) -> str:
    """用系统 curl 兜底发送请求；API key 通过 stdin config 传入，避免出现在进程参数。"""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    tmp_name = None
    try:
        with tempfile.NamedTemporaryFile(prefix="firsthand-llm-", suffix=".json", delete=False) as f:
            f.write(body)
            tmp_name = f.name
        curl_config = "\n".join([
            f'url = "{url}"',
            'request = "POST"',
            'silent',
            'show-error',
            'fail-with-body',
            'header = "content-type: application/json"',
            f'header = "x-api-key: {cfg.api_key}"',
            'header = "anthropic-version: 2023-06-01"',
            f'data-binary = "@{tmp_name}"',
        ])
        proc = subprocess.run(
            ["curl", "--config", "-"],
            input=curl_config,
            capture_output=True,
            text=True,
            timeout=cfg.timeout,
        )
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "").strip()
            raise RuntimeError(f"curl 退出码 {proc.returncode}: {detail or '无输出'}")
        return proc.stdout
    finally:
        if tmp_name:
            try:
                Path(tmp_name).unlink()
            except FileNotFoundError:
                pass


def _extract_text_content(raw: str) -> str:
    obj = json.loads(raw)
    parts = []
    for block in obj.get("content") or []:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(str(block.get("text") or ""))
    if not parts:
        raise ValueError("模型响应中无 text content")
    return "\n".join(parts)


def _parse_json(raw: str) -> dict:
    """从可能含噪声的输出里截取第一个 { 到最后一个 }。"""
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("输出中无 JSON")
    return json.loads(raw[start : end + 1])

def _short(e: Exception, limit: int = 300) -> str:
    """异常 → 单行短描述（类型 + 信息），截断防止超长 traceback 污染 commit/PR。"""
    msg = " ".join(str(e).split())
    return f"{type(e).__name__}: {msg}"[:limit]

def summarize(title: str, body: str, runner=None) -> dict:
    """返回 {summary, tags, error}；任何失败回退占位摘要并把失败原因放进 error
    （成功时 error 为 None）。调用方据 error 把原因贴进 OKF 文件 / PR 正文。"""
    prompt = _PROMPT.format(title=title, body=body[:6000])
    runner = runner or _anthropic_messages_runner
    try:
        obj = _parse_json(runner(prompt))
        tags = list(obj.get("tags") or [])
        summary = str(obj.get("summary") or "").strip()
        if not summary:
            return {"summary": SUMMARY_FAILED, "tags": tags, "error": "模型返回空摘要"}
        return {"summary": summary, "tags": tags, "error": None}
    except Exception as e:
        return {"summary": SUMMARY_FAILED, "tags": [], "error": _short(e)}
