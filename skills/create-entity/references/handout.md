# create-entity: Handout

## Natural language patterns

Directors commonly ask for a Handout like this:

- "Create a handout — the Warden's letter"
- "Add a player-facing document, the ancient map"
- "I need a handout for the cult's manifesto"
- "Make a prop the Heroes find in the vault: a torn journal page"
- "Add a handout — the merchant's ledger that implicates Lord Varek"

A Handout is a player-facing artifact revealed to Heroes during play. It carries a `revealed` status — always written as `revealed: false` at creation, never null. The Director flips it to `true` manually when revealing the handout to Heroes.

## Schema reference

Read `~/.steel-golem/entity-schemas/handout.md` for the full CLI contract: arguments, frontmatter fields, and target directory.

## CLI command

```
steel-golem handouts new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope guidance

Default to the active adventure — omit all scope flags unless the Director specifies otherwise. Handouts are Adventure-scoped by default.

Use `--campaign` when the Director says "campaign-wide", "for the whole campaign", or the handout is a persistent prop referenced across multiple Adventures.

Use `--adventure <slug>` when the Director names a specific adventure other than the active one.

## Error handling

| CLI output | Tell the Director |
|------------|-------------------|
| `Error: Config file not found...` | No campaign is active. Ask them to set one up with the `campaigns-new` skill first. |
| `Error: No active adventure...` | No active adventure is set. Ask them to create or set one first. |
| `Error: Handout directory already exists...` | A Handout with that name already exists. Ask if they want a different name. |
| Any other non-zero exit | Show the error verbatim and ask how to proceed. |
