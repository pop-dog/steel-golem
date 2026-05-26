# Entity Schema: NPC

## CLI command

```
steel-golem npcs new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope options

| Flag | Effect |
|------|--------|
| _(none)_ | Write to the active adventure |
| `--adventure <slug>` | Write to the named adventure |
| `--campaign` | Write to campaign scope |

## Target directory

```
<scope>/npcs/<slug>.md
```

## Frontmatter fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `name` | string | _(from --name)_ | Display name |
| `slug` | string | _(derived from name)_ | Kebab-case identifier |
| `description` | string | `""` | Director-facing summary |
| `faction` | string \| null | `null` | Slug of the NPC's Faction |
| `location` | string \| null | `null` | Slug of the NPC's home Location |
| `scope` | string | `"adventure"` | `"adventure"` or `"campaign"` |

## Example output file

```markdown
---
name: Mira the Innkeeper
slug: mira-the-innkeeper
description: ""
faction: null
location: null
scope: adventure
---
```
