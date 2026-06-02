#!/usr/bin/env python3
"""把当天动态整理成「公众号贴图(newspic) Markdown」，供 wechat-official-draft skill
的 push_draft.mjs --article-type newspic 消费。

Markdown = 文案文字（标题 + 每条摘要）+ 当天小红书整套卡片的 ![]() 图片行。
push_draft.mjs 对 newspic 会：正文取 markdown 纯文本，图片取 markdown 里的 ![]()，
逐张传为永久素材后建贴图草稿（公众号原生图片帖）。

用法：
  python to_wechat_md.py                          # 默认 anthropic，output/anthropic/latest.json 指向的当天
  python to_wechat_md.py --vendor openai          # 指定厂商
  python to_wechat_md.py data/openai/2026-06-02.json  # 指定某天数据文件

产出：
  - 写 output/<vendor>/<date>/公众号贴图.md
  - 向 stdout 打印一行 JSON：{date, vendor, md, title}（title ≤32，与 push_draft.mjs 限制对齐）
"""
import sys, os, json
from pathlib import Path

OUT = Path(os.environ.get("DIGEST_OUT") or os.getcwd())
IMG_EXTS = (".png", ".jpg", ".jpeg")
VENDOR_NAME = {"anthropic": "Anthropic", "openai": "OpenAI", "gemini": "Gemini", "nvidia": "NVIDIA"}


def _arg_value(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def _positional():
    """取非选项的位置参数，跳过 --vendor 及其取值。"""
    out, skip = [], False
    for a in sys.argv[1:]:
        if skip: skip = False; continue
        if a == "--vendor": skip = True; continue
        if a.startswith("--"): continue
        out.append(a)
    return out


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
    args = _positional()
    vendor = _arg_value("--vendor", "anthropic")
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
        raise SystemExit(f"❌ {out_dir} 下没有小红书卡片，请先生成当天卡片。")

    md_path = out_dir / "公众号贴图.md"
    body = build_caption(data) + "\n\n" + "\n\n".join(f"![]({p})" for p in cards) + "\n"
    md_path.write_text(body, "utf-8")

    U = data.get("updates", [])
    name = VENDOR_NAME.get(vendor, "Anthropic")
    title = f"{data.get('cnDate','')}｜{name} 今日 {len(U)} 条动态"[:32]

    print(json.dumps({"date": date, "vendor": vendor, "md": str(md_path), "title": title}, ensure_ascii=False))
    print(f"✓ 已生成 {md_path}（{len(cards)} 图 + 文案）", file=sys.stderr)


if __name__ == "__main__":
    main()
