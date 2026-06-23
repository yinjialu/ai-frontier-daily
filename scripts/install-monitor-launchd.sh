#!/bin/bash
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)/com.jialu.monitor-firsthand.plist"
DST="$HOME/Library/LaunchAgents/com.jialu.monitor-firsthand.plist"
cp "$SRC" "$DST"
launchctl unload "$DST" 2>/dev/null || true
launchctl load "$DST"
echo "已安装并加载：$DST"
echo "查看日志：tail -f ~/Library/Logs/monitor-firsthand.log"
echo "手动触发一次：launchctl start com.jialu.monitor-firsthand"
