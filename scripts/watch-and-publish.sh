#!/usr/bin/env bash
# 本机监听器：把云端 routine 推上来的 daily-<DATE> 分支合并进 main，再为各厂商建微信贴图草稿。
#
# 背景：Claude Code on the web 的 GitHub 代理「只允许推当前工作分支」，云端 routine 推不了 main，
#       只能推 daily-<DATE> 分支（见 SKILL.md）。本脚本在本机（有完整 push 权）做合并 + 微信发布。
#
# 用法：
#   scripts/watch-and-publish.sh            # 合并 daily 分支 → main → 各厂商建微信贴图草稿
#   scripts/watch-and-publish.sh --dry-run  # 只演练（合并照常做，微信只打印结构不碰 API）
#
# 可选环境变量：
#   VENDORS_PUBLISH="anthropic openai"   # 只给这些厂商发微信（缺省＝当天有内容的全部）
#   DIGEST_OUT（默认仓库根）、WeChat 凭据见 publish_wechat_newspic.py
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"; cd "$REPO"
export PATH="/Users/jialu/anaconda3/bin:$PATH:/opt/homebrew/bin:$HOME/.nvm/versions/node/v24.13.0/bin"
# 本机私密配置（手机推送渠道 key、可选微信凭据），不进仓库；供 notify.sh 与发布脚本读取
[ -f "$HOME/.config/ai-frontier-daily/notify.env" ] && { set -a; . "$HOME/.config/ai-frontier-daily/notify.env"; set +a; }

# 代理环境下 git 连接偶发被断（SSH 22 已改走 ssh.github.com:443，见 ~/.ssh/config），网络操作重试 3 次
retry(){ local n=0; until "$@"; do n=$((n+1)); [ "$n" -ge 3 ] && return 1; echo "    ↻ 网络重试 $n/2：$*"; sleep 20; done; }

# set -e 下任何一步失败都会静默退出（launchd 场景没人盯终端），失败也推手机通知
on_exit(){
  local code=$?
  [ "$code" -ne 0 ] && "$REPO/scripts/notify.sh" "AI 前哨 · 发布脚本失败" \
    "watch-and-publish 异常退出（码 $code），看日志：~/Library/Logs/ai-frontier-daily-publish.log" || true
}
trap on_exit EXIT

DRY=""; [ "${1:-}" = "--dry-run" ] && DRY="--dry-run"
# 自适应：留空＝当天 data/ 下有内容的全部厂商（新增厂商自动覆盖）；也可显式覆盖：VENDORS_PUBLISH="anthropic openai"
VENDORS_PUBLISH="${VENDORS_PUBLISH:-}"

echo "[1/3] 同步远端…"
retry git fetch origin --prune --quiet
git checkout main --quiet
retry git pull --ff-only --quiet

echo "[2/3] 合并 daily-* 分支 → main…"
for ref in $(git for-each-ref --format='%(refname:short)' 'refs/remotes/origin/daily-*' 2>/dev/null); do
  br="${ref#origin/}"; date="${br#daily-}"
  if git merge-base --is-ancestor "$ref" main 2>/dev/null; then
    echo "  · $br 已并入 main，清理远端分支"
    [ -z "$DRY" ] && git push origin --delete "$br" --quiet 2>/dev/null || true
    continue
  fi
  echo "  · 合并 $br"
  if [ -n "$DRY" ]; then echo "    (dry-run：跳过实际合并)"; continue; fi
  if ! git merge -X theirs --no-edit "$ref" >/dev/null 2>&1; then
    echo "    ⚠ 合并冲突，放弃 $br（需人工处理）"; git merge --abort || true; continue
  fi
  python3 skills/ai-daily-digest/run.py --reindex   # 以实际文件为准重建 index/latest，避免合并产生的指针错位
  git add -A && git commit -q -m "merge daily $date（云端 routine）" 2>/dev/null || true
  retry git push origin main --quiet
  git push origin --delete "$br" --quiet 2>/dev/null || true
  echo "    ✓ 已合并并推送 main，删除 $br"
done

echo "[3/3] 各厂商建微信贴图草稿…"
TODAY="$(TZ=Asia/Shanghai date +%F)"
# 自适应：未显式指定厂商时，取当天 data/*/<date>.json 存在的全部厂商（新增厂商自动覆盖）
if [ -n "$VENDORS_PUBLISH" ]; then
  vendors="$VENDORS_PUBLISH"
else
  vendors=""
  for f in data/*/"$TODAY".json; do
    [ -f "$f" ] || continue
    vendors="$vendors $(basename "$(dirname "$f")")"
  done
fi
[ -n "${vendors// /}" ] || echo "  · 今天（$TODAY）暂无任何厂商数据，跳过发布"

published=""; failed=""
for v in $vendors; do
  f="data/$v/$TODAY.json"
  [ -f "$f" ] || { echo "  · $v 无 $TODAY 数据，跳过"; continue; }
  mark="$REPO/.last_published.$v"
  if [ -z "$DRY" ] && [ -f "$mark" ] && [ "$(cat "$mark" 2>/dev/null)" = "$TODAY" ]; then
    echo "  · $v $TODAY 已推过草稿，跳过"; continue
  fi
  echo "  · 微信贴图草稿：$v $TODAY"
  if python3 skills/ai-daily-digest/publish_wechat_newspic.py --vendor "$v" $DRY; then
    [ -z "$DRY" ] && echo "$TODAY" > "$mark"
    published="$published $v"
  else
    echo "    ⚠ $v 微信草稿失败（检查 ~/.config/wechat-official-draft/config.yaml、本机公网 IP 白名单、需已认证服务号）"
    failed="$failed $v"
  fi
done

echo "✓ watch-and-publish 完成（$TODAY）"

# 手机推送：本次真的新建了草稿才提醒去后台核对发布（dry-run 不推）
if [ -z "$DRY" ] && [ -n "${published// /}" ]; then
  msg="今日草稿已进箱待发布：${published# }"
  [ -n "${failed// /}" ] && msg="$msg；失败：${failed# }"
  "$REPO/scripts/notify.sh" "AI 前哨 · 公众号草稿就绪" "$msg" || true
fi
