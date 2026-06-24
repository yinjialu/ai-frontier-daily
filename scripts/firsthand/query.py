"""查询内参 OKF 索引："最近有什么新动态"。

可被 firsthand-digest skill 调用，也可当 CLI：
    python3 -m scripts.firsthand.query --days 7 [--json]
"""
import argparse
import datetime
import json
from pathlib import Path


# 内参 source id → 每日早报 vendor 轨。供早报(云端,IP 抓不到 news/blog)消费内参(本机抓)补盲区。
SOURCE_VENDOR = {
    "claude-blog": "anthropic", "anthropic-news": "anthropic",
    "anthropic-research": "anthropic", "anthropic-engineering": "anthropic",
    "transformer-circuits": "anthropic",
    "openai-news": "openai",
    "deepmind-blog": "gemini", "google-models-research": "gemini",
    "google-gemini": "gemini",
    "qwen-blog": "cn", "inclusionai-ling": "cn",
}


def vendor_of(source: str) -> str | None:
    return SOURCE_VENDOR.get(source)


def filter_vendor(items: list[dict], vendor: str) -> list[dict]:
    return [a for a in items if vendor_of(a.get("source")) == vendor]


def load_index(okf_root) -> list[dict]:
    p = Path(okf_root) / "index.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("items", [])


def recent(items: list[dict], days: int, today: str) -> list[dict]:
    """返回 detected 在近 days 天内的条目，按 detected 倒序。today 形如 'YYYY-MM-DD'。"""
    cutoff = (datetime.date.fromisoformat(today)
              - datetime.timedelta(days=days)).isoformat()
    out = [a for a in items if (a.get("detected") or "")[:10] >= cutoff]
    out.sort(key=lambda a: a.get("detected") or "", reverse=True)
    return out


def _render_text(items: list[dict]) -> str:
    if not items:
        return "近期无新动态。"
    by_source: dict[str, list] = {}
    for a in items:
        by_source.setdefault(a.get("source") or "?", []).append(a)
    lines = [f"近期新动态（{len(items)} 篇）：", ""]
    for sid, arts in by_source.items():
        lines.append(f"## {sid}（{len(arts)}）")
        for a in arts:
            pub = a.get("published") or "?"
            lines.append(f"- [{pub}] {a.get('title')} — {a.get('resource')}")
            if a.get("summary"):
                lines.append(f"  > {a['summary']}")
        lines.append("")
    return "\n".join(lines).rstrip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--vendor", default=None,
                    help="按早报 vendor 轨过滤（anthropic/openai/gemini/cn）")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent.parent
                                          / "data" / "firsthand"))
    ap.add_argument("--json", action="store_true", help="输出 JSON（给 agent 消费）")
    args = ap.parse_args()
    today = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=8))).date().isoformat()
    items = recent(load_index(args.root), args.days, today)
    if args.vendor:
        items = filter_vendor(items, args.vendor)
    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
    else:
        print(_render_text(items))


if __name__ == "__main__":
    main()
