---
id: LOOK-EXAMPLE-001
type: look
name_zh: 雨夜调查者
name_en: rainy-night investigator
category: character_look
subcategory: film_costume
aliases: []
periods: [contemporary_fictional]
regions: [unspecified_city]
style_tags: [noir, restrained]
colors: [charcoal, off_white]
materials: [wool, cotton, leather]
source_ids: []
evidence_status: example
review_status: draft
license_status: not_applicable
look_role: 原创虚构的现代都市调查人员（example）
look_items: [GAR-EXAMPLE-001, GAR-0014, GAR-0022]
look_scene: []
continuity_lock: 外套长度至膝上、三枚纽扣、左肩帆布包；雨前与雨后为不同子状态，不得在同一镜头内自动更换衣物颜色
prompt_en: adult fictional urban investigator, charcoal knee-length wool overcoat, off-white stand-collar cotton shirt, straight dark trousers, worn black lace-up leather boots, aged canvas shoulder bag on left shoulder, restrained cinematic styling, realistic cloth response, consistent costume across shots
negative_prompt_en: no unexpected hat, no jewelry added, no coat redesign between shots, no color shifts, no costume morphing
tags: [costume, look, example, noir]
---
# LOOK-EXAMPLE-001 雨夜调查者 / rainy-night investigator

## 定义
原创虚构角色的完整造型样本：现代都市调查人员，夜间户外、情绪紧张、生活略显拮据。它是 `example`，用于演示 Look 卡如何拆解与锁定，不指向真实人物或真实品牌。

## 结构要点
- 上装：[[GAR-EXAMPLE-001-白色立领衬衫]]（暖白棉质、直身剪裁），作为内层。
- 外层：炭灰中长羊毛大衣（知识库暂无现代都市大衣卡，属覆盖缺口；本 Look 以文字描述保留该层）。
- 下装/鞋：以现有卡片替代——[[GAR-0014-牛仔裤]] 近似“深色直筒长裤”，[[GAR-0022-威灵顿靴]] 近似“有磨损的系带皮靴”；左肩旧帆布包无 carried_prop 卡（覆盖缺口）。
- 配色：炭灰、暖白与旧皮革的黑色，低对比三层结构。

## 视觉辨识
中长外套压住比例，暖白领口从灰黑外层中露出；鞋面有磨损，包体旧化。镜头之间保持同一套轮廓与配色，只允许状态（湿度、褶皱、污渍）变化。

## 适用条件
现代/近未来都市悬疑与调查题材；夜景与低照度摄影；需要跨场次一致性与低预算复用。

## 不适用条件
历史年代剧；高饱和商业片；需要多套换装的社交场合；把本示例当作真实品牌或真实人物的服装记录。

## 提示词短语
- 生图主体：`adult fictional urban investigator, charcoal knee-length wool overcoat, off-white stand-collar cotton shirt, straight dark trousers, worn black lace-up leather boots, aged canvas shoulder bag on left shoulder, restrained cinematic styling, realistic cloth response, consistent costume across shots`
- 负向：`no unexpected hat, no jewelry added, no coat redesign between shots, no color shifts, no costume morphing`

## 来源链接
- 无直接来源；本卡为原创示例（example）。参考风格见 [[STY-EXAMPLE-001-克制的都市黑色电影]]。

## 相关卡片
- [[STY-EXAMPLE-001-克制的都市黑色电影]]
- [[GAR-EXAMPLE-001-白色立领衬衫]]
- [[LOOK-0007-当代雨夜调查者连续性]]

## 视觉参考

- REFERENCE_PENDING：无可核验匹配 ASSET。
- 无来源卡；REFERENCE_PENDING

## 生图提示词

### front_full
```text
SUBJECT (INTERPRETATION): complete outfit rainy-night investigator; LOOK-EXAMPLE-001; items=GAR-EXAMPLE-001, GAR-0014, GAR-0022.
COMPOSITION (FACT/OBSERVATION): only listed look_items and their cards; no invented garment.
MATERIAL (OBSERVATION): from listed item cards; unknown where absent.
COLOR (OBSERVATION): card palette only.
LIGHT (CREATIVE): neutral key, soft falloff.
CAMERA (CREATIVE): 50mm full-body, eye level, front.
BACKGROUND (CREATIVE): neutral grey; scene context only.
NEGATIVE (CREATIVE): no extra garments, brands or invented history.
CONSISTENCY (OBSERVATION): preserve item IDs and layering.
DISTINCTION (FACT): LOOK-EXAMPLE-001 rainy-night investigator; type=look; materials=wool,cotton,leather; colors=charcoal,off_white; look_items=GAR-EXAMPLE-001,GAR-0014,GAR-0022; DISTINCT FROM LOOK-0007; preserve these fields and do not merge the two cards.
```

### side_back
```text
SUBJECT (INTERPRETATION): side and back of rainy-night investigator; LOOK-EXAMPLE-001.
COMPOSITION (FACT/OBSERVATION): same look_items=GAR-EXAMPLE-001, GAR-0014, GAR-0022; no added construction.
LIGHT (CREATIVE): neutral soft key with rim separation.
CAMERA (CREATIVE): orthographic side/back, 50-85mm.
BACKGROUND (CREATIVE): neutral grey.
NEGATIVE (CREATIVE): no invented closures or layers.
CONSISTENCY (OBSERVATION): same palette, silhouette and item IDs.
DISTINCTION (FACT): LOOK-EXAMPLE-001 rainy-night investigator; type=look; materials=wool,cotton,leather; colors=charcoal,off_white; look_items=GAR-EXAMPLE-001,GAR-0014,GAR-0022; DISTINCT FROM LOOK-0007; preserve these fields and do not merge the two cards.
```

## 视频提示词
```text
SUBJECT (INTERPRETATION): rainy-night investigator; slow 180-degree turn.
COMPOSITION (OBSERVATION): same look_items=GAR-EXAMPLE-001, GAR-0014, GAR-0022; no morphing.
LIGHT (CREATIVE): neutral key.
CAMERA (CREATIVE): 50mm full-body stable.
NEGATIVE (CREATIVE): no extra garments or logos.
CONSISTENCY (OBSERVATION): preserve item IDs, palette, layering.
```
