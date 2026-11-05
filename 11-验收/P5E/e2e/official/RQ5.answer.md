## 关系追溯结果：沙龙女主人

命令按原样执行，退出码是 `0`。

## Look

- **look_id**: `LOOK-0001`
- **name**: 洛可可沙龙女主人
- **path**: `09-造型组合/LOOK-0001-洛可可沙龙女主人.md`
- **role**: 1770 年代法国沙龙女主人（虚构角色，historical 模式）
- **look evidence**: `interpretive`；来源：`SRC-0150`

## Items (6)

| ID | 类型 | 名称 | Path | 证据状态 |
|---|---|---|---|---|
| GAR-0015 | 服装单品 | 法式长袍 | `01-服装单品/连身/GAR-0015-法式长袍.md` | verified |
| STR-0009 | 结构细节 | 裙侧撑 | `02-结构细节/STR-0009-裙侧撑.md` | verified |
| STR-0006 | 结构细节 | 胸衣插片 | `02-结构细节/STR-0006-胸衣插片.md` | verified |
| GAR-0028 | 服装单品·配饰 | 手笼 | `01-服装单品/配饰/GAR-0028-手笼.md` | verified |
| GAR-0024 | 服装单品·足部 | 穆勒鞋 | `01-服装单品/足部/GAR-0024-穆勒鞋.md` | verified |
| MAT-0002 | 材质纹样 | 尚蒂伊蕾丝 | `03-材质纹样/材料/MAT-0002-尚蒂伊蕾丝.md` | verified |

以上 7 个路径都已在 Vault 中确认存在。

## Continuity lock

> 裙侧撑宽度固定在同场次内不变；后方箱褶垂坠位置、stomacher 暴露形状、手笼与鞋的颜色保持一致；发饰高度不得在镜头间变化

## Approved anchors

**没有**，本次结果中没有 `approved_anchors` 字段。

`relation_trace.py` 只有在传入 `--look-bible` 时才会输出该字段；本次执行没有传入。Vault 中现有的 look-bible 文件（`demo`、`selfapprove`、`_template` 项目）也没有被加载，其中没有针对 `LOOK-0001` 或沙龙女主人的已批准锚点。
