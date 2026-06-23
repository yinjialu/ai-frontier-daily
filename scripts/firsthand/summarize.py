import json
import subprocess

_PROMPT = """只返回 JSON，不要任何解释或代码块标记。
格式：{{"summary": "中文摘要，100字以内", "tags": ["标签1", "标签2"]}}
针对以下文章生成面向中文 AI 从业者的摘要与 2-4 个主题标签。

标题：{title}

正文：
{body}
"""

def _claude_runner(prompt: str) -> str:
    proc = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True, text=True, timeout=120,
    )
    return proc.stdout

def _parse_json(raw: str) -> dict:
    """从可能含噪声的输出里截取第一个 { 到最后一个 }。"""
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no json")
    return json.loads(raw[start : end + 1])

def summarize(title: str, body: str, runner=_claude_runner) -> dict:
    """返回 {summary, tags}；任何失败回退到占位摘要。"""
    prompt = _PROMPT.format(title=title, body=body[:6000])
    try:
        obj = _parse_json(runner(prompt))
        return {
            "summary": str(obj.get("summary") or "(摘要生成失败)"),
            "tags": list(obj.get("tags") or []),
        }
    except Exception:
        return {"summary": "(摘要生成失败)", "tags": []}
