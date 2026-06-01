#!/usr/bin/env python3
"""把当天 data/<date>.json 转成「微信公众号文章 Markdown」，供 wechat-official-draft
skill 的 push_draft.mjs 消费（该 skill 负责 token / 传图 / 建草稿）。

用法：
  python to_wechat_md.py                      # 用 output/latest.json 指向的当天
  python to_wechat_md.py data/2026-06-01.json # 指定某天

产出：
  - 写 output/<date>/公众号正文.md
  - 向 stdout 打印一行 JSON：{date, md, title, digest, cover}
    （title ≤32、digest ≤128，与 push_draft.mjs 的限制对齐；cover 为公众号封面 PNG）

正文走纯文本 Markdown（不内嵌大图）：小红书/正文长图均为 6–9MB，超过公众号在文
图片 1MB 上限；封面单独作为文章 cover（add_material 限 10MB，900×383 没问题）。
"""
import sys, os, json
from pathlib import Path

OUT = Path(os.environ.get("DIGEST_OUT") or os.getcwd())


def build_markdown(data):
    U = data.get("updates", [])
    lines = [f"**ANTHROPIC DAILY · {data.get('edition','')}**", "",
             f"{data.get('cnDate','')} · 共 {len(U)} 条更新", ""]
    for i, u in enumerate(U, 1):
        lines += [f"## {i:02d} · {u.get('tag','')}｜{u.get('title','')}", "",
                  u.get("summary", ""), "",
                  f"↗ 来源：{u.get('source','')}", ""]
        if i < len(U):
            lines += ["---", ""]
    if data.get("outroDesc"):
        lines += ["> " + data["outroDesc"], ""]
    lines.append(data.get("brand", ""))
    return "\n".join(lines).rstrip() + "\n"


def main():
    if len(sys.argv) > 1:
        data_file = Path(sys.argv[1]); date = data_file.stem
    else:
        latest = json.loads((OUT / "output" / "latest.json").read_text("utf-8"))
        date = latest["dir"]; data_file = OUT / "data" / f"{date}.json"
    data = json.loads(data_file.read_text("utf-8"))

    out_dir = OUT / "output" / date
    md_path = out_dir / "公众号正文.md"
    md_path.write_text(build_markdown(data), "utf-8")

    U = data.get("updates", [])
    title = f"{data.get('cnDate','')}｜Anthropic {len(U)} 条动态"
    if len(title) > 32:                                   # push_draft.mjs 硬限制
        title = title[:32]
    digest = "；".join(u.get("title", "") for u in U[:3])[:128]
    cover = out_dir / "公众号_封面_900x383.png"

    print(json.dumps({"date": date, "md": str(md_path), "title": title,
                      "digest": digest, "cover": str(cover)}, ensure_ascii=False))
    print(f"✓ 已生成 {md_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
