#!/usr/bin/env python3
"""主流程编排：采集 → 去重 → 摘要 → 渲染 → 更新审核页。
用法：
  python run.py            # mock 模式：无需联网/密钥，本地跑通整条流程
  python run.py --live     # 真实模式：抓 RSS + 调 Claude API（需 ANTHROPIC_API_KEY）
  python run.py --force    # 忽略去重，强制处理（调试用）
  python run.py --engine playwright   # 用 Playwright 渲染（生产推荐，字体保真）
"""
import sys, os, json, subprocess, datetime
from pathlib import Path
import collector, dedup, curator

ROOT = Path(__file__).parent                                  # 脚本与字体/模板所在目录
OUT = Path(os.environ.get("DIGEST_OUT") or os.getcwd())        # data/ 与 output/ 写到这里（默认当前目录）

IMG_EXTS = (".png", ".jpg", ".jpeg")                          # 卡片可能是 png 或 jpg
def _img_names(d):
    return [p.name for p in sorted(d.glob("*")) if p.suffix.lower() in IMG_EXTS] if d.is_dir() else []

def write_index(out: Path):
    """扫描 data/*.json 与 output/<date>/，生成 output/index.json：
    每天一条 {date, dir, cnDate, edition, count, files}，供展示页浏览与热力图使用。
    count = 当天采集策展后的动态条数（热力图的“数量”）。"""
    days = []
    for df in sorted((out / "data").glob("*.json")):
        date = df.stem
        try:
            d = json.loads(df.read_text("utf-8"))
        except Exception:
            continue
        odir = out / "output" / date
        files = _img_names(odir)
        days.append({
            "date": date,
            "dir": date,
            "cnDate": d.get("cnDate", ""),
            "edition": d.get("edition", ""),
            "count": len(d.get("updates", [])),
            "files": files,
        })
    days.sort(key=lambda x: x["date"])
    idx = {"updated": days[-1]["date"] if days else "", "days": days}
    (out / "output" / "index.json").write_text(
        json.dumps(idx, ensure_ascii=False, indent=2), "utf-8")
    return idx


def reindex(out: Path):
    """仅重建展示页数据：output/latest.json（最新一天）+ output/index.json。
    供 Claude 驱动路径（自己写 data + 渲染）收尾调用：python run.py --reindex"""
    dates = sorted(p.stem for p in (out / "data").glob("*.json"))
    if not dates:
        print("无 data/*.json，跳过。"); return
    date = dates[-1]
    data = json.loads((out / "data" / f"{date}.json").read_text("utf-8"))
    out_dir = out / "output" / date
    (out / "output" / "latest.json").write_text(
        json.dumps({"date": data.get("date", date), "cnDate": data.get("cnDate", ""),
                    "dir": date, "files": _img_names(out_dir)}, ensure_ascii=False, indent=2), "utf-8")
    write_index(out)
    print(f"✓ 已重建 latest.json + index.json（最新 {date}，{len(_img_names(out_dir))} 图）")


def main():
    if "--reindex" in sys.argv:
        reindex(OUT); return
    mock = "--live" not in sys.argv
    force = "--force" in sys.argv
    engine = "auto"
    if "--engine" in sys.argv:
        engine = sys.argv[sys.argv.index("--engine") + 1]

    print(f"[1/5] 采集（{'mock' if mock else 'live'}）…")
    items = collector.collect(mock=mock)
    print(f"      共 {len(items)} 条")

    print("[2/5] 去重…")
    fresh = items if force else dedup.filter_new(items)
    print(f"      增量 {len(fresh)} 条")
    if not fresh:
        print("      今日无新动态，结束。"); return

    print("[3/5] 摘要策展…")
    data = curator.curate(fresh, mock=mock)
    if data.get("skip"):
        print("      策展判定今日不发：", data.get("reason")); return

    date = datetime.date.today().isoformat()
    data_file = OUT / "data" / f"{date}.json"
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    print(f"      写入 {data_file}")

    print("[4/5] 渲染卡片…")
    out_dir = OUT / "output" / date
    subprocess.run(["node", str(ROOT / "render.js"), str(data_file), str(out_dir), "--engine", engine],
                   cwd=ROOT, check=True)

    print("[5/5] 更新展示页指针与索引…")
    files = _img_names(out_dir)
    (OUT / "output" / "latest.json").write_text(
        json.dumps({"date": data["date"], "cnDate": data["cnDate"], "dir": date,
                    "files": files}, ensure_ascii=False, indent=2), "utf-8")
    write_index(OUT)

    dedup.mark_seen(fresh)
    print(f"\n✅ 完成。卡片在 {out_dir}/，本地预览：python -m http.server 后打开 index.html")

if __name__ == "__main__":
    main()
