---
id: STR-0024
type: garment_part
name_zh: 结构属性词表（Fashionpedia）
name_en: structure attribute taxonomy (Fashionpedia)
category: construction
subcategory: layering
aliases: [Fashionpedia attributes, ontology, 结构词表, 属性词表]
periods: []
regions: []
style_tags: [ontology, taxonomy]
colors: []
materials: []
source_ids: [SRC-0001]
evidence_status: verified
review_status: reviewed
license_status: not_applicable
part_family: layering
structural_notes: Fashionpedia 本体把服装类别（categories）与属性（attributes）分层，含 27 个主类别、19 个服饰部件、294 个细粒度属性（SRC-0001）。本卡据此建立 v1.2 可选结构词表的映射原则：类别≠部件≠属性。
construction_era: []
prompt_en: 'ontology-aligned costume description: category (garment type), part (collar/sleeve/waist/hem), attribute (shape, length, closure, material)'
tags: [costume, construction, taxonomy, ontology]
relations:
  - 'target=SRC-0001; type=claim_supported_by; direction=outgoing; evidence=verified; confidence=high; source_ids=SRC-0001; rule=R-SOURCE-IDS'
---
# 结构属性词表（Fashionpedia） / structure attribute taxonomy (Fashionpedia)

## 定义
结构属性词表是用于把“类别/部件/属性”分层描述的术语集合；Fashionpedia 本体是 CC BY 4.0 的专家标注体系（SRC-0001），本库 v1.2 的可选字段参考其分层原则。

## 结构要点
- 类别（category）：garment 的主类（上装/下装/连身/外层/鞋/帽/配饰）。
- 部件（part）：领/袖/肩/腰/摆/门襟/口袋/闭合等结构。
- 属性（attribute）：形状、长度、版型、松量、材料、颜色、纹样、闭合等。
- Fashionpedia：27 个主类别、19 个服饰部件、294 个细粒度属性（SRC-0001）；本库只借分层方法，不复制其图像/标注。

## 视觉辨识
不适用（词表卡）；用于检索与字段设计，不直接对应画面。

## 适用条件
卡片字段设计、检索词归一、跨类目映射；新卡填写 v1.2 可选字段时的参考。

## 不适用条件
作为某件服装的实物证据；替代具体 GAR/STR/MAT 卡；历史/文化判断。

## 提示词短语
- 生图片段：`ontology-aligned costume description: category (garment type), part (collar/sleeve/waist/hem), attribute (shape, length, closure, material)`
- 中文造型说明：按类别/部件/属性分层描述服装：类别（单品类型）、部件（领袖腰摆）、属性（形状/长度/闭合/材料）。

## 来源链接
- [[SRC-0001-fashionpedia]] Fashionpedia 时尚本体（主页） — https://fashionpedia.github.io/home/index.html
- 支撑范围：Fashionpedia 主页（SRC-0001）：专家构建的服饰本体，27 main apparel categories、19 apparel parts、294 fine-grained attributes；类别与属性分离。

## 相关卡片
- [[STR-0012-翻领与驳领]]
- [[STR-0013-装袖与插肩袖]]
- [[STR-0015-腰线]]
- [[STR-0016-衣摆与开衩]]
- [[SRC-0001-fashionpedia]] — cited source (exact source_ids; no URL guessing)

## 视觉参考
- `REFERENCE_PENDING`: no verified ASSET matched for this card; use card fields and source links only; do not embed/download images.
- Source cards:
- [[SRC-0001-fashionpedia|SRC-0001]]
- Structure/material links: [[STR-0012-翻领与驳领]], [[STR-0013-装袖与插肩袖]], [[STR-0015-腰线]], [[STR-0016-衣摆与开衩]]
- Outfit elements: none registered; do not force a LOOK

## 生图提示词
### detail
```text
SUBJECT (FACT): isolated garment component study of structure attribute taxonomy (Fashionpedia); part_family=layering; orthographic front, side and back views; optional cross-section outline marked INFERENCE, no invented cut or pattern pieces.
STRUCTURE (FACT/OBSERVATION): ontology-aligned costume description: category (garment type), part (collar/sleeve/waist/hem), attribute (shape, length, closure, material); relative proportions only, no invented measurements.
MATERIAL (FACT): unknown; no material claim.
COLOR (FACT): unknown; no color claim.
LIGHT (CREATIVE): neutral 5600K studio light, soft directional falloff; no historical-lighting claim.
CAMERA (CREATIVE): 85mm detail lens, f/5.6, orthographic front/side/back, clean edges.
BACKGROUND (CREATIVE): neutral mid-grey studio; no historical set implied.
STYLE (INFERENCE): professional component reference plate; art direction only.
NEGATIVE (CREATIVE): no invented seams, closures, cut lines, fiber, weave, weight, transparency or construction details; no logos/text; no extra objects.
CONSISTENCY (OBSERVATION): preserve card ID STR-0024, part_family, proportions, material tokens and palette across views.
```

### applied
```text
SUBJECT (FACT): structure attribute taxonomy (Fashionpedia) applied on a complete period-appropriate garment; full garment visible; preserve component position and scale.
STRUCTURE (FACT/OBSERVATION): ontology-aligned costume description: category (garment type), part (collar/sleeve/waist/hem), attribute (shape, length, closure, material); do not infer unseen closures or seams.
MATERIAL (FACT): unknown; no material claim.
COLOR (FACT): unknown; no color claim.
LIGHT (CREATIVE): soft directional key with gentle fill; no invented historical lighting.
CAMERA (CREATIVE): full-garment three-quarter view, 50mm, eye level, f/5.6.
BACKGROUND (CREATIVE): neutral studio or card-described context only; no invented set.
STYLE (INFERENCE): applied construction reference; art direction only.
NEGATIVE (CREATIVE): no invented garment layers, closures, fiber/weave/weight or era details; no logos/text; no costume morphing.
CONSISTENCY (OBSERVATION): preserve STR-0024, part_family, palette and relative component proportions across frames.
```

## 视频提示词
```text
SUBJECT (FACT): STR-0024 — slow 180-degree reference turn of structure attribute taxonomy (Fashionpedia) component.
CONSISTENCY (OBSERVATION): preserve card ID, part_family, material tokens, palette and proportions; no construction changes.
LIGHT (CREATIVE): soft directional key, gentle falloff; no historical-lighting claim.
CAMERA (CREATIVE): slow gimbal orbit, 50–85mm, stable macro focus; no morphing.
NEGATIVE (CREATIVE): no invented motion, fabric behavior, seams or structure; no logo/text.
```
