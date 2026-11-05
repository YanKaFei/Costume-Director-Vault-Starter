## Relation trace — `GAR-0015` (法式长袍 / robe à la française), `--max-depth 2 --json`

Command completed with **exit code 0**. Start card is `GAR-0015` (`01-服装单品/连身/GAR-0015-法式长袍.md`, verified; its own card source is `SRC-0116`). Edge provenance below comes from the trace, not from that card source.

### Path 1 — factual chain (both hops verified)

| Hop | From → To | Relation | Confidence | Evidence | Factual | SRC |
|---|---|---|---|---|---|---|
| 1 | `PRD-0001` (1770 年代英法服饰语境) → `GAR-0015` | `context_includes` | high | verified | **true** | `SRC-0150` |
| 2 | `PRD-0001` → `STY-0010` (时代剧历史考据造型) | `in_style` | high | verified | **true** | `SRC-0167`, `SRC-0168`, `SRC-0169` |

**Label: FACTUAL.** `PRD-0001` is documented as including `GAR-0015`, and `PRD-0001` is documented as sitting in the `STY-0010` style system, each backed by a verified source card. This is a sourced context/style claim — it does **not** assert that every 1770s ensemble must use this garment.

### Path 2 — design chain (design edge, then verified source)

| Hop | From → To | Relation | Confidence | Evidence | Factual | SRC |
|---|---|---|---|---|---|---|
| 1 | `GAR-0015` → `GAR-0024` (穆勒鞋 / mule) | `ensemble_with` | medium | interpretive | **false** | `SRC-0150` |
| 2 | `GAR-0024` → `SRC-0125` (FIT：mule) | `claim_supported_by` | high | verified | **true** | `SRC-0125` |

**Label: DESIGN (interpretive), not factual.** The `GAR-0015` + `GAR-0024` pairing is a medium-confidence, `factual=false` styling suggestion for a coherent period look; it is not a documented historical rule. The second hop is factual only about the mule card's own support (`SRC-0125`) — that support does not upgrade the pairing itself to fact.

### Reading rule

- Treat Path 1 as **evidence-backed context** and Path 2 as **design inference**: usable for proposing an outfit, never citable as proof that robe à la française was worn with mules.
- `factual=true` describes the provenance of the edge, not the aesthetic necessity of the combination.
- No IDs or `SRC-*` above are inferred; all are from the trace/`query.py` output.
