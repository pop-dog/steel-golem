# ADR 002: ~/.steel-golem as the Agent's Fixed Home Directory

## Status

Accepted

## Context

The Steel Golem agent needs a stable location to find its authoritative data: the CONTEXT.md glossary, the steel-compendium rules reference, and the live config.yaml. That location must be predictable at agent runtime without reading the config first, because the config itself lives there.

A parallel need exists for the Claude integration layer: the agent definition (agents/steel-golem.md) and skill instruction files (skills/*/SKILL.md) must be installed into ~/.claude/ so that Claude Code discovers them. Both targets are under the user's home directory and must survive re-cloning the repo.

install.sh is the mechanism that bridges the repo and the user's home directory by creating symlinks.

## Decisions

### 1. ~/.steel-golem/ is the canonical home for agent-readable project data

The agent hardcodes `~/.steel-golem/` in all path references (CONTEXT.md, steel-compendium, config.yaml). This makes agent prompts and skill instructions predictable regardless of where the repo is cloned. The directory is created by install.sh if absent, and by `campaigns new` if the CLI runs first.

### 2. install.sh manages symlinks into ~/.steel-golem/ and ~/.claude/

install.sh is an idempotent shell script that:

- Symlinks `~/.steel-golem/CONTEXT.md` → `$REPO/CONTEXT.md`
- Symlinks `~/.steel-golem/steel-compendium` → `$REPO/steel-compendium`
- Symlinks `~/.claude/agents/steel-golem.md` → `$REPO/agents/steel-golem.md`
- Symlinks `~/.claude/skills/<name>` → `$REPO/skills/<name>` for each skill directory

Symlinks mean that editing the source files in the repo immediately updates the installed versions without re-running install.sh. Running install.sh a second time is safe: it re-confirms each link and prints the same confirmation lines.

install.sh respects two environment variable overrides for testing: `STEEL_GOLEM_HOME` (defaults to `~/.steel-golem`) and `CLAUDE_HOME` (defaults to `~/.claude`).

### 3. The agent hardcodes ~/.steel-golem/ paths (not derived from config or symlink resolution)

The agent does not resolve symlinks to find the repo, and does not add a `golem_path` key to config.yaml. Hardcoding `~/.steel-golem/` in the agent system prompt is simpler, more robust, and eliminates a class of bootstrap failures where the agent cannot find its context before it can read config.

## Alternatives Considered

**Extending config.yaml with a `golem_path` key.** This would allow the path to be configurable, but it introduces a chicken-and-egg problem: the agent needs to read CONTEXT.md before it knows where config.yaml is. It also complicates the agent system prompt and every skill instruction file.

**Resolving the `~/.claude/agents/steel-golem.md` symlink at runtime.** The agent could follow the symlink to discover the repo root and derive paths from there. This is fragile across environments and adds indirection with no benefit over a fixed home directory.

**A two-hop staging area** (e.g., copying files into ~/.steel-golem/ rather than symlinking). Copies would become stale whenever source files change. Symlinks are always in sync.
