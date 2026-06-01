#!/usr/bin/env python3
"""把当天动态推送到微信公众号「草稿箱」（不群发，最后一步由你在后台手动发布）。

用法：
  python publish_wechat.py                       # 用 output/latest.json 指向的当天
  python publish_wechat.py data/2026-06-01.json  # 指定某天的 data 文件

前置条件（缺一不可）：
  1. 一个【已认证的服务号】（订阅号无 draft/add 接口权限）。
  2. 在 .env（或环境变量）里配置：
        WECHAT_APPID=wx................
        WECHAT_SECRET=................................
  3. 把【运行本脚本机器的公网 IP】加入公众平台 → 设置与开发 → 安全中心 → IP 白名单。
     （GitHub Actions 的 runner IP 是动态的，无法白名单，故本步骤需在你本机/固定 IP 服务器跑。）

流程：拿 access_token → 上传封面为永久素材拿 thumb_media_id → 用结构化数据拼正文 HTML
→ 调 draft/add 建草稿 → 打印草稿 media_id，提醒你去后台「草稿箱」核对并群发。
"""
import sys, os, json, html, mimetypes, urllib.request, urllib.parse
from pathlib import Path

API = "https://api.weixin.qq.com/cgi-bin"
OUT = Path(os.environ.get("DIGEST_OUT") or os.getcwd())
ROOT = Path(__file__).parent


def load_env():
    """轻量读取仓库根目录 .env（不覆盖已存在的环境变量）。"""
    for p in (OUT / ".env", ROOT.parent.parent / ".env"):
        if p.is_file():
            for line in p.read_text("utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def _get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def _post_json(url, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")   # 不转义中文，避免公众号乱码
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def _post_file(url, filepath):
    """multipart/form-data 上传单个文件，字段名 media。"""
    boundary = "----wechatdigest" + os.urandom(8).hex()
    fname = os.path.basename(filepath)
    ctype = mimetypes.guess_type(fname)[0] or "image/png"
    data = open(filepath, "rb").read()
    pre = (f"--{boundary}\r\n"
           f'Content-Disposition: form-data; name="media"; filename="{fname}"\r\n'
           f"Content-Type: {ctype}\r\n\r\n").encode("utf-8")
    post = f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(url, data=pre + data + post,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def _check(resp, what):
    if isinstance(resp, dict) and resp.get("errcode"):
        code = resp["errcode"]
        msg = resp.get("errmsg", "")
        hint = ""
        if code in (40164, 41010) or "ip" in msg.lower():
            hint = "\n   → 多半是【IP 未加白名单】：把本机公网 IP 加到公众平台安全中心的 IP 白名单。"
        elif code == 40125 or "secret" in msg.lower():
            hint = "\n   → AppSecret 不对，检查 .env 的 WECHAT_SECRET。"
        elif code in (48001, 40097) or "permission" in msg.lower():
            hint = "\n   → 接口无权限：draft/add 需要【已认证的服务号】，订阅号不支持。"
        raise SystemExit(f"❌ {what} 失败：errcode={code} errmsg={msg}{hint}")
    return resp


TAG_COLORS = {"模型发布": "#C1572E", "开发者": "#B26A2E", "企业": "#5A7D5A",
              "研究": "#4A6FA5", "生态": "#8A6FA5", "政策": "#9E3F1E", "安全": "#A53F3F"}


def build_content_html(data):
    """用结构化数据拼公众号正文（公众号会清除 <style>，只能用内联样式）。"""
    U = data.get("updates", [])
    ink, soft, line = "#26221C", "#5A5347", "#E3DCCB"
    parts = [f'<section style="font-size:16px;line-height:1.5;color:{ink};'
             f'font-family:-apple-system,BlinkMacSystemFont,\'PingFang SC\',sans-serif;">']
    parts.append(
        f'<p style="font-size:13px;letter-spacing:1px;color:{TAG_COLORS["模型发布"]};'
        f'margin:0 0 4px;">ANTHROPIC DAILY · {html.escape(data.get("edition",""))}</p>'
        f'<p style="font-size:14px;color:{soft};margin:0 0 22px;">{html.escape(data.get("cnDate",""))} · '
        f'共 {len(U)} 条更新</p>')
    for i, u in enumerate(U, 1):
        color = TAG_COLORS.get(u.get("tag"), "#C1572E")
        parts.append('<section style="margin:0 0 26px;">')
        parts.append(
            f'<span style="display:inline-block;background:{color};color:#fff;font-size:13px;'
            f'padding:3px 12px;border-radius:20px;letter-spacing:1px;">'
            f'{html.escape(u.get("tag",""))}</span>')
        parts.append(
            f'<p style="font-size:19px;font-weight:700;color:{ink};margin:12px 0 0;'
            f'line-height:1.4;">{i:02d} · {html.escape(u.get("title",""))}</p>')
        parts.append(
            f'<p style="font-size:15px;color:{soft};line-height:1.85;margin:10px 0 0;">'
            f'{html.escape(u.get("summary",""))}</p>')
        parts.append(
            f'<p style="font-size:13px;color:{color};margin:8px 0 0;">↗ '
            f'{html.escape(u.get("source",""))}</p>')
        parts.append(f'<p style="border-top:1px solid {line};margin:22px 0 0;height:0;"></p>'
                     if i < len(U) else "")
        parts.append('</section>')
    outro = data.get("outroDesc", "")
    if outro:
        parts.append(f'<p style="font-size:14px;color:{soft};line-height:1.8;margin:8px 0 0;">'
                     f'{html.escape(outro)}</p>')
    parts.append(f'<p style="font-size:13px;color:{soft};margin:20px 0 0;">'
                 f'{html.escape(data.get("brand",""))}</p>')
    parts.append('</section>')
    return "".join(parts)


def main():
    load_env()
    appid = os.environ.get("WECHAT_APPID")
    secret = os.environ.get("WECHAT_SECRET")
    if not appid or not secret:
        raise SystemExit("❌ 缺少 WECHAT_APPID / WECHAT_SECRET。复制 .env.example 为 .env 并填入。")

    # 定位当天 data 与输出目录
    if len(sys.argv) > 1:
        data_file = Path(sys.argv[1])
        date = data_file.stem
    else:
        latest = json.loads((OUT / "output" / "latest.json").read_text("utf-8"))
        date = latest["dir"]
        data_file = OUT / "data" / f"{date}.json"
    data = json.loads(data_file.read_text("utf-8"))
    out_dir = OUT / "output" / date
    cover = out_dir / "公众号_封面_900x383.png"
    if not cover.is_file():
        raise SystemExit(f"❌ 找不到封面 {cover}，请先生成当天卡片。")

    print("[1/3] 获取 access_token…")
    tok = _check(_get(f"{API}/token?grant_type=client_credential"
                      f"&appid={urllib.parse.quote(appid)}&secret={urllib.parse.quote(secret)}"),
                 "获取 access_token")
    token = tok["access_token"]

    print("[2/3] 上传封面为永久素材…")
    mat = _check(_post_file(f"{API}/material/add_material?access_token={token}&type=image", str(cover)),
                 "上传封面素材")
    thumb_media_id = mat["media_id"]

    print("[3/3] 创建草稿…")
    U = data.get("updates", [])
    title = f'{data.get("cnDate","")}｜Anthropic 今日 {len(U)} 条动态'[:64]
    digest = ("；".join(u.get("title", "") for u in U[:3]))[:120]
    article = {
        "title": title,
        "author": (data.get("brand", "AI 前哨"))[:8],
        "digest": digest,
        "content": build_content_html(data),
        "content_source_url": "",
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    }
    res = _check(_post_json(f"{API}/draft/add?access_token={token}", {"articles": [article]}),
                 "创建草稿")

    print(f"\n✅ 草稿已创建：media_id={res.get('media_id')}")
    print("   去【公众号后台 → 草稿箱】核对排版，确认无误后手动「群发」即可。")


if __name__ == "__main__":
    main()
