---
id: LOOK-0030
type: look
name_zh: 1930s 上海雨夜·女记者
name_en: 1930s Shanghai rain, female reporter
category: character_look
subcategory: historical
aliases:
- 1930s Shanghai rain, female reporter
periods:
- 1930s
regions:
- china
- shanghai
style_tags:
- STY-0012
colors:
- indigo
- black
- rain_grey
- off_white
materials:
- silk
- gabardine
- rubber
- satin
source_ids:
- SRC-0200
- SRC-0201
- SRC-0406
- SRC-0123
- SRC-0459
- SRC-0407
- SRC-0141
evidence_status: interpretive
review_status: draft
license_status: not_applicable
look_role: 1930 年代上海女记者（虚构角色；1930s 上海造型）
look_items:
- GAR-0031
- GAR-0046
- GAR-0022
- GAR-0086
- GAR-0047
- MAT-0002
look_scene:
- SCN-0007
continuity_lock: 旗袍开衩/领口、雨衣湿深范围、靴筒泥污、伞面水珠与持握侧固定；雨→室内阴干单向推进。
prompt_en: 1930s Shanghai female reporter in rain, indigo qipao under a dark rubberised
 raincoat, rubber wellington boots, small brooch, black umbrella, wet neon alley,
 film noir lighting, historical analogue
negative_prompt_en: no modern nylon, no high heels in rain, no unchanged dry clothes,
 no clean boots, no fantasy elements
narrative_meaning: 旗袍是都市职业身份，橡胶雨衣与威灵顿靴是雨夜的功能层，胸针结构与蕾丝提供近景细节；伞是移动的“屋檐”。
prompt_image: 1930s Shanghai female reporter in rain, indigo qipao under a dark rubberised
 raincoat, rubber wellington boots, small brooch, black umbrella, wet neon alley,
 film noir lighting, historical analogue
prompt_video: female reporter walking through a rainy Shanghai alley under an umbrella,
 qipao hem and raincoat wet, boots splashing, medium tracking shot, neon reflections,
 continuity on wetness and umbrella side
negative_prompt: no modern nylon, no high heels in rain, no unchanged dry clothes,
 no clean boots, no fantasy elements
slot_coverage: one_piece=GAR-0031；外层=GAR-0046；鞋=GAR-0022；配饰=GAR-0086；携带物=GAR-0047；材料=MAT-0002
scene_states: S0 出门（dry）：旗袍/雨衣干、靴干净；S1 雨中（wet）：雨衣湿深、靴泥、伞水珠；S2 室内（drying）：雨衣挂起、靴泥干。
evidence_limits: 旗袍/雨衣/伞有来源；GAR-0086 为 19 世纪胸针结构类比；无 1930s 上海女记者专门卡；雨夜组合为创作推断。
evidence_type: historical_evidence
character_function: 雨夜后巷里保持职业体面的女性：旗袍的直身轮廓 + 防水外层 + 伞。
hard_constraint_status: "PASS (R1.1 outfit.validate_hard_constraints; validate_outfits 12/12; 0 violations; 2026-11-05)"

risks: 高跟鞋不用于雨；旗袍开衩影响快走；雨衣版型需不压扁旗袍轮廓。
tags:
- costume
- look
- p5c
- complete_outfit
- historical
outfit_slots:
- one_piece=GAR-0031
- outerwear=GAR-0046
- footwear=GAR-0022
- accessory=GAR-0086
- carried_prop=GAR-0047
weather: rain
action: walking
location: Shanghai alley
outfit_silhouette: H_line
constraints_checked:
- period
- region
- identity
- weather
- action
- compatibility
- approved_anchors
context: Shanghai alley；1930 年代上海女记者（虚构角色；1930s 上海造型）
continuity_state:
- S0 出门（dry）：旗袍/雨衣干、靴干净；S1 雨中（wet）：雨衣湿深、靴泥、伞水珠；S2 室内（drying）：雨衣挂起、靴泥干。
historical_evidence:
- SRC-0200
- SRC-0201
- GAR-0031:SRC-0200
approved_anchors: []
relations:
 - 'target=STY-0012; type=in_style; direction=outgoing; evidence=interpretive; confidence=medium; source_ids=SRC-0200; rule=R-STY-EXACT; review_status=review_queue; factual=false; design_only=true'
visual_prompt_profile: outfit_character_scene
visual_prompt_type: [character_scene, detail, video]
visual_evidence: [FACT, OBSERVATION, INFERENCE, CREATIVE]
---
# 1930s 上海雨夜·女记者 / 1930s Shanghai rain, female reporter

## 定义
1930 年代上海女记者（虚构角色；1930s 上海造型）。本卡为**完整 Outfit**（五槽组织），evidence_type=`historical_evidence`；创作组合与缺证据处均在下方注明，不把设计当史实。

## 结构要点
- **槽位**：one_piece=GAR-0031；外层=GAR-0046；鞋=GAR-0022；配饰=GAR-0086；携带物=GAR-0047；材料=MAT-0002
- **人物功能**：雨夜后巷里保持职业体面的女性：旗袍的直身轮廓 + 防水外层 + 伞。
- **叙事意义**：旗袍是都市职业身份，橡胶雨衣与威灵顿靴是雨夜的功能层，胸针结构与蕾丝提供近景细节；伞是移动的“屋檐”。

## 视觉辨识
- 色彩：indigo, black, rain_grey, off_white；材质：silk, gabardine, rubber, satin。
- 关键识别点：旗袍开衩/领口、雨衣湿深范围、靴筒泥污、伞面水珠与持握侧固定；雨→室内阴干单向推进。

## 适用条件
需要完整造型、清晰人物功能与跨镜头连续性的剧情/舞台/概念设计；按 evidence_type 决定史实/类比/创作的使用边界。

## 不适用条件
需要严格历史复原而未做来源核验；把创作组合当历史事实；把类比卡当 11 世纪/某一文化的实证。

## 提示词短语
- 生图：`1930s Shanghai female reporter in rain, indigo qipao under a dark rubberised raincoat, rubber wellington boots, small brooch, black umbrella, wet neon alley, film noir lighting, historical analogue`
- 视频：`female reporter walking through a rainy Shanghai alley under an umbrella, qipao hem and raincoat wet, boots splashing, medium tracking shot, neon reflections, continuity on wetness and umbrella side`
- 负向：`no modern nylon, no high heels in rain, no unchanged dry clothes, no clean boots, no fantasy elements`

## 来源链接
- [[SRC-0200-V&A-上海新新公司旗袍1930]] — 见对应来源卡
- [[SRC-0201-V&A-1930年代末旗袍]] — 见对应来源卡
- [[SRC-0406-V&A-橡胶丝绸雨衣1920]] — 见对应来源卡
- [[SRC-0123-FIT-wellington-boot]] — 见对应来源卡
- [[SRC-0459-V&A-Alice公主哀悼胸针]] — 见对应来源卡
- [[SRC-0407-V&A-丝绸雨伞1927]] — 见对应来源卡
- [[SRC-0141-FIT-chantilly-lace]] — 见对应来源卡

## 相关卡片
- [[GAR-0031-旗袍|旗袍]]
- [[GAR-0046-雨衣|雨衣]]
- [[GAR-0022-威灵顿靴|威灵顿靴]]
- [[GAR-0086-胸针结构|胸针结构]]
- [[GAR-0047-雨伞|雨伞]]
- [[MAT-0002-尚蒂伊蕾丝|尚蒂伊蕾丝]]
- [[STY-0012-1930s-Shanghai-rain-noir|STY-0012]]
- [[SCN-0007-上海雨夜后巷|上海雨夜后巷]]


## 视觉参考
- 本卡暂无已登记 ASSET；仅以现有 source_ids（[[SRC-0200-V&A-上海新新公司旗袍1930|SRC-0200]], [[SRC-0201-V&A-1930年代末旗袍|SRC-0201]], [[SRC-0406-V&A-橡胶丝绸雨衣1920|SRC-0406]], [[SRC-0123-FIT-wellington-boot|SRC-0123]], [[SRC-0459-V&A-Alice公主哀悼胸针|SRC-0459]], [[SRC-0407-V&A-丝绸雨伞1927|SRC-0407]], [[SRC-0141-FIT-chantilly-lace|SRC-0141]]；按来源卡许可）作文字参考，未下载/未内嵌图像。

## 生图提示词
```text
SUBJECT (FACT): full-body character look LOOK-0030 (1930s ·), one complete outfit, no extra layers.
STRUCTURE (FACT): look_items count=6; exact IDs are FACT; do not invent additional garments.
MATERIAL (FACT): materials=silk, gabardine, rubber, satin.
COLOR (FACT): colors=indigo, black, rain_grey, off_white.
LIGHT (CREATIVE): soft directional light, low contrast, gentle falloff; no claim about historical lighting.
CAMERA (CREATIVE): 35mm environmental full-body, eye level, 3/4 angle.
BACKGROUND (CREATIVE): restrained cinematic interior/exterior consistent with card scene; CREATIVE.
STYLE (INFERENCE): style tags=STY-0012; design interpretation only, not a historical claim.
NEGATIVE (CREATIVE): no invented fiber, weave, weight, transparency or structure; no extra garments/accessories; no logos or text; no costume morphing; no brand-specific design copying.
CONSISTENCY (OBSERVATION): keep card ID, palette, material tokens, silhouette/part family and relative proportions identical across frames.
```

## 视频提示词
```text
SUBJECT (FACT): character look LOOK-0030; one continuous walking/turn shot; preserve full outfit.
CONSISTENCY (OBSERVATION): preserve card ID, colors, material tokens, silhouette/part family and accessory placement across frames; no layering changes.
LIGHT (CREATIVE): soft directional key with gentle falloff; no invented historical lighting.
CAMERA (CREATIVE): slow gimbal move, 35-50mm, eye level, shallow but stable depth of field.
NEGATIVE (CREATIVE): no costume morphing, no colour shift, no extra layers, no logo/text/watermark, no brand-specific design copying.
```
