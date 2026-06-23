#!/usr/bin/env bash
# 在新 mac 上安装/刷新「一手信源内参监控」launchd 定时任务（每小时 + 开机自启）。
# 幂等：可重复运行（会先卸载旧任务再重装）。装的是仓库内 scripts/launchd-firsthand.plist
# 的 symlink —— 之后 git pull 更新 plist 即自动生效，无需重装。
#
# 用法：
#   scripts/install-firsthand-launchd.sh             # 安装/刷新
#   scripts/install-firsthand-launchd.sh --uninstall # 卸载
#
# 前置依赖见 scripts/SETUP-NEW-MACHINE.md（仓库路径、Python 依赖、claude/gh 登录态）。
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
LABEL="com.yinjialu.ai-frontier-daily.firsthand"
PLIST_SRC="$REPO/scripts/launchd-firsthand.plist"
PLIST_DST="$HOME/Library/LaunchAgents/$LABEL.plist"
EXPECTED_REPO="$HOME/ai-frontier-daily"
DOMAIN="gui/$(id -u)"

unload_existing() {
  if launchctl list "$LABEL" >/dev/null 2>&1; then
    echo "· 卸载现有任务 $LABEL"
    launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null \
      || launchctl unload "$PLIST_DST" 2>/dev/null || true
  fi
}

if [ "${1:-}" = "--uninstall" ]; then
  unload_existing
  rm -f "$PLIST_DST"
  echo "✓ 已卸载 $LABEL 并移除 $PLIST_DST"
  exit 0
fi

# 0. 路径校验：plist 硬编码 /Users/jialu/ai-frontier-daily 作为仓库根
if [ "$REPO" != "$EXPECTED_REPO" ]; then
  echo "✗ 仓库不在 $EXPECTED_REPO（实际：$REPO）"
  echo "  plist 内 exec 路径硬编码为该路径。"
  echo "  请把仓库克隆/移动到 $EXPECTED_REPO 后重试，或手改 scripts/launchd-firsthand.plist 再装。"
  exit 1
fi

# 1. 运行时依赖（用 plist 指定的 anaconda python 校验，确保与实际执行一致）
ANACONDA_PY="/Users/jialu/anaconda3/bin/python3"
PY="$ANACONDA_PY"; [ -x "$PY" ] || PY="$(command -v python3 || true)"
[ -n "$PY" ] || { echo "✗ 缺 python3"; exit 1; }
if ! "$PY" -c "import yaml, requests, feedparser" 2>/dev/null; then
  echo "✗ $PY 缺 Python 依赖。先安装："
  echo "    \"$PY\" -m pip install -r \"$REPO/requirements.txt\""
  exit 1
fi
echo "· Python 依赖 OK（$PY: yaml / requests / feedparser）"

# 2. 登录态检查（缺失只告警 —— 影响摘要，不影响通知）
command -v gh >/dev/null 2>&1 || echo "⚠ 未找到 gh CLI —— 开 PR 会失败。装：brew install gh && gh auth login"
command -v claude >/dev/null 2>&1 || echo "⚠ 未找到 claude CLI —— 摘要会退回占位文本（通知/PR 仍正常）。"

# 3. 安装 plist（symlink，保持与仓库同步）
mkdir -p "$HOME/Library/LaunchAgents"
unload_existing
ln -sf "$PLIST_SRC" "$PLIST_DST"
echo "· 已 symlink：$PLIST_DST → $PLIST_SRC"

# 4. 加载（优先新式 bootstrap，回退旧式 load）
launchctl bootstrap "$DOMAIN" "$PLIST_DST" 2>/dev/null \
  || launchctl load "$PLIST_DST"

# 5. 校验
if launchctl list "$LABEL" >/dev/null 2>&1; then
  echo "✓ 安装成功：$LABEL（每小时 + 开机登录后触发）"
  echo "  立即试跑： launchctl kickstart -k $DOMAIN/$LABEL"
  echo "  看日志：   tail -f ~/Library/Logs/ai-frontier-daily-firsthand.log"
else
  echo "✗ 加载后未在 launchctl list 出现，请检查 plist 与系统日志"
  exit 1
fi
