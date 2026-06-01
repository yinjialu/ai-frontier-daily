#!/usr/bin/env python3
"""把当天 data/<date>.json 整理成「小红书发布素材包」，供 xhs-publisher skill
（浏览器自动化驱动 creator.xiaohongshu.com）消费。

用法：
  python to_xhs_post.py                      # 用 output/latest.json 指向的当天
  python to_xhs_post.py data/2026-06-01.json # 指定某天

产出：
  - 写 output/<date>/小红书文案.txt（人可读：标题 / 正文 / 标签 / 配图清单）
  - 向 stdout 打印一行 JSON：{date, title(≤20), content(≤10000), tags, images:[png 绝对路径]}

注意：小红书无合规发布 API，xhs-publisher 走浏览器 UI 自动化，需已登录的 Chrome +
Claude 驱动，且按平台规范【最后由人工点击发布】。本脚本只负责把内容备好。
"""
import sys, os, json
from pathlib import Path

OUT = Path(os.environ.get("DIGEST_OUT") or os.getcwd())
KEYCAP = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
TAGS = "#AI #Anthropic #Claude"          # 小红书建议 ≤3 个标签


def build(data):
    U = data.get("updates", [])
    title = f"Anthropic今日{len(U)}条更新"          # ≤20 字硬限制
    if len(title) > 20:
        title = title[:20]
    lines = [f"Anthropic 今日 {len(U)} 条官方动态 👇", ""]
    for i, u in enumerate(U, 1):
        num = KEYCAP[i] if i < len(KEYCAP) else f"{i}."
        lines += [f"{num}【{u.get('tag','')}】{u.get('title','')}", u.get("summary", ""), ""]
    lines += ["—— AI 前哨 · 每日 Anthropic，点关注不错过 🔔"]
    content = "\n".join(lines).rstrip()
    return title, content, TAGS


def main():
    if len(sys.argv) > 1:
        data_file = Path(sys.argv[1]); date = data_file.stem
    else:
        latest = json.loads((OUT / "output" / "latest.json").read_text("utf-8"))
        date = latest["dir"]; data_file = OUT / "data" / f"{date}.json"
    data = json.loads(data_file.read_text("utf-8"))
    out_dir = OUT / "output" / date

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

    print(json.dumps({"date": date, "title": title, "content": content,
                      "tags": tags, "images": images}, ensure_ascii=False))
    print(f"✓ 已生成 {out_dir/'小红书文案.txt'}（{len(images)} 张配图）", file=sys.stderr)


if __name__ == "__main__":
    main()
