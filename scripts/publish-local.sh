#!/usr/bin/env bash
# 云端抓取 → 本机推送：拉取云端最新当天动态，把整套卡片发成公众号【贴图草稿】
# （article_type=newspic，直调 publish_wechat_newspic.py——与 watch-and-publish.sh 同一引擎；
#   不群发，人工最后发布）。
# 注：wechat-official-draft skill 的 push_draft.mjs 只支持图文(news)形态、不支持贴图(newspic)，
#     故贴图链路不走 skill；skill 留给 Claude 交互排版自由文章时用（已项目内安装 .agents/skills/）。
#
# 用法：
#   scripts/publish-local.sh                       # 默认 anthropic，真推贴图草稿
#   scripts/publish-local.sh --vendor openai       # 指定厂商
#   scripts/publish-local.sh --dry-run             # 仅本地预览，不碰微信 API
#
# 依赖：凭据 ~/.config/wechat-official-draft/config.yaml（与 skill 共享），
#       本机公网 IP 在公众号 IP 白名单，需已认证服务号。
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

# 解析参数：--dry-run 与 --vendor <id>（缺省 anthropic）
DRY=""; VENDOR="anthropic"
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY="--dry-run" ;;
    --vendor) VENDOR="$2"; shift ;;
  esac
  shift
done

echo "[1/2] 拉取云端最新…"
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

if [ -n "$DRY" ]; then echo "[2/2] 预览贴图（不建草稿）…"; else echo "[2/2] 创建贴图草稿…"; fi
python3 skills/ai-daily-digest/publish_wechat_newspic.py --vendor "$VENDOR" $DRY

if [ -z "$DRY" ]; then
  echo "$DATE" > "$MARK"
  echo "✅ 已推送 $VENDOR $DATE 贴图草稿，去公众号后台核对并发布。"
  command -v osascript >/dev/null 2>&1 && \
    osascript -e "display notification \"$VENDOR $DATE 贴图草稿已进箱，待发布\" with title \"AI 前哨 · 公众号\"" || true
fi
