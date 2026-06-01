#!/usr/bin/env bash
# 云端抓取 → 本机推送：拉取云端最新当天动态，转成公众号 Markdown，
# 交给本机 wechat-official-draft skill 推到【草稿箱】（不群发，人工最后一步发布）。
#
# 用法：
#   scripts/publish-local.sh            # 真推草稿
#   scripts/publish-local.sh --dry-run  # 仅本地预览，不碰微信 API、不建草稿
#
# 依赖：
#   - 本机已装 wechat-official-draft skill 且配好凭据
#     （~/.config/wechat-official-draft/config.yaml 或 WECHAT_APPID/SECRET）
#   - 本机公网 IP 已加入公众号后台 IP 白名单
#   可用 WECHAT_DRAFT_MJS 覆盖 push_draft.mjs 路径。
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
MJS="${WECHAT_DRAFT_MJS:-$HOME/.codex/skills/wechat-official-draft/scripts/push_draft.mjs}"
DRY=""; [ "${1:-}" = "--dry-run" ] && DRY="--dry-run"

echo "[1/4] 拉取云端最新…"
git pull --ff-only --quiet

DATE="$(python3 -c "import json;print(json.load(open('output/latest.json'))['dir'])")"
MARK="$REPO/.last_published"
if [ -z "$DRY" ] && [ -f "$MARK" ] && [ "$(cat "$MARK")" = "$DATE" ]; then
  echo "今天（$DATE）已推送过草稿，跳过。"; exit 0
fi

echo "[2/4] 生成公众号 Markdown（$DATE）…"
META="$(python3 skills/ai-daily-digest/to_wechat_md.py)"
get(){ printf '%s' "$META" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }
MD="$(get md)"; TITLE="$(get title)"; DIGEST="$(get digest)"; COVER="$(get cover)"

if [ -n "$DRY" ]; then echo "[3/4] 本地预览（不建草稿）…"; else echo "[3/4] 推送到草稿箱…"; fi
node "$MJS" --file "$MD" --title "$TITLE" --digest "$DIGEST" --cover "$COVER" $DRY

if [ -z "$DRY" ]; then
  echo "$DATE" > "$MARK"
  echo "[4/4] ✅ 已推送 $DATE 到公众号草稿箱，去后台核对并群发。"
  command -v osascript >/dev/null 2>&1 && \
    osascript -e "display notification \"$TITLE 已进草稿箱，待群发\" with title \"AI 前哨 · 公众号\"" || true
fi
