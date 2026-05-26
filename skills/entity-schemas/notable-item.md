# Entity Schema: Notable Item

## CLI command

```
steel-golem items new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope options

| Flag | Effect |
|------|--------|
| _(none)_ | Write to the active adventure |
| `--adventure <slug>` | Write to the named adventure |
| `--campaign` | Write to campaign scope |

Notable Items are Campaign-scoped by default, but the CLI defaults to the active adventure when no flag is provided. The Director promotes them to campaign scope manually.

## Target directory

```
<scope>/items/<slug>.md
```

## Frontmatter fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `name` | string | _(from --name)_ | Display name |
| `slug` | string | _(derived from name)_ | Kebab-case identifier |
| `description` | string | `""` | Director-facing summary |
| `owner` | string \| null | `null` | Slug of the current owner (Hero, NPC, or Villain) |
| `location` | string \| null | `null` | Slug of the Location where the item is found or kept |
| `scope` | string | `"adventure"` | `"adventure"` or `"campaign"` |

## Example output file

```markdown
---
name: The Obsidian Key
slug: the-obsidian-key
description: ""
owner: null
location: null
scope: adventure
---
```
