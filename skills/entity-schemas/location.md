# Entity Schema: Location

## CLI command

```
steel-golem locations new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope options

| Flag | Effect |
|------|--------|
| _(none)_ | Write to the active adventure |
| `--adventure <slug>` | Write to the named adventure |
| `--campaign` | Write to campaign scope |

## Target directory

```
<scope>/locations/<slug>.md
```

## Frontmatter fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `name` | string | _(from --name)_ | Display name |
| `slug` | string | _(derived from name)_ | Kebab-case identifier |
| `description` | string | `""` | Director-facing summary |
| `scope` | string | `"adventure"` | `"adventure"` or `"campaign"` |

Locations carry no relationship fields — they are referenced by other Entity types (NPCs, Villains, Encounters, etc.).

## Example output file

```markdown
---
name: The Sunken Archive
slug: the-sunken-archive
description: ""
scope: adventure
---
```
