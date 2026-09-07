#!/usr/bin/env bash
# Run on the existing Hermes VM after copying the reviewed project files.
set -euo pipefail
test "$(id -u)" = 0 || { echo 'Run with sudo on the Hermes VM' >&2; exit 1; }
docker inspect hermes --format '{{.HostConfig.NetworkMode}}' | grep -qx host
task_origin='http://hermes-agent.tail804ea0.ts.net:8787'
task_owner="$(tailscale status --json | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["User"][str(d["Self"]["UserID"])]["LoginName"])')"
test -n "$task_owner"
install -m 600 /dev/null /etc/ai-frontier-feedback.env
printf 'FRONTIER_OWNER_LOGIN=%s\n' "$task_owner" > /etc/ai-frontier-feedback.env
cat > /etc/systemd/system/ai-frontier-feedback.service <<'UNIT'
[Unit]
Description=AI Frontier private reader and preference feedback
After=docker.service tailscaled.service
Requires=docker.service

[Service]
Type=simple
EnvironmentFile=/etc/ai-frontier-feedback.env
ExecStart=/usr/bin/docker exec --user hermes -e FRONTIER_OWNER_LOGIN -e PYTHONPATH=/opt/data/workspace/ai-frontier-daily/.server-packages:/opt/hermes -w /opt/data/workspace/ai-frontier-daily hermes /opt/hermes/.venv/bin/python -m scripts.server.feedback_api --origin http://hermes-agent.tail804ea0.ts.net:8787
ExecStop=-/usr/bin/docker exec --user hermes hermes pkill -f [s]cripts.server.feedback_api
Restart=always
RestartSec=5
TimeoutStopSec=15

[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable ai-frontier-feedback.service
systemctl restart ai-frontier-feedback.service
tailscale serve --bg --http=8787 --yes http://127.0.0.1:8791
systemctl is-active ai-frontier-feedback.service
printf '%s\n' "$task_origin/"
