# adventures-set

Switches the active adventure. First lists available adventures so the Director can confirm the slug, then sets it.

## Step 1 — list adventures

Run this and show the output to the Director:

```
steel-golem adventures list
```

Output format: one adventure per line, with `*` marking the current active one.

If the Director already provided a slug, skip directly to Step 2.

## Step 2 — set the active adventure

```
steel-golem adventures set <slug>
```

## Arguments to extract

| Argument | Source |
|----------|--------|
| `<slug>` | Chosen by the Director from the list, or provided directly in their message |

If the Director has not specified a slug after seeing the list, ask:
> "Which adventure would you like to make active?"

## Error handling

| CLI output | Action |
|------------|--------|
| `Error: Config file not found...` | Tell the Director no campaign is active yet and suggest running the `campaigns-new` skill first. |
| `Error: Adventure '<slug>' not found...` | Tell the Director that slug does not exist and show the list again so they can pick a valid one. |
| Any other non-zero exit | Show the error message verbatim and ask the Director how to proceed. |
