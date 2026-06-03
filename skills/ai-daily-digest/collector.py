"""采集器：从信息源拉取动态。
- mock 模式：读取 fixtures/sample_items.json（无需联网），用于本地跑通流程
- live 模式：抓 RSS（sources.yaml 中 vendors.<vendor>.rss 列表）。
  抓取走「带浏览器 UA 的 urllib + 重试退避 + 超时」再交 feedparser 解析——
  解决 Google CDN（blog.google / deepmind.google）按 UA/指纹拦截裸抓返回 000 的问题；
  失败再兜底交 feedparser 自己抓。每次抓取的成败/产出写入 sources_health.json，
  自动暴露失败源与「停更」源（连续失败或长时间零产出）。
  注：anthropic.com/news、/research 等仍是 JS 渲染、无官方 RSS，需 RSSHub 或 Playwright 另补。
"""
import json, os, time, datetime, urllib.request
from pathlib import Path

ROOT = Path(__file__).parent

# 多数厂商 CDN 会按 UA 拦截裸 requests/curl，这里统一伪装成常见桌面浏览器。
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
_ACCEPT = "application/rss+xml, application/atom+xml, application/xml, text/xml, */*"
_STALE_FAILS = 3        # 连续失败达此次数 → 标记停更
_STALE_DAYS = 14        # 距上次成功超过此天数 → 标记停更


def _norm(item):
    return {
        "title": (item.get("title") or "").strip(),
        "url": (item.get("url") or item.get("link") or "").strip(),
        "published": item.get("published", ""),
        "source": item.get("source", ""),
        "raw": (item.get("raw") or item.get("summary") or "").strip(),
    }

def _vendor_rss(cfg, vendor):
    """兼容两种 sources.yaml：新结构 vendors.<vendor>.rss / 旧结构顶层 rss（视为 anthropic）。"""
    vendors = cfg.get("vendors")
    if vendors:
        return (vendors.get(vendor) or {}).get("rss", [])
    return cfg.get("rss", []) if vendor == "anthropic" else []


# ---------- 抓取：浏览器 UA + 重试退避 + 超时 ----------
def _fetch_bytes(url, tries=3, timeout=20):
    """带 UA 抓原始字节；失败重试（1s/2s/4s 退避）。返回 (bytes|None, error_str)。"""
    last = ""
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": _UA, "Accept": _ACCEPT,
                "Accept-Language": "en-US,en;q=0.9"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read(), ""
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
            if i < tries - 1:
                time.sleep(2 ** i)
    return None, last

def _parse_feed(url):
    """先用 UA 抓字节再 parse；UA 抓失败则兜底交 feedparser 自抓。返回 (parsed, fetch_err)。"""
    import feedparser
    raw, err = _fetch_bytes(url)
    if raw is not None:
        return feedparser.parse(raw), ""
    return feedparser.parse(url, agent=_UA), err   # 兜底：feedparser 内部抓取（带 UA）


# ---------- 信源健康：记录成败/产出，标记失败源与停更源 ----------
def _days_since(iso):
    if not iso:
        return 999
    try:
        dt = datetime.datetime.fromisoformat(iso)
        now = datetime.datetime.now(dt.tzinfo) if dt.tzinfo else datetime.datetime.now()
        return max(0, (now - dt).days)
    except Exception:
        return 999

def _update_health(health_path, vendor, records):
    """读改写 sources_health.json（跨厂商共享，仅更新本厂商条目，保留 last_success 历史）。"""
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    p = Path(health_path)
    data = {}
    if p.exists():
        try:
            data = json.loads(p.read_text("utf-8"))
        except Exception:
            data = {}
    for rec in records:
        key = f"{vendor}/{rec['name']}"
        prev = data.get(key, {})
        data[key] = {
            "vendor": vendor, "name": rec["name"], "url": rec["url"], "type": "rss",
            "last_attempt": now,
            "last_success": now if rec["ok"] else prev.get("last_success"),
            "ok": rec["ok"], "items": rec["items"], "error": rec["error"],
            "consecutive_failures": 0 if rec["ok"] else int(prev.get("consecutive_failures", 0)) + 1,
        }
    for v in data.values():
        ls = v.get("last_success")
        # 停更 = 连续失败达阈值，或「曾经成功过」但长时间无产出；从未成功的新源只算「失败」不算停更
        v["stale"] = (v.get("consecutive_failures", 0) >= _STALE_FAILS) \
                     or bool(ls and _days_since(ls) >= _STALE_DAYS)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), "utf-8")
    return data

def _print_health(data, vendor):
    rows = [v for v in data.values() if v["vendor"] == vendor]
    ok = sum(1 for v in rows if v["ok"])
    print(f"      信源健康：{ok}/{len(rows)} 正常")
    for v in rows:
        if not v["ok"] or v.get("stale"):
            mark = "⚠ 停更" if v.get("stale") else "✗ 失败"
            print(f"        {mark}  {v['name']} — {v['error'] or '本次零产出'}")


def collect(mock=True, sources_file="sources.yaml", vendor="anthropic", health_path=None):
    if mock:
        items = json.loads((ROOT / "fixtures" / "sample_items.json").read_text("utf-8"))
        return [_norm(i) for i in items]

    # ---- live 模式 ----
    import yaml  # pip install pyyaml feedparser
    cfg = yaml.safe_load((ROOT / sources_file).read_text("utf-8"))
    out, records = [], []
    for feed in _vendor_rss(cfg, vendor):
        d, ferr = _parse_feed(feed["url"])
        entries = list(getattr(d, "entries", []) or [])
        bozo = bool(getattr(d, "bozo", 0))
        # 有条目即视为成功；零条目且解析报错（如 soft-404 返回 HTML / 非 feed）视为失败
        ok = len(entries) > 0 or not bozo
        err = ""
        if not ok:
            be = getattr(d, "bozo_exception", "")
            err = ferr or (f"{type(be).__name__}: {be}" if be else "非 feed 或零条目")
        for e in entries[: feed.get("limit", 10)]:
            out.append(_norm({
                "title": e.get("title", ""),
                "url": e.get("link", ""),
                "published": e.get("published", e.get("updated", "")),
                "source": feed["name"],
                "raw": e.get("summary", ""),
            }))
        records.append({"name": feed["name"], "url": feed["url"],
                        "ok": ok, "items": len(entries), "error": err})

    if health_path:
        _print_health(_update_health(health_path, vendor, records), vendor)
    return out


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    live = "--live" in args
    v = next((a for a in args if not a.startswith("--")), "anthropic")
    hp = (Path(os.getcwd()) / "output" / "sources_health.json") if live else None
    items = collect(mock=not live, vendor=v, health_path=hp)
    for it in items:
        print("-", it["source"], "|", it["title"])
    print(f"total: {len(items)}")
