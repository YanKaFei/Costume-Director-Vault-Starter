---
id: LOOK-0035
type: look
name_zh: 1930s 上海雨夜·男记者
name_en: 1930s Shanghai rain, male reporter
category: character_look
subcategory: historical
aliases:
- 1930s Shanghai rain, male reporter
periods:
- 1930s
regions:
- china
- shanghai
style_tags:
- STY-0012
colors:
- charcoal
- indigo
- rain_grey
- brown
materials:
- wool
- gabardine
- rubber
- leather
source_ids:
- SRC-0202
- SRC-0406
- SRC-0420
- SRC-0522
- SRC-0407
- SRC-0141
evidence_status: interpretive
review_status: draft
license_status: not_applicable
look_role: 1930 年代上海男记者（虚构，1930s）
look_items:
- GAR-0032
- GAR-0046
- GAR-0060
- GAR-0083
- GAR-0047
- MAT-0002
look_scene:
- SCN-0004
continuity_lock: 长衫领口/开衩、雨衣湿深、皮鞋水渍、伞持握侧固定；雨→室内单向。
prompt_en: 1930s Shanghai male reporter in rain, charcoal changshan under a dark rubberised
  raincoat, leather Oxford shoes, gloves, black umbrella, wet stone alley, film noir
  light, historical analogue
negative_prompt_en: no modern suit, no sneakers, no unchanged dry clothes, no fantasy
  elements, no clean boots in rain
narrative_meaning: 长衫是公共知识分子的日常，橡胶雨衣/伞/皮鞋是雨夜功能层；用层搭而非西装表达 1930s 上海男性。
prompt_image: 1930s Shanghai male reporter in rain, charcoal changshan under a dark
  rubberised raincoat, leather Oxford shoes, gloves, black umbrella, wet stone alley,
  film noir light, historical analogue
prompt_video: male reporter walking under an umbrella in rain, changshan hem and raincoat
  wet, leather shoes splashing, medium tracking shot, neon reflections, continuity
  on wetness and umbrella
negative_prompt: no modern suit, no sneakers, no unchanged dry clothes, no fantasy
  elements, no clean boots in rain
slot_coverage: one_piece=GAR-0032；外层=GAR-0046；鞋=GAR-0060；配饰=GAR-0083；携带物=GAR-0047；材料=MAT-0002
scene_states: S0 出门（dry）：长衫/雨衣干；S1 雨中（wet）：雨衣湿深、鞋水渍；S2 室内（drying）：雨衣挂起、鞋水痕。
evidence_limits: 长衫/雨衣/伞/鞋有来源；GAR-0083 为 17 世纪手套结构类比；无 1930s 上海男记者专门卡；雨夜组合为创作。
evidence_type: historical_evidence
character_function: 长衫 + 雨衣 + 皮鞋 + 伞的男性职业者：传统轮廓与租界现代性的并置。
hard_constraint_status: "PASS (R1.1 outfit.validate_hard_constraints; validate_outfits 12/12; 0 violations; 2026-11-05)"

risks: 长衫下摆与雨衣长度冲突；皮鞋雨中没有威灵顿靴；手套年代错配需设计说明。
tags:
- costume
- look
- p5c
- complete_outfit
- historical
outfit_slots:
- one_piece=GAR-0032
- outerwear=GAR-0046
- footwear=GAR-0060
- accessory=GAR-0083
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
context: Shanghai alley；1930 年代上海男记者（虚构，1930s）
continuity_state:
- S0 出门（dry）：长衫/雨衣干；S1 雨中（wet）：雨衣湿深、鞋水渍；S2 室内（drying）：雨衣挂起、鞋水痕。
historical_evidence:
- SRC-0202
- GAR-0032:SRC-0202
approved_anchors: []
---
# 1930s 上海雨夜·男记者 / 1930s Shanghai rain, male reporter

## 定义
1930 年代上海男记者（虚构，1930s）。本卡为**完整 Outfit**（五槽组织），evidence_type=`historical_evidence`；创作组合与缺证据处均在下方注明，不把设计当史实。

## 结构要点
- **槽位**：one_piece=GAR-0032；外层=GAR-0046；鞋=GAR-0060；配饰=GAR-0083；携带物=GAR-0047；材料=MAT-0002
- **人物功能**：长衫 + 雨衣 + 皮鞋 + 伞的男性职业者：传统轮廓与租界现代性的并置。
- **叙事意义**：长衫是公共知识分子的日常，橡胶雨衣/伞/皮鞋是雨夜功能层；用层搭而非西装表达 1930s 上海男性。

## 视觉辨识
- 色彩：charcoal, indigo, rain_grey, brown；材质：wool, gabardine, rubber, leather。
- 关键识别点：长衫领口/开衩、雨衣湿深、皮鞋水渍、伞持握侧固定；雨→室内单向。

## 适用条件
需要完整造型、清晰人物功能与跨镜头连续性的剧情/舞台/概念设计；按 evidence_type 决定史实/类比/创作的使用边界。

## 不适用条件
需要严格历史复原而未做来源核验；把创作组合当历史事实；把类比卡当 11 世纪/某一文化的实证。

## 提示词短语
- 生图：`1930s Shanghai male reporter in rain, charcoal changshan under a dark rubberised raincoat, leather Oxford shoes, gloves, black umbrella, wet stone alley, film noir light, historical analogue`
- 视频：`male reporter walking under an umbrella in rain, changshan hem and raincoat wet, leather shoes splashing, medium tracking shot, neon reflections, continuity on wetness and umbrella`
- 负向：`no modern suit, no sneakers, no unchanged dry clothes, no fantasy elements, no clean boots in rain`

## 来源链接
- [[SRC-0202-V&A-1930年代长衫]] — 见对应来源卡
- [[SRC-0406-V&A-橡胶丝绸雨衣1920]] — 见对应来源卡
- [[SRC-0420-V&A-1935男式牛津鞋]] — 见对应来源卡
- [[SRC-0522-V&A-1660s手套]] — 见对应来源卡
- [[SRC-0407-V&A-丝绸雨伞1927]] — 见对应来源卡
- [[SRC-0141-FIT-chantilly-lace]] — 见对应来源卡

## 相关卡片
- [[GAR-0032-长衫|长衫]]
- [[GAR-0046-雨衣|雨衣]]
- [[GAR-0060-1930年代男式皮鞋|1930 年代男式皮鞋]]
- [[GAR-0083-手套|手套]]
- [[GAR-0047-雨伞|雨伞]]
- [[MAT-0002-尚蒂伊蕾丝|尚蒂伊蕾丝]]
- [[STY-0012-1930s-Shanghai-rain-noir|STY-0012]]
- [[SCN-0004-1930年代上海知识分子对话|1930 年代上海知识分子对话]]

