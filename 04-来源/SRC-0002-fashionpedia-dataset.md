---
id: SRC-0002
type: source
name_zh: "Fashionpedia 数据集与本体说明页"
name_en: "Fashionpedia Dataset"
title: "Fashionpedia"
publisher: "Fashionpedia Consortium"
url: "https://fashionpedia.github.io/home/Fashionpedia_download.html"
date_accessed: "2026-11-04"
source_kind: dataset
rights_statement: "内容许可 cc_by；图像许可 link_only（未逐图核验）；本项目仅链接引用，不嵌入图片。"
license_status: cc_by
content_license: cc_by
image_license: link_only
license_verified: partial
evidence_status: verified
review_status: reviewed
note: "数据集构成图说与本体说明：类别/属性分离、与 DeepFashion2、ModaNet 类别映射；下载入口"
tags: [source, ontology, dataset, fashionpedia]
---

# Fashionpedia 数据集与本体说明页

**来源**：Fashionpedia

**发布者**：Fashionpedia Consortium

**来源类型**：dataset

**URL**：https://fashionpedia.github.io/home/Fashionpedia_download.html

## 可支撑事实（verified）

- 页面以图示说明数据集构成：(a) 主服装掩码、(b) 服饰部件掩码、(c) 主服装与部件掩码、(d) 细粒度属性、(e) 标注示意图、(f) 本体可视化。
- 原文说明：本体把「类别（categories）」与「属性（attributes）」概念分开，并覆盖 DeepFashion2 与 ModaNet 使用的预定义服装类别，可与这些数据集做映射。
- 页面说明 Fashionpedia 的 294 个细粒度属性、27 个主类别、19 个部件，以及检测+属性分类的新任务。

## 验证记录

- 验证命令：`curl -sS -m 10 -L -o /tmp/src.html -w '%{http_code}' "https://fashionpedia.github.io/home/Fashionpedia_download.html"`
- 实际返回：HTTP **200**；响应标题／记录标题「Fashionpedia」；命中内容关键词「separate the concept of categories (yellow nodes) and attributes (blue nodes)」
- 验证日期：2026-11-04（Asia/Shanghai）

## 使用限制

- 该页主要用于方法/本体结构参考，不提供任何单件服饰的历史信息。
- 属性词表可借用作描述字段，但中文译名需自行对照，不能声称是官方中文术语。
- 下载数据集图像不在本任务范围，且图像许可需另行遵守原图库条款。
- 引用时保留原始页面标题与发布者；不得把本来源转述当作一手史料；图片仅存链接。

## 可配合的主题

- 部件与属性字段设计、检索标签体系
