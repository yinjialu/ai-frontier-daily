#!/usr/bin/env python3
"""把当天动态整理成「微信公众号图文 Markdown」，供 wechat-official-draft skill
的 push_draft.mjs 消费（它负责 token / 传图 / 建草稿）。

正文＝直接复用当天小红书那套竖图（不重新排版）。卡片渲染已是 JPEG 小图
（约 100–300KB，低于公众号在文图片 1MB 上限），push_draft.mjs 会逐张 uploadimg
并替换为微信 URL。封面缩略图用公众号封面（比例合适）。

用法：
  python to_wechat_md.py                      # 用 output/latest.json 指向的当天
  python to_wechat_md.py data/2026-06-01.json # 指定某天

产出：
  - 写 output/<date>/公众号图文.md（仅按序排列的图片）
  - 向 stdout 打印一行 JSON：{date, md, title, digest, cover}
"""
import sys, os, json
from pathlib import Path

OUT = Path(os.environ.get("DIGEST_OUT") or os.getcwd())
IMG_EXTS = (".png", ".jpg", ".jpeg")


def _imgs(out_dir, prefix):
    return [p for p in sorted(out_dir.glob(prefix + "*")) if p.suffix.lower() in IMG_EXTS]


def main():
    if len(sys.argv) > 1:
        data_file = Path(sys.argv[1]); date = data_file.stem
    else:
        latest = json.loads((OUT / "output" / "latest.json").read_text("utf-8"))
        date = latest["dir"]; data_file = OUT / "data" / f"{date}.json"
    data = json.loads(data_file.read_text("utf-8"))
    out_dir = OUT / "output" / date

    cards = _imgs(out_dir, "小红书_")                       # 正文＝小红书整套竖图
    if not cards:
        raise SystemExit(f"❌ {out_dir} 下没有小红书卡片，请先生成当天卡片。")
    md_path = out_dir / "公众号图文.md"
    md_path.write_text("\n\n".join(f"![]({p})" for p in cards) + "\n", "utf-8")

    # 封面缩略图：优先公众号封面（比例合适），否则退回小红书封面
    gzh_cover = _imgs(out_dir, "公众号_封面")
    cover = str(gzh_cover[0]) if gzh_cover else str(cards[0])

    U = data.get("updates", [])
    title = f"{data.get('cnDate','')}｜Anthropic 今日 {len(U)} 条动态"[:32]
    digest = "；".join(u.get("title", "") for u in U[:3])[:128]

    print(json.dumps({"date": date, "md": str(md_path), "title": title,
                      "digest": digest, "cover": cover}, ensure_ascii=False))
    print(f"✓ 已生成 {md_path}（正文 {len(cards)} 图）", file=sys.stderr)


if __name__ == "__main__":
    main()
