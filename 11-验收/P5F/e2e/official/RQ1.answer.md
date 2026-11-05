## Relation trace — `GAR-0015`

Command run exactly:

```bash
python3 scripts/relation_trace.py --start GAR-0015 --max-depth 2 --json
```

Start card: **GAR-0015** — 法式长袍 / *robe à la française* (garment, evidence `verified`, own source `SRC-0116`). Engine limits: `max_depth=2`, low-confidence edges filtered, design edges included and marked `factual=false`, read-only.

### Path 1 — FACTUAL (period/provenance chain)

`GAR-0015` ← *context_includes* — `PRD-0001` → *claim_supported_by* — `SRC-0150`

| Hop | Stored edge | Relation | Confidence | Evidence | Factual | SRC |
|---|---|---|---|---|---|---|
| 1 | `PRD-0001` → `GAR-0015` (inbound, walked from GAR-0015) | `context_includes` | high | verified | **true** | `SRC-0150` |
| 2 | `PRD-0001` → `SRC-0150` | `claim_supported_by` | high | verified | **true** | `SRC-0150` |

- `PRD-0001` = 1770 年代英法服饰语境
- `SRC-0150` = 1770至1779年 FIT 年代概览

Both edges are documented, high-confidence, verified relations; this path asserts only that the 1770s English/French context includes GAR-0015 and that this contextual claim is supported by SRC-0150. It is **factual**, not a styling recommendation.

### Path 2 — DESIGN (interpretive styling chain)

`GAR-0015` → *ensemble_with* — `GAR-0024` → *claim_supported_by* — `SRC-0125`

| Hop | Stored edge | Relation | Confidence | Evidence | Factual | SRC |
|---|---|---|---|---|---|---|
| 1 | `GAR-0015` → `GAR-0024` | `ensemble_with` | medium | interpretive | **false** | `SRC-0150` |
| 2 | `GAR-0024` → `SRC-0125` | `claim_supported_by` | high | verified | **true** | `SRC-0125` |

- `GAR-0024` = 穆勒鞋 (mule)
- `SRC-0125` = FIT：mule（穆勒鞋）

The pairing GAR-0015 + GAR-0024 is a **design/interpretive** relation (`confidence: medium`, `evidence: interpretive`, `factual: false`) — a proposed ensemble, not a documented historical combination. The terminal `SRC-0125` verifies the mule card's own claim; it does **not** independently verify that the two garments were worn together.

### Label summary

| Path | Classification | Why |
|---|---|---|
| `GAR-0015` ← `PRD-0001` → `SRC-0150` | **Factual** | All edges `factual=true`, `evidence=verified`, `confidence=high` |
| `GAR-0015` → `GAR-0024` → `SRC-0125` | **Design** | First edge `factual=false`, `evidence=interpretive`, `confidence=medium`; second edge only supports GAR-0024 |
