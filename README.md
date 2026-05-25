# Steel Golem

A personal Director assistant for the [Draw Steel](https://mcdm.gg/DrawSteel) TTRPG. Steel Golem tracks campaign state, scaffolds new campaigns and adventures, assists with session planning, and answers rules questions — all backed by a Campaign Database of plain-text markdown files you own and version-control.

## Background

Running a Draw Steel campaign means managing a growing web of interconnected information: Heroes and their goals, Villains and their plans, Adventures with NPCs and Encounters, Plots spanning the whole Campaign, Downtime Projects, Handouts, and more. Steel Golem keeps that information structured and reachable so the Director can focus on the game, not on finding their notes.

Steel Golem is implemented as a `steel-golem` CLI and a set of Claude Skills. The CLI handles filesystem operations; the Skills let you interact with your Campaign Database in natural language inside Claude Code.

## Installation

Requires Python 3.11 or newer and [Claude Code](https://claude.ai/code).

```sh
git clone --recurse-submodules https://github.com/wmyers09/steel-golem.git
cd steel-golem
pip install -e .
./install.sh
```

The `--recurse-submodules` flag pulls in `steel-compendium`, the Draw Steel rules corpus used by the rules-reference skill.

`install.sh` sets up the Claude integration layer: it symlinks the agent definition and skill instruction files into `~/.claude/` so Claude Code discovers them, and symlinks `CONTEXT.md` and `steel-compendium` into `~/.steel-golem/` so the agent can find them at a stable path. The script is idempotent and safe to re-run after pulling new commits.

## Usage

### Create a campaign

```sh
steel-golem campaigns new --name "Iron Throne" --path ~/campaigns
# Created campaign 'Iron Throne' at /home/you/campaigns/iron-throne
```

This creates the full campaign directory tree under `~/campaigns/iron-throne/` and writes `~/.steel-golem/config.yaml` so every subsequent command knows where your campaign lives.

### Manage adventures

```sh
# Create a new adventure
steel-golem adventures new --name "The Sunken Vault"
# Created adventure 'The Sunken Vault' at .../adventures/the-sunken-vault

# List adventures (* marks the active one)
steel-golem adventures list
#   the-sunken-vault   The Sunken Vault
# * the-black-moor     The Black Moor

# Switch the active adventure
steel-golem adventures set the-sunken-vault
# Active adventure set to 'the-sunken-vault'
```

### Claude Skills

With the skills in this repo installed in Claude Code, you can do the same things through natural language:

| Skill | Invoke | What it does |
|-------|--------|-------------|
| campaigns-new | `/campaigns-new` | Create a campaign — Claude extracts name and path from your message |
| adventures-new | `/adventures-new` | Create an adventure under the active campaign |
| adventures-set | `/adventures-set` | List adventures and switch the active one |

### Configuration

The live config lives at `~/.steel-golem/config.yaml` and is created automatically by `campaigns new`. The repo ships `config.yaml.example` as a documented template.

```yaml
campaign_path: /absolute/path/to/your/campaign-root
```

## Campaign Database

The Campaign Database is a directory tree of plain-text markdown files with YAML frontmatter. You own the files — put them in a git repo, edit them in any editor, and back them up however you like. Steel Golem reads and writes this directory; it never touches anything outside it.

```
<campaign-root>/
├── index.md                    # campaign name, slug, status, active adventure
├── heroes/                     # player characters (always campaign-scoped)
├── villains/                   # antagonists (campaign- or adventure-scoped)
├── npcs/                       # named non-villain characters
├── factions/                   # groups sharing goals and interests
├── locations/                  # named places at any scale
├── plots/                      # campaign-level narrative arcs
├── sessions/                   # session logs with embedded story beats
├── items/                      # notable items with history and ownership
├── lore/                       # cross-cutting world-building content
├── downtime-projects/          # Director-designed projects assigned to Heroes
└── adventures/
    └── <slug>/
        ├── index.md            # adventure name, slug, status
        ├── villains/
        ├── npcs/
        ├── factions/
        ├── locations/
        ├── subplots/           # adventure-scoped narrative threads
        ├── handouts/           # player-facing artifacts (revealed: true/false)
        ├── custom-monsters/    # homebrew creatures not in the bestiary
        ├── downtime-projects/
        └── encounters/
            ├── combat/         # monster roster, terrain, objective
            ├── negotiations/   # NPC, Patience, Interest, motivations, pitfalls
            └── montages/       # goal, required tests, success threshold
```

Entities can be **Promoted** from adventure-scope to campaign-scope (a file move plus frontmatter update) when a character or location grows beyond a single adventure.

## Roadmap

- [ ] `rules-reference` skill — answer rules questions with citations to the steel-compendium corpus
- [ ] `lazy-dm` skill — interactive eight-step session prep that reads your Campaign Database and proposes pre-populated answers at each step
- [ ] `build-encounter` skill — scaffold Combat, Negotiation, and Montage encounter files calibrated to the active Adventure and Hero capabilities
- [ ] `campaign-briefing` skill — synthesise recent Sessions, active Plots, and in-progress Downtime Projects into a pre-session summary
- [ ] `import-adventure` skill — extract NPCs, Locations, Encounters, and Handouts from a published adventure PDF
- [ ] Local HTTP server — browse the Campaign Database as HTML; player-facing route shows only `revealed: true` Handouts

## Support

File bugs and feature requests on the [GitHub issue tracker](https://github.com/wmyers09/steel-golem/issues).

## License

Steel Golem is an independent product published under the DRAW STEEL Creator License and is not affiliated with MCDM Productions, LLC. DRAW STEEL © 2024 MCDM Productions, LLC.
