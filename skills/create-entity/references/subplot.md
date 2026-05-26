# create-entity: Subplot

## Natural language patterns

Directors commonly ask for a Subplot like this:

- "Add a subplot — the missing courier"
- "Create a side quest about the haunted manor"
- "I need a narrative thread for the spy in the party's midst"
- "Make a subplot for Sera's personal vendetta against the Warden"
- "Add a storyline about the stolen artifact"

A Subplot is an Adventure-scoped named narrative thread. It may contribute to a Campaign-scoped Plot, but it always lives within a single Adventure.

## Schema reference

Read `~/.steel-golem/entity-schemas/subplot.md` for the full CLI contract: arguments, frontmatter fields, and target directory.

## CLI command

```
steel-golem subplots new --name "<name>" [--description "<description>"] [--adventure <slug>]
```

## Scope guidance

Subplots are always Adventure-scoped. Do not use `--campaign` — it is not supported.

Default to the active adventure — omit the `--adventure` flag unless the Director names a specific adventure other than the active one.

If the Director says "campaign-wide" or "for the whole campaign", clarify that Subplots are Adventure-scoped only. If they want a Campaign-scoped narrative arc, that is a Plot — which is not yet a tracked Entity in steel-golem. Offer to create the Subplot within the active adventure instead.

## Error handling

| CLI output | Tell the Director |
|------------|-------------------|
| `Error: Config file not found...` | No campaign is active. Ask them to set one up with the `campaigns-new` skill first. |
| `Error: No active adventure...` | No active adventure is set. Ask them to create or set one first. |
| `Error: Subplot directory already exists...` | A Subplot with that name already exists. Ask if they want a different name. |
| `Error: --campaign flag is not supported...` | Subplots are Adventure-scoped only. Ask which adventure to write it to. |
| Any other non-zero exit | Show the error verbatim and ask how to proceed. |
