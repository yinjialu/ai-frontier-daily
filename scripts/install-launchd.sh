#!/usr/bin/env bash
# 在新 mac 上安装/刷新「AI 前哨」每日发布 launchd 定时任务。
# 幂等：可重复运行（会先卸载旧任务再重装）。装的是仓库内 scripts/launchd-publish.plist
# 的 symlink —— 之后 git pull 更新 plist 即自动生效，无需重装。
#
# 用法：
#   scripts/install-launchd.sh             # 安装/刷新
#   scripts/install-launchd.sh --uninstall # 卸载
#
# 前置依赖见 scripts/SETUP-NEW-MACHINE.md（仓库路径、Python 依赖、凭据文件）。
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
LABEL="com.yinjialu.ai-frontier-daily.publish"
PLIST_SRC="$REPO/scripts/launchd-publish.plist"
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

# 0. 路径校验：plist 硬编码 $HOME/ai-frontier-daily 作为仓库根
if [ "$REPO" != "$EXPECTED_REPO" ]; then
  echo "✗ 仓库不在 $EXPECTED_REPO（实际：$REPO）"
  echo "  plist 内 exec 路径硬编码为 \$HOME/ai-frontier-daily。"
  echo "  请把仓库克隆/移动到 $EXPECTED_REPO 后重试，或手改 scripts/launchd-publish.plist 再装。"
  exit 1
fi

# 1. 运行时依赖
command -v python3 >/dev/null 2>&1 || { echo "✗ 缺 python3"; exit 1; }
if ! python3 -c "import yaml, requests, feedparser" 2>/dev/null; then
  echo "✗ 缺 Python 依赖。先安装："
  echo "    python3 -m pip install -r \"$REPO/requirements.txt\""
  exit 1
fi
echo "· Python 依赖 OK（yaml / requests / feedparser）"

# 2. 凭据检查（缺失只告警，不阻断 —— 装好后再补也行）
WECHAT_CFG="$HOME/.config/wechat-official-draft/config.yaml"
if [ ! -f "$WECHAT_CFG" ]; then
  echo "⚠ 未找到微信凭据：$WECHAT_CFG"
  echo "  无此文件公众号发布会失败。模板：scripts/config-templates/wechat-official-draft.config.yaml.example"
  echo "  别忘了把本机公网出口 IP 加入公众号后台 IP 白名单。"
fi
NOTIFY_ENV="$HOME/.config/ai-frontier-daily/notify.env"
[ -f "$NOTIFY_ENV" ] || echo "ℹ 无 $NOTIFY_ENV —— 手机推送将退回 macOS 桌面通知（可选）。"

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
  echo "✓ 安装成功：$LABEL（每天 23:15 / 23:45 / 次日 00:30 触发）"
  echo "  立即试跑： launchctl kickstart -k $DOMAIN/$LABEL"
  echo "  看日志：   tail -f ~/Library/Logs/ai-frontier-daily-publish.log"
else
  echo "✗ 加载后未在 launchctl list 出现，请检查 plist 与系统日志"
  exit 1
fi
