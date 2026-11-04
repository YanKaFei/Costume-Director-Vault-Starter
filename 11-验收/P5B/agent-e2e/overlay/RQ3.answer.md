All data gathered and verified on disk. Here is the complete answer.

# Query Results — typed relations in the Costume Director Vault

Both commands were run from the Vault root (`/Users/coffee/Desktop/Costume-Director-Vault-Starter`) with `--limit 0` (all matches). Every card path below was confirmed to exist on disk.

## Query 1 — `PRD-0001` with `--relation-type context_includes`

**Command:**
```bash
python3 scripts/query.py --related-to PRD-0001 --relation-type context_includes --json --limit 0
```

**Subject card:** `PRD-0001` — 1770 年代英法服饰语境 / *1770s France and Britain dress context*
- path: `06-时代地域/PRD-0001-1770年代英法服饰语境.md`
- type: `period_region` · card evidence_status: **verified** · source: **SRC-0150**

**6 outgoing relations returned** (direction `subject_to_object`, i.e. PRD-0001 → target). All six share the same relation metadata: evidence **verified**, confidence **high**, rule `R-PRD-KEY-GARMENTS`, `origin: candidate`, `review_status: migration_ready`, sourced to **SRC-0150**.

| # | Real target ID | Target name | Target type | Target card path |
|---|---|---|---|---|
| 1 | **GAR-0015** | 法式长袍 | garment | `01-服装单品/连身/GAR-0015-法式长袍.md` |
| 2 | **GAR-0024** | 穆勒鞋 (mules) | garment | `01-服装单品/足部/GAR-0024-穆勒鞋.md` |
| 3 | **GAR-0025** | 三角帽 (tricorn hat) | garment | `01-服装单品/头部/GAR-0025-三角帽.md` |
| 4 | **GAR-0028** | 手笼 (muff) | garment | `01-服装单品/配饰/GAR-0028-手笼.md` |
| 5 | **STR-0006** | 胸衣插片 (stomacher) | garment_part | `02-结构细节/STR-0006-胸衣插片.md` |
| 6 | **STR-0009** | 裙侧撑 (panniers) | garment_part | `02-结构细节/STR-0009-裙侧撑.md` |

## Query 2 — a LOOK with `--relation-type appears_in_look`

**Command:**
```bash
python3 scripts/query.py --related-to LOOK-0001 --relation-type appears_in_look --json --limit 0
```

**Subject card:** `LOOK-0001` — 洛可可沙龙女主人 / *rococo salon hostess look* (chosen because it is the 1770s French look belonging to the same PRD context)
- path: `09-造型组合/LOOK-0001-洛可可沙龙女主人.md`
- type: `look` · card evidence_status: **interpretive** · source: **SRC-0150**

**6 outgoing relations returned** (LOOK-0001 → the items appearing in it). All six share: evidence **interpretive**, confidence **medium**, rule `R-LOOK-ITEMS`, `origin: candidate`, `review_status: review_queue`. Each is backed by two sources — the decade overview SRC-0150 plus an item-specific SRC:

| # | Real target ID | Target name | Target type | Target card path | Source IDs on relation |
|---|---|---|---|---|---|
| 1 | **GAR-0015** | 法式长袍 | garment | `01-服装单品/连身/GAR-0015-法式长袍.md` | SRC-0150, **SRC-0116** |
| 2 | **GAR-0024** | 穆勒鞋 | garment | `01-服装单品/足部/GAR-0024-穆勒鞋.md` | SRC-0150, **SRC-0125** |
| 3 | **GAR-0028** | 手笼 | garment | `01-服装单品/配饰/GAR-0028-手笼.md` | SRC-0150, **SRC-0129** |
| 4 | **MAT-0002** | 尚蒂伊蕾丝 (Chantilly lace) | material | `03-材质纹样/材料/MAT-0002-尚蒂伊蕾丝.md` | SRC-0150, **SRC-0141** |
| 5 | **STR-0006** | 胸衣插片 | garment_part | `02-结构细节/STR-0006-胸衣插片.md` | SRC-0150, **SRC-0136** |
| 6 | **STR-0009** | 裙侧撑 | garment_part | `02-结构细节/STR-0009-裙侧撑.md` | SRC-0150, **SRC-0139** |

## Source card paths (all resolved via `query.py --id`, all `verified`)

| Source ID | Source card path |
|---|---|
| **SRC-0150** | `04-来源/SRC-0150-FIT-1770年代概览.md` — FIT Fashion History Timeline, 1770–1779 decade overview |
| **SRC-0116** | `04-来源/SRC-0116-FIT-robe-a-la-francaise.md` |
| **SRC-0125** | `04-来源/SRC-0125-FIT-mule.md` |
| **SRC-0129** | `04-来源/SRC-0129-FIT-muff.md` |
| **SRC-0136** | `04-来源/SRC-0136-FIT-stomacher.md` |
| **SRC-0139** | `04-来源/SRC-0139-FIT-panniers.md` |
| **SRC-0141** | `04-来源/SRC-0141-FIT-chantilly-lace.md` |

## Confidence / evidence state — what the query actually returned

- **`context_includes` (Query 1):** every relation is **evidence=verified, confidence=high**, with a single provenance link **SRC-0150**; review status `migration_ready`. This is production-grade period-context evidence: the 1770s France/Britain context card verifiably includes the robe à la française, mules, tricorn, muff, stomacher, and panniers.
- **`appears_in_look` (Query 2):** every relation is **evidence=interpretive, confidence=medium**, review status `review_queue`. This matches the look card itself: the *individual* garment/material/structure cards are verified by their item-specific FIT sources, but the **composition is the vault's design inference**, not a historically documented outfit — hence the lower grade and the second SRC per item.
- **Provenance origin (important caveat):** all 12 relations carry `"origin": "candidate"`. Re-running either query with `--relations-from cards` returns **0 relations**, meaning the edges currently live in the **RELATION-CANDIDATES index only**, not in the cards' own YAML frontmatter. The `context_includes` edges are queued as `migration_ready`; the `appears_in_look` edges are still in `review_queue`.
- **Overlap between the two sets:** GAR-0015, GAR-0024, GAR-0028, STR-0006, STR-0009 appear in both. Unique to the period context: **GAR-0025** (tricorn). Unique to the look: **MAT-0002** (Chantilly lace).
- No `example`-grade cards or sources appear in either result; nothing was fabricated — all IDs, paths, and confidence/evidence values above are verbatim from `query.py` JSON output, and every target/source/subject file was verified on disk.
