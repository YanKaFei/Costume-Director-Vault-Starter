## Command executed (exact)

```bash
python3 scripts/query.py --relation-type in_style --related-to STY-0010 --json
```

Exit code **0** — 10 cards returned, all **`type: look`**, all **`evidence_status: interpretive`**. Note: the relation query returns **looks**, not garments; garment-level evidence must be traced through each look's relations.

## Style → garment evidence

**Style: `STY-0010` — 时代剧历史考据造型 / historical period-drama research-based styling** (`05-风格体系/STY-0010-时代剧历史考据造型.md`)

Looks returned as `in_style` STY-0010:

| Look | Name | Evidence | Source IDs |
|---|---|---|---|
| LOOK-0001 | 洛可可沙龙女主人 / rococo salon hostess look | interpretive | SRC-0150 |
| LOOK-0003 | 16th-century European court menswear | interpretive | SRC-0101, SRC-0103 |
| LOOK-0005 | 1900 Southern plantation mistress | interpretive | SRC-0167, SRC-0153 |
| LOOK-0008 | 1930s Shanghai changshan intellectual | interpretive | SRC-0202, SRC-0203 |
| **LOOK-0009** | **1930s Shanghai qipao woman intellectual** | interpretive | SRC-0200, SRC-0201, SRC-0205 |
| LOOK-0010 | emergency nurse night-shift uniform | interpretive | SRC-0400 |
| **LOOK-0012** | **1930s Shanghai rainy-night woman journalist** | interpretive | SRC-0200, SRC-0201, SRC-0205 |
| LOOK-0013 | Ghanaian-British wedding bride | interpretive | SRC-0106, SRC-0431, SRC-0205, SRC-0408, SRC-0144, SRC-0145 |
| LOOK-0014 | 1940s postwar women's commute | interpretive | SRC-0412, SRC-0413, SRC-0405, SRC-0407 |
| **LOOK-0015** | **Shanghai banker's wife: ballroom to refugee** | interpretive | SRC-0200, SRC-0201, SRC-0205, SRC-0412, SRC-0405, SRC-0407 |

All `in_style` edges are **interpretive / medium confidence**; candidate-origin edges carry `review_status: review_queue` and are not finalized provenance.

**The garment reached via this style (evidence chain for GAR-0015):**

- **`GAR-0015` — 法式长袍 / robe à la française**, `type: garment`, **`evidence_status: verified`**, path `01-服装单品/连身/GAR-0015-法式长袍.md`
  - Card definition: **18th-century European women's dress** — fitted front, loose back with two box pleats falling from shoulder to floor (sack back), open front revealing a decorated stomacher and petticoat, worn with side hoops (panniers).
  - `claim_supported_by` → **SRC-0116** (FIT: robe à la française) — **verified / high confidence**.
  - Period anchor: **PRD-0001 — 1770年代英法服饰语境 / 1770s France and Britain dress context** → `context_includes` GAR-0015 — **verified / high confidence** (SRC-0150).
  - Reached through the style via **LOOK-0001** (rococo salon hostess) `appears_in_look` GAR-0015 — interpretive / medium (SRC-0150, SRC-0116).
  - Other GAR-0015 relations: `may_have_part` STR-0006 (stomacher), STR-0009 (side hoop); `ensemble_with` GAR-0024 (mules), GAR-0028 (muff). **No relation to any qipao card or to PRD-0007 exists.**

**For contrast — the actual qipao evidence in the KB:**
- **`GAR-0031` — 旗袍 / qipao**, **verified**, `claim_supported_by` **SRC-0200** (V&A: qipao, Sun Sun Company, Shanghai, ca. 1930) and **SRC-0201** (V&A: Chinese silk-damask qipao, late 1930s) — verified / high.
- Its period anchor is **PRD-0011 — 1930年代上海民国语境 / 1930s Shanghai Republican-era context** (`context_includes` GAR-0031, verified / high).
- It appears in LOOK-0009, LOOK-0012, LOOK-0015, LOOK-0019 — all 1930s (or cross-cultural London) settings, none 1950s.

## Explicit refusal: GAR-0015 cannot be asserted as a 1950s Shanghai qipao

**I refuse to make that assertion.** `query.py` and PRD-0007 provide no support for it; the claim fails on three independent, sourced grounds:

1. **Wrong period.** GAR-0015 is a verified **18th-century** garment anchored to **PRD-0001 (1770s France/Britain)** with high-confidence verified evidence (SRC-0116, SRC-0150). It is two centuries removed from the 1950s.
2. **Wrong region and wrong period card.** **PRD-0007 — 1950年代美英战后语境 / 1950s postwar America and Britain context** (verified, SRC-0115) is explicitly scoped to the **United States and Britain**, not Shanghai. Its `context_includes` edges cover only GAR-0006 (dashiki), GAR-0014 (jeans), GAR-0023 (moccasins), and MAT-0004 (Lurex) — **GAR-0015 is not among them, and no relation of any type links GAR-0015 to PRD-0007**.
3. **Wrong garment type.** A qipao is a separate verified card, **GAR-0031**, with a mandarin collar, frog closures (STR-0011), and a fitted tubular cut — structurally unrelated to the robe à la française's sack-back pleats, stomacher, and panniers. No relation path exists between GAR-0015 and GAR-0031.

Additionally, **no `1950s Shanghai` period/region card exists in the KB at all** (full PRD list runs PRD-0001–PRD-0011; the only Shanghai card is PRD-0011, which is **1930s**). Asserting a 1950s Shanghai qipao attribution for GAR-0015 would require fabricating a period, a region, a garment identity, and a source — none of which query.py returns.

**Supportable statement:** GAR-0015 is a verified **18th-century (1770s) French robe à la française** (SRC-0116; anchored in PRD-0001), usable within the interpretive LOOK-0001 rococo salon hostess look under STY-0010. A Shanghai qipao claim belongs to **GAR-0031 under PRD-0011 (1930s Shanghai)**, sourced to SRC-0200/SRC-0201 — and even that evidence is for the 1930s, never the 1950s.
