#!/usr/bin/env python3
"""把当天小红书整套卡片发成微信公众号「贴图」草稿（图片消息 / article_type=newspic）。

与 to_wechat_md.py 的「图文文章(news)」不同：贴图是公众号的图片帖类型（像小红书那样
一张张卡片），更贴合卡片形态。push_draft.mjs（wechat-official-draft skill）只支持 news，
故这里单独走 newspic：每张卡片传为永久素材拿 image_media_id → draft/add(image_info)。

用法：
  python publish_wechat_newspic.py                          # 默认 anthropic，output/anthropic/latest.json 当天
  python publish_wechat_newspic.py --vendor openai          # 指定厂商
  python publish_wechat_newspic.py data/openai/2026-06-02.json  # 指定某天数据文件
  python publish_wechat_newspic.py --dry-run                # 只打印将提交的结构，不碰 API
  python publish_wechat_newspic.py --no-comment             # 本次不开留言（默认开）
  python publish_wechat_newspic.py --fans-only              # 留言仅限粉丝（默认所有人）

凭据：环境变量 WECHAT_APPID/WECHAT_SECRET，或 ~/.config/wechat-official-draft/config.yaml。
前置：本机公网 IP 在公众号 IP 白名单；需已认证服务号。
留言：默认 need_open_comment=1（开启、所有人可评论）。仅当公众号已「开通留言功能」时
      草稿/群发才会真正展示留言区；未开通则该参数被忽略，需到公众号后台申请开通。
"""
import sys, os, re, json, mimetypes, urllib.request
from pathlib import Path

API = "https://api.weixin.qq.com/cgi-bin"
OUT = Path(os.environ.get("DIGEST_OUT") or os.getcwd())
IMG_EXTS = (".png", ".jpg", ".jpeg")
VENDOR_NAME = {"anthropic": "Anthropic", "openai": "OpenAI", "gemini": "Gemini", "nvidia": "NVIDIA", "cn": "国产模型"}


def _arg_value(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def _positional():
    """取非选项的位置参数，跳过 --vendor 及其取值（--dry-run 等无值开关直接略过）。"""
    out, skip = [], False
    for a in sys.argv[1:]:
        if skip: skip = False; continue
        if a == "--vendor": skip = True; continue
        if a.startswith("--"): continue
        out.append(a)
    return out


def load_creds():
    appid, secret = os.environ.get("WECHAT_APPID"), os.environ.get("WECHAT_SECRET")
    if appid and secret:
        return appid, secret
    cfg = Path.home() / ".config" / "wechat-official-draft" / "config.yaml"
    if cfg.is_file():
        txt = cfg.read_text("utf-8")
        a = re.search(r"appid:\s*([^\s#]+)", txt)
        s = re.search(r"secret:\s*([^\s#]+)", txt)
        if a and s:
            return a.group(1), s.group(1)
    raise SystemExit("❌ 缺少凭据：设 WECHAT_APPID/WECHAT_SECRET 或填 ~/.config/wechat-official-draft/config.yaml")


def _get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def _post_json(url, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def _post_file(url, filepath):
    boundary = "----newspic" + os.urandom(8).hex()
    fname = os.path.basename(filepath)
    ctype = mimetypes.guess_type(fname)[0] or "image/jpeg"
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
        code, msg = resp["errcode"], resp.get("errmsg", "")
        hint = {40164: "本机公网 IP 不在白名单", 40125: "AppSecret 不对",
                48001: "接口无权限（需已认证服务号）"}.get(code, "")
        raise SystemExit(f"❌ {what} 失败：errcode={code} errmsg={msg}{(' → '+hint) if hint else ''}")
    return resp


def build_caption(data):
    U = data.get("updates", [])
    name = VENDOR_NAME.get(data.get("vendor", "anthropic"), "Anthropic")
    brand = data.get("brand", f"AI 前哨 · 每日 {name}")
    lines = [f"{data.get('cnDate','')} · {name} 今日 {len(U)} 条动态", ""]
    for i, u in enumerate(U, 1):
        lines += [f"{i}.【{u.get('tag','')}】{u.get('title','')}", u.get("summary", ""), ""]
    lines.append(f"—— {brand}，点关注不错过")
    return "\n".join(lines).rstrip()


def main():
    dry = "--dry-run" in sys.argv
    # 留言：默认开启、所有人可评论；--no-comment 关闭，--fans-only 仅粉丝
    # 注意：草稿层置 1 即请求开启，但能否真正显示留言取决于公众号是否已开通「留言功能」。
    open_comment = 0 if "--no-comment" in sys.argv else 1
    fans_only = 1 if "--fans-only" in sys.argv else 0
    vendor = _arg_value("--vendor", "anthropic")
    args = _positional()
    if args:
        data_file = Path(args[0]); date = data_file.stem
        vendor = data_file.parent.name if data_file.parent.name in VENDOR_NAME else vendor
    else:
        latest = json.loads((OUT / "output" / vendor / "latest.json").read_text("utf-8"))
        date = latest["dir"]; data_file = OUT / "data" / vendor / f"{date}.json"
    data = json.loads(data_file.read_text("utf-8"))
    vendor = data.get("vendor", vendor)
    out_dir = OUT / "output" / vendor / date

    cards = [p for p in sorted(out_dir.glob("小红书_*")) if p.suffix.lower() in IMG_EXTS]
    if not cards:
        raise SystemExit(f"❌ {out_dir} 下没有小红书卡片。")
    cards = cards[:20]                                   # newspic 最多 20 张

    U = data.get("updates", [])
    name = VENDOR_NAME.get(vendor, "Anthropic")
    title = f"{data.get('cnDate','')}｜{name} 今日 {len(U)} 条动态"[:64]
    caption = build_caption(data)

    if dry:
        print(json.dumps({"article_type": "newspic", "title": title,
                          "images": [c.name for c in cards], "content": caption,
                          "need_open_comment": open_comment, "only_fans_can_comment": fans_only},
                         ensure_ascii=False, indent=2))
        return

    appid, secret = load_creds()
    print("[1/3] 获取 access_token…")
    token = _check(_get(f"{API}/token?grant_type=client_credential&appid={appid}&secret={secret}"),
                   "获取 access_token")["access_token"]

    print(f"[2/3] 上传 {len(cards)} 张卡片为永久素材…")
    media_ids = []
    for c in cards:
        mat = _check(_post_file(f"{API}/material/add_material?access_token={token}&type=image", str(c)),
                     f"上传 {c.name}")
        media_ids.append(mat["media_id"])
        print(f"      ✓ {c.name}")

    print("[3/3] 创建贴图草稿…")
    article = {
        "article_type": "newspic",
        "title": title,
        "content": caption,
        "image_info": {"image_list": [{"image_media_id": m} for m in media_ids]},
        "need_open_comment": open_comment,
        "only_fans_can_comment": fans_only,
    }
    res = _check(_post_json(f"{API}/draft/add?access_token={token}", {"articles": [article]}),
                 "创建贴图草稿")
    print(f"\n✅ 贴图草稿已创建：media_id={res.get('media_id')}")
    print("   去【公众号后台 → 草稿箱】核对，确认后手动发布。")


if __name__ == "__main__":
    main()
