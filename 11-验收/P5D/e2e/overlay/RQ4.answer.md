**Command run:** `python3 scripts/relation_trace.py --start GAR-0015 --max-depth 2 --json` (read-only engine; low-confidence filtered; design edges included and marked `factual=false`).

## Path 1 — FACTUAL (both hops)
`SRC-0150 → PRD-0001 → GAR-0015`

1. `PRD-0001`（1770 年代英法服饰语境）—`context_includes`→ **GAR-0015** — high / verified / **factual=true**, SRC: **SRC-0150**（FIT 1770–1779 年代概览）
2. `PRD-0001` —`claim_supported_by`→ **SRC-0150** — high / verified / **factual=true**

→ Entirely factual: period-context inclusion and source backing are both verified evidence.

## Path 2 — DESIGN-ONLY first hop, factual second hop
`GAR-0015 → GAR-0024 → SRC-0125`

1. **GAR-0015** —`ensemble_with`→ `GAR-0024`（穆勒鞋 / mules）— medium / interpretive / **factual=false** ⟵ **design-only edge** (a stylist pairing inference, citing SRC-0150, not a verified historical claim)
2. `GAR-0024` —`claim_supported_by`→ **SRC-0125**（FIT：mule）— high / verified / **factual=true**

→ Mixed: the ensemble suggestion GAR-0015↔GAR-0024 is design-only/interpretive; only GAR-0024's own provenance (SRC-0125) is factual. Per the trace's limits flag, excluding design edges requires `--factual-only`.
