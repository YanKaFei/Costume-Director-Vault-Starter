# P5-D — Conservative relation backfill (pilot 30 → full scan)

- Date: 2026-11-05
- Script: `scripts/backfill_relations.py` (append-only; no fact/source_ids/
  evidence_status changes)
- Schema: `00-系统/关系类型.md` v3; medium design relations are review-queue-only
- Backup: `/tmp/p5d-backup` — **2022 files**, verify PASS, restore PASS
- Evidence: `11-验收/P5D/`
- Tests: `tests/test_backfill_relations.py` — **5/5 PASS**
- Final: relation_consistency **0 errors**, validate **PASS 458/458**, build_sources
  **PASS 234**, validate_outfits **35 looks (12 passed / 23 legacy / 0 failed)**.

## 1. Result up front

The conservative rules found **no safe high-confidence backfill gaps** in the old
cards. Therefore:

- pilot inspected **30 old cards** (type-diverse: look/garment/garment_part/
  period_region/material/style/scene/pattern);
- full scan planned all **189 old content cards**;
- **0 card writes**, **0 new high relations**, **0 new visible links**;
- **269 medium review-queue rows** were generated and not written to cards;
- idempotent: rerun `changed_cards=0`, `non_idempotent=[]`.

This is the intended conservative outcome, not a silent skip: every candidate that
could be useful is explicit in `11-验收/P5D/REVIEW-QUEUE.csv`.

## 2. Review queue distribution (269 rows)

| relation_type | count | confidence | rule |
| --- | ---: | --- | --- |
| appears_in_look | 122 | medium | R-LOOK-ITEMS |
| uses_material | 77 | medium | R-MAT-TOKEN |
| in_style | 39 | medium | R-STY-EXACT (not visible/eligible high) |
| look_appears_in_scene | 22 | medium | R-LOOK-SCENE (LOOK interpretive) |
| may_have_part | 9 | medium | R-LOOK-PART-COOCCUR |

No low-confidence rows were emitted; no medium row was written into a card/body.
All 269 are design/co-occurrence or evidence-gated; none is a historical fact.

## 3. Rules actually applied

- **in_style**: only exact `STY-xxxx` in `style_tags`; high requires subject+target
  verified, subject `source_ids`, and a visible target link; otherwise medium queue.
  No old card with exact STY tags had an unprotected high gap (existing `in_style`
  relations/links already present; self-tags skipped).
- **uses_material**: only unique token→MAT entity, excluding MAT-0012/0013 property
  cards and pattern cards; medium/interpretive queue only.
- **appears_in_look**: LOOK.look_items exact IDs; medium queue.
- **ensemble_with**: same LOOK garment+footwear/accessory; medium queue (no rows
  emitted in current data because no qualifying pairs beyond existing relations).
- **may_have_part**: same-LOOK garment+part co-occurrence only; medium review; never
  `has_part`.
- **look_appears_in_scene**: LOOK.look_scene exact; high only if LOOK+SCN verified
  and LOOK has source_ids, otherwise medium queue. All 23 scene-bearing LOOKs are
  interpretive, so none became high cards.
- **claim_supported_by**: existing relations never duplicated.
- **silhouette**: **N/A** — no target card type; not fabricated.

No keyword/similarity history inference is used.

## 4. Pilot / batches

- **Pilot:** 30 representative old cards (`pilot-dry.json`, `pilot-apply.json`):
  selected 30, inspected 30, changed 0, applied 0, queue 269.
- **Full scan:** 189 old content cards; changed 0, high 0, visible links 0; queue 269
  (`full-dry.json`, `full-apply.json`).
- No batch writes were appropriate; batches should be driven by explicit review of
  the queue, not by force. If a human approves a queue row, a separate migration
  step can add it.

## 5. Safety / rollback / sample accuracy

- Backup/verify/restore: `/tmp/p5d-backup` 2022 files, verify PASS, restore PASS.
- Idempotent full rerun: `changed_cards=0`, `non_idempotent=[]`.
- Rollback test: apply in a temp vault, restore from manifest, original bytes restored
  (`test_backfill_relations.py::test_rollback_roundtrip`).
- Fact safety: no `source_ids`, `evidence_status`, or body facts changed; no card
  writes at all in production this run.
- Sample accuracy (first 10 queue rows checked): every target exists as a real card;
  every type/rule matches the structured source field:
  - GAR-0002→MAT-0016 (uses_material, token match)
  - GAR-0003→MAT-0017
  - GAR-0007→MAT-0016
  - GAR-0043→MAT-0004
  - LOOK items/scenes targets verified by resolver.
  Full resolve/check: `relation_consistency.py` 0 errors over all 458 cards.

## 6. Limits

- Conservative rules intentionally leave most design relations in review; no
  high-confidence additions were justified by current old-card data.
- `ensemble_with`/`may_have_part` are co-occurrence design relations, never
  historical facts or `has_part`.
- `uses_material` unique-token mapping is medium by schema; no MAT property inference.
- No silhouette relation because no target card type.
- Queue rows require human/architect review before any migration into cards.

---

# P5-D addendum — approved 30-card MEDIUM design pilot + P1 fixes

## A. Controlled medium design exception (approved)

The strict backfill remains **0 high / 0 historical facts**. Under the explicit
lead-approved exception, a **30-card medium design pilot** was applied from the
269-row review queue:

- **30 old cards / 30 design relations / 30 visible `[[...]]` markers**.
- Every added relation is `evidence=interpretive`, `confidence=medium`,
  `review_status=review_queue`, `factual=false`, `design_only=true`.
- No `source_ids`, `evidence_status`, or historical fact changed.
- Types: appears_in_look 6, in_style 7, look_appears_in_scene 6, may_have_part 4,
  uses_material 7.
- Backup: `/tmp/p5d-design-backup-20261105-102956`; rollback manifest
  `11-验收/P5D/design-rollback-manifest.json`.
- Remaining queue: **239** rows (`DESIGN-QUEUE-REMAINING.csv`); not auto-migrated.
- Evidence: `design-pilot-report.json`, `DESIGN-PILOT.csv`.

### Before / after coverage split

| Layer | Before pilot | After pilot |
| --- | ---: | ---: |
| Formal high relations | 264 | **264 (unchanged)** |
| Design/review medium relations | 20 | **50** |
| Design-review cards | 0 | **30** |
| Review queue | 269 | **239** |

The pilot is coverage for design/review only and is **never counted as high or
historical evidence**. All 30 relations have visible non-code markers.

## B. P1 regressions fixed

1. **Lady Macbeth stage A difference**: composer now adds a deterministic
   stage-specific variation to look A from explicit context fields (scene/action/
   season/weather/art direction), using a real candidate and preserving the
   occupation anchor. Lady rise/guilt A looks are no longer identical.
   - P4-MACBETH: **11/11 PASS** (`11-验收/P5D/regress-macbeth.log`).
   - P4 composer: **9/9 PASS** (`11-验收/P5D/regress-composer.log`).
2. **Missing torso repair**: a look missing one-piece/set is repaired from real
   unused pool candidates (no invented IDs); action_dance returns 3 valid looks.
3. **Human-closeout isolation**: the protection test no longer requires generator
   success on a pristine HEAD snapshot; it verifies the protected
   `HUMAN-CLOSEOUT.md` hash is unchanged. **3/3 PASS**, 33.8s
   (`11-验收/P5D/test-human-closeout.log`). Generator output is diagnostic only.
4. **P5-C sample WARNs closed**:
   - GAR-0088 now has visible `[[MAT-0017-皮革]]` medium design/review marker;
   - STR-0029 now has visible `[[MAT-0001-平纹细布]]` medium marker;
   - relation_consistency remains **0 errors**.

## C. Final checks

- relation_consistency: **0 errors** (458 cards, 314 relations, 9 MOC skipped).
- validate.py: **PASS 458/458, 0 errors/warnings**.
- build_sources.py: **PASS 234 sources**.
- validate_outfits --all: **35 looks (12 passed / 23 legacy / 0 failed)**.
- Backfill tests: **6/6 PASS**.
- Strict high-conf additions remain **0**; the 30 medium design additions are the
  approved exception and are kept separate in all counts.

---

# P5-D addendum 2 — semantic review corrections

Semantic review found 6 MISLINKs in the applied design/backfill set. Corrected:

| Card | Relation | Fix |
| --- | --- | --- |
| SCN-0001 | →STY-0005 in_style | removed relation + marker (scene cannot assert style) |
| LOOK-0019 | →STR-0011 may_have_part | removed relation + marker (LOOK co-occurrence cannot assert part) |
| LOOK-0003 | →STR-0001 may_have_part | removed relation + marker |
| LOOK-0017 | →STR-0010 may_have_part | removed relation + marker |
| LOOK-0008 | →STR-0011 may_have_part | removed relation + marker |
| GAR-0079 | →SRC-0069 claim_supported_by | downgraded **medium/interpretive** (book_fact, not standalone verified) |
| GAR-0033 | →SRC-0066 claim_supported_by | removed relation, visible link, and SRC-0066 from source_ids (source only 1908 terminology) |

Subject-type validation was added to `relation_consistency.py`:
- `in_style`: garment/garment_part/look/period_region; scene rejected.
- `may_have_part`/`ensemble_with`: garment only; LOOK rejected.
- `appears_in_look`/`look_appears_in_scene`: LOOK only.
- `context_includes`: period_region only.
- `style_interpretation`: look/garment/garment_part/style.

After corrections: relation_consistency **0 errors** (458 cards, 308 relations),
validate **458/458**, build **234**, backfill+consistency tests **14/14**.

The approved design pilot was 30 applied; **25 remain valid** after semantic
removal (5 invalid), still design/review-only. Coverage split now:
formal high **262**, design/review medium **46**, review queue **239**.
