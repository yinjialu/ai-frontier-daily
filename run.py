#!/usr/bin/env python3
"""主流程编排：采集 → 去重 → 摘要 → 渲染 → 更新审核页。
用法：
  python run.py            # mock 模式：无需联网/密钥，本地跑通整条流程
  python run.py --live     # 真实模式：抓 RSS + 调 Claude API（需 ANTHROPIC_API_KEY）
  python run.py --force    # 忽略去重，强制处理（调试用）
  python run.py --engine playwright   # 用 Playwright 渲染（生产推荐，字体保真）
"""
import sys, json, subprocess, datetime
from pathlib import Path
import collector, dedup, curator

ROOT = Path(__file__).parent

def main():
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
    data_file = ROOT / "data" / f"{date}.json"
    data_file.parent.mkdir(exist_ok=True)
    data_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    print(f"      写入 {data_file.relative_to(ROOT)}")

    print("[4/5] 渲染卡片…")
    out_dir = ROOT / "output" / date
    subprocess.run(["node", "render.js", str(data_file), str(out_dir), "--engine", engine],
                   cwd=ROOT, check=True)

    print("[5/5] 更新审核页指针…")
    (ROOT / "output" / "latest.json").write_text(
        json.dumps({"date": data["date"], "cnDate": data["cnDate"], "dir": date,
                    "files": [c + ".png" for c in
                              [f.stem for f in sorted(out_dir.glob("*.png"))]]},
                   ensure_ascii=False, indent=2), "utf-8")

    dedup.mark_seen(fresh)
    print(f"\n✅ 完成。卡片在 output/{date}/，本地预览：python -m http.server 后打开 index.html")

if __name__ == "__main__":
    main()
