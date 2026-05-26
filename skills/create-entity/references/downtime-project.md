# create-entity: Downtime Project

## Natural language patterns

Directors commonly ask for a Downtime Project like this:

- "Create a downtime project — Sera wants to forge a legendary sword"
- "Add a research project for Aldric: deciphering the vault inscription"
- "I need a crafting project for the party to work on during the Respite"
- "Make a downtime project for whoever wants to investigate the cult"
- "Add a project: translating the ancient tome"

A Downtime Project is a Director-designed goal for a Hero pursued across Respites, tracked by Project Points toward a Project Goal. steel-golem only tracks Director-created Downtime Projects; player-initiated projects belong on the character sheet.

A Downtime Project with no Hero assigned is Unowned — the `hero` field is written as `hero: null` at creation. Use this when the owning Hero is not yet known; the Director assigns ownership manually.

## Schema reference

Read `~/.steel-golem/entity-schemas/downtime-project.md` for the full CLI contract: arguments, frontmatter fields, and target directory.

## CLI command

```
steel-golem downtime-projects new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope guidance

Default to the active adventure — omit all scope flags unless the Director specifies otherwise.

Use `--campaign` when the Director says "campaign-wide", "for the whole campaign", or the project persists across multiple Adventures.

Use `--adventure <slug>` when the Director names a specific adventure other than the active one.

## Error handling

| CLI output | Tell the Director |
|------------|-------------------|
| `Error: Config file not found...` | No campaign is active. Ask them to set one up with the `campaigns-new` skill first. |
| `Error: No active adventure...` | No active adventure is set. Ask them to create or set one first. |
| `Error: Downtime project directory already exists...` | A Downtime Project with that name already exists. Ask if they want a different name. |
| Any other non-zero exit | Show the error verbatim and ask how to proceed. |
