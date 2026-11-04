---
id: SRC-0068
type: source
name_zh: "法国时装史"
name_en: "The History of Fashion in France"
title: "The History of Fashion in France"
publisher: "Sampson Low, Marston, Searle & Rivington（伦敦）"
url: "https://www.gutenberg.org/cache/epub/76717/pg76717.txt"
date_accessed: "2026-11-04"
source_kind: reference_work
rights_statement: "Public domain in the USA（Project Gutenberg 电子书页明示）；Project Gutenberg License 适用于再分发其制备文本；插图/图版不在本卡范围，未提取"
license_status: not_applicable
evidence_status: verified
review_status: reviewed
note: "PG #76717《The History of Fashion in France》1882；Gutenberg 审计确认 PD；可支撑：法国服饰通史（1882 年视角），适合「历史演变/时代」线索与 19 世纪史学样本。…"
tags: [source, book, public_domain, gutenberg, gutenberg_pg, fashion_history]
---

# 法国时装史（PG #76717，1882）

**作者/编者**：Augustin Challamel（英译 Frances Cashel Hoey & John Lillie）

**出版**：Sampson Low, Marston, Searle & Rivington（伦敦）

**电子文本**：https://www.gutenberg.org/cache/epub/76717/pg76717.txt

**书目页**：https://www.gutenberg.org/ebooks/76717

## 可支撑事实（verified 来源，内容引用需按章节定位）

- 法国服饰通史（1882 年视角），适合「历史演变/时代」线索与 19 世纪史学样本。
- 结构：导论 + 34 章：高卢/高卢-罗马—墨洛温—加洛林—中世纪—文艺复兴—17/18 世纪—大革命—19 世纪（至 1880 年代）。
- 解析统计：正文 11382 行；自动识别 34 个章节/段；术语命中见 `11-验收/P4-BOOKS/extracted/`。

## 验证记录

- 验证命令：`curl -sS -m 20 -L -o /tmp/pg76717.txt -w '%{http_code}' "https://www.gutenberg.org/cache/epub/76717/pg76717.txt"`
- 实际返回：HTTP **200**，文本 608,063 bytes；下载文本内命中 PG 公有领域声明 2 次（`This eBook is for the use of anyone anywhere in the United States`）。
- 书目页 `https://www.gutenberg.org/ebooks/76717`：网络允许时抽查 HTTP **200** 且含 `Public domain in the USA`；2026-11-04 该站点对部分请求间歇超时，故书目页仅作辅助，**证据以文本 URL + 审计报告为准**。
- 审计依据：`reports/P4-SOURCE-AUDIT.md` B —— PG 页头 Public domain in the USA + PG License（2026-11-04 审计）。
- 验证日期：2026-11-04（Asia/Shanghai）

## 使用限制

- 1882 年旧史学，民族/进步叙事与部分年代判断已被现代研究修正；必须交叉验证；无页码。
- 本书为历史二手/综述文本，**不是现代学术考据**；引用结论须标为 book_fact，重要年代判断须另用 Met/FIT/V&A 交叉验证，否则 candidate/interpretive。
- 纯文本无可靠页码；引用定位用「章 + 段 + 行号」，页码一律 `UNCONFIRMED`。
- 再分发 PG 制备文本须遵守 Project Gutenberg License；不得使用 PG 商标暗示背书；插图/图版不在本库范围。

## 可配合的主题

- 详见 `06-时代地域/书籍研究/` 与 `11-验收/P4-BOOKS/`。
