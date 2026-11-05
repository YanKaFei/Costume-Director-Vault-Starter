---
id: SRC-0547
type: source
name_zh: "AAT 词条：wool（毛织物）"
name_en: "wool (textile)"
title: "Art & Architecture Thesaurus Full Record Display (Getty Research)"
publisher: Getty Research Institute — Art & Architecture Thesaurus (AAT)
url: "https://vocab.getty.edu/page/aat/300243430"
date_accessed: "2026-11-05"
source_kind: vocabulary
license_status: other_permission
rights_statement: Getty AAT 数据按 ODC-BY 1.0 发布，需署名；页面文字与图像另受 Getty 使用条款约束
evidence_status: verified
review_status: reviewed
note: AAT 记录 300243430：wool (textile) 的术语定义；curl 200 + prefLabel/Note 命中
tags: [source, vocabulary, aat, p5c]
---

# AAT 词条：wool（毛织物）

**AAT 记录**：300243430（`wool (textile)`）

**记录页**：https://vocab.getty.edu/page/aat/300243430（.nt 记录：https://vocab.getty.edu/aat/300243430.nt）

## 可支撑事实（verified 来源）

- AAT 首选词 wool (textile)；原文 Note："Textile made from the animal hair wool."
- 可支撑「羊毛织物」作为纺织品的定义；与羊毛纤维（silk/wool fiber）区分。

## 验证记录

- `curl -sS -m 20 -L -o /tmp/a.nt -w '%{http_code}' "https://vocab.getty.edu/aat/300243430.nt"` → HTTP **200**，skos:prefLabel = `wool (textile)`
- `curl -sS -m 20 -L -o /tmp/a.html -w '%{http_code}' "https://vocab.getty.edu/page/aat/300243430"` → HTTP **200**，页面 `Note:` 与上方引文一致
- 验证日期：2026-11-05（Asia/Shanghai）

## 使用限制

- 定义极简，不含 twill/flannel/tweed 组织差异；组织需另引 AAT weave 或实例 V&A 0204/0534。
- 复用需署名 Getty。

## 可配合的主题

- 羊毛织物、材质族

## 相关卡片

- [[MAT-0015-羊毛织物]]
