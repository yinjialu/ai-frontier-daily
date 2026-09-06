"""Run inside Hermes via --script --no-agent. No GitHub writes or public exposure.

python -m scripts.server.worker baseline|poll|scout|daily|health|smoke [--send]
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import yaml

from . import sources, store, curation
from .feishu import Feishu

ROOT = Path(__file__).resolve().parents[2]
STATE = Path(os.getenv("FRONTIER_STATE_DIR", str(ROOT / ".server-state")))
INVENTORY = ROOT / "deploy/server-sources.yaml"
DISCOVERY = ROOT / "deploy/discovery-sources.yaml"


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(path)


def health(db):
    cfg = yaml.safe_load(INVENTORY.read_text())
    rows = {r["id"]: dict(r) for r in db.execute("SELECT * FROM sources")}
    return {"checked_at": datetime.now(timezone.utc).isoformat(),
        "sources": [rows.get(s["id"], {"id": s["id"], "error": "never checked"}) for s in cfg["sources"]],
        "discovery": [rows.get(s["id"], {"id": s["id"], "error": "never checked"}) for s in yaml.safe_load(DISCOVERY.read_text())["sources"]],
        "uncovered": cfg.get("manual_sources", [])}


def deliver(db, client, key, title=None, body=None, path=None):
    if store.delivered(db, key):
        return
    message_id = client.file(key, path) if path else client.card(key, title, body)
    store.record_delivery(db, key, message_id)


def curate_pending(db):
    pending = store.pending(db)
    ready = []
    for item in pending:
        try:
            item = sources.enrich(item)
            # Old entries surfaced by a listing reorder are not today's news.
            if item.get("published") and not curation.recent(item["published"], hours=96):
                with db:
                    db.execute("UPDATE items SET curated=? WHERE id=?", (json.dumps(dict(item, editorial={"relevant": False, "important": False})), item["id"]))
                continue
            if len(item["text"]) < 100:
                raise ValueError("article body unavailable")
            ready.append(item)
        except Exception as exc:
            with db:
                db.execute("UPDATE items SET error=? WHERE id=?", (type(exc).__name__, item["id"]))
    if ready:
        # Persist each batch independently; a later failure does not erase work.
        for offset in range(0, len(ready), 8):
            batch = ready[offset:offset + 8]
            try:
                result = curation.generate(batch)
            except Exception as exc:
                with db:
                    for item in batch:
                        db.execute("UPDATE items SET error=? WHERE id=?", (type(exc).__name__, item["id"]))
                raise
            with db:
                for item in result:
                    db.execute("UPDATE items SET curated=?,error=NULL WHERE id=?", (json.dumps(item, ensure_ascii=False), item["id"]))


def news(db, hours=36):
    result, seen = [], set()
    for row in db.execute("SELECT curated,detected FROM items WHERE baseline=0 AND curated IS NOT NULL ORDER BY detected DESC"):
        item = json.loads(row[0])
        e = item["editorial"]
        if not e["relevant"] or not curation.recent(row[1], hours) or not curation.recent(item.get("published"), 72):
            continue
        key = item["company"] + ":" + e["event_key"]
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return sorted(result, key=lambda item: not item["editorial"]["important"])


def markdown(items):
    return "\n\n".join(f"**{i['editorial']['title']}**\n{i['editorial']['summary']}\n[官方原文]({i['url']}) · 发布：{i['published'][:10]}" for i in items)


def edition_items(db):
    previous_ids, previous_events = set(), set()
    for row in db.execute("SELECT payload FROM editions"):
        for i in json.loads(row[0]):
            previous_ids.add(i["id"])
            previous_events.add((i["company"], i["editorial"]["event_key"]))
    chosen, counts = [], {}
    for i in news(db):
        if i["id"] in previous_ids or (i["company"], i["editorial"]["event_key"]) in previous_events:
            continue
        vendor = i["vendor"]
        if counts.get(vendor, 0) >= (10 if vendor == "cn" else 6):
            continue
        counts[vendor] = counts.get(vendor, 0) + 1
        chosen.append(i)
    return chosen


def render(date, items, folder):
    groups = {}
    for item in items:
        groups.setdefault(item["vendor"], []).append(item)
    for vendor, group in groups.items():
        group = group[:10 if vendor == "cn" else 6]
        dt = datetime.fromisoformat(date)
        data = {"vendor": vendor, "date": date.replace("-", "."),
            "cnDate": f"{dt.month}月{dt.day}日", "edition": dt.strftime("VOL.%j"),
            "brand": "AI 前哨 · " + {"anthropic": "Anthropic", "openai": "OpenAI", "gemini": "Gemini", "nvidia": "NVIDIA", "cn": "国产大模型", "frontier": "全球模型"}[vendor],
            "updates": [{"tag": i["editorial"]["tag"], "title": i["editorial"]["title"],
                         "summary": i["editorial"]["summary"], "source": url_host(i["url"]),
                         "url": i["url"], "company": i["company"]} for i in group],
            "outroTitle": "每天一条\n看懂 AI 大厂动向", "outroDesc": "官方一手来源 · 人工审核后发布", "outroCta": "关注 · 不错过任何更新"}
        data_path = folder / vendor / "data.json"
        write_json(data_path, data)
        subprocess.run(["node", str(ROOT / "skills/ai-daily-digest/render.js"), str(data_path), str(data_path.parent), "--engine", "playwright"],
                       cwd=ROOT, check=True, timeout=240, stdout=sys.stderr)
        (data_path.parent / "发布文案.md").write_text(markdown(group) + "\n")
    archive = folder / f"AI前哨-{date}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(folder.rglob("*")):
            if path.is_file() and path.suffix in {".jpg", ".png", ".md", ".json"}:
                z.write(path, path.relative_to(folder))
    return archive


def url_host(url):
    from urllib.parse import urlparse
    return urlparse(url).hostname


def run(mode, send=False):
    STATE.mkdir(parents=True, exist_ok=True)
    with (STATE / "worker.lock").open("w") as lock:
        # Patrol and the daily job are both due on the hour. Serialize them;
        # never report success while silently skipping the only daily run.
        fcntl.flock(lock, fcntl.LOCK_EX)
        db = store.connect(STATE / "frontier.db")
        if mode == "scout":
            results = sources.collect(DISCOVERY)
            store.ingest(db, results)
            date = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
            write_json(STATE / "research" / (date + ".json"), results)
            print(f"discovery={len(results)} completed={sum(not r['error'] for r in results)}", file=sys.stderr)
        if mode in {"baseline", "poll", "daily"}:
            results = sources.collect(INVENTORY)
            added = store.ingest(db, results)
            write_json(STATE / "health.json", health(db))
            print(f"sources={len(results)} healthy={sum(not r['error'] for r in results)} new={added}", file=sys.stderr)
        if mode in {"poll", "scout", "daily"}:
            curate_pending(db)
        if mode == "health":
            print(json.dumps(health(db), ensure_ascii=False, indent=2))
            return
        client = Feishu(os.environ["FRONTIER_FEISHU_CHAT_ID"]) if send else None
        if mode == "poll" and client:
            for item in news(db, 72):
                if item["editorial"]["important"]:
                    # Across-source event suppression, plus API UUID on uncertain sends.
                    key = "alert:" + item["company"] + ":" + item["editorial"]["event_key"]
                    deliver(db, client, key, "AI 前哨 · 重要更新", markdown([item]))
            failed = sorted(r["id"] for r in health(db)["sources"] if r.get("failures", 0) >= 3)
            if failed:
                day = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
                key = "health:" + day + ":" + hashlib.sha256("|".join(failed).encode()).hexdigest()[:12]
                deliver(db, client, key, "AI 前哨 · 信源需检查", "以下来源连续 3 次抓取失败，不能判断是否有更新：\n" + "、".join(failed))
        if mode == "daily":
            date = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
            # Freeze an edition before side effects; retries use exactly the same content.
            old = db.execute("SELECT payload FROM editions WHERE date=?", (date,)).fetchone()
            items = json.loads(old[0]) if old else edition_items(db)
            if not old:
                with db:
                    db.execute("INSERT INTO editions VALUES (?,?)", (date, json.dumps(items, ensure_ascii=False)))
            folder = STATE / "editions" / date
            report = health(db)
            write_json(folder / "coverage.json", report)
            errors = [r["id"] for r in report["sources"] if r.get("error")]
            gaps = [r["company"] for r in report["uncovered"]]
            body = markdown(items[:15]) if items else "本轮已成功抓取的官方来源中，没有发现可确认、值得制作卡片的新动态。"
            body += f"\n\n覆盖：{len(report['sources']) - len(errors)}/{len(report['sources'])} 个自动源可用。"
            if errors:
                body += "\n抓取失败：" + "、".join(errors)
            if gaps:
                body += "\n通过每日官方站点搜索补充（暂无固定订阅适配）：" + "、".join(gaps)
            discovery_errors = [r["id"] for r in report["discovery"] if r.get("error") or not curation.recent(r.get("checked"), 25)]
            if discovery_errors:
                body += "\n搜索覆盖不完整：" + "、".join(discovery_errors)
            if items:
                archive = folder / f"AI前哨-{date}.zip"
                if not archive.exists():
                    archive = render(date, items, folder)
                body += "\n\n发布包包含小红书竖图、公众号封面/长图、中文文案及原文链接。请审核后手动发布。"
                if client:
                    deliver(db, client, "daily-file:" + date, path=archive)
            if client:
                deliver(db, client, "daily:" + date, "AI 前哨 · " + date + " 早报", body=body)
        if mode == "smoke" and client:
            deliver(db, client, "server-migration-smoke-v1", "AI 前哨 · 服务器迁移验证",
                "飞书通知通路已接通。巡检计划为每 30 分钟；重大模型更新及时通知；北京时间每天 08:00 汇总并准备发布卡片。\n首次采集仅建立去重基线，不推送历史新闻。最终运行状态以部署验收结果为准。")
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("mode", choices=["baseline", "poll", "scout", "daily", "health", "smoke"])
    parser.add_argument("--send", action="store_true", help="Actually deliver to the configured Feishu group")
    args = parser.parse_args()
    run(args.mode, args.send)
