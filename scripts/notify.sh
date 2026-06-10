#!/usr/bin/env bash
# 多渠道推送一条通知。配了哪个渠道的 key 就走哪个（可叠加）；一个都没配则退回 macOS 桌面通知。
#
# 用法：scripts/notify.sh "标题" "正文"
#
# 渠道在 ~/.config/ai-frontier-daily/notify.env 里配置（由调用方 source 进环境），可任选其一或多个：
#   BARK_KEY            iOS Bark 的 device key（默认走官方 https://api.day.app）
#   BARK_BASE           自托管 Bark 根地址（默认 https://api.day.app），与 BARK_KEY 配合
#   SERVERCHAN_SENDKEY  Server 酱 SendKey（直接推到你的微信）
#   NOTIFY_WEBHOOK      通用 webhook，POST application/json: {"title":..,"body":..}
set -uo pipefail
title="${1:-AI 前哨}"; body="${2:-}"
sent=0
CURL=(curl -sS --max-time 15)

urlenc(){ python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$1" 2>/dev/null || printf '%s' "$1"; }

if [ -n "${BARK_KEY:-}" ]; then
  base="${BARK_BASE:-https://api.day.app}"
  "${CURL[@]}" "$base/${BARK_KEY}/$(urlenc "$title")/$(urlenc "$body")?group=AI%E5%89%8D%E5%93%A8" >/dev/null && sent=1 || true
fi
if [ -n "${SERVERCHAN_SENDKEY:-}" ]; then
  "${CURL[@]}" --data-urlencode "title=$title" --data-urlencode "desp=$body" \
    "https://sctapi.ftqq.com/${SERVERCHAN_SENDKEY}.send" >/dev/null && sent=1 || true
fi
if [ -n "${NOTIFY_WEBHOOK:-}" ]; then
  payload="$(python3 -c "import json,sys;print(json.dumps({'title':sys.argv[1],'body':sys.argv[2]},ensure_ascii=False))" "$title" "$body")"
  "${CURL[@]}" -H "Content-Type: application/json; charset=utf-8" -d "$payload" "$NOTIFY_WEBHOOK" >/dev/null && sent=1 || true
fi
if [ "$sent" -eq 0 ]; then
  command -v osascript >/dev/null 2>&1 && \
    osascript -e "display notification \"$body\" with title \"$title\"" >/dev/null 2>&1 || true
  echo "notify: 未配置手机推送渠道，已退回 macOS 桌面通知（在 ~/.config/ai-frontier-daily/notify.env 配 BARK_KEY 等以启用手机推送）" >&2
fi
exit 0
