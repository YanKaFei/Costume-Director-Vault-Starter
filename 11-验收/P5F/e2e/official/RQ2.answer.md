## Query result

Exact command run: `python3 scripts/query.py --relation-type in_style --related-to STY-0010 --json`

**Returned cards — 10 (the query's default `--limit` is 10):**

| # | Card ID | Name (zh) | Type | Evidence |
|---|---|---|---|---|
| 1 | LOOK-0001 | 洛可可沙龙女主人 | look | interpretive |
| 2 | LOOK-0003 | 十六世纪欧洲宫廷男装 | look | interpretive |
| 3 | LOOK-0005 | 1900 南方庄园女主人 | look | interpretive |
| 4 | LOOK-0008 | 1930 年代上海长衫知识分子 | look | interpretive |
| 5 | LOOK-0009 | 1930 年代上海旗袍女性知识分子 | look | interpretive |
| 6 | LOOK-0010 | 急诊科护士夜班职业装 | look | interpretive |
| 7 | LOOK-0012 | 1930 年代上海雨夜女记者 | look | interpretive |
| 8 | LOOK-0013 | 加纳-英国婚礼新娘仪式造型 | look | interpretive |
| 9 | LOOK-0014 | 1940 年代战后通勤女装 | look | interpretive |
| 10 | LOOK-0015 | 上海银行家之妻：从晚宴到难民 | look | interpretive |

**Real relation target (identical for every returned row):**
- `STY-0010` — 时代剧历史考据造型 / period drama historical costume
- Type: `style`; path: `05-风格体系/STY-0010-时代剧历史考据造型.md`
- Card evidence status: **verified**, sources `SRC-0167`, `SRC-0168`, `SRC-0169`

**Relation provenance, per row:**
- Relation type `in_style`, evidence `interpretive`, confidence `medium`, rule `R-STY-EXACT`, direction from look → style.
- Declared in the look card's own YAML (`origin: card`): **LOOK-0001, LOOK-0009, LOOK-0012, LOOK-0015** only.
- All 10 also carry a `review_queue` candidate row from `11-验收/P5/RELATION-CANDIDATES.csv`; for LOOK-0003, LOOK-0005, LOOK-0008, LOOK-0010, LOOK-0013, LOOK-0014 the candidate row is the only source of the link.

**Scope note:** with the default limit lifted, the same filter yields 29 cards (including LOOK-0016/0018/0019/0020/0022, PRD-0001/0010, and 12 SCN cards); the exact command above therefore reports the first 10 only. The target `STY-0010` is a real, verified style card in all cases — the `in_style` links themselves are interpretive, medium-confidence design associations, not verified provenance.
