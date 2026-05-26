# Entity Schema: Negotiation

## CLI command

```
steel-golem encounters negotiation new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope options

| Flag | Effect |
|------|--------|
| _(none)_ | Write to the active adventure |
| `--adventure <slug>` | Write to the named adventure |
| `--campaign` | Write to campaign scope |

## Target directory

```
<scope>/encounters/negotiations/<slug>.md
```

## Frontmatter fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `name` | string | _(from --name)_ | Display name |
| `slug` | string | _(derived from name)_ | Kebab-case identifier |
| `description` | string | `""` | Director-facing summary |
| `npc` | string \| null | `null` | Slug of the NPC at the center of the Negotiation |
| `location` | string \| null | `null` | Slug of the Location where the Negotiation takes place |
| `scope` | string | `"adventure"` | `"adventure"` or `"campaign"` |

## Example output file

```markdown
---
name: Bargaining with the Harbormaster
slug: bargaining-with-the-harbormaster
description: ""
npc: null
location: null
scope: adventure
---
```
