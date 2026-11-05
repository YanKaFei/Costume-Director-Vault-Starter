## Relation trace result

Command run exactly:

```bash
python3 scripts/relation_trace.py --character "沙龙女主人" --json
```

**Look returned:** `LOOK-0001` — 洛可可沙龙女主人
- Path: `09-造型组合/LOOK-0001-洛可可沙龙女主人.md`
- Role: 1770 年代法国沙龙女主人（虚构角色，historical 模式）
- Evidence: `interpretive` · review status: `draft`
- Source: `SRC-0150` — `04-来源/SRC-0150-FIT-1770年代概览.md` — https://fashionhistory.fitnyc.edu/1770-1779/

### Item IDs with real paths

| ID | Name | Real path | Evidence |
|---|---|---|---|
| `GAR-0015` | 法式长袍 | `01-服装单品/连身/GAR-0015-法式长袍.md` | verified |
| `STR-0009` | 裙侧撑 | `02-结构细节/STR-0009-裙侧撑.md` | verified |
| `STR-0006` | 胸衣插片 | `02-结构细节/STR-0006-胸衣插片.md` | verified |
| `GAR-0028` | 手笼 | `01-服装单品/配饰/GAR-0028-手笼.md` | verified |
| `GAR-0024` | 穆勒鞋 | `01-服装单品/足部/GAR-0024-穆勒鞋.md` | verified |
| `MAT-0002` | 尚蒂伊蕾丝 | `03-材质纹样/材料/MAT-0002-尚蒂伊蕾丝.md` | verified |

All seven referenced paths were confirmed to exist inside the Vault.

### Prompts

**Image prompt**
> 1770s French salon hostess, robe à la française in cream silk brocade, panniers widening the skirt sideways, decorated stomacher, Chantilly lace trim, fur muff, silk mule slippers, candlelit interior, historical mode

**Negative prompt**
> no modern shoes, no machine lace, no zippers or visible elastic, no anachronistic jewelry, no changed pannier width between shots, no symmetrical wide skirt front

**Continuity lock**
> 裙侧撑宽度固定在同场次内不变；后方箱褶垂坠位置、stomacher 暴露形状、手笼与鞋的颜色保持一致；发饰高度不得在镜头间变化

### Conflicts

> 户外长途行走、奔跑与狭窄空间（panniers 与长裙限制动作）；现代都市场景；用普通裙撑替代 panniers 造成正面鼓起、轮廓错误；把该造型当作 1780s 后高腰新古典裙装。

### Approved anchors

**None returned.** The command did not include `--look-bible`, so the output contains no `approved_anchors` field. The look’s `continuity_lock` is the only locked continuity guidance in this result.

### Coverage gap noted in the look card

`LOOK-0001` states the KB has no 18th-century women’s headwear/wig card and no 18th-century stays card; those parts must not be invented.

### Trace limits

- Max depth: 3
- Low-confidence relations filtered
- Design/co-occurrence edges included but marked `factual=false`
- Engine: read-only; no card writes
