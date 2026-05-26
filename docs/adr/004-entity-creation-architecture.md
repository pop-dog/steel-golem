# ADR 004: Entity Creation Architecture

## Status

Accepted

## Context

Steel Golem needs to support creation of ten Entity types (NPC, Villain, Location, Combat Encounter, Negotiation, Montage, Faction, Subplot, Handout, Notable Item, Downtime Project) both from the Director via natural language and programmatically from `import-adventure`. Each Entity type has its own CLI arguments, frontmatter schema, target directory, and scope rules. Two skills need access to this information: `create-entity` (human-initiated) and `import-adventure` (programmatic).

## Decisions

### 1. Ten CLI command groups, one per Entity type

Each Entity type gets its own Click command group following the noun-first pattern established in ADR 001:

```
steel-golem npcs new --name "Mira" --description "..."
steel-golem villains new --name "The Warden" --scope adventure
steel-golem encounters combat new --name "Throne Room Battle"
```

A unified `steel-golem entities new --type npc` command was considered and rejected — it is less intuitive, harder to tab-complete, and obscures the noun-first pattern established across the CLI.

### 2. Single `create-entity` skill with per-type reference documents

A single `create-entity` SKILL.md routes to per-type reference documents rather than encoding all ten schemas in one flat file. The structure:

```
skills/create-entity/
├── SKILL.md              ← short: what this skill does + entity type index
└── references/
    ├── npc.md
    ├── villain.md
    ├── location.md
    └── ...               ← one file per Entity type
```

SKILL.md classifies the Entity type from natural language, then reads only the relevant reference document. This prevents cross-contamination (hallucinating fields from one type onto another) while keeping a single entry point for human-initiated entity creation.

Separate skills per Entity type were considered and rejected — ten skills with redundant structure (same routing logic, same error handling patterns) is skill bloat without benefit. The classification step is trivial for an LLM.

### 3. Entity Schemas in a shared `skills/entity-schemas/` directory

The CLI contract for each Entity type (arguments, frontmatter fields, target directory, relationship fields) lives in `skills/entity-schemas/`, separate from skill-specific content:

```
skills/entity-schemas/
├── npc.md
├── villain.md
├── location.md
└── ...
```

Both `create-entity/references/` and `import-adventure`'s extraction instructions reference these files. `install.sh` symlinks `entity-schemas/` into `~/.steel-golem/entity-schemas/`.

Symlinking the full `create-entity/references/` directory into `import-adventure/` was considered and rejected. The two skills need the same CLI contract but different interpretation layers — `create-entity` needs natural language guidance; `import-adventure` needs extraction hints. Sharing the full reference files would cause one skill's edits to pollute the other.

### 4. `import-adventure` calls the CLI directly, bypassing `create-entity`

`import-adventure` calls `steel-golem <type> new` commands directly from the orchestrator. It does not invoke the `create-entity` skill as an intermediary. The `create-entity` skill is optimised for natural language input from the Director; `import-adventure` already has structured data from the entity extraction sub-agent and needs no interpretation layer.

Both paths use the same CLI commands and Entity Schemas — the skill layer is skipped, not the contract.

### 5. Entity scope: active adventure by default, with --adventure and --campaign overrides

See ADR 003 decision 6.

### 6. Entities imported from a PDF are Adventure-scoped by default

All Entities created by `import-adventure` are written to the active Adventure directory regardless of their default scope in CONTEXT.md (e.g., Notable Items are Campaign-scoped by default but land in the Adventure on import). The Director Promotes Entities to Campaign scope manually after review. This keeps `import-adventure` contained within the Adventure it creates.

### 7. Downtime Projects are created Unowned when no Hero is known

A Downtime Project extracted from a PDF has no Hero assigned (the Heroes are Campaign-scoped Entities that exist outside the PDF). The `hero` frontmatter field is set to `null` (Unowned) at import time. The Director assigns ownership manually. See CONTEXT.md: Unowned.

## Alternatives Considered

**Separate skill per Entity type.** Ten skills, each responsible for one type. Rejected: skill bloat — the routing logic and error handling patterns are identical across types. A single `create-entity` skill with per-type reference documents achieves the same isolation without the duplication.

**Unified `steel-golem entities new --type npc` CLI command.** One command handles all Entity types with a `--type` flag. Rejected: less intuitive than noun-first groups, harder to tab-complete, and inconsistent with the established CLI pattern.

**Symlinked reference files between skills.** Share full per-type reference documents between `create-entity` and `import-adventure` via symlinks. Rejected: the two skills need different interpretation layers on top of the shared CLI contract — edits for one skill would pollute the other.
