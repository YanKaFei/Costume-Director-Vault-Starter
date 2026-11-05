---
id: SRC-0530
type: source
name_zh: "V&A 藏品：黑色丝乔其纱方领晚装（Chanel/Kitmir，1923）"
name_en: "Evening dress, Coco Chanel / Kitmir, 1923"
title: "Evening Dress | Coco Chanel | V&A Explore The Collections"
publisher: Victoria and Albert Museum
url: "https://collections.vam.ac.uk/item/O72654/"
date_accessed: "2026-11-05"
source_kind: museum_collection
license_status: link_only
rights_statement: © Victoria and Albert Museum；馆藏记录与图像仅可链接引用，不复制图像；对象描述引用时注明 V&A 与对象号。
evidence_status: verified
review_status: reviewed
note: V&A 对象 O72654；领口形态（square）、丝绸/乔其纱、1920s 晚装；curl 200 验证（对象页 + API 记录）
tags: [source, museum_collection, vam, p5c]
---

# V&A 藏品：黑色丝乔其纱方领晚装（Chanel/Kitmir，1923）

**馆藏**：Victoria and Albert Museum，对象号 `O72654`

**对象页**：https://collections.vam.ac.uk/item/O72654/

**API 记录**：https://api.vam.ac.uk/v2/museumobject/O72654

## 可支撑事实（verified 来源；引用时保留对象号）

- 对象号 O72654（accession T.XXX? 以馆方记录为准）；题名 Evening dress；设计 Coco Chanel，刺绣 Kitmir，1923 春夏；材质 hand-sewn silk georgette, hand-embroidered with glass beads and gold thread。
- 馆方 physicalDescription 原文："Sleeveless and ankle-length evening dress made of black silk georgette embroidered with golden thread and bugle beads. Square-shape neckline and straight long bodice."
- 可用于「领口形态（square neckline）」与「丝绸/乔其纱」两个主题。

## 验证记录

- 命令 `curl -sS -m 20 -L -o /tmp/v.html -w '%{http_code}' "https://collections.vam.ac.uk/item/O72654/"` → HTTP **200**，页面标题「Evening Dress | Coco Chanel | V&A Explore The Collections」
- 命令 `curl -sS -m 20 -L -o /tmp/v.json -w '%{http_code}' "https://api.vam.ac.uk/v2/museumobject/O72654"` → HTTP **200**，`record.physicalDescription` 与上方引文一致
- 验证日期：2026-11-05（Asia/Shanghai）；图片未下载/未内嵌。

## 使用限制

- V&A 页面文字与图像受版权保护；本库只链接，不复制图像。
- 对象描述是馆方著录，不等于对所有 1920s 晚装的概括；引用时限定为该实例。
- 引用时保留 V&A 对象号与对象页链接；不得把馆方描述改写成更普遍的历史结论。

## 可配合的主题

- 领口形态（square）、丝绸/乔其纱、1920s 晚装

## 相关卡片

- [[MAT-0018-丝绸]]
- [[STR-0027-领口形态]]
- [[STR-0035-廓形与比例]]
