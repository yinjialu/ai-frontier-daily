#!/usr/bin/env python3
"""主流程编排：采集 → 去重 → 摘要 → 渲染 → 更新展示页。
多厂商：--vendor anthropic|openai（缺省 anthropic）。数据/产物按厂商分轨：
  data/<vendor>/<date>.json   output/<vendor>/<date>/*.jpg   output/<vendor>/latest.json
展示页索引 output/index.json 汇总所有厂商（每天一条，带 vendor 字段）。

用法：
  python run.py                       # mock 模式：无需联网/密钥，本地跑通整条流程（anthropic）
  python run.py --vendor openai       # 指定厂商
  python run.py --live                # 真实模式：抓 RSS + 调 Claude API（需 ANTHROPIC_API_KEY）
  python run.py --force               # 忽略去重，强制处理（调试用）
  python run.py --engine playwright   # 用 Playwright 渲染（生产推荐，字体保真）
  python run.py --reindex             # 仅重建 latest.json + index.json（jpg 感知，扫描所有厂商）
"""
import sys, os, json, subprocess, datetime
from pathlib import Path
import collector, dedup, curator

ROOT = Path(__file__).parent                                  # 脚本与字体/模板所在目录
OUT = Path(os.environ.get("DIGEST_OUT") or os.getcwd())        # data/ 与 output/ 写到这里（默认当前目录）

IMG_EXTS = (".png", ".jpg", ".jpeg")                          # 卡片可能是 png 或 jpg
def _img_names(d):
    return [p.name for p in sorted(d.glob("*")) if p.suffix.lower() in IMG_EXTS] if d.is_dir() else []

def _arg_value(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def write_index(out: Path):
    """扫描 data/<vendor>/*.json 与 output/<vendor>/<date>/，生成：
      - output/index.json：每天一条 {vendor, date, dir, cnDate, edition, count, files}，供展示页浏览/热力图
      - output/<vendor>/latest.json：各厂商最新一天指针，供发布脚本消费
    dir = "<vendor>/<date>"（相对 output/）。count = 当天策展后的动态条数。"""
    days, latest = [], {}
    for df in sorted((out / "data").glob("*/*.json")):
        vendor = df.parent.name
        date = df.stem
        try:
            d = json.loads(df.read_text("utf-8"))
        except Exception:
            continue
        odir = out / "output" / vendor / date
        files = _img_names(odir)
        entry = {
            "vendor": vendor, "date": date, "dir": f"{vendor}/{date}",
            "cnDate": d.get("cnDate", ""), "edition": d.get("edition", ""),
            "count": len(d.get("updates", [])), "files": files,
        }
        days.append(entry)
        if date >= latest.get(vendor, {}).get("date", ""):
            latest[vendor] = entry

    days.sort(key=lambda x: (x["date"], x["vendor"]))
    vendors = sorted({e["vendor"] for e in days})
    idx = {"updated": days[-1]["date"] if days else "", "vendors": vendors, "days": days}
    (out / "output").mkdir(parents=True, exist_ok=True)
    (out / "output" / "index.json").write_text(
        json.dumps(idx, ensure_ascii=False, indent=2), "utf-8")

    # 各厂商 latest.json（dir 用裸日期，发布脚本据此拼 output/<vendor>/<date>）
    for vendor, e in latest.items():
        (out / "output" / vendor).mkdir(parents=True, exist_ok=True)
        (out / "output" / vendor / "latest.json").write_text(
            json.dumps({"vendor": vendor, "date": e["date"], "cnDate": e["cnDate"],
                        "dir": e["date"], "files": e["files"]}, ensure_ascii=False, indent=2), "utf-8")
    return idx


def list_vendors():
    """打印 vendor 清单 JSON（供 routine/CI 自适应遍历，新增厂商后自动出现）：
    [{id, name, brand, sources:[抓取 URL]}]。清单来源 = curator.VENDOR_META（纯 Python，
    无依赖必可用）；各家源 URL 来自 sources.yaml（需 pyyaml，缺失则 sources 为空，调用方自行读 yaml）。"""
    import curator
    srcmap = {}
    try:
        import yaml
        cfg = yaml.safe_load((ROOT / "sources.yaml").read_text("utf-8"))
        for vid, vcfg in (cfg.get("vendors") or {}).items():
            srcmap[vid] = ([s["url"] for s in (vcfg.get("rss") or [])] +
                           [s["url"] for s in (vcfg.get("webfetch") or [])])
    except Exception:
        pass
    out = [{"id": vid, "name": m["name"], "brand": m["brand"], "sources": srcmap.get(vid, [])}
           for vid, m in curator.VENDOR_META.items()]
    print(json.dumps(out, ensure_ascii=False, indent=2))


def reindex(out: Path):
    """仅重建展示页数据：各厂商 latest.json + 汇总 index.json（jpg 感知）。
    供 Claude 驱动路径（自己写 data + 渲染）收尾调用：python run.py --reindex"""
    idx = write_index(out)
    n_days, n_vendors = len(idx["days"]), len(idx["vendors"])
    print(f"✓ 已重建 index.json + 各厂商 latest.json（{n_vendors} 厂商 / {n_days} 天）")


def probe(out: Path) -> int:
    """监控哨兵：只探测信源健康 + 校验当天 routine 是否已产出，不去重/策展/渲染/调 LLM。
    依赖仅 feedparser + pyyaml（无 node/playwright/ANTHROPIC_API_KEY）。用法：python run.py --probe
    退出码：今日无 routine 产出 或 有「停更」信源 → 1（供 CI 告警）；仅临时失败 → 0（仅记录）。"""
    import curator
    health = out / "output" / "sources_health.json"
    for v in curator.VENDOR_META:
        collector.collect(mock=False, vendor=v, health_path=health)

    try:
        hdata = json.loads(health.read_text("utf-8"))
    except Exception:
        hdata = {}
    stale = [(k, s.get("error") or "长期零产出") for k, s in sorted(hdata.items()) if s.get("stale")]
    failed = [(k, s.get("error") or "本次零产出") for k, s in sorted(hdata.items())
              if not s.get("ok") and not s.get("stale")]

    today = datetime.date.today().isoformat()        # CI 设 TZ=Asia/Shanghai，故为北京日期
    try:
        idx_updated = json.loads((out / "output" / "index.json").read_text("utf-8")).get("updated", "")
    except Exception:
        idx_updated = ""
    routine_ok = idx_updated == today

    print("\n===== 信源监控哨兵报告 =====")
    print(f"今日(Asia/Shanghai)：{today}")
    print("routine 产出：" + ("✓ index.json 已更新到今天"
          if routine_ok else f"✗ index.json updated={idx_updated or '空'}，今天未见产出"))
    print(f"信源：停更 {len(stale)} / 临时失败 {len(failed)}")
    for k, err in stale:
        print(f"  ⚠ 停更  {k} — {err}")
    for k, err in failed:
        print(f"  ✗ 失败  {k} — {err}")

    if (not routine_ok) or stale:
        print("\n⚠ 发现需关注的异常（今日无 routine 产出 或 有停更信源）→ 退出码 1，CI 将告警。")
        return 1
    print("\n✓ 一切正常（临时失败仅记录、不告警）。")
    return 0


def main():
    if "--vendors" in sys.argv:
        list_vendors(); return
    if "--reindex" in sys.argv:
        reindex(OUT); return
    if "--probe" in sys.argv:
        sys.exit(probe(OUT))
    mock = "--live" not in sys.argv
    force = "--force" in sys.argv
    vendor = _arg_value("--vendor", "anthropic")
    engine = _arg_value("--engine", "auto")

    print(f"[1/5] 采集（{'mock' if mock else 'live'} · {vendor}）…")
    items = collector.collect(mock=mock, vendor=vendor,
                              health_path=None if mock else OUT / "output" / "sources_health.json")
    print(f"      共 {len(items)} 条")

    print("[2/5] 去重…")
    fresh = items if force else dedup.filter_new(items, vendor)
    print(f"      增量 {len(fresh)} 条")
    if not fresh:
        print("      今日无新动态，结束。"); return

    print("[3/5] 摘要策展…")
    data = curator.curate(fresh, mock=mock, vendor=vendor)
    if data.get("skip"):
        print("      策展判定今日不发：", data.get("reason")); return
    data["vendor"] = vendor

    date = datetime.date.today().isoformat()
    data_file = OUT / "data" / vendor / f"{date}.json"
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    print(f"      写入 {data_file}")

    print("[4/5] 渲染卡片…")
    out_dir = OUT / "output" / vendor / date
    subprocess.run(["node", str(ROOT / "render.js"), str(data_file), str(out_dir), "--engine", engine],
                   cwd=ROOT, check=True)

    print("[5/5] 更新展示页指针与索引…")
    write_index(OUT)

    dedup.mark_seen(fresh, vendor)
    print(f"\n✅ 完成。卡片在 {out_dir}/，本地预览：python -m http.server 后打开 index.html")

if __name__ == "__main__":
    main()
