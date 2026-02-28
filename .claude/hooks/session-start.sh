#!/bin/bash
set -euo pipefail

# Install Python dependencies
pip install -q scipy || true

# Copy skills from repo into Claude's skill discovery directory
if [ -d "$CLAUDE_PROJECT_DIR/.claude/skills" ]; then
  for skill_dir in "$CLAUDE_PROJECT_DIR/.claude/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p "$HOME/.claude/skills/$skill_name"
    cp "$skill_dir/SKILL.md" "$HOME/.claude/skills/$skill_name/SKILL.md" 2>/dev/null || true
  done
fi
