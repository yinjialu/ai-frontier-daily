#!/usr/bin/env python3
"""把专题深度卡片脚本 xhs.json 渲染成小红书图文卡（1080×1440 PNG）。

链路：xhs.json → 校验(xhs_validate) → build_render_data → node render.js → output/deepdive/<slug>/*.png

用法：
  python -m scripts.deepdive.render_xhs content/deepdive/<slug>
  （目录内需有 xhs.json；封面图相对路径写在 xhs.json 的 cover 字段）
"""
import json
import subprocess
import sys
from pathlib import Path

from scripts.deepdive.xhs_validate import validate_xhs

REPO = Path(__file__).resolve().parents[2]
RENDER_JS = REPO / "skills" / "ai-daily-digest" / "render.js"


def build_render_data(xhs: dict, article_dir: Path) -> dict:
    """xhs.json dict + 文章目录 → render.js 要的 DATA。"""
    cover = xhs.get("cover")
    cover_abs = None
    if cover:
        p = (Path(article_dir) / cover).resolve()
        if p.exists():
            cover_abs = str(p)
    return {
        "kind": "deepdive",
        "slug": xhs.get("slug", ""),
        "title": xhs.get("title", ""),
        "cover": cover_abs,
        "cards": xhs.get("cards", []),
        "caption": xhs.get("caption", ""),
        "tags": xhs.get("tags", []),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("用法：python -m scripts.deepdive.render_xhs <article_dir>", file=sys.stderr)
        return 2
    article_dir = Path(argv[1]).resolve()
    xhs_path = article_dir / "xhs.json"
    xhs = json.loads(xhs_path.read_text(encoding="utf-8"))

    errors = validate_xhs(xhs)
    if errors:
        print("✗ xhs.json 校验未过，先修：", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        return 1

    data = build_render_data(xhs, article_dir)
    render_json = article_dir / "_render.json"
    render_json.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    out_dir = REPO / "output" / "deepdive" / data["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)

    caption = xhs.get("caption", "")
    tags = " ".join("#" + t for t in xhs.get("tags", []))
    (out_dir / "caption.txt").write_text(
        (caption + "\n\n" + tags).strip(), encoding="utf-8")

    print(f"渲染 → {out_dir}")
    subprocess.run(["node", str(RENDER_JS), str(render_json), str(out_dir)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
