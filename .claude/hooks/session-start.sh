#!/bin/bash
set -euo pipefail

# Only run in remote (web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Install Python dependencies
pip install -q scipy || true

# Fetch latest from GitHub so we get up-to-date skills
cd "$CLAUDE_PROJECT_DIR"
git fetch origin --quiet 2>/dev/null || true

# Determine the default remote branch (e.g. main or master)
default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null \
  | sed 's|refs/remotes/origin/||') || default_branch="main"

# List skill directories from the remote ref
skills=$(git ls-tree --name-only "origin/$default_branch:.claude/skills/" 2>/dev/null) || skills=""

if [ -n "$skills" ]; then
  while IFS= read -r skill_name; do
    mkdir -p "$HOME/.claude/skills/$skill_name"
    git show "origin/$default_branch:.claude/skills/$skill_name/SKILL.md" \
      > "$HOME/.claude/skills/$skill_name/SKILL.md" 2>/dev/null || true
  done <<< "$skills"
fi
