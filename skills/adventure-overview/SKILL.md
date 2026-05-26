# adventure-overview

Generates a rich Director-facing reference document (`overview.md`) in the Adventure root. Invoke this skill **after** reviewing and enriching the imported Entities — it reads curated content, not raw extraction.

**This skill does NOT modify any entity files.** It reads all entity files and writes only to `overview.md`.

---

## Before you begin

Confirm the Director's intent:

- If they have provided focus instructions (e.g., "focus on the Villain's scheme", "emphasize the political subplots"), note them — they shape the output.
- If `overview.md` already exists, tell the Director it will be overwritten and proceed.

---

## Step 1 — Locate the active Adventure

Read `~/.steel-golem/config.yaml` to get `campaign_path`.

Read `<campaign_path>/index.md` and extract the `current_adventure` frontmatter field. This is the slug of the active Adventure.

The Adventure root is: `<campaign_path>/adventures/<current_adventure>/`

**Error handling:**

| Condition | Action |
|-----------|--------|
| `~/.steel-golem/config.yaml` does not exist | Tell the Director no campaign is active and suggest running the `campaigns-new` skill first. Stop. |
| `current_adventure` is `null` or absent | Tell the Director no adventure is active and suggest running the `adventures-set` skill. Stop. |
| The Adventure root directory does not exist | Tell the Director the slug points to a missing directory; suggest running `steel-golem adventures list` to verify. Stop. |

---

## Step 2 — Read the Adventure Summary

Read `<adventure_root>/index.md`. The YAML frontmatter contains `name` and `slug`. The body (after the closing `---`) is the Adventure Summary prose written during import.

Note the adventure name for use in the output header.

---

## Step 3 — Read all Entity files

Read every `.md` file in the following directories under `<adventure_root>/`, if the directory exists. Directories that are absent or empty are silently skipped.

| Directory | Entity type |
|-----------|-------------|
| `npcs/` | NPC |
| `villains/` | Villain |
| `locations/` | Location |
| `factions/` | Faction |
| `subplots/` | Subplot |
| `handouts/` | Handout |
| `items/` | Notable Item |
| `downtime-projects/` | Downtime Project |
| `encounters/combat/` | Combat Encounter |
| `encounters/negotiations/` | Negotiation |
| `encounters/montages/` | Montage |

For each file, parse the YAML frontmatter. Collect these fields where present:

- `name`, `slug`, `description`
- Relationship fields: `faction`, `location`, `villain`, `npc`, `plot`, `owner`, `hero`
- Type-specific fields: `revealed` (Handouts), `project_goal`, `project_points` (Downtime Projects)

Ignore `scope` — it is not used in the output.

**Relationship rule:** If a relationship field is `null`, omit it from diagrams and tables entirely. Do not show it as "unknown" or "none".

---

## Step 4 — Build the relationship index

Before generating output, build an in-memory index for cross-referencing:

- A slug-to-name map for all entities (so diagrams use display names, not slugs).
- A subplot-to-entities map: for each Subplot, collect NPCs, Villains, Locations, Encounters, Factions, and Handouts that reference it — **note:** entity files do not carry a `subplot` field directly. Use the Subplot's own description and the narrative prose from entity descriptions to group entities. Where explicit subplot membership cannot be determined from frontmatter alone, use narrative judgment based on the Adventure Summary and entity descriptions.
- A villain-to-encounters map: Combat Encounters that reference a Villain via the `villain` field.
- A subplot-to-plot map: Subplots that carry a non-null `plot` field.

---

## Step 5 — Generate `overview.md`

Write `<adventure_root>/overview.md`. Overwrite if it already exists.

The file uses Markdown with Mermaid code blocks. It has no YAML frontmatter.

### Structure

```
# Overview: <Adventure Name>

## Briefing

<prose>

## Narrative Structure

```mermaid
<flowchart>
```

## Subplots and Threads

<one subsection per Subplot>

## Entity Reference

### NPCs
<table>

### Villains
<table>

### Locations
<table>

### Factions
<table>

### Encounters
<table>

### Handouts
<table>

### Notable Items
<table>

### Downtime Projects
<table>

## Director Focus

<only if the Director provided focus instructions>
```

---

### Briefing section

Write 3–5 paragraphs of narrative prose that **expand on the Adventure Summary** with post-curation knowledge. This is not a copy of the Adventure Summary — it integrates the enriched entity relationships the Director has set during curation.

Cover:
- The adventure's central conflict and what is at stake
- The key Villains and their motivations (drawn from Villain descriptions)
- The major Factions and their roles
- The Subplots and how they connect to the main conflict
- The shape of the adventure arc (how the Encounters sequence, if discernible from descriptions)

Write for the Director as a prep aid, not a player synopsis.

---

### Narrative Structure flowchart

Generate a single Mermaid `flowchart TD` (top-down) diagram showing the high-level narrative structure.

**Nodes to include:**
- Each Subplot (include parent Plot name in the label if `plot` is non-null, e.g., `"The Missing Courier (→ Iron Tide)"`)
- Each Villain
- Each Combat Encounter that references a Villain

**Edges to include:**
- Subplot → parent Plot node (if `plot` is non-null): label `contributes to`
- Villain → Combat Encounter (via encounter's `villain` field): label `leads`
- Subplot → Villain (include only if the Villain's description explicitly mentions driving or anchoring the Subplot — use narrative judgment conservatively)

**Rules:**
- Omit any node whose relationships are all null (isolated nodes add no value)
- Omit any edge where either endpoint has a null relationship field
- Use display names, not slugs, for all node labels
- If no relationships exist across any entity, omit this section entirely with a note: `_No relationships found — enrich entity frontmatter and re-run._`

If Negotiations and Montages have a `location` that is also referenced by a major Subplot, add them as leaf nodes connected to that Location.

---

### Subplots and Threads section

One `###` subsection per Subplot. Each subsection contains:

1. The Subplot's description (from frontmatter).
2. If the Subplot has a parent `plot`, a line: `Contributes to Plot: <plot name>`.
3. A **Entities in this thread** table with columns `Type | Name | Notes`, listing NPCs, Villains, Locations, Factions, and Encounters whose descriptions mention this Subplot or who are grouped here by narrative judgment. Notes is the entity's `description` field, truncated to ~100 characters if long.

If no entities can be associated with a Subplot, write: `_No entities explicitly linked to this Subplot._`

If there are no Subplots at all, write a single paragraph noting that no Subplots were found and suggest creating them with `create-entity`.

---

### Entity Reference tables

One `###` subsection per entity type, in the order listed in the Structure above. Omit any subsection where no entities of that type exist.

**Standard columns for most types:**

| Name | Description | Relationships |

The Relationships cell lists only non-null relationship fields, formatted as `faction: Iron Covenant`, `location: Sunken Archive`, etc. using display names resolved from the slug-to-name index. If all relationships are null, the cell is empty.

**Type-specific columns:**

| Type | Extra columns |
|------|---------------|
| Handout | Add a `Revealed` column (`Yes` / `No`) |
| Downtime Project | Add `Owner` (display name or `Unowned`) and `Progress` (`<project_points> / <project_goal>` or `0 / —` if `project_goal` is null) |

---

### Director Focus section

Include this section **only** if the Director provided focus instructions at invocation.

Write a `## Director Focus` header, restate the focus instructions in a blockquote, then generate a focused subsection:

- If the focus is on a specific Villain, write a "Villain's Scheme" subsection: list every Combat Encounter, Location, Faction, and NPC connected to that Villain.
- If the focus is on Subplots, expand the per-Subplot entity tables with full descriptions (not truncated).
- If the focus is on a Faction, write a "Faction Spotlight" subsection: list the Faction's description, all NPCs and Villains with that faction slug, and any Encounters at Locations that appear in those NPCs' location fields.
- For any other focus instruction, apply judgment to produce a concise focused section relevant to the instruction.

---

## Step 6 — Report to the Director

After writing `overview.md`, report:

> Overview written to `<adventure_root>/overview.md`
>
> - Briefing: <X> paragraphs
> - Subplots charted: <count> (or "none found")
> - Entities indexed: <total count across all types>
> - Mermaid diagram: included / omitted (reason if omitted)
>
> Re-run at any time after enriching entity frontmatter to refresh the overview.

If the Director provided focus instructions, add:

> Focus section included: "<their instruction>"
