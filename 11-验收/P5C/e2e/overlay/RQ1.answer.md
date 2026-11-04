## Command & result

Run exactly from the Vault root (`/Users/coffee/Desktop/Costume-Director-Vault-Starter`):

```
python3 scripts/relation_trace.py --start GAR-0015 --max-depth 3 --json
```

Exit code `0`. **Start card:** `GAR-0015` = 法式长袍 / *robe à la française* (`01-服装单品/连身/GAR-0015-法式长袍.md`, evidence `verified`, own source `SRC-0116`). The engine returned **12 ranked depth‑3 paths**. It treats edges as undirected for traversal but prints each edge in its stored `from→to` orientation (so the first edge below is traversed backward into GAR-0015).

**How the engine labels edges (`scripts/relation_trace.py`, lines 32–35, 109, 131):**
- **FACTUAL** = type ∈ {`claim_supported_by`, `context_includes`, `in_style`} **and** confidence `high` → `"factual": true`.
- **DESIGN / CO-OCCURRENCE** = type ∈ {`appears_in_look`, `uses_material`, `may_have_part`, `ensemble_with`} (and any of the above at `medium` confidence) → `"factual": false`. Low-confidence edges are filtered entirely.

The command's ranked top‑12 are all fully factual; I re-ran the **same read-only engine** with a larger limit to surface the factual/design mixed paths so the distinction is demonstrable (no script or card was modified).

---

## Path A — fully factual (from the command output)

`GAR-0015 → PRD-0001 → STY-0010 → SRC-0167`

| # | Edge (stored orientation) | Type | Conf / evidence | Factual? | SRC |
|---|---|---|---|---|---|
| 1 | `PRD-0001 → GAR-0015` | `context_includes` | high / verified | **FACTUAL** | SRC-0150 |
| 2 | `PRD-0001 → STY-0010` | `in_style` | high / verified | **FACTUAL** | SRC-0167, SRC-0168, SRC-0169 |
| 3 | `STY-0010 → SRC-0167` | `claim_supported_by` | high / verified | **FACTUAL** | SRC-0167 |

Real names: `PRD-0001` 1770年代英法服饰语境 · `STY-0010` 时代剧历史考据造型 · `SRC-0167` 1941 Wyler《小狐狸》(FIT). All three edges are verified facts: the 1770s period context explicitly lists the garment, the context is tagged to the historical-research style, and that style claim is supported by the FIT source.

## Path B — fully factual (from the command output)

`GAR-0015 → PRD-0001 → GAR-0024 → SRC-0125`

| # | Edge | Type | Conf / evidence | Factual? | SRC |
|---|---|---|---|---|---|
| 1 | `PRD-0001 → GAR-0015` | `context_includes` | high / verified | **FACTUAL** | SRC-0150 |
| 2 | `PRD-0001 → GAR-0024` | `context_includes` | high / verified | **FACTUAL** | SRC-0150 |
| 3 | `GAR-0024 → SRC-0125` | `claim_supported_by` | high / verified | **FACTUAL** | SRC-0125 |

Real names: `GAR-0024` 穆勒鞋 / mule (`01-服装单品/足部/`) · `SRC-0125` FIT：mule. Note: edges 1–2 are context-level facts (both garments appear in the 1770s context) — they do **not** assert the two were historically worn together.

## Path C — fully factual (from the command output)

`GAR-0015 → PRD-0001 → STR-0006 → SRC-0136`

| # | Edge | Type | Conf / evidence | Factual? | SRC |
|---|---|---|---|---|---|
| 1 | `PRD-0001 → GAR-0015` | `context_includes` | high / verified | **FACTUAL** | SRC-0150 |
| 2 | `PRD-0001 → STR-0006` | `context_includes` | high / verified | **FACTUAL** | SRC-0150 |
| 3 | `STR-0006 → SRC-0136` | `claim_supported_by` | high / verified | **FACTUAL** | SRC-0136 |

`STR-0006` 胸衣插片 / stomacher · `SRC-0136` FIT：stomacher. The analogous fully-factual path `… → STR-0009 → SRC-0139` (裙侧撑 / panniers; FIT panniers) also appears in the command output, and `PRD-0001 → STY-0010 → SRC-0168 / SRC-0169` (FIT 1964 *Becket*; FIT 1995 *Sense and Sensibility*) repeat Path A's structure.

---

## Paths containing DESIGN / CO-OCCURRENCE edges (factual=false)

These are real edges the engine holds and marks non-factual; they ranked below the 12 all-factual paths, so they are shown from the same-engine re-run.

### Path D — co-occurrence + factual
`GAR-0015 → GAR-0024 → PRD-0001 → SRC-0150`

| # | Edge | Type | Conf / evidence | Factual? | SRC |
|---|---|---|---|---|---|
| 1 | `GAR-0015 → GAR-0024` | **`ensemble_with`** | medium / interpretive | **DESIGN/CO-OCCURRENCE — false** | SRC-0150 |
| 2 | `PRD-0001 → GAR-0024` | `context_includes` | high / verified | FACTUAL | SRC-0150 |
| 3 | `PRD-0001 → SRC-0150` | `claim_supported_by` | high / verified | FACTUAL | SRC-0150 |

The first edge exists only because GAR-0015 and GAR-0024 co-occur in `LOOK-0001.look_items` (rule `R-LOOK-ENSEMBLE`, review queue) — a curated pairing candidate, **not** a historical-dressing proof. `SRC-0150` = 1770–1779 FIT 年代概览 (verified).

### Path E — part candidate + factual
`GAR-0015 → STR-0006 → PRD-0001 → SRC-0150`

| # | Edge | Type | Conf / evidence | Factual? | SRC |
|---|---|---|---|---|---|
| 1 | `GAR-0015 → STR-0006` | **`may_have_part`** | medium / interpretive | **DESIGN/CO-OCCURRENCE — false** | SRC-0150 |
| 2 | `PRD-0001 → STR-0006` | `context_includes` | high / verified | FACTUAL | SRC-0150 |
| 3 | `PRD-0001 → SRC-0150` | `claim_supported_by` | high / verified | FACTUAL | SRC-0150 |

`may_have_part` is explicitly not a `has_part` assertion (rule `R-LOOK-PART-COOCCUR`): stomacher STR-0006 co-occurs with the gown in a curated look. The identical pattern exists for `STR-0009` panniers.

### Other non-factual edges anchored at GAR-0015 (same engine, medium/interpretive)
- `LOOK-0001 → GAR-0015` **`appears_in_look`** → false — the gown's membership in look LOOK-0001 is curatorial, not historical fact (SRC-0150; SRC-0116).
- `GAR-0015 → GAR-0028` **`ensemble_with`** (手笼/muff) → false, SRC-0150.
- `GAR-0015 → STR-0009` **`may_have_part`** (裙侧撑/panniers) → false, SRC-0150.
- At `medium` confidence even factually-typed relations stay false, e.g. `LOOK-0001 → SRC-0150` `claim_supported_by` and `LOOK-0001 → STY-0010` `in_style` (both interpretive/medium).

## Evidence vs inference — summary
- **Factual (verified, high):** GAR-0015 is included in the 1770s Britain/France context PRD-0001 (`SRC-0150`); PRD-0001 relates to style STY-0010 (`SRC-0167/0168/0169`); GAR-0015's own existence claim is `SRC-0116`; GAR-0024/STR-0006/STR-0009 claims are supported by SRC-0125/SRC-0136/SRC-0139.
- **Design/co-occurrence (interpretive, medium):** every `ensemble_with`, `may_have_part`, and `appears_in_look` link above derives solely from co-occurrence in `LOOK-0001.look_items`; the CSV text itself states these are not historical proofs.
- **Gaps:** no `uses_material` edge reaches the top output for GAR-0015 (its silk/brocade/lace data is textual/frontmatter only); all mixed edges remain `review_queue`, so they must not be cited as verified history. No files were written or modified; the engine is read-only.
