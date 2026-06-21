#!/usr/bin/env bash
set -euo pipefail
REPO_DIR="${1:-.}"
cd "$REPO_DIR"

if [ ! -d .git ]; then
  echo "✗ Not a git repo: $REPO_DIR" >&2
  exit 1
fi

if [ -z "$(git remote)" ]; then
  echo "✗ No git remote configured" >&2
  exit 1
fi

git add items.json index.html

if git diff --cached --quiet; then
  echo "⊘ No changes to commit"
  exit 0
fi

git commit -m "chore: update ai dev news feed ($(date '+%Y-%m-%d %H:%M'))"
git push
