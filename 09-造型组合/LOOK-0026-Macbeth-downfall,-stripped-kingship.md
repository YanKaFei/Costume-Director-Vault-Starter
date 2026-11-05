---
id: LOOK-0026
type: look
name_zh: 麦克白·覆灭·剥落的王权
name_en: Macbeth downfall, stripped kingship
category: character_look
subcategory: historical
aliases:
- Macbeth downfall, stripped kingship
periods:
- late_antiquity
- middle_ages
regions:
- scotland
- europe
style_tags:
- STY-0011
colors:
- black
- ash_grey
- iron_grey
- dull_gold
materials:
- linen
- wool
- leather
- iron
source_ids:
- SRC-0421
- SRC-0482
- SRC-0483
- SRC-0489
- SRC-0487
- SRC-0488
- SRC-0490
- SRC-0491
evidence_status: interpretive
review_status: draft
license_status: not_applicable
look_role: 麦克白（虚构，M3 覆灭/暴君终局）
look_items:
- GAR-0061
- GAR-0076
- GAR-0081
- GAR-0080
- GAR-0082
look_scene: []
continuity_lock: 亚麻长袍的撕裂/血污、斗篷披法、皮靴磨损、匕首位置固定；破坏状态只允许按场次单向增加。
prompt_en: Macbeth at the end, undyed Coptic-style linen tunic torn and blood-stained,
  heavy dark cloak, worn leather boots, belt and dagger, ash-grey battlefield, firelight
  and cold moonlight, filmic historical analogue
negative_prompt_en: no crown, no clean royal robe, no tartan, no plate armour, no
  modern fabric, no glowing eyes
narrative_meaning: 用未染亚麻的科普特长袍替代王袍，斗篷像夜色，匕首仍在；把“国王”还原为将死之人。
prompt_image: Macbeth at the end, undyed Coptic-style linen tunic torn and blood-stained,
  heavy dark cloak, worn leather boots, belt and dagger, ash-grey battlefield, firelight
  and cold moonlight, filmic historical analogue
prompt_video: Macbeth stumbling across an ash-grey field, torn linen tunic and dark
  cloak, boots heavy with mud, dagger in hand, handheld medium shot, firelight flashes,
  continuity on tunic tears and cloak
negative_prompt: no crown, no clean royal robe, no tartan, no plate armour, no modern
  fabric, no glowing eyes
slot_coverage: one_piece=GAR-0061；外层=GAR-0076；鞋=GAR-0081；配饰=GAR-0080；携带物=GAR-0082
scene_states: S0 战前（worn）：长袍完整但脏；S1 终局（torn/stained）：袖口/下摆撕裂、血污扩大；只允许单向破坏。
evidence_limits: 科普特长袍为 4–7 世纪埃及类比，不是 11 世纪苏格兰；无锁甲/头盔；终局破坏为创作推断。
evidence_type: creative_inference
character_function: 被战争与暴政消耗的人：王权装饰剥落，只剩功能层与磨损。
hard_constraint_status: "PASS (R1.1 outfit.validate_hard_constraints; validate_outfits 12/12; 0 violations; 2026-11-05)"

risks: 浅色亚麻血污过强；撕裂位置影响动作；匕首必须未开刃。
tags:
- costume
- look
- p5c
- complete_outfit
- historical
outfit_slots:
- one_piece=GAR-0061
- outerwear=GAR-0076
- footwear=GAR-0081
- accessory=GAR-0080
- carried_prop=GAR-0082
weather: storm, cold
action: battle
location: battlefield
outfit_silhouette: A_line torn
constraints_checked:
- period
- region
- identity
- weather
- action
- compatibility
- approved_anchors
context: battlefield；麦克白（虚构，M3 覆灭/暴君终局）
continuity_state:
- S0 战前（worn）：长袍完整但脏；S1 终局（torn/stained）：袖口/下摆撕裂、血污扩大；只允许单向破坏。
creative_inference:
- 把科普特长袍当作“剥落王权”的功能层，属于戏剧化创作推断；不声称 11 世纪苏格兰真实终局服装。
approved_anchors: []
---
# 麦克白·覆灭·剥落的王权 / Macbeth downfall, stripped kingship

## 定义
麦克白（虚构，M3 覆灭/暴君终局）。本卡为**完整 Outfit**（五槽组织），evidence_type=`creative_inference`；创作组合与缺证据处均在下方注明，不把设计当史实。

## 结构要点
- **槽位**：one_piece=GAR-0061；外层=GAR-0076；鞋=GAR-0081；配饰=GAR-0080；携带物=GAR-0082
- **人物功能**：被战争与暴政消耗的人：王权装饰剥落，只剩功能层与磨损。
- **叙事意义**：用未染亚麻的科普特长袍替代王袍，斗篷像夜色，匕首仍在；把“国王”还原为将死之人。

## 视觉辨识
- 色彩：black, ash_grey, iron_grey, dull_gold；材质：linen, wool, leather, iron。
- 关键识别点：亚麻长袍的撕裂/血污、斗篷披法、皮靴磨损、匕首位置固定；破坏状态只允许按场次单向增加。

## 适用条件
需要完整造型、清晰人物功能与跨镜头连续性的剧情/舞台/概念设计；按 evidence_type 决定史实/类比/创作的使用边界。

## 不适用条件
需要严格历史复原而未做来源核验；把创作组合当历史事实；把类比卡当 11 世纪/某一文化的实证。

## 提示词短语
- 生图：`Macbeth at the end, undyed Coptic-style linen tunic torn and blood-stained, heavy dark cloak, worn leather boots, belt and dagger, ash-grey battlefield, firelight and cold moonlight, filmic historical analogue`
- 视频：`Macbeth stumbling across an ash-grey field, torn linen tunic and dark cloak, boots heavy with mud, dagger in hand, handheld medium shot, firelight flashes, continuity on tunic tears and cloak`
- 负向：`no crown, no clean royal robe, no tartan, no plate armour, no modern fabric, no glowing eyes`

## 来源链接
- [[SRC-0421-Met-科普特长袍]] — 见对应来源卡
- [[SRC-0482-V&A-1580-1600男斗篷]] — 见对应来源卡
- [[SRC-0483-V&A-1590-1610女披肩]] — 见对应来源卡
- [[SRC-0489-V&A-15世纪皮靴]] — 见对应来源卡
- [[SRC-0487-V&A-7世纪腰带扣]] — 见对应来源卡
- [[SRC-0488-V&A-1500-1600腰带扣]] — 见对应来源卡
- [[SRC-0490-V&A-1360-1400匕首]] — 见对应来源卡
- [[SRC-0491-V&A-1475-1500匕首]] — 见对应来源卡

## 相关卡片
- [[GAR-0061-科普特束腰长袍|科普特束腰长袍]]
- [[GAR-0076-斗篷与披风|斗篷与披风]]
- [[GAR-0081-皮靴|皮靴]]
- [[GAR-0080-腰带|腰带]]
- [[GAR-0082-匕首|匕首]]
- [[STY-0011-northern-medieval-theatrical-minimalism|STY-0011]]

## 视觉参考

- REFERENCE_PENDING：无可核验匹配 ASSET。
- [[SRC-0421-Met-科普特长袍|SRC-0421]]
- [[SRC-0482-V&A-1580-1600男斗篷|SRC-0482]]
- [[SRC-0483-V&A-1590-1610女披肩|SRC-0483]]
- [[SRC-0489-V&A-15世纪皮靴|SRC-0489]]
- [[SRC-0487-V&A-7世纪腰带扣|SRC-0487]]
- [[SRC-0488-V&A-1500-1600腰带扣|SRC-0488]]
- [[SRC-0490-V&A-1360-1400匕首|SRC-0490]]
- [[SRC-0491-V&A-1475-1500匕首|SRC-0491]]

## 生图提示词

### front_full
```text
SUBJECT (INTERPRETATION): complete outfit Macbeth downfall, stripped kingship; LOOK-0026; items=GAR-0061, GAR-0076, GAR-0081, GAR-0080, GAR-0082.
COMPOSITION (FACT/OBSERVATION): only listed look_items and their cards; no invented garment.
MATERIAL (OBSERVATION): from listed item cards; unknown where absent.
COLOR (OBSERVATION): card palette only.
LIGHT (CREATIVE): neutral key, soft falloff.
CAMERA (CREATIVE): 50mm full-body, eye level, front.
BACKGROUND (CREATIVE): neutral grey; scene context only.
NEGATIVE (CREATIVE): no extra garments, brands or invented history.
CONSISTENCY (OBSERVATION): preserve item IDs and layering.
```

### side_back
```text
SUBJECT (INTERPRETATION): side and back of Macbeth downfall, stripped kingship; LOOK-0026.
COMPOSITION (FACT/OBSERVATION): same look_items=GAR-0061, GAR-0076, GAR-0081, GAR-0080, GAR-0082; no added construction.
LIGHT (CREATIVE): neutral soft key with rim separation.
CAMERA (CREATIVE): orthographic side/back, 50-85mm.
BACKGROUND (CREATIVE): neutral grey.
NEGATIVE (CREATIVE): no invented closures or layers.
CONSISTENCY (OBSERVATION): same palette, silhouette and item IDs.
```

## 视频提示词
```text
SUBJECT (INTERPRETATION): Macbeth downfall, stripped kingship; slow 180-degree turn.
COMPOSITION (OBSERVATION): same look_items=GAR-0061, GAR-0076, GAR-0081, GAR-0080, GAR-0082; no morphing.
LIGHT (CREATIVE): neutral key.
CAMERA (CREATIVE): 50mm full-body stable.
NEGATIVE (CREATIVE): no extra garments or logos.
CONSISTENCY (OBSERVATION): preserve item IDs, palette, layering.
```
