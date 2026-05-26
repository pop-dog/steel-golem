# campaigns-new

Creates a new campaign directory and writes it as the active campaign in `~/.steel-golem/config.yaml`.

## Command

```
steel-golem campaigns new --name "<name>" --path <path>
```

The CLI derives a slug from `<name>` and creates `<path>/<slug>/` on disk.

## Arguments to extract

| Argument | Source |
|----------|--------|
| `--name` | The campaign name the Director provided (quoted string) |
| `--path` | The parent directory where the campaign folder should be created |

If either argument is missing, ask one clarifying question to get both at once:
> "What should the campaign be called, and where should I create it?"

## Error handling

| CLI output | Action |
|------------|--------|
| `Error: Campaign directory already exists: ...` | Tell the Director the directory already exists and ask whether to use a different name or path. |
| `Error: Cannot derive a valid slug from name: ...` | Tell the Director the name must contain at least one letter or number and ask for a new name. |
| Any other non-zero exit | Show the error message verbatim and ask the Director how to proceed. |
