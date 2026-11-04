---
id: SRC-0063
type: source
name_zh: "英国服装"
name_en: "English Costume"
title: "English Costume"
publisher: "Adam & Charles Black（伦敦）"
url: "https://www.gutenberg.org/cache/epub/33020/pg33020.txt"
date_accessed: "2026-11-04"
source_kind: reference_work
rights_statement: "Public domain in the USA（Project Gutenberg 电子书页明示）；Project Gutenberg License 适用于再分发其制备文本；插图/图版不在本卡范围，未提取"
license_status: not_applicable
evidence_status: verified
review_status: reviewed
note: "PG #33020《English Costume》1907；GITenberg 审计确认 PD；可支撑：英国 11—19 世纪初男/女装的时代描述与术语（tunic→doublet 演变、ruff、farthingale 等）；适合「时代地域/…"
tags: [source, book, public_domain, gutenberg, gitenberg, fashion_history]
---

# 英国服装（PG #33020，1907）

**作者/编者**：Dion Clayton Calthrop

**出版**：Adam & Charles Black（伦敦）

**电子文本**：https://www.gutenberg.org/cache/epub/33020/pg33020.txt

**书目页**：https://www.gutenberg.org/ebooks/33020

**GITenberg 镜像（审计条目）**：https://github.com/GITenberg/English-Costume_33020

## 可支撑事实（verified 来源，内容引用需按章节定位）

- 英国 11—19 世纪初男/女装的时代描述与术语（tunic→doublet 演变、ruff、farthingale 等）；适合「时代地域/风格」线索。
- 结构：按英国君主在位期分章：William I 至 George IV（1066—1830），每章分「THE MEN / THE WOMEN」描述。
- 解析统计：正文 9746 行；自动识别 35 个章节/段；术语命中见 `11-验收/P4-BOOKS/extracted/`。

## 验证记录

- 验证命令：`curl -sS -m 20 -L -o /tmp/pg33020.txt -w '%{http_code}' "https://www.gutenberg.org/cache/epub/33020/pg33020.txt"`
- 实际返回：HTTP **200**，文本 504,937 bytes；下载文本内命中 PG 公有领域声明 2 次（`This eBook is for the use of anyone anywhere in the United States`）。
- 书目页 `https://www.gutenberg.org/ebooks/33020`：网络允许时抽查 HTTP **200** 且含 `Public domain in the USA`；2026-11-04 该站点对部分请求间歇超时，故书目页仅作辅助，**证据以文本 URL + 审计报告为准**。
- 审计依据：`reports/P4-SOURCE-AUDIT.md` A12 —— GITenberg 镜像 README 明示 Public Domain + PG License（2026-11-04 审计）。
- 验证日期：2026-11-04（Asia/Shanghai）

## 使用限制

- 通俗插画史（1907），年代与细节需与博物馆实物交叉；常以轶事与文学引文代替考据；无页码。
- 本书为历史二手/综述文本，**不是现代学术考据**；引用结论须标为 book_fact，重要年代判断须另用 Met/FIT/V&A 交叉验证，否则 candidate/interpretive。
- 纯文本无可靠页码；引用定位用「章 + 段 + 行号」，页码一律 `UNCONFIRMED`。
- 再分发 PG 制备文本须遵守 Project Gutenberg License；不得使用 PG 商标暗示背书；插图/图版不在本库范围。

## 可配合的主题

- 详见 `06-时代地域/书籍研究/` 与 `11-验收/P4-BOOKS/`。
