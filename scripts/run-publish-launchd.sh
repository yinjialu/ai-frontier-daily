#!/usr/bin/env bash
set -euo pipefail

REPO="/Users/jialu/ai-frontier-daily"
WORKTREE="/Users/jialu/.local/share/ai-frontier-daily/worktrees/publisher"
LOCK="/tmp/ai-frontier-daily-publisher.lock"

if ! mkdir "$LOCK" 2>/dev/null; then
  echo "publisher 已有实例运行，本次跳过"
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null || true' EXIT

mkdir -p "$(dirname "$WORKTREE")"
git -C "$REPO" fetch origin --prune --quiet
if [ ! -e "$WORKTREE/.git" ]; then
  git -C "$REPO" worktree add --detach "$WORKTREE" origin/main
fi

/bin/bash "$WORKTREE/scripts/watch-and-publish.sh" "$@"
