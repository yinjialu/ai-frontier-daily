"""采集器：从信息源拉取动态。
- mock 模式：读取 fixtures/sample_items.json（无需联网），用于本地跑通流程
- live 模式：用 feedparser 抓 RSS（sources.yaml 中 rss 列表）。
  注：anthropic.com/news、/research 等是 JS 渲染页面，无官方 RSS，
  生产环境建议用 RSSHub 转成 RSS 后填进 sources.yaml，或另写 Playwright 抓取。
"""
import json, os, hashlib
from pathlib import Path

ROOT = Path(__file__).parent

def _norm(item):
    return {
        "title": (item.get("title") or "").strip(),
        "url": (item.get("url") or item.get("link") or "").strip(),
        "published": item.get("published", ""),
        "source": item.get("source", ""),
        "raw": (item.get("raw") or item.get("summary") or "").strip(),
    }

def collect(mock=True, sources_file="sources.yaml"):
    if mock:
        items = json.loads((ROOT / "fixtures" / "sample_items.json").read_text("utf-8"))
        return [_norm(i) for i in items]

    # ---- live 模式 ----
    import yaml, feedparser  # pip install pyyaml feedparser
    cfg = yaml.safe_load((ROOT / sources_file).read_text("utf-8"))
    out = []
    for feed in cfg.get("rss", []):
        d = feedparser.parse(feed["url"])
        for e in d.entries[: feed.get("limit", 10)]:
            out.append(_norm({
                "title": e.get("title", ""),
                "url": e.get("link", ""),
                "published": e.get("published", e.get("updated", "")),
                "source": feed["name"],
                "raw": e.get("summary", ""),
            }))
    return out

if __name__ == "__main__":
    for it in collect(mock=True):
        print("-", it["source"], "|", it["title"])
