# Entity Schema: Downtime Project

## CLI command

```
steel-golem downtime-projects new --name "<name>" [--description "<description>"] [--adventure <slug> | --campaign]
```

## Scope options

| Flag | Effect |
|------|--------|
| _(none)_ | Write to the active adventure |
| `--adventure <slug>` | Write to the named adventure |
| `--campaign` | Write to campaign scope |

## Target directory

```
<scope>/downtime-projects/<slug>.md
```

## Frontmatter fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `name` | string | _(from --name)_ | Display name |
| `slug` | string | _(derived from name)_ | Kebab-case identifier |
| `description` | string | `""` | Director-facing summary |
| `hero` | string \| null | `null` | Slug of the owning Hero; `null` means Unowned |
| `project_goal` | integer \| null | `null` | Total Project Points required to complete |
| `project_points` | integer | `0` | Project Points accrued so far |
| `scope` | string | `"adventure"` | `"adventure"` or `"campaign"` |

A Downtime Project with `hero: null` is Unowned — created before the owning Hero is known. The Director assigns ownership manually.

## Example output file

```markdown
---
name: Decipher the Vault Inscription
slug: decipher-the-vault-inscription
description: ""
hero: null
project_goal: null
project_points: 0
scope: adventure
---
```
