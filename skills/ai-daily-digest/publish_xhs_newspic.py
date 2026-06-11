#!/usr/bin/env python3
"""把当天某厂商的小红书素材包发布为小红书图文笔记（走 xiaohongshu-mcp 本地服务）。

链路：to_xhs_post.py 产出素材 JSON → 本脚本调 localhost:18060/mcp 的 publish_content。
服务未启动时自动拉起（二进制 ~/.local/bin/xiaohongshu-mcp，cookie 在 ~/.config/xiaohongshu-mcp/）。

用法：
  python publish_xhs_newspic.py --vendor anthropic              # 立即公开发布
  python publish_xhs_newspic.py --vendor openai --private       # 仅自己可见（测试链路用）
  python publish_xhs_newspic.py --vendor gemini --dry-run       # 只打印将发布的内容

平台硬限制（xiaohongshu-mcp 文档）：标题 ≤20 字；正文 ≤1000 字；图片路径不能含中文
（本脚本会把卡片复制成 ASCII 临时名再传）。
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

MCP_URL = "http://localhost:18060/mcp"
HEALTH_URL = "http://localhost:18060/health"
MCP_BIN = os.path.expanduser("~/.local/bin/xiaohongshu-mcp")
MCP_HOME = os.path.expanduser("~/.config/xiaohongshu-mcp")
MCP_LOG = os.path.expanduser("~/Library/Logs/xiaohongshu-mcp.log")
HERE = os.path.dirname(os.path.abspath(__file__))
TITLE_MAX, CONTENT_MAX = 20, 1000

# 本地服务，绕过系统代理（TUN 环境下 localhost 也可能被劫持）
_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def _http(url, payload=None, headers=None, timeout=300):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with _opener.open(req, timeout=timeout) as r:
        return r.read().decode(), dict(r.headers)


def _sse_json(body):
    """响应可能是裸 JSON 或 SSE（data: 行）。"""
    for line in body.splitlines():
        if line.startswith("data:"):
            body = line[5:].strip()
            break
    return json.loads(body)


def ensure_service():
    try:
        _http(HEALTH_URL, timeout=5)
        return
    except Exception:
        pass
    print("[0/3] 服务未在线，拉起 xiaohongshu-mcp…", file=sys.stderr)
    with open(MCP_LOG, "a") as log:
        subprocess.Popen([MCP_BIN], cwd=MCP_HOME, stdout=log, stderr=log,
                         start_new_session=True)
    for _ in range(20):
        time.sleep(1)
        try:
            _http(HEALTH_URL, timeout=5)
            return
        except Exception:
            continue
    raise SystemExit("❌ xiaohongshu-mcp 服务拉起失败，看日志 " + MCP_LOG)


class Mcp:
    def __init__(self):
        body, headers = _http(MCP_URL, {
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                       "clientInfo": {"name": "publish_xhs_newspic", "version": "1.0"}},
        }, self._headers())
        self.session = headers.get("Mcp-Session-Id")
        _http(MCP_URL, {"jsonrpc": "2.0", "method": "notifications/initialized"},
              self._headers())

    def _headers(self):
        h = {"Content-Type": "application/json",
             "Accept": "application/json, text/event-stream"}
        if getattr(self, "session", None):
            h["Mcp-Session-Id"] = self.session
        return h

    def call(self, tool, arguments, timeout=300):
        body, _ = _http(MCP_URL, {
            "jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {"name": tool, "arguments": arguments},
        }, self._headers(), timeout=timeout)
        r = _sse_json(body)
        if "error" in r:
            raise RuntimeError(f"{tool} 调用失败：{r['error']}")
        result = r["result"]
        texts = [c.get("text", "") for c in result.get("content", [])
                 if c.get("type") == "text"]
        return result.get("isError", False), "\n".join(texts)


def load_post(vendor):
    """调 to_xhs_post.py 生成素材包，取其 stdout JSON。"""
    p = subprocess.run([sys.executable, os.path.join(HERE, "to_xhs_post.py"),
                        "--vendor", vendor],
                       capture_output=True, text=True, cwd=os.environ.get("DIGEST_OUT") or os.getcwd())
    if p.returncode != 0:
        raise SystemExit(f"❌ to_xhs_post.py 失败：{p.stderr.strip()}")
    return json.loads(p.stdout.strip().splitlines()[-1])


def ascii_copies(images, workdir):
    """图片路径不能含中文：复制成 ASCII 名，保持顺序。"""
    out = []
    for i, src in enumerate(images):
        dst = os.path.join(workdir, f"card_{i:02d}{os.path.splitext(src)[1].lower()}")
        shutil.copyfile(src, dst)
        out.append(dst)
    return out


def main():
    vendor = sys.argv[sys.argv.index("--vendor") + 1] if "--vendor" in sys.argv else "anthropic"
    dry = "--dry-run" in sys.argv
    private = "--private" in sys.argv

    post = load_post(vendor)
    title = post["title"][:TITLE_MAX]
    content = post["content"]
    if len(content) > CONTENT_MAX:
        content = content[:CONTENT_MAX - 12].rstrip() + "\n（更多见图）"
    tags = [t.lstrip("#") for t in post.get("tags", "").split() if t.lstrip("#")]
    if not post["images"]:
        raise SystemExit(f"❌ {vendor} {post['date']} 没有小红书卡片图")

    print(f"  标题（{len(title)} 字）：{title}", file=sys.stderr)
    print(f"  正文 {len(content)} 字；标签 {tags}；图 {len(post['images'])} 张", file=sys.stderr)
    if dry:
        print(json.dumps({"title": title, "content": content, "tags": tags,
                          "images": post["images"]}, ensure_ascii=False, indent=1))
        return

    ensure_service()
    mcp = Mcp()
    is_err, status = mcp.call("check_login_status", {}, timeout=60)
    if is_err or ("true" not in status and "已登录" not in status and "logged" not in status.lower()):
        raise SystemExit(f"❌ 未登录或登录态失效，先跑 ~/.local/bin/xiaohongshu-login（cwd={MCP_HOME}）\n{status}")

    workdir = tempfile.mkdtemp(prefix=f"xhs_{vendor}_")
    try:
        args = {"title": title, "content": content, "tags": tags,
                "images": ascii_copies(post["images"], workdir)}
        if private:
            args["visibility"] = "仅自己可见"
        print(f"[发布] {vendor} {post['date']}（{'仅自己可见' if private else '公开'}）…", file=sys.stderr)
        is_err, text = mcp.call("publish_content", args)
        if is_err:
            raise SystemExit(f"❌ 发布失败：{text}")
        print(text)
        print(f"✅ 小红书笔记已发布：{vendor} {post['date']}", file=sys.stderr)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
