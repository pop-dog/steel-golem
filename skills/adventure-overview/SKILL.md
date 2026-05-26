# adventure-overview

A collaborative session that builds a shared understanding of an Adventure's structure. The agent reads all entity files, walks through each Subplot as a card, surfaces Loose Entities, proposes new Subplots where warranted, agrees on the document shape, then generates `overview.md`.

**Corrections are batched — no entity files are modified until the Director confirms.**

The Director may say **commit** at any point to skip to the corrections summary. The agent always presents the summary and waits for **confirm** before writing anything to disk.

---

## Phase 0 — Read everything

Read `~/.steel-golem/config.yaml` for `campaign_path`. Read `<campaign_path>/index.md` for `current_adventure`.

| Condition | Action |
|-----------|--------|
| Config absent | Tell the Director no campaign is active; suggest `campaigns-new`. Stop. |
| `current_adventure` is null | Tell the Director no adventure is active; suggest `adventures-set`. Stop. |
| Adventure root missing | Suggest `steel-golem adventures list` to verify slug. Stop. |

The Adventure root is: `<campaign_path>/adventures/<current_adventure>/`

Read `<adventure_root>/index.md` — the frontmatter holds `name` and `slug`; the body is the Adventure Summary.

Read every `.md` file in these directories (skip absent or empty directories silently):

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

Parse frontmatter for each file. Build:

- A **slug-to-name map** for all entities.
- A **Subplot membership map**: for each Subplot, collect entities whose descriptions, relationship fields, or the Adventure Summary prose associate them with that thread. Use narrative judgment where frontmatter is sparse.
- A **villain-to-encounters map**: Combat Encounters with a non-null `villain` field.
- A **Loose list**: entities not associated with any Subplot after the membership map is built.
- The **Main Thread**: the Subplot (or chain of Subplots) that defines the central conflict — infer from entity density, Villain connections, and Adventure Summary. Mark it as your best guess; the Director will confirm or correct.

---

## Phase 1 — Orientation summary

Open the session with a brief inventory. Do not begin Subplot cards yet.

> **Adventure: <Adventure Name>**
>
> Here's what I found:
> - **Subplots:** <count> — Main Thread candidate: *<Subplot name>*
> - **Entities:** <total count> across <list of non-empty types>
> - **Loose entities:** <count> (not yet assigned to any Subplot)
>
> I'll walk through each Subplot as a card, then cover Loose entities, then agree on the document shape before generating the overview. You can say **commit** at any time to skip to the corrections summary — I'll always confirm with you before writing anything.
>
> Ready? I'll start with the Main Thread.

---

## Phase 2 — Subplot cards

Present one card per Subplot, starting with the Main Thread, then secondary Subplots ordered by their connection to the Main Thread (most connected first).

For each Subplot, present:

> ---
> **Subplot: <Name>** *(Main Thread)* ← only on the first card if applicable
>
> **Arc:** <one-sentence description of the Subplot's narrative arc, drawn from the Subplot's description field and Adventure Summary>
>
> **Connects to:** <parent Plot name, or "standalone"> 
>
> **Entities in this thread:**
> | Type | Name | Role / Notes |
> |------|------|--------------|
> | Villain | Warden Groth | Drives the central conflict |
> | NPC | Mira | Unwilling informant |
> | Location | Cell Block C | Primary encounter site |
> | Combat Encounter | The Handoff | Climax of this thread |
>
> *(Role / Notes drawn from entity `description` fields, truncated to ~80 characters)*
>
> **My read:** <one sentence synthesising what this Subplot is about and how it connects to the adventure as a whole>
>
> Does this look right? Anything to add, remove, correct, or rename?

Wait for the Director's response. Apply any corrections to the **corrections batch** — do not write to disk yet. Reference the corrected version in subsequent cards.

If the Director says the Main Thread candidate is wrong, update your internal Main Thread designation before presenting remaining cards.

---

## Phase 3 — Loose entities card

After all Subplot cards, present the Loose entities.

First, look for **clusters**: groups of 3 or more Loose entities whose descriptions, locations, or relationship fields suggest they belong to a common narrative thread the import may have missed.

> ---
> **Loose Entities** — <count> entities not yet threaded into a Subplot
>
> *(If clusters found):*
> I noticed a possible undiscovered thread:
>
> **Possible Subplot: <proposed name>**
> These entities seem to belong together — <one sentence explaining the pattern you observed>:
> - <Entity type>: <Name> — <brief note>
> - <Entity type>: <Name> — <brief note>
>
> Want to create this Subplot and thread them in?
>
> *(Remaining Loose entities not in any cluster):*
> | Type | Name | Notes |
> |------|------|-------|
> | NPC | The Blacksmith | Description mentions the vault but no Subplot |
>
> For each: do you want to thread it into an existing Subplot, leave it Loose, or note it for removal?

If the Director approves a new Subplot, add it to the corrections batch (new file to create: `subplots/<slug>.md`) and update entity associations accordingly.

If there are no Loose entities, skip this phase and say so briefly.

---

## Phase 4 — Document planning

Propose the Adventure Overview sections based on what the adventure actually contains. Only propose sections with content.

> ---
> **Adventure Overview — proposed sections**
>
> Based on our walkthrough, here's what I'd include:
>
> | # | Section | Why |
> |---|---------|-----|
> | 1 | Adventure Flowchart | <count> Subplots, <count> Plot connections |
> | 2 | Subplot Summaries | <count> Subplots including Main Thread |
> | 3 | Faction Table | <count> Factions with clear roles |
> | 4 | NPC Spotlight | <names> appear across multiple Subplots |
> | 5 | Notable Items | <count> items, <name> flagged as plot-critical |
> | 6 | Encounter Map | <count> Encounters sequenced by Subplot |
> | 7 | Handouts | <count> handouts (<count> revealed) |
> | 8 | Loose Entities | <count> remaining after threading |
>
> Anything to add, remove, or reorder?

Omit any row from the table where there is no content. The default sections to consider are:

- **Adventure Flowchart** — Mermaid `flowchart TD`: Subplots → parent Plots, Villain → Encounters. Include only when relationships exist.
- **Subplot Summaries** — one subsection per Subplot with entity list and arc description.
- **Faction Table** — Name, Description, Role in the adventure.
- **NPC Spotlight** — NPCs appearing in 2+ Subplots, or flagged as critical by the Director.
- **Notable Items** — Name, Description, Owner, plot-critical flag.
- **Encounter Map** — Encounters grouped by Subplot with Villain and Location references.
- **Handouts** — Name, Content summary, Revealed status.
- **Loose Entities** — Entities not threaded into any Subplot after the session.

Wait for the Director's confirmation before proceeding to commit.

---

## Phase 5 — Commit

When the Director says **commit** — whether at the end of Phase 4 or at any earlier point — present the corrections summary. Never write to disk without it. Writing only happens after the Director says **confirm**.

> ---
> **Ready to commit.** Here's what I'll apply:
>
> **Entity file updates (<count>):**
> - `npcs/mira.md` → `faction: ironveil-cult`
> - `subplots/the-smuggling-ring.md` → new file
> - `encounters/combat/the-handoff.md` → `villain: warden-groth`
> *(etc.)*
>
> **No changes:** <count> entities confirmed as-is.
>
> Type **confirm** to apply all changes and generate `overview.md`, or tell me what to adjust.

On **confirm**:

1. Write all batched entity file corrections (update frontmatter using `python-frontmatter` conventions — preserve existing fields, update only changed ones).
2. Create any new Subplot files approved during Phase 3.
3. Generate `<adventure_root>/overview.md` using the agreed section list. Overwrite if it exists.
4. Report:

> **Done.**
> - <count> entity files updated
> - <count> new files created
> - `overview.md` written: <count> sections, <count> Subplots charted
>
> Re-run `adventure-overview` after further enrichment to refresh the document.

---

## Generating overview.md

Use this structure, including only sections agreed in Phase 4:

```
# Overview: <Adventure Name>

## Adventure Flowchart

```mermaid
flowchart TD
  ...
```

## Subplot Summaries

### <Main Thread Name> *(Main Thread)*
<arc description>
**Connects to:** <Plot or "standalone">
| Type | Name | Notes |
...

### <Subplot Name>
...

## Faction Table

| Name | Description | Role |
...

## NPC Spotlight

| Name | Subplots | Notes |
...

## Notable Items

| Name | Description | Owner | Plot-Critical |
...

## Encounter Map

| Name | Type | Subplot | Villain | Location |
...

## Handouts

| Name | Content | Revealed |
...

## Loose Entities

| Type | Name | Notes |
...
```

**Flowchart rules:**
- Nodes: each Subplot, each Villain, each Campaign Plot referenced by a Subplot.
- Edges: Subplot → Plot (`contributes to`); Villain → Combat Encounter (`leads`).
- Omit nodes and edges where relationships are null.
- Use display names (not slugs) for all labels.
- If no relationships exist to chart, omit the section with a note: *No relationships found — enrich entity frontmatter and re-run.*

**NPC Spotlight:** include NPCs appearing in 2 or more Subplots, or any NPC the Director flagged during the session.

**Notable Items:** flag an item as plot-critical if the Director confirmed it during the session or if its description references the Main Thread conflict.
