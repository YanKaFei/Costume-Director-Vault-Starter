## Query: `--relation-type in_style --related-to STY-0010`

**10 cards returned** (all type `look`, evidence `interpretive`):

| Card ID | Name | Real card-declared relation (`origin: card`) | Candidate-only relation (`origin: candidate`, `review_queue`) |
|---|---|---|---|
| LOOK-0001 | 洛可可沙龙女主人 | ✅ → STY-0010 | ✅ also queued |
| LOOK-0003 | 十六世纪欧洲宫廷男装 | — | ✅ |
| LOOK-0005 | 1900 南方庄园女主人 | — | ✅ |
| LOOK-0008 | 1930 年代上海长衫知识分子 | — | ✅ |
| LOOK-0009 | 1930 年代上海旗袍女性知识分子 | ✅ → STY-0010 | ✅ also queued |
| LOOK-0010 | 急诊科护士夜班职业装 | — | ✅ |
| LOOK-0012 | 1930 年代上海雨夜女记者 | ✅ → STY-0010 | ✅ also queued |
| LOOK-0013 | 加纳-英国婚礼新娘仪式造型 | — | ✅ |
| LOOK-0014 | 1940 年代战后通勤女装 | — | ✅ |
| LOOK-0015 | 上海银行家之妻：从晚宴到难民 | ✅ → STY-0010 | ✅ also queued |

**Real relation target** (identical for every relation, both origins):
- **STY-0010 — 时代剧历史考据造型** (type: `style`)
- Path: `05-风格体系/STY-0010-时代剧历史考据造型.md`
- Relation: `in_style`, rule `R-STY-EXACT`, evidence `interpretive`, confidence `medium`

**Key distinction:**
- **4 cards carry a real, card-embedded `in_style → STY-0010` relation** (direction `outgoing`, `origin: card`): **LOOK-0001, LOOK-0009, LOOK-0012, LOOK-0015**.
- **6 cards have NO card-declared relation** — they appear only through unreviewed machine candidates (`origin: candidate`, `review_status: review_queue`, backed by SRC-0167/SRC-0168/SRC-0169): **LOOK-0003, LOOK-0005, LOOK-0008, LOOK-0010, LOOK-0013, LOOK-0014**. These are inferred links, not confirmed card relations.
