# create-entity: Montage

## Natural language patterns

Directors commonly ask for a Montage like this:

- "Add a montage — crossing the Storm Peaks"
- "Create a skill challenge for the Heroes to escape the flooding dungeon"
- "I need a montage encounter: the chase through the market"
- "Make a group test scene for infiltrating the gala"
- "Add a montage: the Heroes race to reach the lighthouse before the storm"

A Montage is resolved through a series of coordinated skill tests toward a shared goal. It uses Draw Steel's Montage Test mechanics.

## Schema reference

Read `~/.steel-golem/entity-schemas/encounter-montage.md` for the full CLI contract: arguments, frontmatter fields, and target directory.

## CLI command

```
steel-golem encounters montage new --name "<name>" [--description "<description>"] [--adventure <slug>]
```

## Scope guidance

Montages are always Adventure-scoped. Do not use `--campaign` — it is not supported.

Default to the active adventure — omit the `--adventure` flag unless the Director names a specific adventure other than the active one.

If the Director says "campaign-wide" or "for the whole campaign", clarify that Montages are Adventure-scoped only and ask which adventure to write it to.

## Error handling

| CLI output | Tell the Director |
|------------|-------------------|
| `Error: Config file not found...` | No campaign is active. Ask them to set one up with the `campaigns-new` skill first. |
| `Error: No active adventure...` | No active adventure is set. Ask them to create or set one first. |
| `Error: Montage directory already exists...` | A Montage with that name already exists. Ask if they want a different name. |
| Any other non-zero exit | Show the error verbatim and ask how to proceed. |
