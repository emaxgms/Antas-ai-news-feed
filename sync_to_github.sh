#!/usr/bin/env bash
set -euo pipefail
REPO_DIR="/home/ema/Antas-ai-news-feed"
cd "$REPO_DIR"

if [ ! -d .git ]; then
  echo "✗ Not a git repo: $REPO_DIR" >&2
  exit 1
fi

if [ -z "$(git remote)" ]; then
  echo "✗ No git remote configured" >&2
  exit 1
fi

git add items.json index.html README.md

if git diff --cached --quiet; then
  echo "⊘ No changes to commit"
  exit 0
fi

git commit -m "chore: update Antas AI News feed ($(date '+%Y-%m-%d %H:%M'))"
git push -u  origin main
