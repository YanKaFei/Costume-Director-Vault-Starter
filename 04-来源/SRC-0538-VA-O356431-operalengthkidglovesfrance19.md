---
id: SRC-0538
type: source
name_zh: "V&A 藏品：白色小羊皮歌剧长度晚装手套（法国，1910 年代）"
name_en: "Opera-length kid gloves, France, 1910s"
title: "Pair of Gloves | V&A Explore The Collections"
publisher: Victoria and Albert Museum
url: "https://collections.vam.ac.uk/item/O356431/"
date_accessed: "2026-11-05"
source_kind: museum_collection
license_status: link_only
rights_statement: © Victoria and Albert Museum；馆藏记录与图像仅可链接引用，不复制图像；对象描述引用时注明 V&A 与对象号。
evidence_status: verified
review_status: reviewed
note: V&A 对象 O356431；晚装长手套、正式配饰、皮革；curl 200 验证（对象页 + API 记录）
tags: [source, museum_collection, vam, p5c]
---

# V&A 藏品：白色小羊皮歌剧长度晚装手套（法国，1910 年代）

**馆藏**：Victoria and Albert Museum，对象号 `O356431`

**对象页**：https://collections.vam.ac.uk/item/O356431/

**API 记录**：https://api.vam.ac.uk/v2/museumobject/O356431

## 可支撑事实（verified 来源；引用时保留对象号）

- 对象号 O356431；题名 Pair of gloves；made in France, retailed by A. Bide, London, 1910s；材质 kid leather。
- 馆方 physicalDescription 原文："Pair of kid leather gloves. Fine white kid evening or opera length gloves designed to cover the entire arm."
- 可支撑「晚装长手套（opera-length evening gloves）」及「遮臂」的正式性功能。

## 验证记录

- 命令 `curl -sS -m 20 -L -o /tmp/v.html -w '%{http_code}' "https://collections.vam.ac.uk/item/O356431/"` → HTTP **200**，页面标题「Pair of Gloves | Unknown | V&A Explore The Collections」
- 命令 `curl -sS -m 20 -L -o /tmp/v.json -w '%{http_code}' "https://api.vam.ac.uk/v2/museumobject/O356431"` → HTTP **200**，`record.physicalDescription` 与上方引文一致
- 验证日期：2026-11-05（Asia/Shanghai）；图片未下载/未内嵌。

## 使用限制

- 1910s 实例；手套长度/材质随年代与场合变化，不要泛化为所有晚装手套。
- 仅链接引用。
- 引用时保留 V&A 对象号与对象页链接；不得把馆方描述改写成更普遍的历史结论。

## 可配合的主题

- 晚装长手套、正式配饰、皮革
