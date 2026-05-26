# create-entity

Single entry point for Directors to create any Entity type by describing what they want in natural language.

## Entity types

| Type | Description |
|------|-------------|
| NPC | Named character controlled by the Director who is not a Villain |
| Villain | Antagonist controlled by the Director |
| Location | Named place at any scale |
| Faction | Named group of characters sharing goals and interests |
| Subplot | Adventure-scoped narrative thread |
| Handout | Player-facing artifact revealed to Heroes during play |
| Notable Item | Named item with history and a current owner |
| Downtime Project | Director-designed goal for a Hero pursued across Respites |
| Combat Encounter | Encounter resolved through tactical combat |
| Negotiation | Encounter resolved through structured social mechanics |
| Montage | Encounter resolved through coordinated skill tests |

## How to create an Entity

### Step 1 — Classify the Entity type

Determine which of the 11 types above the Director is asking for based on their natural language description.

### Step 2 — Read the reference doc

Read only the reference doc for that type from `~/.claude/skills/create-entity/references/<type>.md`. Do not read reference docs for other types.

### Step 3 — Run the CLI command

Follow the instructions in the reference doc: interpret scope, assemble arguments, and run the exact CLI command shown.

### Step 4 — Confirm to the Director

Report what was created and where.
