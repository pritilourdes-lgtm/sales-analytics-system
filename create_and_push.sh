#!/usr/bin/env bash
# Helper: create GitHub repo and push current repo
# Usage: ./scripts/create_and_push.sh -u USERNAME [-p public|private]

set -euo pipefail

USAGE="Usage: $0 -u <github-username> [-p public|private]"
VISIBILITY="public"
USER=""

while getopts "u:p:" opt; do
  case "$opt" in
    u) USER="$OPTARG" ;;
    p) VISIBILITY="$OPTARG" ;;
    *) echo "$USAGE"; exit 1 ;;
  esac
done

if [ -z "$USER" ]; then
  echo "$USAGE"
  exit 1
fi

REPO_NAME=$(basename "$(pwd)")

if command -v gh >/dev/null 2>&1; then
  echo "Using gh to create repo ${USER}/${REPO_NAME} (${VISIBILITY}) and push..."
  gh repo create "${USER}/${REPO_NAME}" --${VISIBILITY} --source=. --remote=origin --push
  echo "Done. Remote origin set to https://github.com/${USER}/${REPO_NAME}.git"
else
  echo "gh CLI not found. Please run these commands manually (or install gh):"
  echo
  echo "  git remote add origin https://github.com/${USER}/${REPO_NAME}.git"
  echo "  git branch -M main"
  echo "  git push -u origin main"
  echo
  echo "Or install gh: https://cli.github.com/"
fi
