"""从 OKF 库反向生成索引产物：index.json（给 agent/skill 消费）+ feed.xml（RSS 阅读器）。

不打分、不做个性化——只是把 data/firsthand/<id>/*.md 汇成一个按发布时间倒序的清单。
updated 字段取已有内容里的最大 detected（稳定值），内容不变时重复生成字节一致 → 不刷屏。
"""
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

_FM = {
    "title": re.compile(r"^title:\s*(.+?)\s*$", re.M),
    "source": re.compile(r"^source:\s*(\S+)\s*$", re.M),
    "resource": re.compile(r"^resource:\s*(\S+)\s*$", re.M),
    "published": re.compile(r"^published:\s*(\S+)\s*$", re.M),
    "detected": re.compile(r"^detected:\s*(\S+)\s*$", re.M),
    "tags": re.compile(r"^tags:\s*\[(.*)\]\s*$", re.M),
}


def parse_okf(text: str) -> dict:
    parts = text.split("---", 2)
    fm = parts[1] if len(parts) >= 3 else ""
    body = parts[2].strip() if len(parts) >= 3 else ""
    out = {}
    for k, rx in _FM.items():
        m = rx.search(fm)
        out[k] = m.group(1).strip() if m else None
    out["tags"] = [t.strip() for t in (out["tags"] or "").split(",") if t.strip()]
    out["summary"] = body
    return out


def build_index(okf_root) -> list[dict]:
    """扫 <root>/<source>/*.md，按 published 倒序（None 最后），再按 detected 倒序。"""
    root = Path(okf_root)
    items = [parse_okf(md.read_text(encoding="utf-8")) for md in root.glob("*/*.md")]
    items.sort(key=lambda a: (a.get("published") or "0000-00-00",
                              a.get("detected") or ""), reverse=True)
    return items


def _rss(items: list[dict], updated: str) -> str:
    rss_items = []
    for a in items:
        pub = a.get("published") or ""
        rss_items.append(
            "<item>"
            f"<title>{escape(a.get('title') or '')}</title>"
            f"<link>{escape(a.get('resource') or '')}</link>"
            f"<guid isPermaLink=\"true\">{escape(a.get('resource') or '')}</guid>"
            f"<category>{escape(a.get('source') or '')}</category>"
            f"<pubDate>{escape(pub)}</pubDate>"
            f"<description>{escape(a.get('summary') or '')}</description>"
            "</item>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0"><channel>'
        "<title>一手信源内参</title>"
        "<link>https://github.com/yinjialu/ai-frontier-daily</link>"
        "<description>AI 大厂官方一手动态内参（OKF 库导出）</description>"
        f"<lastBuildDate>{escape(updated)}</lastBuildDate>"
        + "".join(rss_items) +
        "</channel></rss>\n")


def write_outputs(okf_root) -> tuple[Path, Path]:
    """生成 index.json + feed.xml 到 okf_root 根，返回两文件路径。"""
    root = Path(okf_root)
    items = build_index(root)
    updated = max((a.get("detected") or "" for a in items), default="")
    index = {"updated": updated, "count": len(items), "items": items}
    json_path = root / "index.json"
    json_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    feed_path = root / "feed.xml"
    feed_path.write_text(_rss(items, updated), encoding="utf-8")
    return json_path, feed_path
