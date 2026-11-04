## GAR-0002 structured relations — complete answer

**Subject card:** `GAR-0002` 达布里特 / doublet — garment, evidence_status `verified`, SRC-0103 — `01-服装单品/上装/GAR-0002-达布里特.md`

**Command run (offline, via `scripts/query.py`):**
```bash
python3 scripts/query.py --related-to GAR-0002 \
  --relation-type may_have_part --relation-type ensemble_with \
  --relations-from all --limit 0 --json
```

### Returned relations (2 total)

| # | Relation | Target | Target name | Target type | Resolves to real card? | Target evidence |
|---|---|---|---|---|---|---|
| 1 | `may_have_part` | **STR-0001** | 美第奇领 / Medici collar | garment_part | ✅ Yes — `02-结构细节/STR-0001-美第奇领.md` | verified (SRC-0101) |
| 2 | `ensemble_with` | **GAR-0024** | 穆勒鞋 / mule | garment | ✅ Yes — `01-服装单品/足部/GAR-0024-穆勒鞋.md` | verified (SRC-0125) |

Both targets were independently re-queried with `query.py --id` and resolve to existing cards; there are **no dangling/unresolvable targets**.

### Relation metadata (exactly as returned)

**GAR-0002 → STR-0001 (`may_have_part`)**
- evidence: `interpretive` · confidence: `medium`
- source_ids on the relation: SRC-0101, SRC-0103
- rule: `R-LOOK-PART-COOCCUR` · origin: `candidate` · review_status: `review_queue`

**GAR-0002 → GAR-0024 (`ensemble_with`)**
- evidence: `interpretive` · confidence: `medium`
- source_ids on the relation: SRC-0101, SRC-0103
- rule: `R-LOOK-ENSEMBLE` · origin: `candidate` · review_status: `review_queue`

### Important provenance caveats

- **Both relations come from the RELATION-CANDIDATES index, not card YAML.** Running the same query with `--relations-from cards` returns `[]` — i.e., neither relation is asserted in the cards' own frontmatter; both are machine-generated co-occurrence candidates still in the review queue (`interpretive`, medium confidence).
- All three cited sources resolve to real `verified` source cards: SRC-0101 (FIT, Medici collar), SRC-0103 (FIT, doublet), SRC-0125 (FIT, mule).
- Note the relation on `GAR-0024` cites SRC-0101 + SRC-0103, while the mule card itself is backed by SRC-0125 — another reason these remain unreviewed candidates rather than confirmed facts. The card definitions themselves also point to a plausible gender/period tension worth a reviewer's attention (doublet = 14–17th c. men's upper garment; Medici collar = late 16th–early 17th c. women's ruff variant; mule = 16th c. French women's indoor shoe).
- Nothing was inferred from wikilinks or body text: the two relations above are the **complete** structured-relation output for these two relation types (default candidate + card indexes, `--limit 0`).
