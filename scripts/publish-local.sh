#!/usr/bin/env bash
# 云端抓取 → 本机推送：拉取云端最新当天动态，把整套卡片发成公众号【贴图草稿】
# （article_type=newspic，复用 wechat-official-draft skill 的 push_draft.mjs；不群发，人工最后发布）。
#
# 用法：
#   scripts/publish-local.sh                       # 默认 anthropic，真推贴图草稿
#   scripts/publish-local.sh --vendor openai       # 指定厂商
#   scripts/publish-local.sh --dry-run             # 仅本地预览，不碰微信 API
#
# 依赖：wechat-official-draft skill 已配凭据（~/.config/wechat-official-draft/config.yaml
#       或 WECHAT_APPID/SECRET），本机公网 IP 在公众号 IP 白名单，需已认证服务号。
#       可用 WECHAT_DRAFT_MJS 覆盖 push_draft.mjs 路径。
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
MJS="${WECHAT_DRAFT_MJS:-$HOME/.codex/skills/wechat-official-draft/scripts/push_draft.mjs}"

# 解析参数：--dry-run 与 --vendor <id>（缺省 anthropic）
DRY=""; VENDOR="anthropic"
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY="--dry-run" ;;
    --vendor) VENDOR="$2"; shift ;;
  esac
  shift
done

echo "[1/3] 拉取云端最新…"
git pull --ff-only --quiet

DATE="$(python3 -c "import json;print(json.load(open('output/$VENDOR/latest.json'))['dir'])")"
TODAY="$(date +%F)"
MARK="$REPO/.last_published.$VENDOR"
if [ -z "$DRY" ] && [ "$DATE" != "$TODAY" ]; then
  echo "云端尚未产出今天（$TODAY）的 $VENDOR 内容（latest=$DATE），跳过；稍后兜底再试。"; exit 0
fi
if [ -z "$DRY" ] && [ -f "$MARK" ] && [ "$(cat "$MARK")" = "$DATE" ]; then
  echo "今天（$DATE）$VENDOR 已推送过草稿，跳过。"; exit 0
fi

echo "[2/3] 生成贴图 Markdown（$VENDOR · $DATE）…"
META="$(python3 skills/ai-daily-digest/to_wechat_md.py --vendor "$VENDOR")"
get(){ printf '%s' "$META" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }
MD="$(get md)"; TITLE="$(get title)"

if [ -n "$DRY" ]; then echo "[3/3] 预览贴图（不建草稿）…"; else echo "[3/3] 创建贴图草稿…"; fi
node "$MJS" --file "$MD" --title "$TITLE" --article-type newspic $DRY

if [ -z "$DRY" ]; then
  echo "$DATE" > "$MARK"
  echo "✅ 已推送 $VENDOR $DATE 贴图草稿，去公众号后台核对并发布。"
  command -v osascript >/dev/null 2>&1 && \
    osascript -e "display notification \"$VENDOR $DATE 贴图草稿已进箱，待发布\" with title \"AI 前哨 · 公众号\"" || true
fi
