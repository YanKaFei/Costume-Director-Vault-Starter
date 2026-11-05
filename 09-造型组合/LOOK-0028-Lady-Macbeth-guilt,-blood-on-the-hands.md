---
id: LOOK-0028
type: look
name_zh: 麦克白夫人·罪恶危机·血手
name_en: Lady Macbeth guilt, blood on the hands
category: character_look
subcategory: historical
aliases:
- Lady Macbeth guilt, blood on the hands
periods:
- middle_ages
- early_modern
regions:
- scotland
- england
- europe
style_tags:
- STY-0011
colors:
- deep_red
- black
- ivory
- blood_red
materials:
- linen
- wool
- silk
- leather
source_ids:
- SRC-0482
- SRC-0483
- SRC-0125
- SRC-0487
- SRC-0488
- SRC-0490
- SRC-0491
- SRC-0429
- SRC-0423
evidence_status: interpretive
review_status: draft
license_status: not_applicable
look_role: 麦克白夫人（虚构，L2 罪恶危机/血手）
look_items:
- GAR-0079
- GAR-0076
- GAR-0024
- GAR-0080
- GAR-0082
- GAR-0068
- MAT-0011
look_scene: []
continuity_lock: 头纱位置、斗篷遮手侧、腰带、匕首、穆勒鞋固定；血手只允许在洗手事件后减少，不得自动消失。
prompt_en: Lady Macbeth with bloodied hands, deep-red kirtle and black cloak, anachronistic
  pale 1902 veil, leather mules, belt and dagger, candlelit stone chamber, expressionist
  guilt, filmic theatrical
negative_prompt_en: no crown, no modern dress, no clean hands after murder, no tartan,
  no glowing eyes
narrative_meaning: 深红基尔特与黑斗篷压住血色；1902 头纱（theatrical）像一层不合时宜的圣洁；匕首是共谋的物证。
prompt_image: Lady Macbeth with bloodied hands, deep-red kirtle and black cloak, anachronistic
  pale 1902 veil, leather mules, belt and dagger, candlelit stone chamber, expressionist
  guilt, filmic theatrical
prompt_video: Lady Macbeth rubbing blood from her hands, veil and cloak moving, candlelight,
  close-up on hands then medium shot, continuity on blood amount and veil position
negative_prompt: no crown, no modern dress, no clean hands after murder, no tartan,
  no glowing eyes
slot_coverage: one_piece=GAR-0079；外层=GAR-0076；鞋=GAR-0024；配饰=GAR-0080；携带物=GAR-0082；头饰=GAR-0068；材料=MAT-0011
scene_states: S0 弑君后（stained）：血手、斗篷遮手；S1 洗手（less blood）：血减少但未净；只允许单向/事件驱动。
evidence_limits: GAR-0079 interpretive；GAR-0068 为 1902 英国婚礼头纱，仅 theatrical，不是中世纪证据；无中世纪血/珠宝卡。
evidence_type: creative_inference
character_function: 她把“王后”的体面穿在外面，却盖不住手上的血；越体面，反差越大。
hard_constraint_status: "PASS (R1.1 outfit.validate_hard_constraints; validate_outfits 12/12; 0 violations; 2026-11-05)"

risks: 头纱易滑向“婚纱”误读；血手在深红上不明显；穆勒鞋动作不便。
tags:
- costume
- look
- p5c
- complete_outfit
- historical
outfit_slots:
- one_piece=GAR-0079
- outerwear=GAR-0076
- footwear=GAR-0024
- accessory=GAR-0080
- carried_prop=GAR-0082
weather: indoor
action: washing hands
location: castle chamber
outfit_silhouette: A_line
constraints_checked:
- period
- region
- identity
- weather
- action
- compatibility
- approved_anchors
context: castle chamber；麦克白夫人（虚构，L2 罪恶危机/血手）
continuity_state:
- S0 弑君后（stained）：血手、斗篷遮手；S1 洗手（less blood）：血减少但未净；只允许单向/事件驱动。
creative_inference:
- 1902 头纱用于罪疚/圣洁反差，是 theatrical 设计推断；不当中世纪头纱史实。
approved_anchors: []
---
# 麦克白夫人·罪恶危机·血手 / Lady Macbeth guilt, blood on the hands

## 定义
麦克白夫人（虚构，L2 罪恶危机/血手）。本卡为**完整 Outfit**（五槽组织），evidence_type=`creative_inference`；创作组合与缺证据处均在下方注明，不把设计当史实。

## 结构要点
- **槽位**：one_piece=GAR-0079；外层=GAR-0076；鞋=GAR-0024；配饰=GAR-0080；携带物=GAR-0082；头饰=GAR-0068；材料=MAT-0011
- **人物功能**：她把“王后”的体面穿在外面，却盖不住手上的血；越体面，反差越大。
- **叙事意义**：深红基尔特与黑斗篷压住血色；1902 头纱（theatrical）像一层不合时宜的圣洁；匕首是共谋的物证。

## 视觉辨识
- 色彩：deep_red, black, ivory, blood_red；材质：linen, wool, silk, leather。
- 关键识别点：头纱位置、斗篷遮手侧、腰带、匕首、穆勒鞋固定；血手只允许在洗手事件后减少，不得自动消失。

## 适用条件
需要完整造型、清晰人物功能与跨镜头连续性的剧情/舞台/概念设计；按 evidence_type 决定史实/类比/创作的使用边界。

## 不适用条件
需要严格历史复原而未做来源核验；把创作组合当历史事实；把类比卡当 11 世纪/某一文化的实证。

## 提示词短语
- 生图：`Lady Macbeth with bloodied hands, deep-red kirtle and black cloak, anachronistic pale 1902 veil, leather mules, belt and dagger, candlelit stone chamber, expressionist guilt, filmic theatrical`
- 视频：`Lady Macbeth rubbing blood from her hands, veil and cloak moving, candlelight, close-up on hands then medium shot, continuity on blood amount and veil position`
- 负向：`no crown, no modern dress, no clean hands after murder, no tartan, no glowing eyes`

## 来源链接
- [[SRC-0482-V&A-1580-1600男斗篷]] — 见对应来源卡
- [[SRC-0483-V&A-1590-1610女披肩]] — 见对应来源卡
- [[SRC-0125-FIT-mule]] — 见对应来源卡
- [[SRC-0487-V&A-7世纪腰带扣]] — 见对应来源卡
- [[SRC-0488-V&A-1500-1600腰带扣]] — 见对应来源卡
- [[SRC-0490-V&A-1360-1400匕首]] — 见对应来源卡
- [[SRC-0491-V&A-1475-1500匕首]] — 见对应来源卡
- [[SRC-0429-V&A-1902婚礼头纱]] — 见对应来源卡
- [[SRC-0423-V&A-拜占庭samite丝绸]] — 见对应来源卡

## 相关卡片
- [[GAR-0079-基尔特长袍|基尔特长袍]]
- [[GAR-0076-斗篷与披风|斗篷与披风]]
- [[GAR-0024-穆勒鞋|穆勒鞋]]
- [[GAR-0080-腰带|腰带]]
- [[GAR-0082-匕首|匕首]]
- [[GAR-0068-婚礼头纱|婚礼头纱]]
- [[MAT-0011-拜占庭samite丝绸|拜占庭 samite 丝绸]]
- [[STY-0011-northern-medieval-theatrical-minimalism|STY-0011]]

## 视觉参考

- REFERENCE_PENDING：无可核验匹配 ASSET。
- [[SRC-0482-V&A-1580-1600男斗篷|SRC-0482]]
- [[SRC-0483-V&A-1590-1610女披肩|SRC-0483]]
- [[SRC-0125-FIT-mule|SRC-0125]]
- [[SRC-0487-V&A-7世纪腰带扣|SRC-0487]]
- [[SRC-0488-V&A-1500-1600腰带扣|SRC-0488]]
- [[SRC-0490-V&A-1360-1400匕首|SRC-0490]]
- [[SRC-0491-V&A-1475-1500匕首|SRC-0491]]
- [[SRC-0429-V&A-1902婚礼头纱|SRC-0429]]
- [[SRC-0423-V&A-拜占庭samite丝绸|SRC-0423]]

## 生图提示词

### front_full
```text
SUBJECT (INTERPRETATION): complete outfit Lady Macbeth guilt, blood on the hands; LOOK-0028; items=GAR-0079, GAR-0076, GAR-0024, GAR-0080, GAR-0082, GAR-0068, MAT-0011.
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
SUBJECT (INTERPRETATION): side and back of Lady Macbeth guilt, blood on the hands; LOOK-0028.
COMPOSITION (FACT/OBSERVATION): same look_items=GAR-0079, GAR-0076, GAR-0024, GAR-0080, GAR-0082, GAR-0068, MAT-0011; no added construction.
LIGHT (CREATIVE): neutral soft key with rim separation.
CAMERA (CREATIVE): orthographic side/back, 50-85mm.
BACKGROUND (CREATIVE): neutral grey.
NEGATIVE (CREATIVE): no invented closures or layers.
CONSISTENCY (OBSERVATION): same palette, silhouette and item IDs.
```

## 视频提示词
```text
SUBJECT (INTERPRETATION): Lady Macbeth guilt, blood on the hands; slow 180-degree turn.
COMPOSITION (OBSERVATION): same look_items=GAR-0079, GAR-0076, GAR-0024, GAR-0080, GAR-0082, GAR-0068, MAT-0011; no morphing.
LIGHT (CREATIVE): neutral key.
CAMERA (CREATIVE): 50mm full-body stable.
NEGATIVE (CREATIVE): no extra garments or logos.
CONSISTENCY (OBSERVATION): preserve item IDs, palette, layering.
```
