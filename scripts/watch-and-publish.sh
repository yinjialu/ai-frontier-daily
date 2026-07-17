#!/usr/bin/env bash
# 本机监听器：从远程 main / 当天日报分支读取内容，再为各厂商建微信贴图草稿。
# 小红书图文笔记（走本地 xiaohongshu-mcp 服务，见 publish_xhs_newspic.py）：平台已警告三方工具/脚本
# 发布，[4/4] 段默认暂停（XHS_PUBLISH=1 才发），代码与登录态保留以便后续恢复或更换合规方案。
#
# 背景：云端代理「只允许推当前工作分支」，routine 推不了 main，只能推内容分支
#       （如 daily-<DATE>、Codex/daily-<DATE>）。本脚本在本机（有完整 push 权）做合并 + 微信发布。
#
# 用法：
#   scripts/watch-and-publish.sh            # 合并每日内容分支 → main → 各厂商建微信贴图草稿
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
python3 scripts/doctor_publish.py --stage pages
retry git fetch origin --prune --quiet

# 22:00 Automation 预制次日刊：晚间运行取次日，午夜后运行取当天。
# PUBLISH_DATE 可用于手动补发或测试，格式 YYYY-MM-DD。
if [ -n "${PUBLISH_DATE:-}" ]; then
  TARGET_DATE="$PUBLISH_DATE"
elif [ "$(TZ=Asia/Shanghai date +%H)" -ge 18 ]; then
  TARGET_DATE="$(TZ=Asia/Shanghai date -v+1d +%F)"
else
  TARGET_DATE="$(TZ=Asia/Shanghai date +%F)"
fi

echo "[2/3] 选择日报刊期：$TARGET_DATE"
source_ref="origin/main"
for candidate in "origin/Codex/daily-$TARGET_DATE" "origin/codex/daily-$TARGET_DATE" "origin/daily-$TARGET_DATE"; do
  if git rev-parse --verify --quiet "$candidate" >/dev/null; then
    source_ref="$candidate"
    break
  fi
done
echo "  · 内容来源：$source_ref ($(git rev-parse --short "$source_ref"))"

# 不切换当前 worktree（避免覆盖正在执行的脚本）；只把目标 ref 的发布素材导出到临时目录。
CONTENT_ROOT="${PUBLISH_CONTENT_ROOT:-$HOME/.local/share/ai-frontier-daily/publisher-content}"
rm -rf "$CONTENT_ROOT"
mkdir -p "$CONTENT_ROOT"
git archive "$source_ref" data output | tar -x -C "$CONTENT_ROOT"
export DIGEST_OUT="$CONTENT_ROOT"

echo "[3/4] 各厂商建微信贴图草稿…"
# 自适应：未显式指定厂商时，取当天 data/*/<date>.json 存在的全部厂商（新增厂商自动覆盖）
if [ -n "$VENDORS_PUBLISH" ]; then
  vendors="$VENDORS_PUBLISH"
else
  vendors=""
  for f in "$CONTENT_ROOT"/data/*/"$TARGET_DATE".json; do
    [ -f "$f" ] || continue
    vendors="$vendors $(basename "$(dirname "$f")")"
  done
fi
[ -n "${vendors// /}" ] || echo "  · 刊期（$TARGET_DATE）暂无任何厂商数据，跳过发布"
[ -z "${vendors// /}" ] || python3 scripts/doctor_publish.py --stage wechat

published=""; failed=""
for v in $vendors; do
  f="$CONTENT_ROOT/data/$v/$TARGET_DATE.json"
  [ -f "$f" ] || { echo "  · $v 无 $TARGET_DATE 数据，跳过"; continue; }
  mark="$REPO/.last_published.$v"
  if [ -z "$DRY" ] && [ -f "$mark" ] && [ "$(cat "$mark" 2>/dev/null)" = "$TARGET_DATE" ]; then
    echo "  · $v $TARGET_DATE 已推过草稿，跳过"; continue
  fi
  echo "  · 微信贴图草稿：$v $TARGET_DATE"
  if python3 skills/ai-daily-digest/publish_wechat_newspic.py "$f" $DRY; then
    [ -z "$DRY" ] && echo "$TARGET_DATE" > "$mark"
    published="$published $v"
  else
    echo "    ⚠ $v 微信草稿失败（检查 ~/.config/wechat-official-draft/config.yaml、本机公网 IP 白名单、需已认证服务号）"
    failed="$failed $v"
  fi
done

echo "[4/4] 各厂商发布小红书图文笔记…"
# 小红书已开始警告「使用三方工具/脚本发布内容」，为规避账号风控，暂停自动发布链路（走 xiaohongshu-mcp）。
# 发布器代码与登录态均保留；确需手动发布时显式开启：XHS_PUBLISH=1 scripts/watch-and-publish.sh
XHS_PUBLISH="${XHS_PUBLISH:-0}"
xhs_published=""; xhs_failed=""
if [ "$XHS_PUBLISH" != "1" ]; then
  echo "  · 小红书自动发布已暂停（XHS_PUBLISH≠1，规避三方工具发布风控），跳过"
else
[ -z "${vendors// /}" ] || python3 scripts/doctor_publish.py --stage xhs
for v in $vendors; do
  f="$CONTENT_ROOT/data/$v/$TARGET_DATE.json"
  [ -f "$f" ] || continue
  mark="$REPO/.last_published_xhs.$v"
  if [ -z "$DRY" ] && [ -f "$mark" ] && [ "$(cat "$mark" 2>/dev/null)" = "$TARGET_DATE" ]; then
    echo "  · $v $TARGET_DATE 已发过小红书，跳过"; continue
  fi
  echo "  · 小红书笔记：$v $TARGET_DATE"
  if [ -n "$DRY" ]; then
    python3 skills/ai-daily-digest/publish_xhs_newspic.py --vendor "$v" --dry-run >/dev/null && echo "    (dry-run：素材组装 OK，不发布)"
    continue
  fi
  if python3 skills/ai-daily-digest/publish_xhs_newspic.py --vendor "$v"; then
    echo "$TARGET_DATE" > "$mark"
    xhs_published="$xhs_published $v"
    sleep 45   # 厂商间隔，避免连发触发风控
  else
    echo "    ⚠ $v 小红书发布失败（登录态看 ~/.config/xiaohongshu-mcp/，服务日志 ~/Library/Logs/xiaohongshu-mcp.log）"
    xhs_failed="$xhs_failed $v"
  fi
done
fi

echo "✓ watch-and-publish 完成（刊期 ${TARGET_DATE}）"

# 手机推送：本次真的有动作才提醒（dry-run 不推）
if [ -z "$DRY" ] && { [ -n "${published// /}" ] || [ -n "${xhs_published// /}" ] || [ -n "${xhs_failed// /}" ]; }; then
  msg=""
  [ -n "${published// /}" ] && msg="公众号草稿进箱：${published# }"
  [ -n "${failed// /}" ] && msg="$msg；公众号失败：${failed# }"
  [ -n "${xhs_published// /}" ] && msg="$msg；小红书已发：${xhs_published# }"
  [ -n "${xhs_failed// /}" ] && msg="$msg；小红书失败：${xhs_failed# }"
  "$REPO/scripts/notify.sh" "AI 前哨 · 今日发布" "${msg#；}" || true
fi

[ -z "${failed// /}" ] && [ -z "${xhs_failed// /}" ]
