# import-adventure

Imports a published Draw Steel adventure PDF into the active campaign, extracting Entities and scaffolding an Adventure directory.

**Required argument:** path to the PDF file.

If the Director has not provided a PDF path, ask:
> "What is the path to the adventure PDF?"

---

## Step 0 — Prerequisite check

Before doing anything else, check whether `~/.claude/skills/pdf-to-md/` exists.

If it does not exist, stop immediately and respond:

> "The pdf-to-md skill is required but not installed. Install it from https://github.com/pop-dog/ai-tools, then run install.sh."

Do not proceed past this step until the prerequisite is satisfied.

---

## Step 1 — Scaffold the Adventure

Ask the Director for the adventure name if not already provided.

Run:

```
steel-golem adventures new --name "<adventure name>"
```

Note the slug printed in the CLI output (e.g., `Created adventure 'The Sunken Archive' at .../the-sunken-archive`). The slug is the directory name at the end of the path.

Then set it as the active adventure:

```
steel-golem adventures set <slug>
```

### Error handling

| CLI output | Action |
|------------|--------|
| `Error: Config file not found...` | Tell the Director no campaign is active and suggest running the `campaigns-new` skill first. Stop. |
| `Error: Adventure directory already exists: ...` | Tell the Director an adventure with that slug already exists and ask for a different name. |
| `Error: Adventure '<slug>' not found...` | Tell the Director the slug was not found. Re-run `steel-golem adventures list` and confirm the correct slug. |
| Any other non-zero exit | Show the error verbatim and ask the Director how to proceed. Stop. |

---

## Step 2 — pdf-to-md sub-agent

Spawn a sub-agent with the pdf-to-md skill and the PDF path. The sub-agent converts the PDF into a directory of structured markdown files, one per page or chapter.

Instruction to sub-agent:
> Use the pdf-to-md skill to convert `<pdf path>` to markdown. Return the path to the output directory when complete.

Note the output directory returned by the sub-agent. All subsequent steps read from this directory.

---

## Step 3 — Entity extraction sub-agent

Spawn a sub-agent with the following instructions:

---

Read ALL markdown files in `<pdf-to-md output directory>` from beginning to end.

Consult `~/.steel-golem/entity-schemas/` for the field names and CLI contracts for each Entity type.

Identify every instance of the following 11 Entity types that is **explicitly named** in the text:

- NPC
- Villain
- Location
- Faction
- Subplot
- Handout
- Notable Item
- Downtime Project
- Combat Encounter
- Negotiation
- Montage

Return a structured JSON list. Each entry must include at minimum `type` and `name`. Include a `description` field if the text provides a clear summary sentence or two. Do not include relationship fields (faction, location, etc.) — those are set in Step 5.

Be conservative: only extract Entities that are clearly named and meaningfully described. Do not infer Entities from passing mentions. Do not fabricate.

Example output shape:
```json
[
  {"type": "npc", "name": "Mira the Innkeeper", "description": "Runs the Copper Flagon inn; knows about the cult's movements."},
  {"type": "villain", "name": "The Warden", "description": "Commander of the prison fortress; seeks to contain the artifact."},
  {"type": "location", "name": "The Sunken Archive", "description": "A flooded library beneath the city."},
  {"type": "faction", "name": "The Ironveil Cult", "description": "A secretive group worshipping the artifact."},
  {"type": "combat-encounter", "name": "Throne Room Battle", "description": "Final confrontation with the Warden in the throne room."},
  {"type": "negotiation", "name": "Bargaining with the Harbormaster", "description": "Convincing the harbormaster to allow access to the archive."},
  {"type": "montage", "name": "Crossing the Storm Peaks", "description": "The heroes race through a mountain pass in worsening weather."},
  {"type": "subplot", "name": "The Missing Courier", "description": "Someone intercepted the message that started everything."},
  {"type": "handout", "name": "The Warden's Letter", "description": "A letter revealing the Warden's true orders."},
  {"type": "notable-item", "name": "The Obsidian Key", "description": "Opens the innermost vault of the Sunken Archive."},
  {"type": "downtime-project", "name": "Decipher the Vault Inscription", "description": "Translate the inscription on the vault door to learn its secrets."}
]
```

Return the JSON list only. No prose before or after.

---

Receive the structured entity list from the sub-agent. Parse it. Proceed to Step 4.

---

## Step 4 — Create entities (orchestrator)

For each entity in the extraction list, call the appropriate CLI command directly. The active adventure is already set, so no scope flag is needed — all Entities default to the active adventure.

### CLI commands by type

| Entity type | CLI command |
|-------------|-------------|
| `npc` | `steel-golem npcs new --name "<name>" [--description "<desc>"]` |
| `villain` | `steel-golem villains new --name "<name>" [--description "<desc>"]` |
| `location` | `steel-golem locations new --name "<name>" [--description "<desc>"]` |
| `faction` | `steel-golem factions new --name "<name>" [--description "<desc>"]` |
| `subplot` | `steel-golem subplots new --name "<name>" [--description "<desc>"]` |
| `handout` | `steel-golem handouts new --name "<name>" [--description "<desc>"]` |
| `notable-item` | `steel-golem items new --name "<name>" [--description "<desc>"]` |
| `downtime-project` | `steel-golem downtime-projects new --name "<name>" [--description "<desc>"]` |
| `combat-encounter` | `steel-golem encounters combat new --name "<name>" [--description "<desc>"]` |
| `negotiation` | `steel-golem encounters negotiation new --name "<name>" [--description "<desc>"]` |
| `montage` | `steel-golem encounters montage new --name "<name>" [--description "<desc>"]` |

### Rules

- Do NOT invoke the `create-entity` skill. Call the CLI directly.
- Omit `--description` if the entity has no description (the CLI defaults to `""`).
- Do NOT pass `--campaign` or `--adventure`. All Entities land in the active adventure.
- If an individual command fails, log the failure and continue. Do not stop the whole import.
- Collect all errors in a list to report to the Director at the end.
- Note the slug printed in each CLI output — you will pass the full entity list (names and slugs) to the finalization sub-agent.

---

## Step 5 — Finalization sub-agent

Spawn a sub-agent with the following instructions:

---

You have two inputs:

1. The entity list extracted and created during import (names, types, slugs, descriptions).
2. The pdf-to-md output directory at `<pdf-to-md output directory>`.

### Task A — Relationships

Re-read the markdown files in the pdf-to-md output directory.

For each Entity file that was created, identify relationships that are **explicitly stated** in the text. Do not infer relationships — only write what the source material says directly.

Examples of explicit statements:
- "Mira is a member of the Ironveil Cult" → write `faction: ironveil-cult` to the NPC file.
- "The throne room battle takes place in the Citadel of Chains" → write `location: citadel-of-chains` to the combat encounter file.

Use the following relationship fields per type (sourced from `~/.steel-golem/entity-schemas/`):

| Entity type | Relationship fields |
|-------------|---------------------|
| NPC | `faction` (faction slug), `location` (location slug) |
| Villain | `location` (location slug) |
| Notable Item | `owner` (hero/npc/villain slug), `location` (location slug) |
| Combat Encounter | `location` (location slug), `villain` (villain slug) |
| Negotiation | `npc` (npc slug), `location` (location slug) |
| Montage | `location` (location slug) |
| Subplot | `plot` (campaign plot slug — only if explicitly named) |

Edit each entity's `.md` file directly to update these frontmatter fields. Use slugs (kebab-case), not display names. If a relationship is not explicitly stated, leave the field as `null`.

### Task B — Adventure Summary

Write the Adventure Summary to the body of the Adventure's `index.md`.

The body begins after the YAML frontmatter block (after the closing `---`). Write narrative prose that:
- Describes the adventure's plot and overarching conflict
- Names and situates the key Entities and their roles
- Describes the connective tissue: how the Entities relate to the plot and to each other

Do NOT include a table of imported Entities. The Adventure directory is self-indexing.
Do NOT use headers — write plain narrative prose.

---

## Finalization report

After the finalization sub-agent completes, report to the Director:

- Adventure name and slug
- Total Entities extracted and created (count by type)
- Any Entity creation failures (name + error message)
- A note that relationships and the Adventure Summary have been written

Example:
> Import complete: **The Sunken Archive** (`the-sunken-archive`)
>
> Created: 3 NPCs, 1 Villain, 4 Locations, 2 Factions, 1 Subplot, 1 Handout, 1 Notable Item, 1 Downtime Project, 2 Combat Encounters, 1 Negotiation, 1 Montage
>
> Failures: none
>
> Relationships and Adventure Summary written to `index.md`.
