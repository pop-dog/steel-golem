# create-entity: Notable Item

## Natural language patterns

Directors commonly ask for a Notable Item like this:

- "Add a notable item — the Obsidian Key"
- "Create a magic item, the Sword of Veltharion"
- "I need to track a legendary artifact: the Crown of Ash"
- "Make the cursed amulet the Heroes found a tracked item"
- "Add the merchant's signet ring as a notable item — it's important to the plot"

A Notable Item is a named item with a history and current owner, significant enough to track independently. Notable Items are Campaign-scoped by default but the CLI writes to the active adventure until the Director promotes them.

## Schema reference

Read `~/.steel-golem/entity-schemas/notable-item.md` for the full CLI contract: arguments, frontmatter fields, and target directory.

## CLI command

```
steel-golem items new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope guidance

Default to the active adventure — omit all scope flags unless the Director specifies otherwise. Notable Items are Campaign-scoped by default conceptually, but the CLI writes to the active adventure when no flag is given. The Director can promote to campaign scope manually later.

Use `--campaign` when the Director explicitly says "campaign-wide", "for the whole campaign", or "this item persists across adventures".

Use `--adventure <slug>` when the Director names a specific adventure other than the active one.

## Error handling

| CLI output | Tell the Director |
|------------|-------------------|
| `Error: Config file not found...` | No campaign is active. Ask them to set one up with the `campaigns-new` skill first. |
| `Error: No active adventure...` | No active adventure is set. Ask them to create or set one first. |
| `Error: Item directory already exists...` | A Notable Item with that name already exists. Ask if they want a different name. |
| Any other non-zero exit | Show the error verbatim and ask how to proceed. |
