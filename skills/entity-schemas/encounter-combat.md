# Entity Schema: Combat Encounter

## CLI command

```
steel-golem encounters combat new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope options

| Flag | Effect |
|------|--------|
| _(none)_ | Write to the active adventure |
| `--adventure <slug>` | Write to the named adventure |
| `--campaign` | Write to campaign scope |

## Target directory

```
<scope>/encounters/combat/<slug>.md
```

## Frontmatter fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `name` | string | _(from --name)_ | Display name |
| `slug` | string | _(derived from name)_ | Kebab-case identifier |
| `description` | string | `""` | Director-facing summary |
| `location` | string \| null | `null` | Slug of the Location where the encounter takes place |
| `villain` | string \| null | `null` | Slug of the Villain leading or present in this encounter |
| `scope` | string | `"adventure"` | `"adventure"` or `"campaign"` |

## Example output file

```markdown
---
name: Throne Room Battle
slug: throne-room-battle
description: ""
location: null
villain: null
scope: adventure
---
```
