# P5-A — Source links & typed relation migration

- Date: 2026-11-05
- Scripts: `scripts/relation_migrate.py`, `scripts/graph_apply.py`
- Schema contract: `00-系统/关系类型.md` (architect v1) + `11-验收/P5/RELATION-CANDIDATES.csv`
- Source whitelist: `11-验收/P5/source-audit.csv` (researcher)
- Backup: `/tmp/p5-backup` (1455 files; verify PASS, restore PASS)
- Rollback: `11-验收/P5/last-rollback-manifest.json` + `rollback-<timestamp>/`
- Evidence: `11-验收/P5/{pilot-report.json,full-report.json,REVIEW-QUEUE.csv,validate.log,build-sources.log,graph-summary.json}`
- Tests: `tests/test_relation_migrate.py` — **7/7 PASS**
- Final `validate.py`: **PASS 400/400, 0 errors/warnings**; `build_sources.py --check`: **PASS**.

## 0. P0 incident and root cause (fixed)

First full write produced 29 cards with broken frontmatter (`... rule=R-SOURCE-IDS'---`
where the closing YAML fence had no newline), so `validate.py` failed 371/400. The
tree was **never committed**.

Root cause: `apply_plan()` concatenated `"---\n" + new_fm + "---\n"` while
`append_yaml_relations()` could return a frontmatter string whose last line had no
trailing newline. Fix:

```python
new_fm = append_yaml_relations(fm, plan["relations"]).rstrip("\n")
text = "---\n" + new_fm + "\n---\n" + new_body
```

Recovery: restored all content dirs from the pre-migration verified backup
`/tmp/p5-backup/tree`, then re-ran migration from the clean tree. No `source_ids`
or facts were lost (verified: 0 source_ids differences vs backup). Broken state was
not committed; `validate.py` and `build_sources.py --check` are green.

## 1. Resolution rule (no guessing)

- Only exact-ID matching: `source_ids` entry `SRC-xxxx` -> `04-来源/SRC-xxxx-*.md`.
- No URL/title/alias fuzzy matching; unresolved IDs would go to REVIEW-QUEUE and
  would **not** be linked.
- No new target IDs are invented; only explicit source_ids and explicit existing
  related-card wikilinks are considered.
- Canonical duplicate policy: `SRC-0163→SRC-0022`, `SRC-0175→SRC-0036`,
  `SRC-0157→SRC-0115`; duplicate IDs stay in `source_ids`, but new links point to
  the canonical source; no duplicate relations were added (current duplicate
  citations: 0).
- Researcher classes honored: 143 `whitelist_connected`; 49
  `whitelist_independent` not force-linked; 3 blacklist duplicates; 6
  `action_should_connect` candidates only queued (not linked); 9
  `action_needs_citation` book sources not forced.
- `05-系统/关系类型.md` / `RELATION-CANDIDATES.csv` untouched.

## 2. Typed relation representation (flat scalar)

Per architect v1.1 flat-YAML rule, no nested maps. Example from GAR-0008:

```yaml
relations:
  - 'target=SRC-0109; type=claim_supported_by; direction=outgoing; evidence=verified; confidence=high; source_ids=SRC-0109; rule=R-SOURCE-IDS'
```

High-confidence relations written to cards/body:
- `claim_supported_by` (content→source, from exact source_ids; both endpoints
  verified);
- `in_style` (only when explicit STY ID in `style_tags`, both verified, source_ids
  non-empty);
- `uses_material` (only when explicit material field matches the MAT card, both
  verified, source_ids non-empty).
`may_have_part`/`ensemble_with` are capped at medium and were not written into
cards. `context_includes` candidates were not migrated into per-garment facts (queued
for review by human, per architect). Medium/low only in
`11-验收/P5/REVIEW-QUEUE.csv`; they never enter body links or YAML relations.

## 3. Counts

| Stage | Cards selected | High relations | Source links added |
| --- | ---: | ---: | ---: |
| Pilot | 30 | 34 | 34 |
| Full migration | 113 | 168 | 157 |
| Current migrated cards | 142 | 202 | 191 (141 unique sources) |

Queue: **981 rows** (980 medium, 1 low; 0 high). Breakdown includes 867
medium relation-cap/evidence rows, 107 source-evidence-medium rows, and 7
researcher `action_should_connect` candidate-only rows. High-confidence relations
are in cards only.

Graph: `graph_apply.py` → 400 nodes / 201 edges / 0 unresolved.

## 4. Idempotence and preservation

- Second full run: `selected=0`, `changed=0`, `non_idempotent=[]`.
- The tool appends only: `relations:` flat list + new `## 来源链接` wikilink lines;
  existing YAML fields, `source_ids`, `evidence_status`, body facts are preserved.
- Original content hashes and source_ids checked against the pre-migration backup:
  0 source_ids changes; all originals parse as YAML dict.
- No cards deleted; `evidence_status` unchanged.

## 5. Backup / rollback

Pre-migration backup:

```bash
python3 scripts/backup_restore.py backup --dest /tmp/p5-backup --json
python3 scripts/backup_restore.py verify /tmp/p5-backup --json   # PASS, 1455 files
python3 scripts/backup_restore.py restore /tmp/p5-backup --dest /tmp/p5-restore --json
```

Rollback manifest for the last full apply:
`11-验收/P5/last-rollback-manifest.json` (113 files) + originals under
`11-验收/P5/rollback-<timestamp>/`. Restore:

```bash
python3 scripts/relation_migrate.py --rollback 11-验收/P5/last-rollback-manifest.json
```

## 6. Tests

`tests/test_relation_migrate.py` — **7/7 PASS**:
every source_id resolves exactly; added source links are only for cited IDs; flat
typed relations have allowed type/direction/evidence/confidence and existing targets;
review queue contains no high-confidence rows; full dry-run is idempotent (0 changed);
source_ids and original body facts are preserved vs rollback snapshots; graph builder
is callable.

## 7. Residual risks

1. High source links are only as good as the content's own `verified` status plus
   source card `verified`; this migration does not re-verify external URLs.
2. `in_style`/`uses_material` high entries are explicit-field relations, not
   historical proof; `context_includes`/co-occurrence relations remain review-only.
3. The relation schema is a contract with architect; if schema v2 changes, re-run
   `relation_migrate.py --dry-run --full` and review queue before writing.
4. `RELATION-CANDIDATES.csv` has 244 migration-ready suggested links that are **not**
   cited in `source_ids`; they remain candidates/queue until a human/source
   curator adds citations, so no uncited source links were written.
