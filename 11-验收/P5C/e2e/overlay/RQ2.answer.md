## 运行结果：`relation_trace.py --character "沙龙女主人" --json`

引擎参数：max_depth=3；低置信关系已过滤；设计边保留并标记 `factual=false`；只读，未写入卡片。命中 **1 个造型**。

## 完整造型（Look）

**LOOK-0001 — 洛可可沙龙女主人**
- 卡片路径：`09-造型组合/LOOK-0001-洛可可沙龙女主人.md` ✅ 已核实存在
- 角色设定：1770 年代法国沙龙女主人（虚构角色，historical 模式）
- 造型证据等级：**interpretive**；来源：**SRC-0150**

全部 6 个单品（均为 `verified`，路径均已核实存在）：

| 物品 ID | 名称 | 真实卡片路径 |
| --- | --- | --- |
| GAR-0015 | 法式长袍 | `01-服装单品/连身/GAR-0015-法式长袍.md` |
| STR-0009 | 裙侧撑（panniers） | `02-结构细节/STR-0009-裙侧撑.md` |
| STR-0006 | 胸衣插片（stomacher） | `02-结构细节/STR-0006-胸衣插片.md` |
| GAR-0028 | 手笼（muff） | `01-服装单品/配饰/GAR-0028-手笼.md` |
| GAR-0024 | 穆勒鞋（mules） | `01-服装单品/足部/GAR-0024-穆勒鞋.md` |
| MAT-0002 | 尚蒂伊蕾丝 | `03-材质纹样/材料/MAT-0002-尚蒂伊蕾丝.md` |

## 图像 / 视频提示词

**Image prompt:**
> 1770s French salon hostess, robe à la française in cream silk brocade, panniers widening the skirt sideways, decorated stomacher, Chantilly lace trim, fur muff, silk mule slippers, candlelit interior, historical mode

**Negative prompt:**
> no modern shoes, no machine lace, no zippers or visible elastic, no anachronistic jewelry, no changed pannier width between shots, no symmetrical wide skirt front

**Video prompt：** 该命令输出中**未提供独立的视频提示词**（仅有 image + negative；负面提示词中含跨镜头连续性约束，可直接用于视频生成）。

## 冲突（Conflicts）

- 户外长途行走、奔跑与狭窄空间：panniers 与长裙限制动作
- 现代都市场景不适用
- 用普通裙撑替代 panniers 会造成正面鼓起、轮廓错误
- 不可把该造型当作 1780s 之后的高腰新古典裙装

## 连续性锁定 / 锚点（Anchors）

输出中**没有单独的 "approved anchors" 字段**；最接近的是该 look 的 `continuity_lock`：

> 裙侧撑宽度固定在同场次内不变；后方箱褶垂坠位置、stomacher 暴露形状、手笼与鞋的颜色保持一致；发饰高度不得在镜头间变化。

即跨镜头锚定项：① panniers（STR-0009）宽度；② 后箱褶垂坠位置；③ stomacher（STR-0006）暴露形状；④ 手笼（GAR-0028）与穆勒鞋（GAR-0024）颜色；⑤ 发饰高度。除该 continuity_lock 外，无其他经批准的锚点记录。
