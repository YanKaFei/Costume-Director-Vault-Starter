---
id: SRC-0531
type: source
name_zh: "V&A 藏品：粉色刺绣雪纺日装（巴黎，约 1925）"
name_en: "Dress, Paris, ca. 1925"
title: "Dress | Unknown | V&A Explore The Collections"
publisher: Victoria and Albert Museum
url: "https://collections.vam.ac.uk/item/O85657/"
date_accessed: "2026-11-05"
source_kind: museum_collection
license_status: link_only
rights_statement: © Victoria and Albert Museum；馆藏记录与图像仅可链接引用，不复制图像；对象描述引用时注明 V&A 与对象号。
evidence_status: verified
review_status: reviewed
note: V&A 对象 O85657；领口形态（round）、抽褶、1920s 日装；curl 200 验证（对象页 + API 记录）
tags: [source, museum_collection, vam, p5c]
---

# V&A 藏品：粉色刺绣雪纺日装（巴黎，约 1925）

**馆藏**：Victoria and Albert Museum，对象号 `O85657`

**对象页**：https://collections.vam.ac.uk/item/O85657/

**API 记录**：https://api.vam.ac.uk/v2/museumobject/O85657

## 可支撑事实（verified 来源；引用时保留对象号）

- 对象号 O85657；题名 Dress；Paris, ca. 1925；材质 machine-sewn chiffon and hand embroidery。
- 馆方 physicalDescription 原文："Short day dress made of pink embroidered chiffon. … a round and wide neckline, and short sleeves. The long bodice ends at hips level and the skirt of the dress is slightly gathered at the hips."
- 可用于「领口形态（round neckline）」与「抽褶（gathered at hips）」的实例证据。

## 验证记录

- 命令 `curl -sS -m 20 -L -o /tmp/v.html -w '%{http_code}' "https://collections.vam.ac.uk/item/O85657/"` → HTTP **200**，页面标题「Dress | Unknown | V&A Explore The Collections」
- 命令 `curl -sS -m 20 -L -o /tmp/v.json -w '%{http_code}' "https://api.vam.ac.uk/v2/museumobject/O85657"` → HTTP **200**，`record.physicalDescription` 与上方引文一致
- 验证日期：2026-11-05（Asia/Shanghai）；图片未下载/未内嵌。

## 使用限制

- 馆方著录为单件实例；不得据此断言 1920s 全部日装领口。
- 仅链接引用，不复制图像。
- 引用时保留 V&A 对象号与对象页链接；不得把馆方描述改写成更普遍的历史结论。

## 可配合的主题

- 领口形态（round）、抽褶、1920s 日装
