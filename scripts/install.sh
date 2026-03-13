#!/usr/bin/env sh
set -eu

REPO_URL="https://github.com/yorrany/Skills_Codex.git"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
TARGET_DIR="$CODEX_HOME/skills"

if ! command -v git >/dev/null 2>&1; then
  printf "Error: git is required but not installed.\n" >&2
  printf "Install git and re-run this installer.\n" >&2
  exit 1
fi

if [ -d "$TARGET_DIR/.git" ]; then
  printf "Updating existing skills repo in %s\n" "$TARGET_DIR"
  git -C "$TARGET_DIR" pull --ff-only
  exit 0
fi

if [ -e "$TARGET_DIR" ]; then
  printf "Error: %s exists but is not a git repo.\n" "$TARGET_DIR" >&2
  printf "Move it aside or remove it, then re-run this installer.\n" >&2
  exit 1
fi

printf "Cloning skills repo into %s\n" "$TARGET_DIR"
mkdir -p "$CODEX_HOME"

git clone "$REPO_URL" "$TARGET_DIR"
