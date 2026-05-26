# create-entity: NPC

## Natural language patterns

Directors commonly ask for an NPC like this:

- "Add an innkeeper named Mira"
- "Create a merchant in the dockside market"
- "Make an NPC — the city guard captain, name him Aldric"
- "I need a quest-giver for this adventure, a retired soldier"
- "Add Sera the blacksmith to the campaign"

Any named, non-Villain character controlled by the Director is an NPC.

## Schema reference

Read `~/.steel-golem/entity-schemas/npc.md` for the full CLI contract: arguments, frontmatter fields, and target directory.

## CLI command

```
steel-golem npcs new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope guidance

Default to the active adventure — omit all scope flags unless the Director specifies otherwise.

Use `--campaign` when the Director says "campaign-wide", "for the whole campaign", "across all adventures", or similar.

Use `--adventure <slug>` when the Director names a specific adventure other than the active one.

## Error handling

| CLI output | Tell the Director |
|------------|-------------------|
| `Error: Config file not found...` | No campaign is active. Ask them to set one up with the `campaigns-new` skill first. |
| `Error: No active adventure...` | No active adventure is set. Ask them to create or set one first. |
| `Error: NPC directory already exists...` | An NPC with that name already exists. Ask if they want a different name. |
| Any other non-zero exit | Show the error verbatim and ask how to proceed. |
