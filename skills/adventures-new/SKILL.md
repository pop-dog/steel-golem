# adventures-new

Creates a new adventure directory under the active campaign's `adventures/` folder.
Reads the active campaign path from `~/.steel-golem/config.yaml`.

## Command

```
steel-golem adventures new --name "<name>"
```

The CLI derives a slug from `<name>` and creates `<campaign_path>/adventures/<slug>/`.

## Arguments to extract

| Argument | Source |
|----------|--------|
| `--name` | The adventure name the Director provided (quoted string) |

If the name is missing, ask:
> "What should this adventure be called?"

## Error handling

| CLI output | Action |
|------------|--------|
| `Error: Config file not found...` | Tell the Director no campaign is active yet and suggest running the `campaigns-new` skill first. |
| `Error: Adventure directory already exists: ...` | Tell the Director an adventure with that slug already exists and ask for a different name. |
| Any other non-zero exit | Show the error message verbatim and ask the Director how to proceed. |
