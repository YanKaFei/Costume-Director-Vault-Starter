Command run from the Vault root; exit code 0.

```bash
python3 scripts/relation_trace.py --start GAR-0015 --max-depth 2 --json
```

**Start card (confirmed via `query.py --id GAR-0015`)**: `GAR-0015` — 法式长袍 / robe à la française, `evidence_status: verified`, card source `SRC-0116`. The trace returned 12 depth-2 paths over 12 related IDs; the engine reports itself as `read-only; no card writes`.

## Path 1 — Factual (verified evidence chain)

| Hop | Subject | Relation | Object | Confidence | Evidence | Factual | SRC |
|---|---|---|---|---|---|---|---|
| 1 | `PRD-0001` (1770 年代英法服饰语境) | `context_includes` | `GAR-0015` | high | verified | **true** | `SRC-0150` |
| 2 | `PRD-0001` | `in_style` | `STY-0010` (时代剧历史考据造型) | high | verified | **true** | `SRC-0167`, `SRC-0168`, `SRC-0169` |

Traversal note: the first edge is stored as `PRD-0001 → GAR-0015` because the trace walks the *incoming* `context_includes` edge from the start card — i.e. the 1770s context claims the robe à la française, then that period context sits in the historical-costume-drama style system. Both hops are `factual: true`, so this path is **factual**, not design inference.

## Path 2 — Design-only (interpretive pairing)

| Hop | Subject | Relation | Object | Confidence | Evidence | Factual | SRC |
|---|---|---|---|---|---|---|---|
| 1 | `GAR-0015` | `ensemble_with` | `GAR-0024` (穆勒鞋 / mule) | medium | interpretive | **false** | `SRC-0150` |
| 2 | `GAR-0024` | `claim_supported_by` | `SRC-0125` (FIT: mule) | high | verified | **true** | `SRC-0125` |

This path contains one **design-only** edge and one **factual** edge, so the *path as a whole is design-only*: the "these two pieces are worn together" claim is a styling suggestion (`interpretive`, medium confidence, `factual: false`), not a documented historical pairing. `SRC-0150` supports the period context, **not** the ensemble claim itself. Only the second hop — `GAR-0024` being documented by `SRC-0125` — is verified provenance for the shoe.

## Design-only vs factual — how to read the set

- The run's own limits say it plainly: `design_edges: "included and marked factual=false; use --factual-only to exclude"`, with `low_confidence: "filtered"`.
- Of the 12 returned paths, **7 begin with the factual `PRD-0001 → GAR-0015` context edge** (leads to `SRC-0150`, `STY-0010`, `GAR-0024`, `GAR-0025`, `GAR-0028`, `STR-0006`, `STR-0009`).
- **5 begin with the design-only `GAR-0015 → GAR-0024 ensemble_with` edge** (leads to `SRC-0125`, `PRD-0001`, `PRD-0002`, `PRD-0004`, `PRD-0005`). Those five all inherit `factual: false` at the first hop, even where the second hop is verified — a verified source about a shoe does not make "wear it with the gown" a fact.
- Per the skill contract, these are retrieval leads only: a design-only `ensemble_with` edge must not be cited as production evidence, and `GAR-0024`'s verified `SRC-0125` provenance must be kept separate from the styling inference.

**Consistency check**: `GAR-0024` appears both as a factual member of the 1770s context (`PRD-0001`, `SRC-0150`) and as a design-only ensemble partner of `GAR-0015` — so the shoe is period-appropriate evidence, while the specific gown+shoe combination remains an interpretive design decision.
