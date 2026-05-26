# Entity Schema: Subplot

## CLI command

```
steel-golem subplots new --name "<name>" [--description "<description>"] [--adventure <slug>]
```

## Scope options

Subplots are Adventure-scoped only. The `--campaign` flag is not supported.

| Flag | Effect |
|------|--------|
| _(none)_ | Write to the active adventure |
| `--adventure <slug>` | Write to the named adventure |

## Target directory

```
<adventure>/subplots/<slug>.md
```

## Frontmatter fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `name` | string | _(from --name)_ | Display name |
| `slug` | string | _(derived from name)_ | Kebab-case identifier |
| `description` | string | `""` | Director-facing summary |
| `plot` | string \| null | `null` | Slug of the parent Campaign Plot, if this Subplot contributes to one |
| `scope` | string | `"adventure"` | Always `"adventure"` |

## Example output file

```markdown
---
name: The Missing Courier
slug: the-missing-courier
description: ""
plot: null
scope: adventure
---
```
