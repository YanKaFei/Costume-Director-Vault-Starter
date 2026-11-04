## Lookup result

Command run exactly as requested:

```bash
python3 scripts/relation_trace.py --character "沙龙女主人" --json
```

Exit code `0`. One look returned (`LOOK-0001`). Engine is read-only; low-confidence relations filtered; max depth 3.

## Complete look

- **look_id:** `LOOK-0001`
- **look card:** `09-造型组合/LOOK-0001-洛可可沙龙女主人.md`
- **Name:** 洛可可沙龙女主人 / rococo salon hostess look
- **Role:** 1770 年代法国沙龙女主人（虚构角色，historical 模式）
- **Look evidence:** `interpretive`
- **Source:** `SRC-0150` — FIT Fashion History Timeline, 1770–1779 ([link](https://fashionhistory.fitnyc.edu/1770-1779/))

| # | Item ID | Card name | Real card path | Evidence |
|---|---|---|---|---|
| 1 | `GAR-0015` | 法式长袍 / robe à la française | `01-服装单品/连身/GAR-0015-法式长袍.md` | verified |
| 2 | `STR-0009` | 裙侧撑 / panniers | `02-结构细节/STR-0009-裙侧撑.md` | verified |
| 3 | `STR-0006` | 胸衣插片 / stomacher | `02-结构细节/STR-0006-胸衣插片.md` | verified |
| 4 | `GAR-0028` | 手笼 / muff | `01-服装单品/配饰/GAR-0028-手笼.md` | verified |
| 5 | `GAR-0024` | 穆勒鞋 / mule | `01-服装单品/足部/GAR-0024-穆勒鞋.md` | verified |
| 6 | `MAT-0002` | 尚蒂伊蕾丝 / Chantilly lace | `03-材质纹样/材料/MAT-0002-尚蒂伊蕾丝.md` | verified |

All six paths exist and pass `scripts/path_guard.py check` (`ALLOW`).

**Construction/design:** cream silk-brocade robe à la française with fitted front and two shoulder-to-hem box pleats at the back; panniers widening the skirt sideways while keeping front/back relatively flat; decorated stomacher filling the open front; Chantilly lace at neckline/cuffs; fur muff; silk mule slippers. Intended for candlelit 1770s French salon interiors.

## Prompts

**Image prompt** (exact `prompt_image` from the trace):

```text
1770s French salon hostess, robe à la française in cream silk brocade, panniers widening the skirt sideways, decorated stomacher, Chantilly lace trim, fur muff, silk mule slippers, candlelit interior, historical mode
```

**Negative prompt** (exact `prompt_negative`):

```text
no modern shoes, no machine lace, no zippers or visible elastic, no anachronistic jewelry, no changed pannier width between shots, no symmetrical wide skirt front
```

**Video prompt:** none available. `LOOK-0001` has no `prompt_video` field, and this command emits only `prompt_image` / `prompt_negative`. No video prompt was returned, so none is reported.

**Continuity lock (card-level, not an approved anchor):**

```text
裙侧撑宽度固定在同场次内不变；后方箱褶垂坠位置、stomacher 暴露形状、手笼与鞋的颜色保持一致；发饰高度不得在镜头间变化
```

## Conflicts

Trace-returned conflict string:

```text
户外长途行走、奔跑与狭窄空间（panniers 与长裙限制动作）；现代都市场景；用普通裙撑替代 panniers 造成正面鼓起、轮廓错误；把该造型当作 1780s 后高腰新古典裙装。
```

Broken out:

1. **Movement/location conflict** — outdoor long walking, running, and narrow spaces; panniers plus a floor-length gown restrict stride and turning radius.
2. **Period/setting conflict** — modern urban settings are incompatible with the 1770s silhouette.
3. **Construction substitution conflict** — using an ordinary hoop skirt instead of panniers produces front fullness and the wrong silhouette; panniers must widen sideways with a relatively flat front/back.
4. **Period misreading conflict** — this is not the post-1780s high-waisted neoclassical dress.

Additional integrity notes:

- The **look combination is `interpretive`**, not verified. The six item cards are individually `verified`, but the ensemble itself is a design inference and is not tied to a surviving garment or real person.
- `SRC-0150` supports the 1770s context for the robe à la française and panniers; it does not certify one exact ensemble, year, or maker.
- **Coverage gap:** the look card states there is no 18th-century women’s headwear/wig card and no 18th-century stays card. The continuity lock nevertheless locks “发饰高度” (headdress height), so headwear is an unresolved layer — it cannot be specified from the KB.
- **Palette nuance:** `MAT-0002` is canonically black/ivory silk Chantilly lace, while the look palette is cream/pastel/gold. The prompt says only “Chantilly lace trim” without a color; if a single color must be locked, state “ivory” explicitly.

## Approved anchors

**None.** This run passed no `--look-bible`, so no `approved_anchors` key was emitted and no approved hard/soft anchors exist for `LOOK-0001`. The vault’s Look Bible template (`projects/_template/look-bible/look-bible.json`) has empty `approved_anchors` arrays and a sample look unrelated to `LOOK-0001`; it is not approval data for this look.

The only locked data attached to this look is the card’s `continuity_lock` quoted above — that is a continuity constraint, not a Look Bible approval.
