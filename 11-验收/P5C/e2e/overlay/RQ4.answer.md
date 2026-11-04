## Relation Paths from GAR-0015 (max-depth 2)

**Path 1 — FACTUAL (verified, high confidence)**
`GAR-0015` → `PRD-0001` → `SRC-0150`

| Hop | From → To (target) | Relation | Confidence / Evidence | factual |
|---|---|---|---|---|
| 1 | GAR-0015 → **PRD-0001** (1770年代英法服饰语境) | `context_includes` | high / verified | **true — factual** |
| 2 | PRD-0001 → **SRC-0150** (FIT 1770–1779 年代概览) | `claim_supported_by` | high / verified | **true — factual** |

- SRC IDs: hop 1 = **SRC-0150**; hop 2 = **SRC-0150**
- Classification: both edges factual — GAR-0015 is included in the 1770s British/French context, which is supported by the FIT source.

**Path 2 — DESIGN hop, then FACTUAL hop**
`GAR-0015` → `GAR-0024` → `SRC-0125`

| Hop | From → To (target) | Relation | Confidence / Evidence | factual |
|---|---|---|---|---|
| 1 | GAR-0015 → **GAR-0024** (穆勒鞋 / mules) | `ensemble_with` | medium / interpretive | **false — DESIGN** |
| 2 | GAR-0024 → **SRC-0125** (FIT：mule) | `claim_supported_by` | high / verified | **true — factual** |

- SRC IDs: hop 1 = **SRC-0150**; hop 2 = **SRC-0125**
- Classification: the GAR-0015↔GAR-0024 pairing is a designer-level inference (interpretive, not a sourced fact); the mule card's own claim is verified by the FIT mule source SRC-0125.
