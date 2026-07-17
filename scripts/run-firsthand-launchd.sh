#!/usr/bin/env bash
set -euo pipefail

REPO="/Users/jialu/ai-frontier-daily"
WORKTREE="/Users/jialu/.local/share/ai-frontier-daily/worktrees/firsthand"
LOCK="/tmp/ai-frontier-daily-firsthand.lock"

if ! mkdir "$LOCK" 2>/dev/null; then
  echo "firsthand monitor 已有实例运行，本次跳过"
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null || true' EXIT

mkdir -p "$(dirname "$WORKTREE")"
git -C "$REPO" fetch origin --prune --quiet
if [ ! -e "$WORKTREE/.git" ]; then
  git -C "$REPO" worktree add --detach "$WORKTREE" origin/main
fi

cd "$WORKTREE"
/Users/jialu/anaconda3/bin/python3 scripts/monitor_firsthand.py
