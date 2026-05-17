# ADR 001: Scaffold CLI Design

## Status

Accepted

## Context

The first concrete implementation in steel-golem is the scaffold layer: commands to create a new Campaign directory structure and a new Adventure directory structure within it. These commands must be invokable both manually from the terminal and from Claude Skills. This ADR records all design decisions made for this layer.

## Decisions

### 1. `campaign_path` points directly to the campaign root

The `campaign_path` value in `config.yaml` is the campaign root directory itself. Entity directories (`heroes/`, `sessions/`, etc.) live directly under it. The PRD's `campaign/<type>/` phrasing is prose, not a literal subdirectory.

### 2. Unified CLI with command groups

All steel-golem functionality is exposed through a single `steel-golem` CLI entry point, organised into noun-first command groups:

```
steel-golem campaigns new "Iron Throne" --path ~/campaigns
steel-golem adventures new "The Sunken Vault"
steel-golem adventures set the-sunken-vault
steel-golem adventures list
```

Future groups (`sessions`, `entities`, etc.) follow the same pattern. `--help` is useful at each group level.

### 3. Click as the CLI library

`click` is used for command dispatch. `argparse` subcommand syntax is too verbose for a growing multi-command tool; `typer` adds abstraction that obscures incremental extension. `click` is the right balance.

### 4. Config lives at `~/.steel-golem/config.yaml`

The live config is at `~/.steel-golem/config.yaml`, not in the repo and not resolved from `$PWD`. This means:

- The CLI can be invoked from any directory
- The repo config stub is never overwritten by real values
- `~/.steel-golem/` is the natural home for any future user-specific state

The repo ships `config.yaml.example` as a documented template. It is never modified by any script.

### 5. `campaigns new` bootstraps `~/.steel-golem/`

`campaigns new` is the only command that can run before a config exists — every other command requires a campaign. Therefore it is the only command responsible for creating `~/.steel-golem/` and writing the initial `config.yaml`. Any other command that requires config and finds it absent fails with: `"No campaign found. Run 'steel-golem campaigns new' first."`

### 6. Hard fail if the target directory already exists

Both `campaigns new` and `adventures new` exit with a non-zero code and a clear error message if the target directory already exists. Scaffold commands are one-shot operations; running them twice against the same target almost certainly means a mistake.

### 7. Scaffold creates directories and a root `index.md` only

No stub files are created inside entity subdirectories. No `.gitkeep` files. The campaign root gets one `index.md`; each adventure gets one `index.md`. Empty directories are left empty.

### 8. Campaign `index.md` frontmatter schema

```yaml
---
name: Iron Throne
slug: iron-throne
created: 2026-05-17
status: active
current_adventure: null
---
```

`current_adventure` is always present, initially `null`. Skills read it without defensive `.get()` calls.

### 9. Adventure `index.md` frontmatter schema

```yaml
---
name: The Sunken Vault
slug: the-sunken-vault
created: 2026-05-17
status: active
---
```

No `campaign` field — the adventure's location in the directory tree encodes the campaign relationship.

### 10. `adventures new` does not change the active adventure, except when null

Directors prep adventures in advance while a different adventure is active. `adventures new` sets `current_adventure` in the campaign `index.md` only if it is currently `null` (i.e., the very first adventure). All other transitions require an explicit `adventures set <slug>`.

### 11. `adventures set` takes a slug

```
steel-golem adventures set the-sunken-vault
```

The slug is the directory name — visible via `ls` or `adventures list`. Accepting a human-readable name would require fuzzy matching that can fail silently. The command fails clearly if the slug does not exist as a directory.

### 12. `adventures list` output format

```
  the-sunken-vault   The Sunken Vault
* the-black-moor     The Black Moor
```

A `*` marks the current adventure. Slug and name on each line. No other fields.

### 13. Slugification rules

- Lowercase everything
- Replace spaces and underscores with hyphens
- Strip characters that are not alphanumeric or hyphens
- Collapse consecutive hyphens to one
- Strip leading and trailing hyphens
- If the result is empty, fail with a clear error

### 14. Package structure

```
steel-golem/
├── config.yaml.example
├── pyproject.toml
├── src/
│   └── steel_golem/
│       ├── __init__.py
│       ├── cli.py             # click entry point and group dispatch
│       └── scaffold.py        # shared scaffold logic
├── skills/
│   ├── new-campaign/
│   │   └── SKILL.md           # pure instructions; no code
│   └── new-adventure/
│       └── SKILL.md           # pure instructions; no code
└── tests/
    └── test_scaffold.py
```

`pyproject.toml` defines the entry point:

```toml
[project.scripts]
steel-golem = "steel_golem.cli:main"
```

`pip install -e .` is the one-time setup step. After that, `steel-golem` is on the PATH.

### 15. Skills are pure instruction files

`SKILL.md` files contain instructions telling Claude what CLI command to run and what arguments to extract from the Director's message. No Python or shell code lives in skill directories for these commands.

### 16. `python-frontmatter` for reading and writing `index.md` files

`python-frontmatter` reads and writes YAML frontmatter in markdown files without disturbing the markdown body. It replaces direct PyYAML use for all file I/O. PyYAML becomes a transitive dependency.

### 17. Test strategy

- **Unit tests** (`test_scaffold.py`): import `steel_golem.scaffold` directly, call functions with a `tmp_path` fixture, assert directory tree and frontmatter values. Cover edge cases: empty slug, existing directory, missing config.
- **Integration tests**: use Click's `CliRunner` to invoke commands as a black box and assert filesystem side effects. One or two tests per command to verify argument parsing and the `~/.steel-golem/` bootstrap end to end.
