#!/usr/bin/env python3
"""把当天 data/<date>.json 整理成「小红书发布素材包」，供 xhs-publisher skill
（浏览器自动化驱动 creator.xiaohongshu.com）消费。

用法：
  python to_xhs_post.py                          # 默认 anthropic，用 output/anthropic/latest.json 指向的当天
  python to_xhs_post.py --vendor openai          # 指定厂商
  python to_xhs_post.py data/openai/2026-06-02.json  # 指定某天数据文件

产出：
  - 写 output/<vendor>/<date>/小红书文案.txt（人可读：标题 / 正文 / 标签 / 配图清单）
  - 向 stdout 打印一行 JSON：{date, vendor, title(≤20), content(≤10000), tags, images:[png 绝对路径]}

注意：小红书无合规发布 API，xhs-publisher 走浏览器 UI 自动化，需已登录的 Chrome +
Claude 驱动，且按平台规范【最后由人工点击发布】。本脚本只负责把内容备好。
"""
import sys, os, json
from pathlib import Path

OUT = Path(os.environ.get("DIGEST_OUT") or os.getcwd())
KEYCAP = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
# 各厂商：显示名 + 小红书标签（建议 ≤3 个）
VENDOR_META = {
    "anthropic": {"name": "Anthropic", "tags": "#AI #Anthropic #Claude"},
    "openai":    {"name": "OpenAI", "tags": "#AI #OpenAI #ChatGPT"},
    "gemini":    {"name": "Gemini", "tags": "#AI #Gemini #Google"},
    "nvidia":    {"name": "NVIDIA", "tags": "#AI #NVIDIA #GPU"},
}


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


def build(data):
    U = data.get("updates", [])
    meta = VENDOR_META.get(data.get("vendor", "anthropic"), VENDOR_META["anthropic"])
    name, tags = meta["name"], meta["tags"]
    brand = data.get("brand", f"AI 前哨 · 每日 {name}")
    title = f"{name}今日{len(U)}条更新"[:20]          # ≤20 字硬限制
    lines = [f"{name} 今日 {len(U)} 条官方动态 👇", ""]
    for i, u in enumerate(U, 1):
        num = KEYCAP[i] if i < len(KEYCAP) else f"{i}."
        lines += [f"{num}【{u.get('tag','')}】{u.get('title','')}", u.get("summary", ""), ""]
    lines += [f"—— {brand}，点关注不错过 🔔"]
    content = "\n".join(lines).rstrip()
    return title, content, tags


def main():
    args = _positional()
    vendor = _arg_value("--vendor", "anthropic")
    if args:
        data_file = Path(args[0]); date = data_file.stem
        vendor = data_file.parent.name if data_file.parent.name in VENDOR_META else vendor
    else:
        latest = json.loads((OUT / "output" / vendor / "latest.json").read_text("utf-8"))
        date = latest["dir"]; data_file = OUT / "data" / vendor / f"{date}.json"
    data = json.loads(data_file.read_text("utf-8"))
    vendor = data.get("vendor", vendor)
    out_dir = OUT / "output" / vendor / date

    title, content, tags = build(data)
    # 配图：按文件名排序的小红书竖图（00 封面 → 99 结尾），jpg/png 皆可
    images = [str(p) for p in sorted(out_dir.glob("小红书_*"))
              if p.suffix.lower() in (".png", ".jpg", ".jpeg")]

    txt = (f"【标题】（≤20 字）\n{title}\n\n"
           f"【正文】\n{content}\n\n"
           f"【标签】\n{tags}\n\n"
           f"【配图】（按此顺序上传，共 {len(images)} 张）\n" +
           "\n".join(f"  {i+1}. {os.path.basename(p)}" for i, p in enumerate(images)) + "\n")
    (out_dir / "小红书文案.txt").write_text(txt, "utf-8")

    print(json.dumps({"date": date, "vendor": vendor, "title": title, "content": content,
                      "tags": tags, "images": images}, ensure_ascii=False))
    print(f"✓ 已生成 {out_dir/'小红书文案.txt'}（{len(images)} 张配图）", file=sys.stderr)


if __name__ == "__main__":
    main()
