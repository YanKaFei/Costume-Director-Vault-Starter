# 《麦克白》麦克白三阶段 A/B/C 造型（costume-director）

已运行：`workflow.py`（4 场/3 阶段，exit 0）+ 三阶段 `recommend.py`（`abc_distinct=true`）+ `query.py` 逐卡核验。产物在 `projects/macbeth-3stages/outputs/`。

## Brief
11 世纪苏格兰（莎剧）；inspired；当代艺术剧场/暗黑古装片；预算 medium。未知：季候、实战铠甲供给。

## 场景造型表（Macbeth；女巫由脚本误识别，已剔除）
| 阶段 | 场次 | A（战功） | B（仪礼/伪装） | C（毁灭） | 状态 |
|---|---|---|---|---|---|
| 1 战功 | 1-3 | 0075+0080+0081+0082 | +0076 斗篷 | 0079‡+0080+0081 | 湿/战损/泥 |
| 2 弑君 | 2-1/2-2 | 0078+0075+0081+0082 | 0075+0076+0081 | 0079‡+0081+0082 | 干/血渍 |
| 3 覆灭 | 5-8 | 0075+0080+0081（撕裂） | 0075+0076（残破斗篷） | 0079‡+0081（缺扣） | 湿/撕裂/灰血泥 |

## 真实卡与证据（均为 analogue，非 11 世纪苏格兰实物）
- **GAR-0075** 束腰长袍 tunic｜verified｜SRC-0480/0481（V&A 埃及 450–650 羊毛童袍 O119606；6–7c 防染棉袍 O115594）
- **GAR-0081** 皮靴｜verified｜SRC-0489（V&A 伦敦 15c 皮踝靴 O107847）
- **GAR-0080** 腰带｜verified｜SRC-0487/0488（7c 墨洛温铁带扣 O112685；挪威 1500–1600 银鎏金带 O126654）
- **GAR-0082** 匕首｜verified｜SRC-0490/0491（V&A 北意 c.1360–1400 / 佛兰德斯 1475–1500）
- **GAR-0076** 斗篷｜verified｜SRC-0482/0483（法 1580–1600 深红缎斗篷 O77731；葡萄牙亚麻 mantle）
- **GAR-0078** 亚麻衬衣｜verified｜SRC-0486（英 1620–40 smock）
- **GAR-0079** 基尔特长袍 kirtle｜**interpretive，无 SRC**（仅 C 线，不可作生产证据）

设计取舍：脚本自动给的 **GAR-0045 风衣(SRC-0405)、GAR-0022 威灵顿靴(SRC-0123)、GAR-0023 莫卡辛(SRC-0124)** 属 19–20c/北美，时代穿帮，弃用。

## 证据缺口
KB 无 11 世纪苏格兰服饰、锁子甲/头盔/盾牌/王冠卡；所有单品为埃及/英格兰/欧陆跨年代 analogue，跨用属 interpretive；GAR-0079 无来源；无羊毛/亚麻材料卡。

## 连续性
锚点 GAR-0075+GAR-0081 贯穿三幕；M1 干净湿泥→M2 同件染邓肯血、匕首留手→M3 血成黑褐、斗篷撕裂、带扣缺失。

## English prompts（A 线示例；ID 锁定）
**M1 image:** `battle-weary Macbeth on rain-swept heath, GAR-0075 early-medieval wool tunic T-cut side gores indigo/natural dye over GAR-0078 linen smock, GAR-0080 iron-buckle leather belt with GAR-0082 dagger, GAR-0081 muddy medieval leather ankle boots, iron-grey palette, raw exposed seams, no tartan, cold rain light, medium-wide handheld, continuity lock GAR-0075|GAR-0080|GAR-0081|GAR-0082; wetness=wet; mud hem`
**M2 video:** `slow dolly, torch/candle, Macbeth rigid clutching GAR-0082 dagger, GAR-0075 tunic over GAR-0078 smock, GAR-0081 boots, fresh dark blood across chest and hands, no crown cliche, continuity lock GAR-0075|GAR-0078|GAR-0081|GAR-0082; damage=bloodstained`
**M3 image:** `cornered tyrant at Dunsinane, GAR-0075 tunic torn at shoulder, GAR-0080 belt with missing buckle, GAR-0081 boots caked ash and mud, old black blood, ash-grey storm light, handheld close, continuity lock; damage=rent, wetness=wet`
