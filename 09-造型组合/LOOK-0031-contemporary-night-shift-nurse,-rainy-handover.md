---
id: LOOK-0031
type: look
name_zh: 当代夜班护士·雨夜交班
name_en: contemporary night-shift nurse, rainy handover
category: character_look
subcategory: contemporary
aliases:
- contemporary night-shift nurse, rainy handover
periods:
- contemporary
regions:
- britain
- global
style_tags:
- STY-0013
colors:
- white
- navy
- pale_blue
- black
materials:
- cotton
- polyester
- rubber
- leather
source_ids:
- SRC-0400
- SRC-0406
- SRC-0410
- SRC-0408
evidence_status: interpretive
review_status: draft
license_status: not_applicable
look_role: 当代急诊科护士（虚构，夜班雨夜交班）
look_items:
- GAR-0036
- GAR-0046
- GAR-0044
- GAR-0050
- GAR-0048
look_scene:
- SCN-0005
continuity_lock: 制服领口/口袋、工牌位置、雨衣湿深、工作鞋鞋底/颜色固定；液体污渍只按事件增加。
prompt_en: contemporary emergency nurse at night in rain, white uniform under a dark
  raincoat, closed non-slip medical shoes, badge, off-duty bag, hospital entrance,
  wet pavement, realistic cinematic light
negative_prompt_en: no printed scrubs, no high heels, no open-toe shoes, no jewelry,
  no instant stain removal, no costume change
narrative_meaning: 白色制服是秩序与专业，雨衣与工作鞋是通勤功能层，工牌/包是身份与下班界线。
prompt_image: contemporary emergency nurse at night in rain, white uniform under a
  dark raincoat, closed non-slip medical shoes, badge, off-duty bag, hospital entrance,
  wet pavement, realistic cinematic light
prompt_video: nurse walking quickly into an emergency department in rain, raincoat
  over white uniform, badge catching light, bag set down, handheld medium shot, continuity
  on uniform and badge
negative_prompt: no printed scrubs, no high heels, no open-toe shoes, no jewelry,
  no instant stain removal, no costume change
slot_coverage: one_piece=GAR-0036；外层=GAR-0046；鞋=GAR-0044；配饰=GAR-0050；携带物=GAR-0048
scene_states: S0 雨中到院（wet）：雨衣湿、鞋面水；S1 交班（drying）：雨衣挂起、制服干；液体污渍仅事件后增加。
evidence_limits: GAR-0036 为 1960s V&A 护士装，非现代临床制服；GAR-0044 为 interpretive 医疗工作鞋；无现代
  scrub/PPE/口罩；不得声称某医院真实制服。
evidence_type: sourced_style_observation
character_function: 雨夜赶到医院的护士：职业锚点（护士服/工牌/闭口工作鞋）+ 防水外层。
hard_constraint_status: "PASS (R1.1 outfit.validate_hard_constraints; validate_outfits 12/12; 0 violations; 2026-11-05)"

risks: 制服年代错位；雨衣压皱制服；工牌替代物（ENSA 徽章）需近景说明。
tags:
- costume
- look
- p5c
- complete_outfit
- contemporary
outfit_slots:
- one_piece=GAR-0036
- outerwear=GAR-0046
- footwear=GAR-0044
- accessory=GAR-0050
- carried_prop=GAR-0048
weather: rain
action: walking
location: hospital entrance
outfit_silhouette: straight
constraints_checked:
- period
- region
- identity
- weather
- action
- compatibility
- approved_anchors
context: hospital entrance；当代急诊科护士（虚构，夜班雨夜交班）
continuity_state:
- S0 雨中到院（wet）：雨衣湿、鞋面水；S1 交班（drying）：雨衣挂起、制服干；液体污渍仅事件后增加。
style_observation:
- 职业锚点（护士服/工牌/闭口工作鞋/雨衣）来自来源卡与库内职业卡；医院场景为设计观察。
approved_anchors: []
relations:
  - 'target=GAR-0036; type=appears_in_look; direction=outgoing; evidence=interpretive; confidence=medium; source_ids=SRC-0400; rule=R-LOOK-ITEMS; review_status=review_queue; factual=false; design_only=true'
---
# 当代夜班护士·雨夜交班 / contemporary night-shift nurse, rainy handover

## 定义
当代急诊科护士（虚构，夜班雨夜交班）。本卡为**完整 Outfit**（五槽组织），evidence_type=`sourced_style_observation`；创作组合与缺证据处均在下方注明，不把设计当史实。

## 结构要点
- **槽位**：one_piece=GAR-0036；外层=GAR-0046；鞋=GAR-0044；配饰=GAR-0050；携带物=GAR-0048
- **人物功能**：雨夜赶到医院的护士：职业锚点（护士服/工牌/闭口工作鞋）+ 防水外层。
- **叙事意义**：白色制服是秩序与专业，雨衣与工作鞋是通勤功能层，工牌/包是身份与下班界线。

## 视觉辨识
- 色彩：white, navy, pale_blue, black；材质：cotton, polyester, rubber, leather。
- 关键识别点：制服领口/口袋、工牌位置、雨衣湿深、工作鞋鞋底/颜色固定；液体污渍只按事件增加。

## 适用条件
需要完整造型、清晰人物功能与跨镜头连续性的剧情/舞台/概念设计；按 evidence_type 决定史实/类比/创作的使用边界。

## 不适用条件
需要严格历史复原而未做来源核验；把创作组合当历史事实；把类比卡当 11 世纪/某一文化的实证。

## 提示词短语
- 生图：`contemporary emergency nurse at night in rain, white uniform under a dark raincoat, closed non-slip medical shoes, badge, off-duty bag, hospital entrance, wet pavement, realistic cinematic light`
- 视频：`nurse walking quickly into an emergency department in rain, raincoat over white uniform, badge catching light, bag set down, handheld medium shot, continuity on uniform and badge`
- 负向：`no printed scrubs, no high heels, no open-toe shoes, no jewelry, no instant stain removal, no costume change`

## 来源链接
- [[SRC-0400-V&A-1960年代护士戏服]] — 见对应来源卡
- [[SRC-0406-V&A-橡胶丝绸雨衣1920]] — 见对应来源卡
- [[SRC-0410-V&A-ENSA制服徽章]] — 见对应来源卡
- [[SRC-0408-V&A-1930年代刺绣手袋]] — 见对应来源卡

## 相关卡片
- [[GAR-0036-护士制服|护士制服]]
- [[GAR-0046-雨衣|雨衣]]
- [[GAR-0044-医疗工作鞋|医疗工作鞋]]
- [[GAR-0050-制服徽章|制服徽章]]
- [[GAR-0048-手提包|手提包]]
- [[STY-0013-contemporary-occupational-uniform-realism|STY-0013]]
- [[SCN-0005-急诊夜班抢救|急诊夜班抢救]]

