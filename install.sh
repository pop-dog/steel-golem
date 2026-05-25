#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
STEEL_GOLEM_HOME="${STEEL_GOLEM_HOME:-$HOME/.steel-golem}"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"

link() {
    local target="$1"
    local link="$2"
    local label="$3"

    if [ -L "$link" ] && [ "$(readlink "$link")" = "$target" ]; then
        echo "✓ Linked $label"
        return
    fi

    if [ -e "$link" ] || [ -L "$link" ]; then
        rm -f "$link"
    fi

    ln -s "$target" "$link"
    echo "✓ Linked $label"
}

# 1. Create ~/.steel-golem/ if absent
mkdir -p "$STEEL_GOLEM_HOME"

# 2. Symlink CONTEXT.md
link "$REPO/CONTEXT.md" "$STEEL_GOLEM_HOME/CONTEXT.md" "~/.steel-golem/CONTEXT.md"

# 3. Symlink steel-compendium
link "$REPO/steel-compendium" "$STEEL_GOLEM_HOME/steel-compendium" "~/.steel-golem/steel-compendium"

# 4. Create ~/.claude/agents/ if absent; symlink agent definition
mkdir -p "$CLAUDE_HOME/agents"
link "$REPO/agents/steel-golem.md" "$CLAUDE_HOME/agents/steel-golem.md" "~/.claude/agents/steel-golem.md"

# 5. Create ~/.claude/skills/ if absent; symlink each skill directory
mkdir -p "$CLAUDE_HOME/skills"
for skill_dir in "$REPO/skills"/*/; do
    skill_name="$(basename "$skill_dir")"
    link "$REPO/skills/$skill_name" "$CLAUDE_HOME/skills/$skill_name" "~/.claude/skills/$skill_name"
done
