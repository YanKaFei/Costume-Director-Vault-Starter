## Brief
- **Character queried:** 沙龙女主人 (salon hostess)
- **Look bible:** `projects/_template/look-bible/versions/SAMPLE-M1-A/v5.json`
- **Retrieved role:** 1770s French salon hostess, fictional character, `historical` mode
- **Period/region:** 1770s / France (stated in the look role, not separately supplied by a script)
- **Unknowns:** production title, scene/stage assignment, budget, structured palette, wearer age/class detail beyond the role line. Not invented.
- Both commands exited `0`; `relation_trace` reports a read-only engine, and `candidate_review` reports `card_writes: 0`.

## Character → complete outfit
Single retrieved look: **LOOK-0001 — 洛可可沙龙女主人** (`09-造型组合/LOOK-0001-洛可可沙龙女主人.md`). No A/B/C alternatives were returned by this trace.

| Slot | ID | Name | Evidence |
|---|---|---|---|
| Main garment | `GAR-0015` | 法式长袍 (robe à la française) | verified |
| Structure | `STR-0009` | 裙侧撑 (panniers) | verified |
| Structure | `STR-0006` | 胸衣插片 (stomacher) | verified |
| Accessory | `GAR-0028` | 手笼 (muff) | verified |
| Footwear | `GAR-0024` | 穆勒鞋 (mule slippers) | verified |
| Material | `MAT-0002` | 尚蒂伊蕾丝 (Chantilly lace) | verified |

- **Look-level evidence:** `interpretive`; **source:** `SRC-0150`.
- **Outfit as recorded is complete for these six slots** (garment, two structural pieces, accessory, footwear, material). No outerwear, headwear, jewelry, or underpinning item is listed, and none was added.
- **Prompt-level description (design text, not structured card data):** cream silk brocade robe, panniers widening the skirt sideways, decorated stomacher, Chantilly lace trim, fur muff, silk mule slippers, candlelit interior.
- **Negative prompt (design constraint):** no modern shoes, no machine lace, no zippers or visible elastic, no anachronistic jewelry, no changed pannier width between shots, no symmetrical wide skirt front.

## Continuity lock
Exact returned lock:

> 裙侧撑宽度固定在同场次内不变；后方箱褶垂坠位置、stomacher 暴露形状、手笼与鞋的颜色保持一致；发饰高度不得在镜头间变化

Meaning: pannier width fixed within the same scene; back box-pleat drape position, visible stomacher shape, muff color, and shoe color kept consistent; hair-ornament height must not change between shots.

Gaps inside the lock itself:
- It locks **hair-ornament height**, but no hair ornament/headwear item appears in LOOK-0001 — the constrained element has no ID. It was not invented.
- It locks **muff and shoe color**, but the trace supplies no structured color values for `GAR-0028` or `GAR-0024`; “cream / fur / silk” exists only in the prompt text. The lock currently has no numeric or named color baseline.

## Approved anchors
```json
"approved_anchors": { "hard": [], "soft": [] }
```
**No approved anchors were returned — neither hard nor soft.** This run therefore provides no anchor IDs sanctioned for cross-scene carry-over. I did not promote the six look items, the continuity lock, or `SRC-0150` into anchors; an anchor claim would require an explicit approved-anchor entry, which is absent.

Practical consequence: continuity for this character currently rests only on the lock text above, not on an approved anchor set. That is a pre-shoot gap, not a design result.

## Candidate review (`--design-only`)
| Metric | Value |
|---|---|
| Input | `11-验收/P5D/DESIGN-QUEUE-REMAINING.csv` |
| Candidates | 239 |
| Reviewed | 239 |
| `source_verifiable` | 39 |
| `needs_human` | 163 |
| `reject_or_rework` | 37 |
| `design_only` | 239 |
| `auto_promotions` | 0 |
| `card_writes` | 0 |

Policy returned: `NEVER auto-promote medium/review to high/verified`. This is a queue-level QA/process report; it is **not** evidence about LOOK-0001 and does not approve, rank, or alter that outfit.

## Fact / design / interpretation separation
**Facts (query + command output)**
- Character string `沙龙女主人`; look `LOOK-0001`; role “1770s French salon hostess (fictional, historical mode)”.
- The six item IDs, their names, paths, and `verified` statuses.
- Look-level `evidence: interpretive`; `source_ids: ["SRC-0150"]`.
- Continuity-lock text, the listed conflicts, and trace limits (`max_depth: 3`, low-confidence filtered, design edges marked `factual=false`, read-only).
- Candidate-review counts above, with zero card writes/promotions.

**Card evidence**
- Six individually `verified` cards; one look-level source `SRC-0150`. Verified item cards attest the pieces, not that this exact 1770s ensemble is documentary.

**Design decisions**
- `prompt_image`, `prompt_negative`, the continuity lock wording, and the conflicts list are designer/constraint artifacts. “Cream silk brocade,” “candlelit interior,” and the negative-prompt rules are design specifications, not cited historical facts.

**Interpretation**
- “Rococo salon hostess” as a character reading, and the assembly of these six cards into one 1770s French look, are interpretive. This is consistent with the look’s `evidence: interpretive` despite every component being `verified` — component verification does not upgrade the combination.

## Conflicts and gaps
- **Conflicts returned:** outdoor long-distance walking/running and narrow spaces (panniers and long skirt restrict movement); modern urban settings; substituting an ordinary skirt support for panniers, causing front bulge and wrong silhouette; treating this look as post-1780s high-waisted neoclassical dress.
- **Approved anchors:** empty (`hard: []`, `soft: []`) — no cross-scene anchor IDs available.
- **Lock references an unlisted hair ornament** and color invariants with no baseline values.
- **No structured palette**; only prompt prose.
- **One look only**, no A/B/C differentiation to evaluate, and no scene/stage mapping in the output.
- **Candidate review** is unrelated to this character’s outfit and cannot be used as approval evidence for it.
