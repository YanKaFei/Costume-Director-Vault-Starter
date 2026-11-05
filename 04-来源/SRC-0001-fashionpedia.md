---
id: SRC-0001
type: source
name_zh: "Fashionpedia 时尚本体（主页）"
name_en: "Fashionpedia"
title: "Fashionpedia"
publisher: "Fashionpedia Consortium"
url: "https://fashionpedia.github.io/home/index.html"
date_accessed: "2026-11-04"
source_kind: dataset
rights_statement: "内容许可 cc_by；图像许可 link_only（未逐图核验）；本项目仅链接引用，不嵌入图片。"
license_status: cc_by
content_license: cc_by
image_license: link_only
license_verified: partial
evidence_status: verified
review_status: reviewed
note: "专家构建的服饰本体：27 个主服装类别、19 个服饰部件、294 个细粒度属性及关系；仅作类别/属性分层参考"
tags: [source, ontology, terminology, fashionpedia]
---

# Fashionpedia 时尚本体（主页）

**来源**：Fashionpedia

**发布者**：Fashionpedia Consortium

**来源类型**：dataset

**URL**：https://fashionpedia.github.io/home/index.html

## 可支撑事实（verified）

- Fashionpedia 由两部分组成：(1) 由时尚专家构建的本体，含 27 个主服装类别、19 个服饰部件、294 个细粒度属性及其关系；(2) 48k 日常与名人活动时尚图像数据集，附分割掩码与逐掩码细粒度属性。
- 本体把「类别 categories」与「属性 attributes」明确分开，可作为本库「单品类别 / 部件 / 属性」分层的术语参照。
- 提供 Fashionpedia API、Attribute Mask-RCNN 基线模型与 iMat-Fashion (Kaggle) 任务入口。

## 验证记录

- 验证命令：`curl -sS -m 10 -L -o /tmp/src.html -w '%{http_code}' "https://fashionpedia.github.io/home/index.html"`
- 实际返回：HTTP **200**；响应标题／记录标题「Fashionpedia」；命中内容关键词「27 main apparel categories, 19 apparel parts, 294 fine-grained attributes」
- 验证日期：2026-11-04（Asia/Shanghai）

## 使用限制

- 本体与属性为英文视觉识别体系，不是历史考据，不能直接当作年代或文化事实。
- 类别体系与 DeepFashion2 / ModaNet 等数据集存在映射，映射本身不等于服饰史分类。
- 图像版权不属于 Fashionpedia，禁止复制或嵌入 Vault。
- 引用时保留原始页面标题与发布者；不得把本来源转述当作一手史料；图片仅存链接。

## 可配合的主题

- 单品类别、部件、属性标签；提示词与检索字段设计

## 相关卡片

- [[STR-0024-结构属性词表（Fashionpedia）]]
