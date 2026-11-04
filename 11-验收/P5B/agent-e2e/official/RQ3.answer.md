## Query brief
- Vault: `/Users/coffee/Desktop/Costume-Director-Vault-Starter`
- Mode: read-only knowledge-base query; no cards, scripts, or sources modified
- Queries run from the Vault root (`query.py` exit `0` for both):
```bash
python3 scripts/query.py --related-to PRD-0001 --relation-type context_includes --limit 0 --json
python3 scripts/query.py --related-to LOOK-0001 --relation-type appears_in_look --limit 0 --json
```
- No IDs or source IDs below are invented; all come from `query.py` output. Paths were checked with `scripts/path_guard.py check` (all `OK`).

---

## 1. PRD-0001 → `context_includes`

**Subject card**
- `PRD-0001` — 1770 年代英法服饰语境 / *1770s France and Britain dress context*
- Type: `period_region`; card evidence: `verified`; card review: `draft`
- Card path: `06-时代地域/PRD-0001-1770年代英法服饰语境.md`
- Card `source_ids`: `SRC-0150`

**Targets returned (6 relations, all `subject_to_object`)**

| Relation | Target ID | Target name | Type | Target card path | Relation evidence | Confidence | Relation source_ids | Review status |
|---|---|---|---|---|---|---|---|---|
| REL-0421 | `GAR-0015` | 法式长袍 | garment | `01-服装单品/连身/GAR-0015-法式长袍.md` | `verified` | `high` | `SRC-0150` | `migration_ready` |
| REL-0422 | `GAR-0024` | 穆勒鞋 | garment | `01-服装单品/足部/GAR-0024-穆勒鞋.md` | `verified` | `high` | `SRC-0150` | `migration_ready` |
| REL-0423 | `GAR-0025` | 三角帽 | garment | `01-服装单品/头部/GAR-0025-三角帽.md` | `verified` | `high` | `SRC-0150` | `migration_ready` |
| REL-0424 | `GAR-0028` | 手笼 | garment | `01-服装单品/配饰/GAR-0028-手笼.md` | `verified` | `high` | `SRC-0150` | `migration_ready` |
| REL-0425 | `STR-0006` | 胸衣插片 | garment_part | `02-结构细节/STR-0006-胸衣插片.md` | `verified` | `high` | `SRC-0150` | `migration_ready` |
| REL-0426 | `STR-0009` | 裙侧撑 | garment_part | `02-结构细节/STR-0009-裙侧撑.md` | `verified` | `high` | `SRC-0150` | `migration_ready` |

**Relation provenance**
- Rule: `R-PRD-KEY-GARMENTS`; direction: `subject_to_object`
- `origin`: `candidate` — these were read from the typed-relation candidate index, **not** from the card's YAML. Re-running with `--relations-from cards` returns `[]`; `--relations-from candidates` returns the same six.
- Candidate record file: `11-验收/P5/RELATION-CANDIDATES.csv` (rows REL-0421–REL-0426)
- Recorded rationale, verbatim in substance: each ID is explicitly listed in `PRD.key_garments`; the source is taken from `PRD.source_ids` and is **context-level evidence, not per-item historical proof** (`属语境级证据（非逐单品历史证明）`).

**Source card**
- `SRC-0150` — 1770至1779年 FIT 年代概览
- Path: `04-来源/SRC-0150-FIT-1770年代概览.md`
- Card evidence: `verified`; review: `reviewed`; URL: [https://fashionhistory.fitnyc.edu/1770-1779/](https://fashionhistory.fitnyc.edu/1770-1779/)
- Scope caveat on the source card: it supports the decade's general dress context but **cannot** support a specific garment's exact date, place of origin, or extant-collection details.

**Note on target-card evidence:** each target is itself a `verified` card, with its own source: `GAR-0015` → `SRC-0116`; `GAR-0024` → `SRC-0125`; `GAR-0025` → `SRC-0126`; `GAR-0028` → `SRC-0129`; `STR-0006` → `SRC-0136`; `STR-0009` → `SRC-0139`. Those per-item sources are **not** listed on the PRD relation records, which cite only `SRC-0150`.

---

## 2. LOOK-0001 → `appears_in_look`

**Subject card**
- `LOOK-0001` — 洛可可沙龙女主人 / *rococo salon hostess look*
- Type: `look`; card evidence: `interpretive`; card review: `draft`
- Card path: `09-造型组合/LOOK-0001-洛可可沙龙女主人.md`
- Period/region: `1770s` / France — same context as `PRD-0001`
- Card `source_ids`: `SRC-0150`

**Targets returned (6 relations, all `subject_to_object`)**

| Relation | Target ID | Target name | Type | Target card path | Relation evidence | Confidence | Relation source_ids | Review status |
|---|---|---|---|---|---|---|---|---|
| REL-0001 | `GAR-0015` | 法式长袍 | garment | `01-服装单品/连身/GAR-0015-法式长袍.md` | `interpretive` | `medium` | `SRC-0150`; `SRC-0116` | `review_queue` |
| REL-0002 | `GAR-0024` | 穆勒鞋 | garment | `01-服装单品/足部/GAR-0024-穆勒鞋.md` | `interpretive` | `medium` | `SRC-0150`; `SRC-0125` | `review_queue` |
| REL-0003 | `GAR-0028` | 手笼 | garment | `01-服装单品/配饰/GAR-0028-手笼.md` | `interpretive` | `medium` | `SRC-0150`; `SRC-0129` | `review_queue` |
| REL-0004 | `MAT-0002` | 尚蒂伊蕾丝 | material | `03-材质纹样/材料/MAT-0002-尚蒂伊蕾丝.md` | `interpretive` | `medium` | `SRC-0150`; `SRC-0141` | `review_queue` |
| REL-0005 | `STR-0006` | 胸衣插片 | garment_part | `02-结构细节/STR-0006-胸衣插片.md` | `interpretive` | `medium` | `SRC-0150`; `SRC-0136` | `review_queue` |
| REL-0006 | `STR-0009` | 裙侧撑 | garment_part | `02-结构细节/STR-0009-裙侧撑.md` | `interpretive` | `medium` | `SRC-0150`; `SRC-0139` | `review_queue` |

**Relation provenance**
- Rule: `R-LOOK-ITEMS`; direction: `subject_to_object`; `origin`: `candidate`
- Candidate record file: `11-验收/P5/RELATION-CANDIDATES.csv` (rows REL-0001–REL-0006)
- Recorded rationale: each ID is explicitly listed in `LOOK.look_items`; the combination is curation/design, so item presence does **not** automatically equal historical fact (`组合为策展/设计，不自动等同史实`).
- Consistency check: `LOOK-0001` frontmatter `look_items` is `[GAR-0015, STR-0009, STR-0006, GAR-0028, GAR-0024, MAT-0002]` — exactly the six returned targets.

**Evidence reading:** the relation evidence is `interpretive` / `medium` even though every target card is individually `verified`. `LOOK-0001`'s own definition says the garments and structures reference verified cards, but the **combination** is the Vault's design inference, not a surviving historical ensemble.

---

## Source-card paths used above

| Source ID | Source name | Path | Evidence |
|---|---|---|---|
| `SRC-0150` | FIT 1770–1779 decade overview | `04-来源/SRC-0150-FIT-1770年代概览.md` | `verified` |
| `SRC-0116` | FIT: robe à la française | `04-来源/SRC-0116-FIT-robe-a-la-francaise.md` | `verified` |
| `SRC-0125` | FIT: mule | `04-来源/SRC-0125-FIT-mule.md` | `verified` |
| `SRC-0126` | FIT: tricorne hat | `04-来源/SRC-0126-FIT-tricorne-hat.md` | `verified` |
| `SRC-0129` | FIT: muff | `04-来源/SRC-0129-FIT-muff.md` | `verified` |
| `SRC-0136` | FIT: stomacher | `04-来源/SRC-0136-FIT-stomacher.md` | `verified` |
| `SRC-0139` | FIT: panniers | `04-来源/SRC-0139-FIT-panniers.md` | `verified` |
| `SRC-0141` | FIT: Chantilly lace | `04-来源/SRC-0141-FIT-chantilly-lace.md` | `verified` |

---

## Confidence / evidence summary

- **`PRD-0001` `context_includes`:** 6/6 relations returned as **`evidence: verified`, `confidence: high`**, rule `R-PRD-KEY-GARMENTS`, `review_status: migration_ready`. This is the strongest grade returned, but it is explicitly **context-level** evidence sourced to the decade overview `SRC-0150`, not per-garment provenance.
- **`LOOK-0001` `appears_in_look`:** 6/6 relations returned as **`evidence: interpretive`, `confidence: medium`**, rule `R-LOOK-ITEMS`, `review_status: review_queue`. The items are real verified cards, but the look is a designed combination.
- **Provenance caveat:** both relation sets come from `RELATION-CANDIDATES` (`origin: candidate`). For `PRD-0001`, the card's own YAML contains no `context_includes` relations — only `claim_supported_by` and `in_style` — so a cards-only query returns nothing. The PRD relation set is therefore migration-ready candidate metadata, not yet embedded card metadata.
- **Overlap:** the PRD context and the look share five IDs (`GAR-0015`, `GAR-0024`, `GAR-0028`, `STR-0006`, `STR-0009`). `PRD-0001` additionally lists `GAR-0025` (三角帽); `LOOK-0001` additionally uses `MAT-0002` (尚蒂伊蕾丝). This is expected: `context_includes` describes the period's key garments, while `appears_in_look` describes one specific outfit — neither implies the other set must be identical.

## Gaps / caveats

- No `context_includes` relation is stored in `PRD-0001`'s YAML; only the candidate index has it. Treat it as candidate-level provenance until migrated.
- `LOOK-0001` itself records a coverage gap: the Vault has no 18th-century women's headwear/wig card and no 18th-century stays card, so those cannot be specified from the KB.
- `SRC-0150`'s text is CC BY-NC-SA 4.0; its images are not covered by that license (the Vault stores links only). It cannot support precise per-garment dates or collection claims.
- No `example`-grade cards were used; default query behavior excludes them.
