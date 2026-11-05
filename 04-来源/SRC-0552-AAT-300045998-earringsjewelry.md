---
id: SRC-0552
type: source
name_zh: "AAT 词条：earrings（耳环）"
name_en: "earrings (jewelry)"
title: "Art & Architecture Thesaurus Full Record Display (Getty Research)"
publisher: Getty Research Institute — Art & Architecture Thesaurus (AAT)
url: "https://vocab.getty.edu/page/aat/300045998"
date_accessed: "2026-11-05"
source_kind: vocabulary
license_status: other_permission
rights_statement: Getty AAT 数据按 ODC-BY 1.0 发布，需署名；页面文字与图像另受 Getty 使用条款约束
evidence_status: verified
review_status: reviewed
note: AAT 记录 300045998：earrings (jewelry) 的术语定义；curl 200 + prefLabel/Note 命中
tags: [source, vocabulary, aat, p5c]
---

# AAT 词条：earrings（耳环）

**AAT 记录**：300045998（`earrings (jewelry)`）

**记录页**：https://vocab.getty.edu/page/aat/300045998（.nt 记录：https://vocab.getty.edu/aat/300045998.nt）

## 可支撑事实（verified 来源）

- AAT 首选词 earrings (jewelry)；原文 Note："Ear ornaments worn suspended from a bent wire or a thin loop passed through a hole pierced in the lobe of the ear or clipped or screwed to the lobe."
- 可支撑「耳环」定义及三种佩戴方式（穿耳/夹/螺旋）。

## 验证记录

- `curl -sS -m 20 -L -o /tmp/a.nt -w '%{http_code}' "https://vocab.getty.edu/aat/300045998.nt"` → HTTP **200**，skos:prefLabel = `earrings (jewelry)`
- `curl -sS -m 20 -L -o /tmp/a.html -w '%{http_code}' "https://vocab.getty.edu/page/aat/300045998"` → HTTP **200**，页面 `Note:` 与上方引文一致
- 验证日期：2026-11-05（Asia/Shanghai）

## 使用限制

- 不含具体年代/材质；实例需另引藏品。
- 复用需署名 Getty。

## 可配合的主题

- 耳环、配饰/珠宝

## 相关卡片

- [[GAR-0090-项链与耳环]]
