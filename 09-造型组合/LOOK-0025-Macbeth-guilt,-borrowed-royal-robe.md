---
id: LOOK-0025
type: look
name_zh: 麦克白·罪恶危机·借来的王袍
name_en: Macbeth guilt, borrowed royal robe
category: character_look
subcategory: historical
aliases:
- Macbeth guilt, borrowed royal robe
periods:
- middle_ages
- early_modern
regions:
- scotland
- europe
style_tags:
- STY-0011
colors:
- dark_red
- gold
- charcoal
- iron_grey
materials:
- wool
- linen
- leather
- iron
source_ids:
- SRC-0110
- SRC-0482
- SRC-0483
- SRC-0489
- SRC-0487
- SRC-0488
- SRC-0490
- SRC-0491
- SRC-0423
evidence_status: interpretive
review_status: draft
license_status: not_applicable
look_role: 麦克白（虚构，M2 罪恶危机/新王）
look_items:
- GAR-0009
- GAR-0076
- GAR-0081
- GAR-0080
- GAR-0082
- MAT-0011
look_scene: []
continuity_lock: 袍长/袖口位置、斗篷遮血侧、腰带与匕首位置固定；血只允许在米白/暗红内层上单向扩大，不自动变浅。
prompt_en: usurping Macbeth in a borrowed ceremonial dalmatic, dark red and gold samite
  flashes under a charcoal cloak, leather belt and dagger, blood hidden at the cuff,
  candlelit stone hall, deep shadow, filmic historical analogue
negative_prompt_en: no crown, no clean hands, no tartan, no plate armour, no modern
  tailoring, no glowing eyes
narrative_meaning: 达尔马提亚长袍作为王权外壳，斗篷遮住血袖；金色 samite 只在动作中闪现；匕首仍在，提醒王位来自暴力。
prompt_image: usurping Macbeth in a borrowed ceremonial dalmatic, dark red and gold
  samite flashes under a charcoal cloak, leather belt and dagger, blood hidden at
  the cuff, candlelit stone hall, deep shadow, filmic historical analogue
prompt_video: Macbeth standing in a cold stone hall, cloak drawn over one bloodied
  cuff, samite lining flashing, dagger at belt, slow push-in, candlelight, continuity
  on hidden blood and cloak drape
negative_prompt: no crown, no clean hands, no tartan, no plate armour, no modern tailoring,
  no glowing eyes
slot_coverage: one_piece=GAR-0009；外层=GAR-0076；鞋=GAR-0081；配饰=GAR-0080；携带物=GAR-0082；材料=MAT-0011
scene_states: S0 加冕后（dry）：袍与斗篷整洁，血在袖内；S1 宴前（stained）：袖口血痕扩大，斗篷遮住；只允许单向增加。
evidence_limits: 达尔马提亚为拜占庭/中世纪类比，不是 11 世纪苏格兰王袍；无王冠/权杖/regalia 卡；samite 为拜占庭织物类比；不得声称加冕礼真实形制。
evidence_type: sourced_style_observation
character_function: 新王穿着“借来的”仪式袍：看起来是国王，但血藏在袖口里；权力与不合身感同时出现。
hard_constraint_status: "PASS (R1.1 outfit.validate_hard_constraints; validate_outfits 12/12; 0 violations; 2026-11-05)"

risks: 血在暗红上不明显；斗篷遮血调度需排练；王权感依赖版型而非真实 regalia。
tags:
- costume
- look
- p5c
- complete_outfit
- historical
outfit_slots:
- one_piece=GAR-0009
- outerwear=GAR-0076
- footwear=GAR-0081
- accessory=GAR-0080
- carried_prop=GAR-0082
weather: cold, indoor
action: standing
location: stone hall
outfit_silhouette: H_line ceremonial
constraints_checked:
- period
- region
- identity
- weather
- action
- compatibility
- approved_anchors
context: stone hall；麦克白（虚构，M2 罪恶危机/新王）
continuity_state:
- S0 加冕后（dry）：袍与斗篷整洁，血在袖内；S1 宴前（stained）：袖口血痕扩大，斗篷遮住；只允许单向增加。
style_observation:
- 达尔马提亚/斗篷/皮靴的层搭来自类比来源；王权“不合身”是设计观察，不是加冕礼史实。
approved_anchors: []
---
# 麦克白·罪恶危机·借来的王袍 / Macbeth guilt, borrowed royal robe

## 定义
麦克白（虚构，M2 罪恶危机/新王）。本卡为**完整 Outfit**（五槽组织），evidence_type=`sourced_style_observation`；创作组合与缺证据处均在下方注明，不把设计当史实。

## 结构要点
- **槽位**：one_piece=GAR-0009；外层=GAR-0076；鞋=GAR-0081；配饰=GAR-0080；携带物=GAR-0082；材料=MAT-0011
- **人物功能**：新王穿着“借来的”仪式袍：看起来是国王，但血藏在袖口里；权力与不合身感同时出现。
- **叙事意义**：达尔马提亚长袍作为王权外壳，斗篷遮住血袖；金色 samite 只在动作中闪现；匕首仍在，提醒王位来自暴力。

## 视觉辨识
- 色彩：dark_red, gold, charcoal, iron_grey；材质：wool, linen, leather, iron。
- 关键识别点：袍长/袖口位置、斗篷遮血侧、腰带与匕首位置固定；血只允许在米白/暗红内层上单向扩大，不自动变浅。

## 适用条件
需要完整造型、清晰人物功能与跨镜头连续性的剧情/舞台/概念设计；按 evidence_type 决定史实/类比/创作的使用边界。

## 不适用条件
需要严格历史复原而未做来源核验；把创作组合当历史事实；把类比卡当 11 世纪/某一文化的实证。

## 提示词短语
- 生图：`usurping Macbeth in a borrowed ceremonial dalmatic, dark red and gold samite flashes under a charcoal cloak, leather belt and dagger, blood hidden at the cuff, candlelit stone hall, deep shadow, filmic historical analogue`
- 视频：`Macbeth standing in a cold stone hall, cloak drawn over one bloodied cuff, samite lining flashing, dagger at belt, slow push-in, candlelight, continuity on hidden blood and cloak drape`
- 负向：`no crown, no clean hands, no tartan, no plate armour, no modern tailoring, no glowing eyes`

## 来源链接
- [[SRC-0110-FIT-dalmatic-tunic]] — 见对应来源卡
- [[SRC-0482-V&A-1580-1600男斗篷]] — 见对应来源卡
- [[SRC-0483-V&A-1590-1610女披肩]] — 见对应来源卡
- [[SRC-0489-V&A-15世纪皮靴]] — 见对应来源卡
- [[SRC-0487-V&A-7世纪腰带扣]] — 见对应来源卡
- [[SRC-0488-V&A-1500-1600腰带扣]] — 见对应来源卡
- [[SRC-0490-V&A-1360-1400匕首]] — 见对应来源卡
- [[SRC-0491-V&A-1475-1500匕首]] — 见对应来源卡
- [[SRC-0423-V&A-拜占庭samite丝绸]] — 见对应来源卡

## 相关卡片
- [[GAR-0009-达尔马提亚长袍|达尔马提亚长袍]]
- [[GAR-0076-斗篷与披风|斗篷与披风]]
- [[GAR-0081-皮靴|皮靴]]
- [[GAR-0080-腰带|腰带]]
- [[GAR-0082-匕首|匕首]]
- [[MAT-0011-拜占庭samite丝绸|拜占庭 samite 丝绸]]
- [[STY-0011-northern-medieval-theatrical-minimalism|STY-0011]]

## 视觉参考

- REFERENCE_PENDING：无可核验匹配 ASSET；构成来自 look_items=GAR-0009, GAR-0076, GAR-0081, GAR-0080, GAR-0082, MAT-0011。

## 生图提示词

### front_full
```text
SUBJECT (INTERPRETATION): complete outfit Macbeth guilt, borrowed royal robe; LOOK-0025; items=GAR-0009, GAR-0076, GAR-0081, GAR-0080, GAR-0082, MAT-0011.
COMPOSITION (FACT/OBSERVATION): only listed look_items and their card structure; no invented garment.
MATERIAL (OBSERVATION): from listed item cards; unknown where absent.
COLOR (OBSERVATION): card palette only.
LIGHT (CREATIVE): neutral key, soft falloff.
CAMERA (CREATIVE): full-body 50mm, front.
BACKGROUND (CREATIVE): neutral grey; scene=scene not specified as context only.
NEGATIVE (CREATIVE): no extra garments, brands or invented history.
CONSISTENCY (OBSERVATION): preserve item IDs and layering.
```

### side_back
```text
SUBJECT (INTERPRETATION): side and back of Macbeth guilt, borrowed royal robe; LOOK-0025.
COMPOSITION (FACT/OBSERVATION): same look_items=GAR-0009, GAR-0076, GAR-0081, GAR-0080, GAR-0082, MAT-0011; no added construction.
LIGHT (CREATIVE): neutral soft key with rim separation.
CAMERA (CREATIVE): orthographic side/back, 50-85mm.
BACKGROUND (CREATIVE): neutral grey.
NEGATIVE (CREATIVE): no invented closures or layers.
CONSISTENCY (OBSERVATION): same palette, silhouette, item IDs.
```

## 视频提示词
```text
SUBJECT (INTERPRETATION): Macbeth guilt, borrowed royal robe; slow 180-degree turn.
COMPOSITION (OBSERVATION): same look_items=GAR-0009, GAR-0076, GAR-0081, GAR-0080, GAR-0082, MAT-0011; no morphing.
LIGHT (CREATIVE): neutral key.
CAMERA (CREATIVE): 50mm full-body stable.
NEGATIVE (CREATIVE): no extra garments or logos.
CONSISTENCY (OBSERVATION): preserve item IDs, palette, layering.
```
