---
id: LOOK-0033
type: look
name_zh: 零重力歌剧女伶
name_en: zero-gravity opera singer
category: character_look
subcategory: sci_fi
aliases:
- zero-gravity opera singer
periods:
- future
regions:
- fictional
style_tags:
- STY-0015
colors:
- silver
- black
- deep_blue
- bone_white
materials:
- synthetic
- metal_fiber
- rubber
- silk
source_ids:
- SRC-0402
- SRC-0401
- SRC-0123
- SRC-0403
- SRC-0410
- SRC-0408
evidence_status: interpretive
review_status: draft
license_status: not_applicable
look_role: 零重力歌剧女伶（虚构科幻角色）
look_items:
- GAR-0038
- GAR-0037
- GAR-0022
- GAR-0039
- GAR-0050
- GAR-0048
look_scene:
- SCN-0006
continuity_lock: 连体服拉链/口袋、外层肩线、头盔面罩、手套、徽章与包位置固定；零重力下不得出现重力垂坠。
prompt_en: zero-gravity opera singer on a derelict space station, fitted coverall
  under a protective jacket, helmet and gloves, silver/black/deep-blue palette, stage
  haze and artificial key light, operatic silhouette, fictional sci-fi, no realistic
  engineering claim
negative_prompt_en: no historical costume, no tartan, no glowing magic, no modern
  fashion runway, no gravity droop, no extra limbs
narrative_meaning: 连体工作服与防火外层提供“工程/生存”骨架，头盔/徽章/手套是系统身份，包是随身工具；歌剧性来自轮廓与光，不是历史服饰。
prompt_image: zero-gravity opera singer on a derelict space station, fitted coverall
  under a protective jacket, helmet and gloves, silver/black/deep-blue palette, stage
  haze and artificial key light, operatic silhouette, fictional sci-fi, no realistic
  engineering claim
prompt_video: singer floating in a derelict station, coverall and protective layer
  drifting, helmet catching light, slow operatic gesture, camera drifting, zero-gravity
  fabric response, continuity on badges and gloves
negative_prompt: no historical costume, no tartan, no glowing magic, no modern fashion
  runway, no gravity droop, no extra limbs
slot_coverage: one_piece=GAR-0038；外层=GAR-0037；鞋=GAR-0022；配饰=GAR-0039/GAR-0050；携带物=GAR-0048（工具包，创作）
scene_states: S0 演出前（dry）：层搭整齐；S1 演出（dry）：外层/头盔固定、无重力；不做雨/污。
evidence_limits: 连体工作服/消防外套/头盔/徽章来自现实卡，作为结构类比；空间站/歌剧世界为虚构；GAR-0039 为 1969 玩具头盔，仅道具结构参考；无真实
  EVA/供氧/通讯卡。
evidence_type: creative_inference
character_function: 在废弃空间站/剧场表演的歌者：工作服结构 + 舞台夸张轮廓 + 防护层。
hard_constraint_status: "PASS (R1.1 outfit.validate_hard_constraints; validate_outfits 12/12; 0 violations; 2026-11-05)"

risks: 将现实工作服误读为航天装备；头盔闷热/视线；零重力布料需 VFX/钢丝测试。
tags:
- costume
- look
- p5c
- complete_outfit
- sci_fi
outfit_slots:
- one_piece=GAR-0038
- outerwear=GAR-0037
- footwear=GAR-0022
- accessory=GAR-0039
- carried_prop=GAR-0048
weather: indoor
action: singing
location: derelict space station
outfit_silhouette: H_line functional
constraints_checked:
- period
- region
- identity
- weather
- action
- compatibility
- approved_anchors
context: derelict space station；零重力歌剧女伶（虚构科幻角色）
continuity_state:
- S0 演出前（dry）：层搭整齐；S1 演出（dry）：外层/头盔固定、无重力；不做雨/污。
creative_inference:
- 零重力歌剧世界、头盔/连体服/工具包的组合为虚构设计推断；现实卡仅作结构类比。
approved_anchors: []
---
# 零重力歌剧女伶 / zero-gravity opera singer

## 定义
零重力歌剧女伶（虚构科幻角色）。本卡为**完整 Outfit**（五槽组织），evidence_type=`creative_inference`；创作组合与缺证据处均在下方注明，不把设计当史实。

## 结构要点
- **槽位**：one_piece=GAR-0038；外层=GAR-0037；鞋=GAR-0022；配饰=GAR-0039/GAR-0050；携带物=GAR-0048（工具包，创作）
- **人物功能**：在废弃空间站/剧场表演的歌者：工作服结构 + 舞台夸张轮廓 + 防护层。
- **叙事意义**：连体工作服与防火外层提供“工程/生存”骨架，头盔/徽章/手套是系统身份，包是随身工具；歌剧性来自轮廓与光，不是历史服饰。

## 视觉辨识
- 色彩：silver, black, deep_blue, bone_white；材质：synthetic, metal_fiber, rubber, silk。
- 关键识别点：连体服拉链/口袋、外层肩线、头盔面罩、手套、徽章与包位置固定；零重力下不得出现重力垂坠。

## 适用条件
需要完整造型、清晰人物功能与跨镜头连续性的剧情/舞台/概念设计；按 evidence_type 决定史实/类比/创作的使用边界。

## 不适用条件
需要严格历史复原而未做来源核验；把创作组合当历史事实；把类比卡当 11 世纪/某一文化的实证。

## 提示词短语
- 生图：`zero-gravity opera singer on a derelict space station, fitted coverall under a protective jacket, helmet and gloves, silver/black/deep-blue palette, stage haze and artificial key light, operatic silhouette, fictional sci-fi, no realistic engineering claim`
- 视频：`singer floating in a derelict station, coverall and protective layer drifting, helmet catching light, slow operatic gesture, camera drifting, zero-gravity fabric response, continuity on badges and gloves`
- 负向：`no historical costume, no tartan, no glowing magic, no modern fashion runway, no gravity droop, no extra limbs`

## 来源链接
- [[SRC-0402-V&A-1960年代连体工作服]] — 见对应来源卡
- [[SRC-0401-V&A-日本消防员外套]] — 见对应来源卡
- [[SRC-0123-FIT-wellington-boot]] — 见对应来源卡
- [[SRC-0403-V&A-1969年宇航员头盔]] — 见对应来源卡
- [[SRC-0410-V&A-ENSA制服徽章]] — 见对应来源卡
- [[SRC-0408-V&A-1930年代刺绣手袋]] — 见对应来源卡

## 相关卡片
- [[GAR-0038-连体工作服|连体工作服]]
- [[GAR-0037-消防防护外套|消防防护外套]]
- [[GAR-0022-威灵顿靴|威灵顿靴]]
- [[GAR-0039-安全头盔|安全头盔]]
- [[GAR-0050-制服徽章|制服徽章]]
- [[GAR-0048-手提包|手提包]]
- [[STY-0015-zero-gravity-opera-and-sci-fi-theatre|STY-0015]]
- [[SCN-0006-废弃空间站维修|废弃空间站维修]]

## 视觉参考

- REFERENCE_PENDING：无可核验匹配 ASSET。
- [[SRC-0402-V&A-1960年代连体工作服|SRC-0402]]
- [[SRC-0401-V&A-日本消防员外套|SRC-0401]]
- [[SRC-0123-FIT-wellington-boot|SRC-0123]]
- [[SRC-0403-V&A-1969年宇航员头盔|SRC-0403]]
- [[SRC-0410-V&A-ENSA制服徽章|SRC-0410]]
- [[SRC-0408-V&A-1930年代刺绣手袋|SRC-0408]]

## 生图提示词

### front_full
```text
SUBJECT (INTERPRETATION): complete outfit zero-gravity opera singer; LOOK-0033; items=GAR-0038, GAR-0037, GAR-0022, GAR-0039, GAR-0050, GAR-0048.
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
SUBJECT (INTERPRETATION): side and back of zero-gravity opera singer; LOOK-0033.
COMPOSITION (FACT/OBSERVATION): same look_items=GAR-0038, GAR-0037, GAR-0022, GAR-0039, GAR-0050, GAR-0048; no added construction.
LIGHT (CREATIVE): neutral soft key with rim separation.
CAMERA (CREATIVE): orthographic side/back, 50-85mm.
BACKGROUND (CREATIVE): neutral grey.
NEGATIVE (CREATIVE): no invented closures or layers.
CONSISTENCY (OBSERVATION): same palette, silhouette and item IDs.
```

## 视频提示词
```text
SUBJECT (INTERPRETATION): zero-gravity opera singer; slow 180-degree turn.
COMPOSITION (OBSERVATION): same look_items=GAR-0038, GAR-0037, GAR-0022, GAR-0039, GAR-0050, GAR-0048; no morphing.
LIGHT (CREATIVE): neutral key.
CAMERA (CREATIVE): 50mm full-body stable.
NEGATIVE (CREATIVE): no extra garments or logos.
CONSISTENCY (OBSERVATION): preserve item IDs, palette, layering.
```
