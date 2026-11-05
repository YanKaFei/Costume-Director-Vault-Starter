`python3 scripts/relation_trace.py --character "沙龙女主人" --json` ran successfully (**exit 0**). It returned one matching look.

## Look

| Field | Value |
|---|---|
| look_id | **LOOK-0001** |
| path | `09-造型组合/LOOK-0001-洛可可沙龙女主人.md` |
| name_zh | 洛可可沙龙女主人 |
| role | 1770 年代法国沙龙女主人（虚构角色，historical 模式） |
| evidence | interpretive |
| source_ids | SRC-0150 |

## Item IDs and paths

| ID | Name | Path | Evidence |
|---|---|---|---|
| GAR-0015 | 法式长袍 | `01-服装单品/连身/GAR-0015-法式长袍.md` | verified |
| STR-0009 | 裙侧撑 | `02-结构细节/STR-0009-裙侧撑.md` | verified |
| STR-0006 | 胸衣插片 | `02-结构细节/STR-0006-胸衣插片.md` | verified |
| GAR-0028 | 手笼 | `01-服装单品/配饰/GAR-0028-手笼.md` | verified |
| GAR-0024 | 穆勒鞋 | `01-服装单品/足部/GAR-0024-穆勒鞋.md` | verified |
| MAT-0002 | 尚蒂伊蕾丝 | `03-材质纹样/材料/MAT-0002-尚蒂伊蕾丝.md` | verified |

## Continuity lock

> 裙侧撑宽度固定在同场次内不变；后方箱褶垂坠位置、stomacher 暴露形状、手笼与鞋的颜色保持一致；发饰高度不得在镜头间变化

## Approved anchors

**None returned.** This exact invocation did not use `--look-bible`, so the JSON contains no `approved_anchors` field. Approved anchors are only loaded when a look-bible file is explicitly supplied with that option.

## Additional look data

- **Prompt (image):** `1770s French salon hostess, robe à la française in cream silk brocade, panniers widening the skirt sideways, decorated stomacher, Chantilly lace trim, fur muff, silk mule slippers, candlelit interior, historical mode`
- **Prompt (negative):** `no modern shoes, no machine lace, no zippers or visible elastic, no anachronistic jewelry, no changed pannier width between shots, no symmetrical wide skirt front`
- **Conflicts:** 户外长途行走、奔跑与狭窄空间（panniers 与长裙限制动作）；现代都市场景；用普通裙撑替代 panniers 造成正面鼓起、轮廓错误；把该造型当作 1780s 后高腰新古典裙装。
