# create-entity: Combat Encounter

## Natural language patterns

Directors commonly ask for a Combat Encounter like this:

- "Add a combat encounter — the throne room battle"
- "Create a fight scene in the sewers"
- "I need a combat encounter for when the Heroes reach the vault"
- "Make an encounter: ambush on the bridge"
- "Add a battle encounter — the final showdown with the Warden"

A Combat Encounter is resolved through tactical combat. It involves a monster roster and an objective.

## Schema reference

Read `~/.steel-golem/entity-schemas/encounter-combat.md` for the full CLI contract: arguments, frontmatter fields, and target directory.

## CLI command

```
steel-golem encounters combat new --name "<name>" [--description "<description>"] [--adventure <slug>]
```

## Scope guidance

Combat Encounters are always Adventure-scoped. Do not use `--campaign` — it is not supported.

Default to the active adventure — omit the `--adventure` flag unless the Director names a specific adventure other than the active one.

If the Director says "campaign-wide" or "for the whole campaign", clarify that Combat Encounters are Adventure-scoped only and ask which adventure to write it to.

## Error handling

| CLI output | Tell the Director |
|------------|-------------------|
| `Error: Config file not found...` | No campaign is active. Ask them to set one up with the `campaigns-new` skill first. |
| `Error: No active adventure...` | No active adventure is set. Ask them to create or set one first. |
| `Error: Combat encounter directory already exists...` | A Combat Encounter with that name already exists. Ask if they want a different name. |
| Any other non-zero exit | Show the error verbatim and ask how to proceed. |
