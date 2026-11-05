## What was run (Vault root, offline, read-only)

1. `python3 scripts/relation_trace.py --start GAR-0015 --max-depth 2 --json` → exit 0, 12 depth-2 paths (engine cap; ranked by factual-count/diversity).
2. `python3 scripts/query.py --relation-type uses_material --related-to GAR-0015 --json` → exit 0, output **`[]`**.

**Start card:** `GAR-0015` 法式长袍 / *robe à la française* — `01-服装单品/连身/GAR-0015-法式长袍.md`, `evidence_status: verified`, source `SRC-0116`.

## Headline finding

- **Garment → material: no typed relation exists.** The `uses_material` query against GAR-0015 (as subject *or* target) is a true empty set. The 38 `uses_material` rows in the candidate store involve other garments, not GAR-0015.
- **Garment → structure: two typed edges exist, but both are `may_have_part`, interpretive/medium, co-occurrence-derived — explicitly *not* `has_part` facts.**
- The structure/material association is nevertheless **textually factual inside the verified card body** (cited to `SRC-0116`); the distinction is card-text vs typed graph edge, detailed below.

## All direct typed edges on GAR-0015 (verified via depth-1 trace of the same engine)

| # | Relation edge | Type | Conf / evidence | Factual? | Rule / origin (candidate ID) |
|---|---|---|---|---|---|
| 1 | GAR-0015 → **SRC-0116** | `claim_supported_by` | high / verified | ✅ **factual** | R-SOURCE-IDS; card frontmatter + REL-0137 (migration_ready) |
| 2 | **PRD-0001** → GAR-0015 | `context_includes` | high / verified | ✅ factual* | R-PRD-KEY-GARMENTS; REL-0421 |
| 3 | **LOOK-0001** → GAR-0015 | `appears_in_look` | medium / interpretive | ❌ design | R-LOOK-ITEMS; REL-0001 (review_queue) |
| 4 | GAR-0015 → **GAR-0024** 穆勒鞋 | `ensemble_with` | medium / interpretive | ❌ co-occurrence | R-LOOK-ENSEMBLE; REL-0479 |
| 5 | GAR-0015 → **GAR-0028** 手笼 | `ensemble_with` | medium / interpretive | ❌ co-occurrence | R-LOOK-ENSEMBLE; REL-0480 |
| 6 | GAR-0015 → **STR-0006** 胸衣插片 | `may_have_part` | medium / interpretive | ❌ design/co-occurrence | R-LOOK-PART-COOCCUR; REL-0616 |
| 7 | GAR-0015 → **STR-0009** 裙侧撑 | `may_have_part` | medium / interpretive | ❌ design/co-occurrence | R-LOOK-PART-COOCCUR; REL-0617 |

\* Edge 2 is marked `factual=true` by the engine, but its own candidate note says it is **语境级证据（非逐单品历史证明）** — context-level membership, not item-level historical proof.

### Real paths for every ID (from script JSON)
- `04-来源/SRC-0116-FIT-robe-a-la-francaise.md` — FIT: robe à la française (https://fashionhistory.fitnyc.edu/robe-a-la-francaise/)
- `06-时代地域/PRD-0001-1770年代英法服饰语境.md` (source `SRC-0150`, `04-来源/SRC-0150-FIT-1770年代概览.md`)
- `09-造型组合/LOOK-0001-洛可可沙龙女主人.md`
- `01-服装单品/足部/GAR-0024-穆勒鞋.md`; `01-服装单品/配饰/GAR-0028-手笼.md`
- **`02-结构细节/STR-0006-胸衣插片.md`**; **`02-结构细节/STR-0009-裙侧撑.md`**

## Evidence vs design / co-occurrence

**Factual (verified, high confidence):**
- GAR-0015's claims are supported by `SRC-0116` (edge 1). The card body, under that source, factually states: open front reveals a decorative **stomacher (胸衣插片)** and petticoat, and the gown is **often worn with panniers (裙撑)**; materials "以丝绸、织锦、蕾丝为主" (silk, brocade, lace).
- GAR-0015 is a key garment in the 1770s Britain/France context PRD-0001 per `SRC-0150` (context-level only).

**Design / co-occurrence (interpretive, medium, `factual=false`) — do not treat as historical fact:**
- Edges 3–7 were all generated from co-occurrence in `LOOK-0001.look_items`, citing `SRC-0150`. The CSV states verbatim: ensemble edges "搭配候选，**不是历史搭配证明**"; the structure edges "**仅为 may_have_part 候选，不是 has_part 断言**"; the look link "组合为策展/设计，**不自动等同史实**".
- So **STR-0006 and STR-0009 relation IDs are real graph edges but are design candidates**; the factual backing for stomacher/panniers lives in the card text + `SRC-0116`, not in the typed edges.

## Depth-2 paths returned by the exact command

- Via factual `PRD-0001 → GAR-0015` (7 paths): PRD-0001 also connects to `SRC-0150` (`claim_supported_by`), `STY-0010` 时代剧历史考据造型 (`in_style`; SRC-0167/0168/0169), and co-context items `GAR-0024`, `GAR-0025` 三角帽, `GAR-0028`, `STR-0006`, `STR-0009` (all `context_includes`, verified) — i.e., STR-0006/0009 also appear as **shared-period co-members**, not as garment parts, on these paths.
- Via the non-factual `GAR-0015 → GAR-0024 ensemble_with` (5 paths): GAR-0024 → `SRC-0125` (FIT mule; verified), ← `PRD-0001` (1770s), `PRD-0002` (1790–1810), `PRD-0004` (1920s), `PRD-0005` (1930s Hollywood). These later-period links belong to the mule card, not GAR-0015 — they are context traversals, not claims that GAR-0015 belongs to those eras.
- The 12-path ranking cap cut the direct depth-1 `SRC-0116` and `may_have_part` edges from this output (two-factual paths outranked them); completeness was restored by the read-only depth-1 run above.

## Material note (important non-edge)

GAR-0015's frontmatter `materials: [silk, brocade, lace]` are free-text tags (not card IDs), and the body wiki-links `[[MAT-0002-尚蒂伊蕾丝]]` (`03-材质纹样/材料/MAT-0002-尚蒂伊蕾丝.md`, verified via `SRC-0141`). **Neither produces a graph edge** — the engine builds edges only from frontmatter `relations:` and the candidate CSV, never from wiki-links or the materials list. Therefore no `GAR-0015 → MAT-*` relation ID can be reported without fabrication; the only honest material evidence is the card text attributed to `SRC-0116`.

## Gaps / caveats
- No typed `uses_material` edge GAR-0015 → any MAT card (query-confirmed empty).
- No typed `has_part`; only weaker `may_have_part` candidates for STR-0006/STR-0009.
- `PRD-0001 context_includes` is context-level, not per-garment historical proof.
- No cards, scripts, or sources were modified; all IDs/paths above come from script output.
