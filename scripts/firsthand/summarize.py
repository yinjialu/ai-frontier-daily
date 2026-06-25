import json
import subprocess

# 摘要生成失败时写入的占位文本（PR 正文据此打 ⚠️ 标记）
SUMMARY_FAILED = "(摘要生成失败)"

_PROMPT = """只返回 JSON，不要任何解释或代码块标记。
格式：{{"summary": "中文摘要，100字以内", "tags": ["标签1", "标签2"]}}
针对以下文章生成面向中文 AI 从业者的摘要与 2-4 个主题标签。

标题：{title}

正文：
{body}
"""

def _claude_runner(prompt: str) -> str:
    # timeout 抛 TimeoutExpired；非零退出（限流/未登录/网络）时错误多在 stderr，
    # 显式抛出带 stderr 的异常 —— 否则空 stdout 会坍缩成无用的 "no json"。
    proc = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True, text=True, timeout=120,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"claude 退出码 {proc.returncode}: {detail or '无输出'}")
    return proc.stdout

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

def summarize(title: str, body: str, runner=_claude_runner) -> dict:
    """返回 {summary, tags, error}；任何失败回退占位摘要并把失败原因放进 error
    （成功时 error 为 None）。调用方据 error 把原因贴进 OKF 文件 / PR 正文。"""
    prompt = _PROMPT.format(title=title, body=body[:6000])
    try:
        obj = _parse_json(runner(prompt))
        tags = list(obj.get("tags") or [])
        summary = str(obj.get("summary") or "").strip()
        if not summary:
            return {"summary": SUMMARY_FAILED, "tags": tags, "error": "模型返回空摘要"}
        return {"summary": summary, "tags": tags, "error": None}
    except Exception as e:
        return {"summary": SUMMARY_FAILED, "tags": [], "error": _short(e)}
