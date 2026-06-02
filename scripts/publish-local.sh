#!/usr/bin/env bash
# 云端抓取 → 本机推送：拉取云端最新当天动态，把整套卡片发成公众号【贴图草稿】
# （article_type=newspic，不群发，人工最后一步发布）。
#
# 用法：
#   scripts/publish-local.sh            # 真推贴图草稿
#   scripts/publish-local.sh --dry-run  # 仅打印将提交的结构，不碰微信 API
#
# 依赖：凭据 ~/.config/wechat-official-draft/config.yaml 或 WECHAT_APPID/SECRET；
#       本机公网 IP 已加入公众号后台 IP 白名单；需已认证服务号。
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
DRY=""; [ "${1:-}" = "--dry-run" ] && DRY="--dry-run"

echo "[1/3] 拉取云端最新…"
git pull --ff-only --quiet

DATE="$(python3 -c "import json;print(json.load(open('output/latest.json'))['dir'])")"
TODAY="$(date +%F)"
MARK="$REPO/.last_published"
if [ -z "$DRY" ] && [ "$DATE" != "$TODAY" ]; then
  echo "云端尚未产出今天（$TODAY）的内容（latest=$DATE），跳过；稍后兜底再试。"; exit 0
fi
if [ -z "$DRY" ] && [ -f "$MARK" ] && [ "$(cat "$MARK")" = "$DATE" ]; then
  echo "今天（$DATE）已推送过草稿，跳过。"; exit 0
fi

if [ -n "$DRY" ]; then echo "[2/3] 预览贴图结构（不建草稿）…"; else echo "[2/3] 上传卡片 + 创建贴图草稿…"; fi
python3 skills/ai-daily-digest/publish_wechat_newspic.py $DRY

if [ -z "$DRY" ]; then
  echo "$DATE" > "$MARK"
  echo "[3/3] ✅ 已推送 $DATE 贴图草稿，去公众号后台核对并发布。"
  command -v osascript >/dev/null 2>&1 && \
    osascript -e "display notification \"$DATE 贴图草稿已进箱，待发布\" with title \"AI 前哨 · 公众号\"" || true
fi
