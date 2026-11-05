## 沙龙女主人 → Complete outfit

**LOOK-0001 — 洛可可沙龙女主人 (Rococo salon hostess)**
`09-造型组合/LOOK-0001-洛可可沙龙女主人.md`
Role: 1770s French salon hostess (fictional character, historical mode)

| Slot | ID | Item | Card evidence |
|---|---|---|---|
| Gown | GAR-0015 | 法式长袍 (robe à la française) | verified |
| Structure | STR-0009 | 裙侧撑 (panniers) | verified |
| Structure | STR-0006 | 胸衣插片 (stomacher) | verified |
| Accessory | GAR-0028 | 手笼 (muff) | verified |
| Footwear | GAR-0024 | 穆勒鞋 (mule slippers) | verified |
| Material | MAT-0002 | 尚蒂伊蕾丝 (Chantilly lace) | verified |

Image prompt: *1770s French salon hostess, robe à la française in cream silk brocade, panniers widening the skirt sideways, decorated stomacher, Chantilly lace trim, fur muff, silk mule slippers, candlelit interior, historical mode*
Negative: no modern shoes, no machine lace, no zippers/visible elastic, no anachronistic jewelry, no changed pannier width between shots, no symmetrical wide skirt front.

## Continuity lock
- Pannier (STR-0009) width fixed, unchanged within the same scene.
- Back box-pleat drape position, exposed stomacher shape, muff and shoe colors stay consistent.
- Hair-ornament height must not change between shots.
- Conflicts flagged: long outdoor walking/running and narrow spaces (panniers + long skirt restrict movement); modern urban settings; substituting a generic hoopskirt for panniers (wrong front-bulging silhouette); treating the look as post-1780s high-waisted neoclassical dress.

## Approved anchors
**None.**
- relation_trace: `approved_anchors.hard = []`, `approved_anchors.soft = []`
- candidate_review (--design-only): 239 candidates reviewed (39 source_verifiable, 163 needs_human, 37 reject_or_rework); **auto_promotions = 0, card_writes = 0**; policy: NEVER auto-promote medium/review to high/verified. Anchors require human approval; nothing was locked.

## Fact / design / interpretation separation
- **Fact (verified cards):** the six component cards GAR-0015, STR-0009, STR-0006, GAR-0028, GAR-0024, MAT-0002 are individually `verified`.
- **Interpretation (look level):** LOOK-0001 itself is evidence = **interpretive**, tied to **SRC-0150**; the "1770s French salon hostess, historical mode" assembly is an interpretive composition, not a verified ensemble. Design edges are included but explicitly marked `factual=false` (max depth 3; low-confidence filtered; engine read-only, no card writes).
- **Design constraints (not facts):** the continuity lock and the action/period conflict list are design-direction rules. The candidate review is design-only triage — 39 candidates are source-verifiable pending review, but none is promoted or constitutes approved evidence/anchors.
