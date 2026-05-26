# ADR 003: import-adventure Orchestration Model

## Status

Accepted

## Context

`import-adventure` is a skill that ingests a published Draw Steel adventure PDF and populates a new Adventure with extracted Entities (NPCs, Villains, Locations, Encounters, Factions, Subplots, Handouts, Notable Items, Downtime Projects, Negotiations, Montages). It delegates PDF extraction to an external `pdf-to-md` skill maintained in a separate repository.

The orchestration model must handle: (1) a large PDF corpus that exceeds practical single-agent context limits, (2) structured entity creation via CLI commands, (3) relationship establishment between entities, and (4) Adventure Summary generation. Several competing models were considered.

## Decisions

### 1. Hybrid sub-agent model: sub-agents for reasoning-heavy steps, direct CLI calls for entity creation

`import-adventure` orchestrates four steps:

1. **pdf-to-md sub-agent** — spawned with the PDF path; returns a directory of structured markdown files, one per page/chapter.
2. **Entity extraction sub-agent** — spawned with the pdf-to-md output; reads the full markdown corpus and returns a structured entity list (type, name, fields) for all identified Entities.
3. **Orchestrator CLI calls** — the main `import-adventure` agent iterates the entity list and calls `steel-golem <type> new` directly for each Entity. No sub-agent per entity.
4. **Finalization sub-agent** — spawned after all Entities are created; reads the entity list and pdf-to-md output together; establishes low-hanging-fruit relationships in entity frontmatter; writes the Adventure Summary to `index.md`.

Sub-agents are used only where LLM reasoning over large content is required (steps 1, 2, 4). Entity creation (step 3) is structured data → CLI command — no reasoning needed, so the orchestrator handles it directly.

### 2. One sub-agent per reasoning step, not one sub-agent per entity

A per-entity sub-agent model (one spawn per NPC, per Location, etc.) was considered and rejected. Each sub-agent spawn has a cold context load; for a large adventure with 50+ entities this is prohibitively slow. The extraction sub-agent returns a complete structured list in one pass; the orchestrator iterates it without further spawns.

### 3. Finalization sub-agent is responsible for both relationship establishment and Adventure Summary

The finalization sub-agent runs after all entity files exist on disk, meaning all slugs are available for cross-referencing. This is the earliest point at which relationships can be written to entity frontmatter without sequencing errors. Combining relationship establishment and Adventure Summary generation into one sub-agent avoids a fifth step and re-use of the same source material (entity list + pdf-to-md output).

Relationships written at this stage are limited to those **explicitly stated** in the PDF — not inferred. A confidently wrong relationship is harder to correct than a missing one. Relationships may be augmented later by the `adventure-overview` skill.

### 4. Adventure Summary is prose only; no entity table

The Adventure Summary written to `index.md` body contains narrative prose describing the adventure's plot and key connective tissue. It does not include a table of imported Entities — the Adventure directory is self-indexing (`ls npcs/`, `ls locations/`, etc.). A table would duplicate the filesystem and become stale as Entities are added, removed, or Promoted.

### 5. pdf-to-md is a declared runtime dependency, not a submodule

`pdf-to-md` is maintained in a separate repository (`pop-dog/ai-tools`) with its own evolution cycle. Importing it as a submodule would couple steel-golem to a specific version and conflate static reference data (steel-compendium) with a live LLM workflow skill.

Instead, `pdf-to-md` is documented as a required skill dependency in `import-adventure`'s SKILL.md. `install.sh` checks for its presence at `~/.claude/skills/pdf-to-md/` and warns if absent. `import-adventure` fails gracefully with installation instructions if the skill is not found at invocation time.

### 6. Entity scope defaults to active adventure; --adventure and --campaign override

Entity creation commands (`steel-golem npcs new`, etc.) default to the active adventure, read from `current_adventure` in the campaign `index.md`. Two optional flags override this:

- `--adventure <slug>` — targets a specific adventure (for prepping ahead)
- `--campaign` — writes directly to Campaign scope

This matches the existing pattern where the active adventure is the implicit context for all adventure-scoped operations.

## Alternatives Considered

**Single-agent import.** One agent reads the PDF markdown and creates all entities. Rejected: a full adventure module produces enough markdown to flood a single agent's context window before entity creation begins.

**Per-entity sub-agents.** One sub-agent spawn per entity, called sequentially. Rejected: cold context load per spawn makes this prohibitively slow for large adventures (50+ entities). The extraction sub-agent returns a complete structured list in one pass.

**pdf-to-md as submodule.** Pull `pdf-to-md` into the steel-golem repo as a submodule, symlinked by `install.sh`. Rejected: `pdf-to-md` is a live skill with its own evolution cycle; treating it like static reference data (steel-compendium) couples the repos unnecessarily and complicates upgrades.

**Entity table in Adventure Summary.** Include a Markdown table of all imported Entities in `index.md`. Rejected: duplicates the filesystem, becomes stale as Entities are added or Promoted, and the Adventure directory structure is already self-indexing.
