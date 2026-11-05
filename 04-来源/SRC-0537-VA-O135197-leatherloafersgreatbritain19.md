---
id: SRC-0537
type: source
name_zh: "V&A 藏品：黑色皮革乐福鞋（英国，1970 年代）"
name_en: "Leather loafers, Great Britain, 1970s"
title: "Pair of Shoes | | V&A Explore The Collections"
publisher: Victoria and Albert Museum
url: "https://collections.vam.ac.uk/item/O135197/"
date_accessed: "2026-11-05"
source_kind: museum_collection
license_status: link_only
rights_statement: © Victoria and Albert Museum；馆藏记录与图像仅可链接引用，不复制图像；对象描述引用时注明 V&A 与对象号。
evidence_status: verified
review_status: reviewed
note: V&A 对象 O135197；乐福鞋/便装鞋、流苏饰；curl 200 验证（对象页 + API 记录）
tags: [source, museum_collection, vam, p5c]
---

# V&A 藏品：黑色皮革乐福鞋（英国，1970 年代）

**馆藏**：Victoria and Albert Museum，对象号 `O135197`

**对象页**：https://collections.vam.ac.uk/item/O135197/

**API 记录**：https://api.vam.ac.uk/v2/museumobject/O135197

## 可支撑事实（verified 来源；引用时保留对象号）

- 对象号 O135197；题名 Pair of shoes（loafers）；Great Britain, 1970s；材质 leather。
- 馆方 physicalDescription 原文："Black leather loafers, a bit worn. With tassel and fringes."
- 可支撑「乐福鞋（loafer）」作为 20 世纪便装鞋型，以及流苏/穗饰细节。

## 验证记录

- 命令 `curl -sS -m 20 -L -o /tmp/v.html -w '%{http_code}' "https://collections.vam.ac.uk/item/O135197/"` → HTTP **200**，页面标题「Pair of Shoes | V&A Explore The Collections」
- 命令 `curl -sS -m 20 -L -o /tmp/v.json -w '%{http_code}' "https://api.vam.ac.uk/v2/museumobject/O135197"` → HTTP **200**，`record.physicalDescription` 与上方引文一致
- 验证日期：2026-11-05（Asia/Shanghai）；图片未下载/未内嵌。

## 使用限制

- 1970s 实例；不要把 loafer 与 oxford 混为一类（oxford 见 SRC-0420）。
- 仅链接引用。
- 引用时保留 V&A 对象号与对象页链接；不得把馆方描述改写成更普遍的历史结论。

## 可配合的主题

- 乐福鞋/便装鞋、流苏饰

## 相关卡片

- [[GAR-0091-乐福鞋]]
