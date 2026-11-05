---
id: SRC-0535
type: source
name_zh: "V&A 藏品：淡紫丝绸连衣裙（英国，1870–72）"
name_en: "Silk dress, England, 1870–1872"
title: "Dress | Unknown | V&A Explore The Collections"
publisher: Victoria and Albert Museum
url: "https://collections.vam.ac.uk/item/O355340/"
date_accessed: "2026-11-05"
source_kind: museum_collection
license_status: link_only
rights_statement: © Victoria and Albert Museum；馆藏记录与图像仅可链接引用，不复制图像；对象描述引用时注明 V&A 与对象号。
evidence_status: verified
review_status: reviewed
note: V&A 对象 O355340；拖尾、方领、纽扣开合、钟形袖；curl 200 验证（对象页 + API 记录）
tags: [source, museum_collection, vam, p5c]
---

# V&A 藏品：淡紫丝绸连衣裙（英国，1870–72）

**馆藏**：Victoria and Albert Museum，对象号 `O355340`

**对象页**：https://collections.vam.ac.uk/item/O355340/

**API 记录**：https://api.vam.ac.uk/v2/museumobject/O355340

## 可支撑事实（verified 来源；引用时保留对象号）

- 对象号 O355340；题名 Dress；England, 1870–1872；材质 lilac silk，satin ribbon and machine-made lace。
- 馆方 physicalDescription 原文："The bodice has a low square neckline, button fastening, and bell-shaped sleeves. The skirt is long with a rounded train."
- 可支撑「拖尾（rounded train）」「方领（square neckline）」「纽扣开合（button fastening）」「钟形袖（bell-shaped sleeves）」的实例。

## 验证记录

- 命令 `curl -sS -m 20 -L -o /tmp/v.html -w '%{http_code}' "https://collections.vam.ac.uk/item/O355340/"` → HTTP **200**，页面标题「Dress | Unknown | V&A Explore The Collections」
- 命令 `curl -sS -m 20 -L -o /tmp/v.json -w '%{http_code}' "https://api.vam.ac.uk/v2/museumobject/O355340"` → HTTP **200**，`record.physicalDescription` 与上方引文一致
- 验证日期：2026-11-05（Asia/Shanghai）；图片未下载/未内嵌。

## 使用限制

- 1870s 实例；train 长度与场合等级相关，不可跨年代套用。
- 仅链接引用。
- 引用时保留 V&A 对象号与对象页链接；不得把馆方描述改写成更普遍的历史结论。

## 可配合的主题

- 拖尾、方领、纽扣开合、钟形袖

## 相关卡片

- [[MAT-0018-丝绸]]
- [[STR-0027-领口形态]]
- [[STR-0034-拖尾]]
- [[STR-0035-廓形与比例]]
