---
id: SRC-0069
type: source
name_zh: "服装漫谈"
name_en: "Chats on Costume"
title: "Chats on Costume"
publisher: "T. Fisher Unwin（伦敦）"
url: "https://www.gutenberg.org/cache/epub/46949/pg46949.txt"
date_accessed: "2026-11-04"
source_kind: reference_work
rights_statement: "Public domain in the USA（Project Gutenberg 电子书页明示）；Project Gutenberg License 适用于再分发其制备文本；插图/图版不在本卡范围，未提取"
license_status: not_applicable
evidence_status: verified
review_status: reviewed
note: "PG #46949《Chats on Costume》1906；Gutenberg 审计确认 PD；可支撑：按服装部件分章的通史：tunic、mantle、doublet & hose、kirtle、crinoline、collar/cuff、帽、…"
tags: [source, book, public_domain, gutenberg, gutenberg_pg, fashion_history]
---

# 服装漫谈（PG #46949，1906）

**作者/编者**：G. Woolliscroft Rhead

**出版**：T. Fisher Unwin（伦敦）

**电子文本**：https://www.gutenberg.org/cache/epub/46949/pg46949.txt

**书目页**：https://www.gutenberg.org/ebooks/46949

## 可支撑事实（verified 来源，内容引用需按章节定位）

- 按服装部件分章的通史：tunic、mantle、doublet & hose、kirtle、crinoline、collar/cuff、帽、鞋；适合「单品/结构/年代」线索。
- 结构：十章：总览 / Tunic / Mantle / Doublet and Hose / Kirtle or Petticoat / Crinoline / Collars and Cuffs / Hats, Caps and Bonnets / 发须 / Boots and Shoes。
- 解析统计：正文 6544 行；自动识别 10 个章节/段；术语命中见 `11-验收/P4-BOOKS/extracted/`。

## 验证记录

- 验证命令：`curl -sS -m 20 -L -o /tmp/pg46949.txt -w '%{http_code}' "https://www.gutenberg.org/cache/epub/46949/pg46949.txt"`
- 实际返回：HTTP **200**，文本 327,366 bytes；下载文本内命中 PG 公有领域声明 2 次（`This eBook is for the use of anyone anywhere in the United States`）。
- 书目页 `https://www.gutenberg.org/ebooks/46949`：网络允许时抽查 HTTP **200** 且含 `Public domain in the USA`；2026-11-04 该站点对部分请求间歇超时，故书目页仅作辅助，**证据以文本 URL + 审计报告为准**。
- 审计依据：`reports/P4-SOURCE-AUDIT.md` B —— PG 页头 Public domain in the USA + PG License（2026-11-04 审计）。
- 验证日期：2026-11-04（Asia/Shanghai）

## 使用限制

- 通俗随笔，文学引文多、可核证细节少于学术著作；观点性语句需剔除；无页码。
- 本书为历史二手/综述文本，**不是现代学术考据**；引用结论须标为 book_fact，重要年代判断须另用 Met/FIT/V&A 交叉验证，否则 candidate/interpretive。
- 纯文本无可靠页码；引用定位用「章 + 段 + 行号」，页码一律 `UNCONFIRMED`。
- 再分发 PG 制备文本须遵守 Project Gutenberg License；不得使用 PG 商标暗示背书；插图/图版不在本库范围。

## 可配合的主题

- 详见 `06-时代地域/书籍研究/` 与 `11-验收/P4-BOOKS/`。
