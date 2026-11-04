---
id: SRC-0534
type: source
name_zh: "V&A 藏品：羊毛佩斯利披肩改制的夹克（英国，1865–1885）"
name_en: "Wool jacket, England, 1865–1885"
title: "Jacket | Unknown | V&A Explore The Collections"
publisher: Victoria and Albert Museum
url: "https://collections.vam.ac.uk/item/O353447/"
date_accessed: "2026-11-05"
source_kind: museum_collection
license_status: link_only
rights_statement: © Victoria and Albert Museum；馆藏记录与图像仅可链接引用，不复制图像；对象描述引用时注明 V&A 与对象号。
evidence_status: verified
review_status: reviewed
note: V&A 对象 O353447；羊毛织物、里布/贴边、后长下摆；curl 200 验证（对象页 + API 记录）
tags: [source, museum_collection, vam, p5c]
---

# V&A 藏品：羊毛佩斯利披肩改制的夹克（英国，1865–1885）

**馆藏**：Victoria and Albert Museum，对象号 `O353447`

**对象页**：https://collections.vam.ac.uk/item/O353447/

**API 记录**：https://api.vam.ac.uk/v2/museumobject/O353447

## 可支撑事实（verified 来源；引用时保留对象号）

- 对象号 O353447；题名 Jacket；England, 1865–1885；材质 wool，faced with satin and lined with glazed cotton。
- 馆方 physicalDescription 原文："Jacket of wool Paisley shawl, restyled into a jacket with a band collar, long sleeves, fitted and with skirt basques, longer at the back."
- 可支撑「羊毛织物（wool）」「里布（lined with glazed cotton）」「贴边/衬（faced with satin）」「后长下摆（basques）」的实例。

## 验证记录

- 命令 `curl -sS -m 20 -L -o /tmp/v.html -w '%{http_code}' "https://collections.vam.ac.uk/item/O353447/"` → HTTP **200**，页面标题「Jacket | Unknown | V&A Explore The Collections」
- 命令 `curl -sS -m 20 -L -o /tmp/v.json -w '%{http_code}' "https://api.vam.ac.uk/v2/museumobject/O353447"` → HTTP **200**，`record.physicalDescription` 与上方引文一致
- 验证日期：2026-11-05（Asia/Shanghai）；图片未下载/未内嵌。

## 使用限制

- 改制衣（restyled）不是原始裁片，引用裁片结构时须说明改制背景。
- 仅链接引用。
- 引用时保留 V&A 对象号与对象页链接；不得把馆方描述改写成更普遍的历史结论。

## 可配合的主题

- 羊毛织物、里布/贴边、后长下摆
