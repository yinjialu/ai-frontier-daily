#!/usr/bin/env bash
# Guard a daily digest content commit before it is created or pushed.
#
# Usage:
#   git add -A data output
#   scripts/guard-daily-content-commit.sh 2026-07-07
#
# The guard intentionally checks the staged diff. Run it after staging and
# before `git commit -m "daily: YYYY-MM-DD"`.
set -euo pipefail

DATE="${1:-}"
if [[ ! "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "usage: $0 YYYY-MM-DD" >&2
  exit 2
fi

branch="$(git branch --show-current 2>/dev/null || true)"
expected="Codex/daily-$DATE"
if [[ "$branch" != "$expected" ]]; then
  echo "Refusing daily commit: current branch is '${branch:-detached}', expected '$expected'." >&2
  exit 1
fi

if git diff --cached --quiet --exit-code; then
  echo "Refusing daily commit: staged diff is empty." >&2
  exit 1
fi

bad_paths="$(git diff --cached --name-only --diff-filter=ACMRTUXB | grep -vE '^(data|output)/' || true)"
if [[ -n "$bad_paths" ]]; then
  echo "Refusing daily commit: staged files outside data/ and output/:" >&2
  echo "$bad_paths" >&2
  exit 1
fi

if git diff --cached --name-only --diff-filter=ACMRTUXB | grep -q '^data/firsthand/'; then
  echo "Refusing daily commit: data/firsthand belongs to firsthand PRs, not daily content branches." >&2
  exit 1
fi

if ! git diff --cached --name-only --diff-filter=ACMRTUXB | grep -qE "^(data|output)/[^/]+/$DATE(\\.json|/)"; then
  echo "Refusing daily commit: staged files do not include content for $DATE." >&2
  exit 1
fi

echo "Daily content commit guard passed for $branch."
