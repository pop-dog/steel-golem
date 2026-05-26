# Entity Schema: Faction

## CLI command

```
steel-golem factions new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope options

| Flag | Effect |
|------|--------|
| _(none)_ | Write to the active adventure |
| `--adventure <slug>` | Write to the named adventure |
| `--campaign` | Write to campaign scope |

## Target directory

```
<scope>/factions/<slug>.md
```

## Frontmatter fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `name` | string | _(from --name)_ | Display name |
| `slug` | string | _(derived from name)_ | Kebab-case identifier |
| `description` | string | `""` | Director-facing summary |
| `scope` | string | `"adventure"` | `"adventure"` or `"campaign"` |

Factions carry no relationship fields — NPCs and Villains reference Factions, not the reverse.

## Example output file

```markdown
---
name: The Iron Covenant
slug: the-iron-covenant
description: ""
scope: adventure
---
```
