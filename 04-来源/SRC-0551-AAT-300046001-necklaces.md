---
id: SRC-0551
type: source
name_zh: "AAT 词条：necklaces（项链）"
name_en: "necklaces"
title: "Art & Architecture Thesaurus Full Record Display (Getty Research)"
publisher: Getty Research Institute — Art & Architecture Thesaurus (AAT)
url: "https://vocab.getty.edu/page/aat/300046001"
date_accessed: "2026-11-05"
source_kind: vocabulary
license_status: other_permission
rights_statement: Getty AAT 数据按 ODC-BY 1.0 发布，需署名；页面文字与图像另受 Getty 使用条款约束
evidence_status: verified
review_status: reviewed
note: AAT 记录 300046001：necklaces 的术语定义；curl 200 + prefLabel/Note 命中
tags: [source, vocabulary, aat, p5c]
---

# AAT 词条：necklaces（项链）

**AAT 记录**：300046001（`necklaces`）

**记录页**：https://vocab.getty.edu/page/aat/300046001（.nt 记录：https://vocab.getty.edu/aat/300046001.nt）

## 可支撑事实（verified 来源）

- AAT 首选词 necklaces；原文 Note："Ornaments worn around the neck, usually in the form of chains or strands of beads, pearls, stones, or decorative or precious materials, and often including a suspended ornamental pendant."
- 可支撑「项链/耳环套装」中项链的定义与佩戴方式。

## 验证记录

- `curl -sS -m 20 -L -o /tmp/a.nt -w '%{http_code}' "https://vocab.getty.edu/aat/300046001.nt"` → HTTP **200**，skos:prefLabel = `necklaces`
- `curl -sS -m 20 -L -o /tmp/a.html -w '%{http_code}' "https://vocab.getty.edu/page/aat/300046001"` → HTTP **200**，页面 `Note:` 与上方引文一致
- 验证日期：2026-11-05（Asia/Shanghai）

## 使用限制

- 不含具体历史款式（parure/rastra 等）；实例需另引 V&A/Met 藏品。
- 复用需署名 Getty。

## 可配合的主题

- 项链、配饰/珠宝
