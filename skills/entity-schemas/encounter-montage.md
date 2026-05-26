# Entity Schema: Montage

## CLI command

```
steel-golem encounters montage new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope options

| Flag | Effect |
|------|--------|
| _(none)_ | Write to the active adventure |
| `--adventure <slug>` | Write to the named adventure |
| `--campaign` | Write to campaign scope |

## Target directory

```
<scope>/encounters/montages/<slug>.md
```

## Frontmatter fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `name` | string | _(from --name)_ | Display name |
| `slug` | string | _(derived from name)_ | Kebab-case identifier |
| `description` | string | `""` | Director-facing summary |
| `location` | string \| null | `null` | Slug of the Location where the Montage takes place |
| `scope` | string | `"adventure"` | `"adventure"` or `"campaign"` |

## Example output file

```markdown
---
name: Crossing the Storm Peaks
slug: crossing-the-storm-peaks
description: ""
location: null
scope: adventure
---
```
