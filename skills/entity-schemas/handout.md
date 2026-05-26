# Entity Schema: Handout

## CLI command

```
steel-golem handouts new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope options

| Flag | Effect |
|------|--------|
| _(none)_ | Write to the active adventure |
| `--adventure <slug>` | Write to the named adventure |
| `--campaign` | Write to campaign scope |

## Target directory

```
<scope>/handouts/<slug>.md
```

## Frontmatter fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `name` | string | _(from --name)_ | Display name |
| `slug` | string | _(derived from name)_ | Kebab-case identifier |
| `description` | string | `""` | Director-facing summary of the handout |
| `revealed` | boolean | `false` | Whether the Handout has been revealed to the Heroes; always written, never null |
| `scope` | string | `"adventure"` | `"adventure"` or `"campaign"` |

`revealed` is always written to the file. It is never null — a Handout is either revealed or not.

## Example output file

```markdown
---
name: The Warden's Letter
slug: the-wardens-letter
description: ""
revealed: false
scope: adventure
---
```
