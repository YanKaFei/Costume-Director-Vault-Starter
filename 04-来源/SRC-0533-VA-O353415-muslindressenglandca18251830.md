---
id: SRC-0533
type: source
name_zh: "V&A 藏品：白色细布高腰连衣裙（英国，约 1825–30）"
name_en: "Muslin dress, England, ca. 1825–1830"
title: "Dress | Unknown | V&A Explore The Collections"
publisher: Victoria and Albert Museum
url: "https://collections.vam.ac.uk/item/O353415/"
date_accessed: "2026-11-05"
source_kind: museum_collection
license_status: link_only
rights_statement: © Victoria and Albert Museum；馆藏记录与图像仅可链接引用，不复制图像；对象描述引用时注明 V&A 与对象号。
evidence_status: verified
review_status: reviewed
note: V&A 对象 O353415；泡泡袖、褶裥、抽褶、高腰线、后开合；curl 200 验证（对象页 + API 记录）
tags: [source, museum_collection, vam, p5c]
---

# V&A 藏品：白色细布高腰连衣裙（英国，约 1825–30）

**馆藏**：Victoria and Albert Museum，对象号 `O353415`

**对象页**：https://collections.vam.ac.uk/item/O353415/

**API 记录**：https://api.vam.ac.uk/v2/museumobject/O353415

## 可支撑事实（verified 来源；引用时保留对象号）

- 对象号 O353415；题名 Dress；England, ca. 1825–1830；材质 muslin + whitework embroidery，附 lilac silk belt（1870–1899）。
- 馆方 physicalDescription 原文："Muslin dress with high round neckline, long puffed and pleated sleeves, high waistline, back fastening and long skirt gathered at the waist."
- 可支撑「泡泡袖（puffed sleeves）」「褶裥（pleated）」「抽褶（gathered at waist）」「高腰线（high waistline）」「后开合（back fastening）」的实例。

## 验证记录

- 命令 `curl -sS -m 20 -L -o /tmp/v.html -w '%{http_code}' "https://collections.vam.ac.uk/item/O353415/"` → HTTP **200**，页面标题「Dress | Unknown | V&A Explore The Collections」
- 命令 `curl -sS -m 20 -L -o /tmp/v.json -w '%{http_code}' "https://api.vam.ac.uk/v2/museumobject/O353415"` → HTTP **200**，`record.physicalDescription` 与上方引文一致
- 验证日期：2026-11-05（Asia/Shanghai）；图片未下载/未内嵌。

## 使用限制

- 19 世纪初实例；不同年代的 puff sleeve 体量差异很大，不可跨年代泛化。
- 仅链接引用。
- 引用时保留 V&A 对象号与对象页链接；不得把馆方描述改写成更普遍的历史结论。

## 可配合的主题

- 泡泡袖、褶裥、抽褶、高腰线、后开合

## 相关卡片

- [[STR-0027-领口形态]]
- [[STR-0029-泡泡袖]]
- [[STR-0032-褶裥与抽褶]]
- [[STR-0035-廓形与比例]]
