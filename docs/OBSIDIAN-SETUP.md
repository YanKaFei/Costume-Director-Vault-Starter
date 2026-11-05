# Obsidian setup (portable, R1.2-A)

## What is portable

Tracked templates:
- `config/obsidian/app.recommended.json` — **only** `userIgnoreFilters`.
- `config/obsidian/graph.recommended.json` — graph display/force parameters only;
  no scale/close/user personal layout, no credentials, no absolute paths.

The live config lives in `.obsidian/app.json` and `.obsidian/graph.json`.
`.obsidian/` is in `.gitignore`, so it is not portable by itself; the templates are
the portable source. Obsidian version at audit: **1.14.5**.

## Recommended ignore filters

```
11-验收/
reports/
projects/
docs/
tests/
skills/
.dsh/
TASKS/
TASKS.md
AGENTS.md
```

Purpose: keep audit/sandbox/reports/tooling out of the knowledge graph while
retaining `00-系统` (MOC/index) through `09-造型组合`.

`userIgnoreFilters` is Obsidian's global "Excluded files" setting: excluded paths
are omitted from graph/search **and** from backlinks/quick-open results. The graph
pane's `search` field is a temporary graph-only filter and is different: it does
not change search/backlinks. The recommended template keeps graph `"search": ""`
and relies on `userIgnoreFilters` for a stable scope.

Do not overwrite:
- `appearance.json` (themes)
- `core-plugins.json`, `community-plugins.json`
- `hotkeys.json`
- `workspace.json`
- `themes/`, `plugins/`

`scripts/obsidian_config.py` touches only `app.json`/`graph.json` and backs up the
whole `.obsidian` directory before an apply.

## Install

```bash
# 1. Inspect diff (default dry-run; no writes)
python3 scripts/obsidian_config.py --diff

# 2. Apply; backs up .obsidian first
python3 scripts/obsidian_config.py --apply

# 3. Verify scope and idempotence
python3 scripts/obsidian_config.py --scope-report
python3 scripts/obsidian_config.py --apply      # second time: changed=false
```

Merge policy:
- `app.json`: preserve all existing keys; union existing `userIgnoreFilters` with
  recommended values (user filters are kept).
- `graph.json`: preserve all existing keys; only fill keys that are missing.
  User `scale`, custom keys, etc. remain untouched.
- Missing `.obsidian/app.json`/`graph.json` are created with the templates only.

## Rollback

`--apply` prints the backup path, e.g.
`/tmp/obsidian-config-backup-20261105-.../`. Restore only app/graph:

```bash
python3 scripts/obsidian_config.py --restore /tmp/obsidian-config-backup-...
```

The restore leaves themes/plugins/hotkeys/workspace untouched.

## Cross-device checklist

1. Copy/clone the vault (excluding `.obsidian`, or preserving it without merging).
2. Run `--diff`, then `--apply`.
3. Verify `--scope-report`: expected **488 nodes / 0 zero-degree / 1 component**
   for the current knowledge scope.
4. Open Obsidian → Graph: MOC/cards/backlinks should show; audit/reports/tests
   should be absent.
5. If user custom filters/themes exist, confirm they are still listed/present.
6. Keep the backup until after GUI inspection.

## Scope note

The 488/0/1 target is the **knowledge scope** after userIgnoreFilters; it is not
the full-vault graph (which includes sandboxes/audit files and is intentionally
excluded). The graph is for card navigation, not a claim that all historical
relations are verified.
