# PRD: Entity Creation and Adventure Import

## Problem Statement

Directors using steel-golem have no way to create individual game Entities (NPCs, Villains, Locations, Encounters, Factions, etc.) within an Adventure, and no way to import a published adventure PDF into the Campaign Database. Populating an Adventure currently requires manually writing markdown files with correct frontmatter, in the correct directories, following conventions that exist only in the developer's head. When a Director acquires a commercial adventure module, they must manually transcribe every NPC, Location, Encounter, and Handout into the Campaign Database before steel-golem can assist with session prep — a process that takes hours and is error-prone.

## Solution

A two-layer solution: (1) a CLI-backed entity creation system with a `create-entity` skill that lets Directors create any of ten Entity types in natural language; and (2) an `import-adventure` skill that ingests a published adventure PDF and automatically populates the Adventure with extracted Entities, low-hanging-fruit relationships, and an Adventure Summary. A companion `adventure-overview` skill generates richer reference documents (Mermaid diagrams, relationship tables) after the Director has reviewed and enriched the imported content.

## User Stories

### Entity Creation

1. As a Director, I want to create an NPC by describing them in natural language, so that I don't need to know the frontmatter schema or directory structure.
2. As a Director, I want to create a Villain at Adventure or Campaign scope, so that I can track antagonists whether they are local to one Adventure or span the whole Campaign.
3. As a Director, I want to create a Location at Adventure or Campaign scope, so that named places are browsable and referenceable across Sessions.
4. As a Director, I want to create a Combat Encounter with a monster roster and objective, so that I have everything I need to run a tactical fight.
5. As a Director, I want to create a Negotiation with Patience, Interest, motivations, and pitfalls, so that the Draw Steel social mechanics are fully prepped.
6. As a Director, I want to create a Montage with a goal and required tests, so that group challenges have clear structure before play.
7. As a Director, I want to create a Faction with a description and goals, so that named groups are tracked at the appropriate scope.
8. As a Director, I want to create a Subplot within an Adventure, so that local narrative threads are documented and linkable to parent Plots.
9. As a Director, I want to create a Handout with content and a revealed status, so that player-facing artifacts are tracked independently from session notes.
10. As a Director, I want to create a Notable Item with a history and owner, so that named items with narrative significance are tracked as first-class Entities.
11. As a Director, I want to create an Unowned Downtime Project with a goal and Project Goal, so that Director-designed narrative projects are tracked even before I assign them to a Hero.
12. As a Director, I want entity creation to default to the active Adventure, so that I don't have to specify scope for the common case.
13. As a Director, I want to target a specific Adventure with `--adventure <slug>` when creating an Entity, so that I can prep a future Adventure while a different one is active.
14. As a Director, I want to write an Entity directly to Campaign scope with `--campaign`, so that Campaign-scoped Entities like recurring NPCs can be created without creating an Adventure first.
15. As a Director, I want the CLI to fail with a clear message if no Adventure is active and no scope flag is provided, so that I know how to resolve the error.
16. As a Director, I want each entity creation command to accept a name and type-specific fields, so that the resulting file has meaningful frontmatter from the start.

### Adventure Import

17. As a Director, I want to import a published adventure PDF by providing its path, so that the Campaign Database is populated without manual transcription.
18. As a Director, I want `import-adventure` to scaffold a new Adventure directory before populating it, so that the Adventure structure is consistent with hand-created Adventures.
19. As a Director, I want `import-adventure` to extract and create NPC files from the PDF, so that named characters are immediately browsable and annotatable.
20. As a Director, I want `import-adventure` to extract and create Villain files from the PDF, so that antagonists are tracked at Adventure scope and Promotable to Campaign scope later.
21. As a Director, I want `import-adventure` to extract and create Location files from the PDF, so that the adventure's spatial structure is browsable without reading the full PDF.
22. As a Director, I want `import-adventure` to extract and create Combat Encounter files with monster rosters from the PDF, so that tactical fights are prepped.
23. As a Director, I want `import-adventure` to extract and create Negotiation files from the PDF, so that Draw Steel social encounters are fully structured.
24. As a Director, I want `import-adventure` to extract and create Montage files from the PDF, so that group challenges have clear structure before play.
25. As a Director, I want `import-adventure` to extract and create Faction files from the PDF, so that named groups are tracked even when they appear only in narrative prose.
26. As a Director, I want `import-adventure` to extract and create Subplot files from the PDF, so that the adventure's narrative threads are documented from the start.
27. As a Director, I want `import-adventure` to extract and create Handout files with `revealed: false` from the PDF, so that player-facing artifacts are ready to reveal without manual setup.
28. As a Director, I want `import-adventure` to extract and create Notable Item files from the PDF, so that named items with narrative significance are tracked as Adventure-scoped Entities.
29. As a Director, I want `import-adventure` to extract and create Unowned Downtime Project files from the PDF, so that Director-designed projects are tracked even before I assign them to a Hero.
30. As a Director, I want all imported Entities to be Adventure-scoped by default, so that I can review them before Promoting any to Campaign scope.
31. As a Director, I want `import-adventure` to write obvious relationships between Entities (e.g., NPC faction membership, Encounter location) to frontmatter where the PDF states them explicitly, so that the imported content is partially connected from the start.
32. As a Director, I want `import-adventure` to write an Adventure Summary to `index.md` after all Entities are created, so that I can quickly understand the adventure's plot and cast without re-reading the PDF.
33. As a Director, I want `import-adventure` to fail with a clear installation message if the `pdf-to-md` skill is not installed, so that I know exactly how to resolve the dependency.
34. As a Director, I want the import to be a starting point for review, not a final product, so that I can correct extraction errors before using the adventure in play.

### Adventure Overview

35. As a Director, I want to invoke `adventure-overview` after reviewing imported Entities, so that a richer reference document is generated from curated content rather than raw extraction.
36. As a Director, I want `adventure-overview` to generate Mermaid flowcharts of Plot and Subplot connections, so that the narrative structure is visually scannable during prep.
37. As a Director, I want `adventure-overview` to generate tables of key Entities grouped by narrative thread, so that I can see at a glance which NPCs, Locations, and Encounters belong to each Subplot.
38. As a Director, I want the `adventure-overview` output written to `overview.md` in the Adventure root, so that it is versioned alongside the entity files.
39. As a Director, I want to direct `adventure-overview` with natural language focus instructions (e.g., "focus on the Villain's scheme"), so that the output emphasises what matters for my specific prep needs.

## Implementation Decisions

### Ten CLI Command Groups

Each Entity type gets its own Click command group following the noun-first pattern established in ADR 001 and ADR 004:

- `steel-golem npcs new`
- `steel-golem villains new`
- `steel-golem locations new`
- `steel-golem factions new`
- `steel-golem subplots new`
- `steel-golem handouts new`
- `steel-golem items new`
- `steel-golem downtime-projects new`
- `steel-golem encounters combat new`
- `steel-golem encounters negotiation new`
- `steel-golem encounters montage new`

All commands share three optional scope flags: `--adventure <slug>` (target a specific adventure), `--campaign` (Campaign scope). Default is the active adventure, read from `current_adventure` in the campaign `index.md`.

### Python Entity Creation Module

A new `steel_golem/entities.py` module encapsulates all entity creation logic. Each Entity type has a dedicated creation function with a stable, minimal interface. The CLI commands in `cli.py` are thin wrappers over these functions. This is the primary deep module — testable in isolation via `pytest` with a `tmp_path` fixture, following the pattern established in `test_scaffold.py`.

### Entity Schema Files

A `skills/entity-schemas/` directory contains one file per Entity type documenting the CLI contract: arguments, frontmatter fields (including relationship fields), and target directory. These files are shared between `create-entity` and `import-adventure` without duplication. `install.sh` symlinks `entity-schemas/` into `~/.steel-golem/entity-schemas/`.

### `create-entity` Skill Structure

```
skills/create-entity/
├── SKILL.md          ← entity type index + routing instructions
└── references/
    ├── npc.md        ← natural language interpretation guidance + pointer to Entity Schema
    ├── villain.md
    └── ...           ← one file per Entity type
```

SKILL.md classifies the Entity type from Director natural language, then reads only the relevant reference document. Reference documents layer skill-specific interpretation guidance on top of the shared Entity Schema.

### `import-adventure` Four-Step Orchestration (ADR 003)

1. **pdf-to-md sub-agent** — spawned with the PDF path; produces structured markdown files.
2. **Entity extraction sub-agent** — reads full pdf-to-md output; returns a structured entity list.
3. **Orchestrator CLI calls** — main agent iterates entity list, calls `steel-golem <type> new` for each Entity. No per-entity sub-agent.
4. **Finalization sub-agent** — reads entity list + pdf-to-md output; writes explicit relationships to entity frontmatter; writes Adventure Summary prose to `index.md` body.

### Relationship Fields in Entity Frontmatter

Entity Schemas include relationship fields for each type (e.g., NPCs get `faction:` and `location:`, Encounters get `location:` and `villain:`). These default to `null` at creation time. The finalization sub-agent populates them where the PDF explicitly states the relationship. These may be augmented by `adventure-overview`.

### `pdf-to-md` as Declared Runtime Dependency

`pdf-to-md` is not a submodule. `import-adventure`'s SKILL.md documents it as a required skill. `install.sh` checks for `~/.claude/skills/pdf-to-md/` and warns if absent. `import-adventure` fails gracefully with installation instructions if the skill is not found.

### Adventure Summary

Written to the `index.md` body by the finalization sub-agent. Contains narrative prose only — plot framing, key connective tissue, tone. No entity table (the Adventure directory is self-indexing). Distinct from the `adventure-overview` skill output (`overview.md`).

### Unowned Downtime Projects

Downtime Projects extracted from a PDF have `hero: null` in frontmatter (Unowned). The Director assigns ownership manually. See CONTEXT.md: Unowned.

### Adventure `index.md` — `status` Field Removed

Per the ADR 001 amendment, adventure `index.md` files no longer carry a `status` field. Active/inactive state is conveyed entirely by `current_adventure` in the campaign `index.md`. `scaffold.py`'s `create_adventure` function must be updated to omit this field.

### `adventure-overview` Skill

A separate skill, invoked by the Director after reviewing and enriching imported Entities. Reads all entity files in the Adventure directory plus `index.md`. Generates `overview.md` with Mermaid diagrams and grouped entity tables. Director can provide natural language focus instructions. Not part of the import flow.

### `install.sh` Updates

- Symlink `~/.steel-golem/entity-schemas/` → `$REPO/skills/entity-schemas/`
- Symlink `~/.claude/skills/create-entity/` → `$REPO/skills/create-entity/`
- Symlink `~/.claude/skills/import-adventure/` → `$REPO/skills/import-adventure/`
- Symlink `~/.claude/skills/adventure-overview/` → `$REPO/skills/adventure-overview/`
- Check for `~/.claude/skills/pdf-to-md/` and print a warning if absent

## Testing Decisions

Good tests verify observable filesystem behavior: does the correct file exist at the correct path with the correct frontmatter values? Tests should not inspect internal function logic or implementation details.

**Modules to test:**

- `steel_golem/entities.py` — one test per Entity type asserting: file exists at the correct path, frontmatter fields are correct, directory is created if absent, `FileExistsError` raised if file already exists, scope flags route to the correct directory. Follow the pattern in `tests/test_scaffold.py`.
- CLI command groups (via Click's `CliRunner`) — one integration test per command asserting argument parsing and filesystem side effects end-to-end.
- `scaffold.py` — add a test asserting `create_adventure` no longer writes a `status` field to `index.md`.

**Modules not suitable for deterministic tests:**

- `create-entity` skill — LLM-driven; verify manually with known Director inputs.
- `import-adventure` skill — LLM-driven; verify manually against a known adventure PDF fixture.
- `adventure-overview` skill — LLM-driven; verify manually against a known Adventure directory fixture.

## Out of Scope

- **Custom Monsters** — the bestiary/custom distinction requires knowing which creatures are in the steel-compendium, which is a separate lookup problem. Custom Monster creation is deferred.
- **Lore** — Campaign-scoped by default; a dedicated `create-lore` skill is deferred to a future PRD.
- **Adventure Overview** — the `adventure-overview` skill is defined here but its full implementation is a separate workstream; this PRD covers only its interface contract.
- **Promotion workflow** — moving Entities from Adventure scope to Campaign scope is a separate skill (`promote`), already identified in the top-level PRD.
- **Entity table in Adventure Summary** — the Adventure directory is self-indexing; a generated table would become stale.
- **Relationship inference** — only relationships explicitly stated in the PDF are written at import time. Inferred relationships are out of scope.
- **HTTP serving** — covered in the top-level PRD; no changes here.

## Further Notes

- All imported Entities are Adventure-scoped regardless of their default scope in CONTEXT.md (e.g., Notable Items default to Campaign-scope but land in the Adventure on import). The Director Promotes them manually. See ADR 004.
- The `pdf-to-md` skill is maintained at `pop-dog/ai-tools`. steel-golem does not pin a version; the Director is responsible for keeping it up to date.
- The `create-entity` skill is for human-initiated Entity creation only. `import-adventure` calls the CLI directly — it does not invoke `create-entity` as an intermediary.
- Monster rosters in Combat Encounter files are plain text lists (e.g., `- Goblin Sniper x3`) at import time. They are not resolved against the steel-compendium bestiary or linked to Custom Monster files.
- The finalization sub-agent writes only relationships that are **explicitly stated** in the PDF. Confident wrong relationships are harder to correct than absent ones.
