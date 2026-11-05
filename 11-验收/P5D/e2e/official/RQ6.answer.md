## Query run

Command (exactly as specified, from the Vault root):

```bash
python3 scripts/query.py --relation-type in_style --related-to STY-0010 --json
```

Exit code `0`, JSON array, **10 cards**. All returned rows are `type: look`; no garments, structures, materials or sources came back.

## Returned card IDs

| # | Card ID | Name (zh / en) | Card evidence | Card `source_ids` |
|---|---|---|---|---|
| 1 | `LOOK-0001` | 洛可可沙龙女主人 / rococo salon hostess look | `interpretive` | `SRC-0150` |
| 2 | `LOOK-0003` | 十六世纪欧洲宫廷男装 / 16th-century European court menswear look | `interpretive` | `SRC-0101`, `SRC-0103` |
| 3 | `LOOK-0005` | 1900 南方庄园女主人 / 1900 Southern plantation mistress look | `interpretive` | `SRC-0167`, `SRC-0153` |
| 4 | `LOOK-0008` | 1930 年代上海长衫知识分子 / 1930s Shanghai changshan intellectual look | `interpretive` | `SRC-0202`, `SRC-0203` |
| 5 | `LOOK-0009` | 1930 年代上海旗袍女性知识分子 / 1930s Shanghai qipao woman intellectual look | `interpretive` | `SRC-0200`, `SRC-0201`, `SRC-0205` |
| 6 | `LOOK-0010` | 急诊科护士夜班职业装 / emergency nurse night-shift uniform look | `interpretive` | `SRC-0400` |
| 7 | `LOOK-0012` | 1930 年代上海雨夜女记者 / 1930s Shanghai rainy-night woman journalist look | `interpretive` | `SRC-0200`, `SRC-0201`, `SRC-0205` |
| 8 | `LOOK-0013` | 加纳-英国婚礼新娘仪式造型 / Ghanaian-British wedding bride ceremonial look | `interpretive` | `SRC-0106`, `SRC-0431`, `SRC-0205`, `SRC-0408`, `SRC-0144`, `SRC-0145` |
| 9 | `LOOK-0014` | 1940 年代战后通勤女装 / 1940s postwar women's commute look | `interpretive` | `SRC-0412`, `SRC-0413`, `SRC-0405`, `SRC-0407` |
| 10 | `LOOK-0015` | 上海银行家之妻：从晚宴到难民 / Shanghai banker's wife: ballroom to refugee | `interpretive` | `SRC-0200`, `SRC-0201`, `SRC-0205`, `SRC-0412`, `SRC-0405`, `SRC-0407` |

All 10 paths resolve under `09-造型组合/` (e.g. `09-造型组合/LOOK-0008-1930年代上海长衫知识分子.md`). All have `score: 0.0` — this is membership listing, not ranked similarity.

## Real relation targets

**One single target for every row, and it is the queried card itself:**

- `STY-0010` — 时代剧历史考据造型 (period-drama historically-researched styling)
- `target_type: style`
- `target_path: 05-风格体系/STY-0010-时代剧历史考据造型.md`
- `rule: R-STY-EXACT`, `confidence: medium`, relation `evidence: interpretive`
- Direction: `subject_to_object` (LOOK → STY) on the candidate edges; the four card-origin stubs use `direction: outgoing`

No second style, period, region, garment or source is a target of an `in_style` edge in this result. Because the target is always the card you queried, this is a **self-referential membership lookup** — it does not cross-link styles to each other.

## Factual vs design

**Factual (direct tool output):**
- The 10 `LOOK-*` IDs, their names, paths, `evidence_status: interpretive`, and the `SRC-*` IDs listed above.
- Every `in_style` edge points to `STY-0010` at `05-风格体系/STY-0010-时代剧历史考据造型.md`; rule `R-STY-EXACT`; confidence `medium`.
- 4 cards (`LOOK-0001`, `LOOK-0009`, `LOOK-0012`, `LOOK-0015`) carry **two** relation objects: a card-origin stub with `source_ids: []`, plus a candidate edge with `SRC-0167`, `SRC-0168`, `SRC-0169` carrying `review_status: review_queue`.
- The other 6 cards carry only the candidate edge, also with `review_status: review_queue`.
- None of the 10 cards is `verified`; no `example` card was included (query default exclusion).

**Design / interpretive (must not be read as fact):**
- The `in_style` attribution itself is `interpretive`, not verified provenance. It is a **curator/design classification** — "this look is filed under period-drama historically-researched styling" — not evidence that the look is historically accurate.
- Each `LOOK-*` is an `interpretive` **assembly** (card text says the pieces cite verified cards but the combination is the library's design reasoning). "Verified garment inside" ≠ "verified complete look."
- Ten candidate edges sit in `review_queue`, so their style membership is **proposed, not accepted**.
- The card-origin stubs have empty `source_ids`, so the card-declared edge is **unsourced at relation level**; only the candidate edges carry `SRC-0167/0168/0169`.
- Treating these 10 as a coherent stylistic set would be a design inference: the set spans Rococo, 16th-century court, 1900 US South, 1930s Shanghai, contemporary emergency nursing, Ghanaian-British wedding and 1940s Britain. `STY-0010` is broad enough that membership **does not discriminate period, region or culture** — do not infer shared era/place from co-membership.

## Gaps

- No garment (`GAR-*`), structure (`STR-*`), material or source cards returned; to build an actual look, resolve each `LOOK-*` via `query.py --id LOOK-00xx --json` or go through `recommend.py`/`outfit.py`.
- `STY-0010`'s definition was not expanded by this command; the style's own card body and the meaning of `R-STY-EXACT` were not read.
- Read-only run; no files written. The duplicate card/candidate edge pattern is a data-hygiene observation only — not something I edited.
