---
id: SRC-0023
type: source
name_zh: "Met 藏品（API）：连衣裙 ca. 1855"
name_en: "Dress, ca. 1855"
title: "Dress"
publisher: "The Metropolitan Museum of Art — Costume Institute"
url: "https://collectionapi.metmuseum.org/public/collection/v1/objects/159244"
date_accessed: "2026-11-04"
source_kind: museum_object_record
rights_statement: "Met Open Access 记录：API 返回 isPublicDomain=true，按 Met Open Access 政策该馆藏图像与记录数据以 CC0 提供；本卡仅存链接与元数据，不嵌入图像"
license_status: cc0
evidence_status: verified
review_status: reviewed
note: "Met 159244：美国 1855 年前后羊毛+丝绸连衣裙，Costume Institute，isPublicDomain=true"
tags: [source, museum_object, met, dress, 1850s]
---

# Met 藏品（API）：连衣裙 ca. 1855

**来源**：Dress

**发布者**：The Metropolitan Museum of Art — Costume Institute

**来源类型**：museum_object_record

**URL**：https://collectionapi.metmuseum.org/public/collection/v1/objects/159244

## 可支撑事实（verified）

- 对象号 159244；题名 Dress；年代 ca. 1855（1853–1857）；材质 wool, silk；文化 American；部门 Costume Institute。
- 来源：Brooklyn Museum Costume Collection at The Metropolitan Museum of Art, Gift of the Brooklyn Museum, 2009; Gift of Miss F. P. Weiss, 1948。
- API 返回 isPublicDomain=true，附官方对象页 https://www.metmuseum.org/art/collection/search/159244。

## 验证记录

- 验证命令：`curl -sS -m 10 -L -o /tmp/src.html -w '%{http_code}' "https://collectionapi.metmuseum.org/public/collection/v1/objects/159244"`
- 实际返回：HTTP **200**；响应标题／记录标题「Dress」；命中内容关键词「isPublicDomain: true」
- 验证日期：2026-11-04（Asia/Shanghai）

## 使用限制

- 对象页 www.metmuseum.org 在本次网络下返回 429（Vercel 校验），故以 API URL 为验证链接；对象页链接仅作参考。
- Met 元数据未给具体裙型细节，结构结论需结合图像或馆方研究。
- 仅存链接与元数据；不下载、不嵌入图像。
- 引用时保留原始页面标题与发布者；不得把本来源转述当作一手史料；图片仅存链接。

## 可配合的主题

- 19 世纪中女装、博物馆实物、年代/材质证据
