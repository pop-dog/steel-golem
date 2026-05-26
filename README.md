# Steel Golem

A personal Director assistant for the [Draw Steel](https://mcdm.gg/DrawSteel) TTRPG.

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![Version](https://img.shields.io/badge/version-0.1.0-informational)
![License](https://img.shields.io/badge/license-DRAW%20STEEL%20Creator%20License-lightgrey)

Steel Golem tracks campaign state, scaffolds new campaigns and adventures, assists with session planning, and answers rules questions — all backed by a Campaign Database of plain-text markdown files you own and version-control. Running a Draw Steel campaign means managing a growing web of Heroes, Villains, Adventures, Encounters, Plots, and Downtime Projects. Steel Golem keeps that information structured and reachable so the Director can focus on the game, not on finding their notes.

## Features

- **Campaign Database** — a directory tree of plain-text markdown files with YAML frontmatter; edit in any editor, version-control however you like
- **CLI** — `steel-golem` commands to create campaigns, adventures, and all ten entity types (NPCs, Villains, Locations, Factions, Subplots, Handouts, Items, Encounters, and more)
- **Claude Skills** — interact with your Campaign Database in natural language inside Claude Code
- **Adventure import** — extract Entities from a published adventure PDF and scaffold the full adventure directory automatically
- **Rules reference** — answer Draw Steel rules questions with citations sourced from the bundled `steel-compendium` corpus
- **Adventure overview** — guided Q&A session that produces a rich Director-facing reference document with Mermaid flowcharts and entity relationship diagrams
- **Entity promotion** — move an Entity from adventure scope to campaign scope as characters and locations grow beyond a single adventure

## Installation

Requires Python 3.11 or newer and [Claude Code](https://claude.ai/code).

```sh
git clone --recurse-submodules https://github.com/wmyers09/steel-golem.git
cd steel-golem
pip install -e .
./install.sh
```

`--recurse-submodules` pulls in `steel-compendium`, the Draw Steel rules corpus used by the `rules-reference` skill.

`install.sh` symlinks the agent definition and skill files into `~/.claude/` so Claude Code discovers them, and symlinks `CONTEXT.md` and `steel-compendium` into `~/.steel-golem/` so the agent can find them at a stable path. The script is idempotent and safe to re-run after pulling new commits.

## Usage

### Create a campaign

```sh
steel-golem campaigns new --name "Iron Throne" --path ~/campaigns
# Created campaign 'Iron Throne' at /home/you/campaigns/iron-throne
```

This creates the full campaign directory tree and writes `~/.steel-golem/config.yaml` so every subsequent command knows where your campaign lives.

### Manage adventures

```sh
steel-golem adventures new --name "The Sunken Vault"
# Created adventure 'The Sunken Vault' at .../adventures/the-sunken-vault

steel-golem adventures list
#   the-sunken-vault   The Sunken Vault
# * the-black-moor     The Black Moor

steel-golem adventures set the-sunken-vault
# Active adventure set to 'the-sunken-vault'
```

### Create entities

```sh
steel-golem npcs new --name "Mira the Innkeeper" --description "Runs the Copper Flagon; knows about the cult."
steel-golem villains new --name "The Warden" --campaign   # campaign-scoped
steel-golem encounters combat new --name "Throne Room Battle"
```

All entity commands accept `--adventure <slug>` to target a specific adventure, or `--campaign` (where supported) to write to campaign scope instead.

### Claude Skills

With the skills installed, you can do all of the above through natural language in Claude Code:

| Skill | Invoke | What it does |
|-------|--------|--------------|
| `campaigns-new` | `/campaigns-new` | Create a campaign — Claude extracts name and path from your message |
| `adventures-new` | `/adventures-new` | Create an adventure under the active campaign |
| `adventures-set` | `/adventures-set` | List adventures and switch the active one |
| `import-adventure` | `/import-adventure` | Extract Entities from a PDF and scaffold a full adventure directory |
| `adventure-overview` | `/adventure-overview` | Guided Q&A that produces a reference doc with Mermaid diagrams |
| `rules-reference` | `/rules-reference` | Answer rules questions with citations from the compendium |

## Campaign Database layout

```
<campaign-root>/
├── index.md                    # campaign name, slug, status, active adventure
├── heroes/                     # player characters (always campaign-scoped)
├── villains/
├── npcs/
├── factions/
├── locations/
├── plots/
├── sessions/
├── items/
├── lore/
├── downtime-projects/
└── adventures/
    └── <slug>/
        ├── index.md            # adventure name, slug, status, summary
        ├── villains/
        ├── npcs/
        ├── factions/
        ├── locations/
        ├── subplots/
        ├── handouts/           # revealed: true/false controls player visibility
        ├── custom-monsters/
        ├── downtime-projects/
        └── encounters/
            ├── combat/
            ├── negotiations/
            └── montages/
```

Entities can be **promoted** from adventure scope to campaign scope (a file move plus frontmatter update) when a character or location grows beyond a single adventure.

## Configuration

The live config is created automatically at `~/.steel-golem/config.yaml` by `campaigns new`. See `config.yaml.example` for the documented template.

```yaml
campaign_path: /absolute/path/to/your/campaign-root
```

## Roadmap

See [docs/roadmap.md](docs/roadmap.md) for planned features.

## Support

File bugs and feature requests on the [GitHub issue tracker](https://github.com/wmyers09/steel-golem/issues).

## License

Steel Golem is an independent product published under the DRAW STEEL Creator License and is not affiliated with MCDM Productions, LLC. DRAW STEEL © 2024 MCDM Productions, LLC.
