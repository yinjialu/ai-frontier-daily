"""Run inside the existing Hermes container after dependencies and baseline pass.

FRONTIER_FEISHU_CHAT_ID=oc_... python deploy/install-hermes.py
Creates only this project's jobs; does not modify the bot, global model or timezone.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, "/opt/hermes")
from cron.jobs import load_jobs
from hermes_time import now

chat = os.environ["FRONTIER_FEISHU_CHAT_ID"]
if not chat.startswith("oc_"):
    raise SystemExit("An explicit Feishu group chat ID is required")
offset = now().utcoffset().total_seconds()
if offset not in (0, 28800):
    raise SystemExit("Installer supports Hermes UTC or Asia/Shanghai; verify timezone mapping before proceeding")
hour = 0 if offset == 0 else 8
home = Path(os.environ.get("HERMES_HOME", "/opt/data"))
owner = home.stat()
# docker exec defaults to root; the long-running gateway executes as the Hermes
# data owner. Give only this project's files to that existing identity.
if os.geteuid() == 0:
    subprocess.run(["chown", "-R", f"{owner.st_uid}:{owner.st_gid}", str(ROOT)], check=True)
script_dir = home / "scripts"
script_dir.mkdir(parents=True, exist_ok=True)
config = home / "frontier-server.json"
config.write_text(json.dumps({"chat_id": chat, "root": str(ROOT)}, indent=2))
config.chmod(0o600)
if os.geteuid() == 0:
    os.chown(config, owner.st_uid, owner.st_gid)
jobs = [("poll", "*/30 * * * *", "AI 前哨 · 半小时巡检"),
        ("scout", f"30 {(hour-1)%24} * * *", "AI 前哨 · 官方信源补充搜索"),
        ("daily", f"0 {hour} * * *", "AI 前哨 · 08点早报卡片"),
        ("retry", f"15 {hour} * * *", "AI 前哨 · 早报失败补偿")]
existing = {j.get("name"): j for j in load_jobs()}
for kind, schedule, name in jobs:
    path = script_dir / ("frontier_" + kind + ".py")
    body = f'''import json, os, sys
from pathlib import Path
cfg = json.loads(Path({str(config)!r}).read_text())
root = Path(cfg['root'])
sys.path[:0] = [str(root), str(root / '.server-packages'), '/opt/hermes']
os.chdir(root)
os.environ['FRONTIER_FEISHU_CHAT_ID'] = cfg['chat_id']
os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '/opt/data/cache/frontier-playwright'
from scripts.server.worker import run, STATE
from scripts.server import store
'''
    if kind == "retry":
        body += '''from datetime import datetime
from zoneinfo import ZoneInfo
date = datetime.now(ZoneInfo('Asia/Shanghai')).date().isoformat()
db = store.connect(STATE / 'frontier.db')
done = store.delivered(db, 'daily:' + date)
db.close()
if not done:
    run('daily', send=True)
'''
    else:
        body += f"run({kind!r}, send={kind != 'scout'!r})\n"
    path.write_text(body)
    if os.geteuid() == 0:
        os.chown(path, owner.st_uid, owner.st_gid)
    if name in existing:
        print("Existing job preserved:", name, existing[name]["id"])
        continue
    subprocess.run(["hermes", "cron", "create", schedule, "--name", name,
        "--script", path.name, "--no-agent", "--deliver", "local",
        "--failure-deliver", "feishu:" + chat], check=True)
    # Some Hermes CLI versions print a create error but exit zero.
    if not any(j.get("name") == name for j in load_jobs()):
        raise SystemExit("Hermes did not persist the requested job: " + name)
print("Hermes timezone:", str(now().tzinfo), "08:00 Shanghai maps to cron hour:", hour)
