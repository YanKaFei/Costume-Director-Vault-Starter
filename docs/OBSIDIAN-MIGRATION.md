# Obsidian migration notes (R1.2-A)

## Why templates instead of copying `.obsidian`

`.obsidian/` is machine-specific and git-ignored; copying it can overwrite themes,
plugins, hotkeys, workspace layout and user filters. The portable contract is the
small pair of recommended templates, merged into a local `.obsidian` by
`scripts/obsidian_config.py`.

## Behavior differences to know

- `userIgnoreFilters` (app.json) affects graph + search + backlinks/open-file
  results globally. It is the recommended way to keep audit/report/sandbox files
  out of the knowledge graph.
- `graph.json` `search` is a temporary graph-only filter; clearing it restores the
  full graph within the app's excluded-file scope. It does **not** affect search or
  backlinks.
- Obsidian version differences may add fields; the script only fills missing graph
  keys and unions ignore filters, so newer settings are retained.
- `.gitignore` ignores `.obsidian/`; do not commit the live directory. The
  recommended templates under `config/obsidian/` are the tracked source.

## Migration procedure

```bash
python3 scripts/obsidian_config.py --diff
python3 scripts/obsidian_config.py --apply
```

If `--apply` reports `changed: false`, the local config already contains all
recommended ignore filters and graph keys; no files were written.

## Safety

- Default is dry-run; `--apply` is required for writes.
- Whole `.obsidian` backup is taken before writes.
- Only `app.json` and `graph.json` are modified; other user files are never read
  for writing.
- `--restore` restores app/graph from a backup and leaves themes/plugins/hotkeys/
  workspace intact.
- Idempotent: a second apply returns `changed: false`.

## Expected isolated-vault result

After applying to a clean knowledge copy:
- **501 nodes**, **0 zero-degree**, **1 component**;
- cards/MOC/backlinks resolve normally;
- user custom keys/themes/plugins/hotkeys/workspace preserved;
- repeated apply and restore verified.

The full vault includes audit/reports/sandboxes, so a raw full-vault graph will be
larger; that is expected and excluded by the filters.
