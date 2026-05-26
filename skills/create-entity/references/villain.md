# create-entity: Villain

## Natural language patterns

Directors commonly ask for a Villain like this:

- "Create a villain — the corrupt magistrate, call him Lord Varek"
- "Add the Warden as the main antagonist"
- "I need a BBEG for this campaign, the Lich Queen"
- "Make the cult leader a villain, name her Sister Maerath"
- "Add a villain for this adventure — the dragon Vreth"

A Villain is an antagonist controlled by the Director. The primary Campaign-scoped Villain driving the overarching story is called the BBEG.

## Schema reference

Read `~/.steel-golem/entity-schemas/villain.md` for the full CLI contract: arguments, frontmatter fields, and target directory.

## CLI command

```
steel-golem villains new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope guidance

Default to the active adventure — omit all scope flags unless the Director specifies otherwise.

Use `--campaign` when the Director says "campaign-wide", "for the whole campaign", "this is the BBEG", "spans all adventures", or similar. Campaign-scoped Villains are referenceable across all Adventures.

Use `--adventure <slug>` when the Director names a specific adventure other than the active one.

## Error handling

| CLI output | Tell the Director |
|------------|-------------------|
| `Error: Config file not found...` | No campaign is active. Ask them to set one up with the `campaigns-new` skill first. |
| `Error: No active adventure...` | No active adventure is set. Ask them to create or set one first. |
| `Error: Villain directory already exists...` | A Villain with that name already exists. Ask if they want a different name. |
| Any other non-zero exit | Show the error verbatim and ask how to proceed. |
