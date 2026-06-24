#!/usr/bin/env python3
"""把专题深度卡片脚本 xhs.json 渲染成小红书图文卡（1080×1440 PNG）。

链路：xhs.json → 校验(xhs_validate) → build_render_data → node render.js → output/deepdive/<slug>/*.png

用法：
  python -m scripts.deepdive.render_xhs content/deepdive/<slug>
  （目录内需有 xhs.json；封面图相对路径写在 xhs.json 的 cover 字段）
"""
import base64
import json
import mimetypes
import subprocess
import sys
from pathlib import Path

from scripts.deepdive.xhs_validate import validate_xhs

REPO = Path(__file__).resolve().parents[2]
RENDER_JS = REPO / "skills" / "ai-daily-digest" / "render.js"


def _image_data_uri(path: Path) -> str:
    """封面图 → base64 data URI。

    render.js 用 page.setContent 渲染（origin=about:blank），Chromium 会拦截
    file:// 子资源，故封面必须内联成 data URI 才能在渲染时加载出来。
    """
    mime = mimetypes.guess_type(str(path))[0] or "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def build_render_data(xhs: dict, article_dir: Path) -> dict:
    """xhs.json dict + 文章目录 → render.js 要的 DATA。cover 内联成 data URI。"""
    cover = xhs.get("cover")
    cover_uri = None
    if cover:
        p = (Path(article_dir) / cover).resolve()
        if p.exists():
            cover_uri = _image_data_uri(p)
    return {
        "kind": "deepdive",
        "slug": xhs.get("slug", ""),
        "title": xhs.get("title", ""),
        "cover": cover_uri,
        "cards": xhs.get("cards", []),
        "caption": xhs.get("caption", ""),
        "tags": xhs.get("tags", []),
    }


def update_index(deepdive_root: Path, slug: str, title: str) -> list[dict]:
    """维护 output/deepdive/index.json（发布页下拉用）：按 slug upsert，最新置顶。"""
    idx_path = deepdive_root / "index.json"
    items: list[dict] = []
    if idx_path.exists():
        try:
            items = json.loads(idx_path.read_text(encoding="utf-8")).get("items", [])
        except (ValueError, OSError):
            items = []
    items = [it for it in items if it.get("slug") != slug]
    items.insert(0, {"slug": slug, "title": title})
    idx_path.parent.mkdir(parents=True, exist_ok=True)
    idx_path.write_text(
        json.dumps({"items": items}, ensure_ascii=False, indent=2), encoding="utf-8")
    return items


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
    if xhs.get("cover") and data["cover"] is None:
        print(f"⚠ 封面路径不存在（{xhs['cover']}），退回文字封面卡", file=sys.stderr)
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
    update_index(REPO / "output" / "deepdive", data["slug"], data["title"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
