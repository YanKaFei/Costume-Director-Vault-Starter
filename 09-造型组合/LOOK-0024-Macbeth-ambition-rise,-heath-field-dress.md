---
id: LOOK-0024
type: look
name_zh: 麦克白·野心上升·荒野战袍
name_en: Macbeth ambition rise, heath field dress
category: character_look
subcategory: historical
aliases:
- Macbeth ambition rise, heath field dress
periods:
- early_middle_ages
regions:
- scotland
- europe
style_tags:
- STY-0011
colors:
- earth_brown
- charcoal
- iron_grey
- blood_red
materials:
- wool
- linen
- leather
- iron
source_ids:
- SRC-0480
- SRC-0481
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
look_role: 麦克白（虚构，11 世纪苏格兰戏剧化版本；M1 野心上升）
look_items:
- GAR-0075
- GAR-0076
- GAR-0081
- GAR-0080
- GAR-0082
- MAT-0011
look_scene: []
continuity_lock: 斗篷披法、腰带位置、匕首持握侧、靴筒泥污范围跨镜头固定；雨/泥状态只允许按场次单向增加，不做自动变干。
prompt_en: 'full-body Macbeth in early-medieval analogue field dress: earth-brown
  wool tunic with side gores and belt, charcoal cloak, leather ankle boots, dagger
  at belt, mud and sweat, storm heath, cold overcast light, filmic historical analogue'
negative_prompt_en: no crown, no tartan, no plate armour, no clean dry clothes, no
  modern fabric, no glowing eyes
narrative_meaning: 荒野/战场之后的实用层：束腰长袍、斗篷、腰带、皮靴与匕首都是“还在打仗的人”的工具；没有王权装饰。
prompt_image: 'full-body Macbeth in early-medieval analogue field dress: earth-brown
  wool tunic with side gores and belt, charcoal cloak, leather ankle boots, dagger
  at belt, mud and sweat, storm heath, cold overcast light, filmic historical analogue'
prompt_video: Macbeth on a storm heath, wool tunic and cloak moving in wind, mud on
  boots, hand near dagger, medium tracking shot, cold moonlight and torchlight, continuity
  on cloak drape and dagger side
negative_prompt: no crown, no tartan, no plate armour, no clean dry clothes, no modern
  fabric, no glowing eyes
slot_coverage: one_piece=GAR-0075；外层=GAR-0076；鞋=GAR-0081；配饰=GAR-0080；携带物=GAR-0082；材料=MAT-0011
scene_states: S0 荒野风暴（wet/dirty）：长袍下摆与靴面泥水、斗篷湿重；S1 城堡内（drying）：斗篷挂起、靴泥干裂；只允许单向推进。
evidence_limits: 11 世纪苏格兰无直接服饰证据；GAR-0075/0076/0077/0080/0081 为欧洲/地中海中世纪—早期近代类比；MAT-0011
  为拜占庭 samite 类比；无锁甲/头盔/王冠。不得声称历史复原。
evidence_type: sourced_style_observation
character_function: 战场归来的领主：功能优先、泥与汗；预言的“借来的袍子”尚未出现。
hard_constraint_status: "PASS (R1.1 outfit.validate_hard_constraints; validate_outfits 12/12; 0 violations; 2026-11-05)"

risks: 长袍下摆限制奔跑；斗篷在动作戏可能被勾住；匕首必须未开刃；泥污在浅色亚麻上过显眼。
tags:
- costume
- look
- p5c
- complete_outfit
- historical
outfit_slots:
- one_piece=GAR-0075
- outerwear=GAR-0076
- footwear=GAR-0081
- accessory=GAR-0080
- carried_prop=GAR-0082
weather: storm, cold
action: battle
location: heath
outfit_silhouette: H_line layered
constraints_checked:
- period
- region
- identity
- weather
- action
- compatibility
- approved_anchors
context: heath；麦克白（虚构，11 世纪苏格兰戏剧化版本；M1 野心上升）
continuity_state:
- S0 荒野风暴（wet/dirty）：长袍下摆与靴面泥水、斗篷湿重；S1 城堡内（drying）：斗篷挂起、靴泥干裂；只允许单向推进。
style_observation:
- 羊毛/亚麻的哑光层搭与铁灰/土褐来自 GAR-0075/0076/0081 来源卡；北方戏剧化组合为设计观察。
approved_anchors: []
relations:
  - 'target=GAR-0075; type=appears_in_look; direction=outgoing; evidence=interpretive; confidence=medium; source_ids=SRC-0480; rule=R-LOOK-ITEMS; review_status=review_queue; factual=false; design_only=true'
visual_prompt_profile: outfit_standard
visual_prompt_type: [full_body, detail, video]
visual_evidence: [FACT, OBSERVATION, INFERENCE, CREATIVE]
---
# 麦克白·野心上升·荒野战袍 / Macbeth ambition rise, heath field dress

## 定义
麦克白（虚构，11 世纪苏格兰戏剧化版本；M1 野心上升）。本卡为**完整 Outfit**（五槽组织），evidence_type=`sourced_style_observation`；创作组合与缺证据处均在下方注明，不把设计当史实。

## 结构要点
- **槽位**：one_piece=GAR-0075；外层=GAR-0076；鞋=GAR-0081；配饰=GAR-0080；携带物=GAR-0082；材料=MAT-0011
- **人物功能**：战场归来的领主：功能优先、泥与汗；预言的“借来的袍子”尚未出现。
- **叙事意义**：荒野/战场之后的实用层：束腰长袍、斗篷、腰带、皮靴与匕首都是“还在打仗的人”的工具；没有王权装饰。

- R1.3B 完整构成：look_items 精确 ID 见下；不新增未登记单品。
- 正面/侧背：full-body front + side/back 两视图；结构/材质锚点：materials=wool, linen, leather, iron；colors=earth_brown, charcoal, iron_grey, blood_red。
- 角色/场景：scene=unknown；跨镜连续性以原 `continuity_lock` 为准，视觉层不修改。
- 动作响应：见生图/视频 prompt 的 ACTION_RESPONSE；Look Bible/Approved Anchors 保留。
## 视觉辨识
- 色彩：earth_brown, charcoal, iron_grey, blood_red；材质：wool, linen, leather, iron。
- 关键识别点：斗篷披法、腰带位置、匕首持握侧、靴筒泥污范围跨镜头固定；雨/泥状态只允许按场次单向增加，不做自动变干。

## 适用条件
需要完整造型、清晰人物功能与跨镜头连续性的剧情/舞台/概念设计；按 evidence_type 决定史实/类比/创作的使用边界。

## 不适用条件
需要严格历史复原而未做来源核验；把创作组合当历史事实；把类比卡当 11 世纪/某一文化的实证。

## 提示词短语
- 生图：`full-body Macbeth in early-medieval analogue field dress: earth-brown wool tunic with side gores and belt, charcoal cloak, leather ankle boots, dagger at belt, mud and sweat, storm heath, cold overcast light, filmic historical analogue`
- 视频：`Macbeth on a storm heath, wool tunic and cloak moving in wind, mud on boots, hand near dagger, medium tracking shot, cold moonlight and torchlight, continuity on cloak drape and dagger side`
- 负向：`no crown, no tartan, no plate armour, no clean dry clothes, no modern fabric, no glowing eyes`

## 来源链接
- [[SRC-0480-V&A-450-650束腰长袍]] — 见对应来源卡
- [[SRC-0481-V&A-6-7世纪束腰长袍]] — 见对应来源卡
- [[SRC-0482-V&A-1580-1600男斗篷]] — 见对应来源卡
- [[SRC-0483-V&A-1590-1610女披肩]] — 见对应来源卡
- [[SRC-0489-V&A-15世纪皮靴]] — 见对应来源卡
- [[SRC-0487-V&A-7世纪腰带扣]] — 见对应来源卡
- [[SRC-0488-V&A-1500-1600腰带扣]] — 见对应来源卡
- [[SRC-0490-V&A-1360-1400匕首]] — 见对应来源卡
- [[SRC-0491-V&A-1475-1500匕首]] — 见对应来源卡
- [[SRC-0423-V&A-拜占庭samite丝绸]] — 见对应来源卡

## 相关卡片
- [[GAR-0075-束腰长袍|束腰长袍]]
- [[GAR-0076-斗篷与披风|斗篷与披风]]
- [[GAR-0081-皮靴|皮靴]]
- [[GAR-0080-腰带|腰带]]
- [[GAR-0082-匕首|匕首]]
- [[MAT-0011-拜占庭samite丝绸|拜占庭 samite 丝绸]]
- [[STY-0011-northern-medieval-theatrical-minimalism|STY-0011]]


## 视觉参考
- REFERENCE_PENDING：本卡无已登记匹配 ASSET；现有 source_ids [[SRC-0480-V&A-450-650束腰长袍|SRC-0480]], [[SRC-0481-V&A-6-7世纪束腰长袍|SRC-0481]], [[SRC-0482-V&A-1580-1600男斗篷|SRC-0482]], [[SRC-0483-V&A-1590-1610女披肩|SRC-0483]], [[SRC-0489-V&A-15世纪皮靴|SRC-0489]], [[SRC-0487-V&A-7世纪腰带扣|SRC-0487]], [[SRC-0488-V&A-1500-1600腰带扣|SRC-0488]], [[SRC-0490-V&A-1360-1400匕首|SRC-0490]], [[SRC-0491-V&A-1475-1500匕首|SRC-0491]], [[SRC-0423-V&A-拜占庭samite丝绸|SRC-0423]] 仅为 link_only 文字参考，未下载/未内嵌图像。
- Look Bible / Approved Anchors：本批未改 `continuity_lock`、`look_items`、Approved Anchors；视觉层仅追加，不覆盖硬约束。

## 生图提示词
```text
SUBJECT (FACT): LOOK-0024; fictional character look; scene ID unknown.
FULL OUTFIT COMPOSITION (FACT): look_items IDs=GAR-0075, GAR-0076, GAR-0081, GAR-0080, GAR-0082, MAT-0011.
FRONT FULL BODY (CREATIVE): centered full-body front view, neutral standing pose, complete outfit visible.
SIDE_BACK (CREATIVE): side and three-quarter back view, same outfit, same styling.
STRUCTURE/MATERIAL ANCHORS (FACT): materials=wool, linen, leather, iron; colors=earth_brown, charcoal, iron_grey, blood_red; preserve stated structure and layer order.
CHARACTER/SCENE (OBSERVATION): scene ID unknown; environment per card, no new narrative facts.
CONTINUITY (OBSERVATION): preserve garment IDs, layer order, closure/accessory side and wet/mud state direction across shots.
ACTION RESPONSE (OBSERVATION): full-body Macbeth in early-medieval analogue field dress: earth-brown wool tunic with side gores and belt, charcoal cloak, leather ankle boots, dagger at belt, mud and sweat, storm heath, cold overcast light, filmic historical analogue
LIGHT (CREATIVE): soft cinematic key, controlled contrast, period-appropriate ambience without claiming historical lighting.
CAMERA (CREATIVE): 35–50mm, full-body, eye level, 3/4 for side/back.
BACKGROUND (CREATIVE): restrained environment per scene; no invented landmarks.
NEGATIVE (CREATIVE): no logo/text/watermark, no extra layers, no costume morphing, no colour shift, no brand copy.
CONSISTENCY (OBSERVATION): keep outfit composition, palette, structure and accessory placement identical across frames.
```

## 视频提示词
```text
SUBJECT (FACT): LOOK-0024; one continuous character look; scene ID unknown.
ACTION/MOTION (OBSERVATION): walking/turning response; garment and layers move according to their structure.
CONTINUITY (OBSERVATION): preserve garment IDs, layer order, closure/accessory side, wet/mud direction and palette across frames.
LIGHT (CREATIVE): controlled cinematic key; no historical lighting claim.
CAMERA (CREATIVE): medium tracking shot, 35–50mm, eye level, stable.
NEGATIVE (CREATIVE): no costume morphing, no colour shift, no extra layers, no logo/text/watermark, no anachronistic additions.
```