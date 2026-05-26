# create-entity: Faction

## Natural language patterns

Directors commonly ask for a Faction like this:

- "Create a faction — the Iron Covenant"
- "Add the thieves' guild as a faction"
- "I need an organization, the Crimson Hand cult"
- "Make the city guard a faction for this adventure"
- "Add the merchant consortium as a campaign-wide faction"

A Faction is a named group of characters sharing goals and interests. NPCs and Villains reference Factions — the Faction itself carries no member list.

## Schema reference

Read `~/.steel-golem/entity-schemas/faction.md` for the full CLI contract: arguments, frontmatter fields, and target directory.

## CLI command

```
steel-golem factions new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope guidance

Default to the active adventure — omit all scope flags unless the Director specifies otherwise.

Use `--campaign` when the Director says "campaign-wide", "for the whole campaign", "this faction appears across adventures", or similar.

Use `--adventure <slug>` when the Director names a specific adventure other than the active one.

## Error handling

| CLI output | Tell the Director |
|------------|-------------------|
| `Error: Config file not found...` | No campaign is active. Ask them to set one up with the `campaigns-new` skill first. |
| `Error: No active adventure...` | No active adventure is set. Ask them to create or set one first. |
| `Error: Faction directory already exists...` | A Faction with that name already exists. Ask if they want a different name. |
| Any other non-zero exit | Show the error verbatim and ask how to proceed. |
