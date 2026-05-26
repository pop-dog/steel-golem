# create-entity: Location

## Natural language patterns

Directors commonly ask for a Location like this:

- "Add a location — the Sunken Archive"
- "Create the merchant district of Veltharion"
- "I need a dungeon location, the Obsidian Vault"
- "Make the Harbormaster's office a location"
- "Add the city of Keth to the campaign"

A Location is any named place at any scale — a room, a building, a district, a city, or a region.

## Schema reference

Read `~/.steel-golem/entity-schemas/location.md` for the full CLI contract: arguments, frontmatter fields, and target directory.

## CLI command

```
steel-golem locations new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope guidance

Default to the active adventure — omit all scope flags unless the Director specifies otherwise.

Use `--campaign` when the Director says "campaign-wide", "for the whole campaign", "this city recurs across adventures", or similar. A campaign-scoped Location is referenceable from any Adventure.

Use `--adventure <slug>` when the Director names a specific adventure other than the active one.

## Error handling

| CLI output | Tell the Director |
|------------|-------------------|
| `Error: Config file not found...` | No campaign is active. Ask them to set one up with the `campaigns-new` skill first. |
| `Error: No active adventure...` | No active adventure is set. Ask them to create or set one first. |
| `Error: Location directory already exists...` | A Location with that name already exists. Ask if they want a different name. |
| Any other non-zero exit | Show the error verbatim and ask how to proceed. |
