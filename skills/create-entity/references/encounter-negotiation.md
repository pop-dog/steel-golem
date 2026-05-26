# create-entity: Negotiation

## Natural language patterns

Directors commonly ask for a Negotiation like this:

- "Create a negotiation — bargaining with the Harbormaster"
- "Add a social encounter with the city council"
- "I need a negotiation scene for convincing the rebel leader"
- "Make a negotiation: the Heroes try to reason with the dragon"
- "Add a structured conversation with Lord Varek"

A Negotiation is a structured social encounter resolved through Draw Steel's Negotiation mechanics — the NPC has Patience, Interest, motivations, and pitfalls.

## Schema reference

Read `~/.steel-golem/entity-schemas/encounter-negotiation.md` for the full CLI contract: arguments, frontmatter fields, and target directory.

## CLI command

```
steel-golem encounters negotiation new --name "<name>" [--description "<description>"] [--adventure <slug>]
```

## Scope guidance

Negotiations are always Adventure-scoped. Do not use `--campaign` — it is not supported.

Default to the active adventure — omit the `--adventure` flag unless the Director names a specific adventure other than the active one.

If the Director says "campaign-wide" or "for the whole campaign", clarify that Negotiations are Adventure-scoped only and ask which adventure to write it to.

## Error handling

| CLI output | Tell the Director |
|------------|-------------------|
| `Error: Config file not found...` | No campaign is active. Ask them to set one up with the `campaigns-new` skill first. |
| `Error: No active adventure...` | No active adventure is set. Ask them to create or set one first. |
| `Error: Negotiation directory already exists...` | A Negotiation with that name already exists. Ask if they want a different name. |
| Any other non-zero exit | Show the error verbatim and ask how to proceed. |
