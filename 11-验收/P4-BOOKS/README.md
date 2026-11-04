# 11-验收/P4-BOOKS — 验收说明（P4-1）

- 日期：2026-11-04；worker：researcher（task-40）
- 输入：`reports/P4-SOURCE-AUDIT.md` 确认的 9 本 PD 书；工具：`scripts/books_extract.py`（stdlib）。
- **来源卡编号说明**：SRC-0520..0524 已被并行 worker 的 FreeSewing/V&A 卡占用，为避免重复 ID，本任务的 9 张书籍卡使用 researcher 预留段 **SRC-0061..0069**（无冲突、无重复）。
- 书目索引：`reports/P4-BOOKS-INDEX.md`；研究笔记：`06-时代地域/书籍研究/书籍研究-历史服饰术语与结构.md`；来源卡：`04-来源/SRC-0061…0069`。

## 文件清单

| 文件 | 内容 |
| --- | --- |
| `extracted/books_extract.json` | 9 本书元数据/章节/统计（无 hits，供索引与机器读取） |
| `extracted/<PG>.json` | 单书：metadata、TOC、章节、术语 hits（含章/段/行定位）、词典型书籍的词条表 |
| `extracted/TERMS-HITS.md` | 每本书的章节与命中统计摘要 |
| `TERMS-GLOSSARY.md` | 31 条术语/结构结论总表（书内定义 + 定位 + 独立佐证 + 状态） |
| `README.md` | 本验收说明 |

## 结果

| 指标 | 结果 |
| --- | --- |
| 解析书籍 | 9/9（审计清单 5 GITenberg + 4 Gutenberg；均为 PD in USA） |
| 文本 HTTP 200 | 9/9（Project Gutenberg cache/epub；2026-11-04） |
| 文本内含 PG 公有领域声明 | 9/9（`This eBook is for the use of anyone anywhere in the United States`） |
| 书目页抽查 200 + `Public domain in the USA` | 6/9（48551/56978/76299 等 3 个因 Gutenberg 站点间歇超时未取到，书目页不作唯一证据） |
| 自动识别章/节 | 8/9 书按章识别（49559 为文集，单段）；总章/节 157 |
| 词典词条 | PG 76299：5,391 个男装词条头 |
| 术语 hits（记录上限 2,000/书） | 9 书合计 12,640；各书去重术语 23–82 个 |
| 研究结论 | 31 条（≥20 要求） |
| verified（独立交叉验证） | 15/31 = 48% |
| 含部分/类别级佐证 | 26/31 = 84% |
| candidate（未交叉验证） | 5 条 |

## 复现命令与退出码

```bash
python3 scripts/books_extract.py --download; echo $?   # 0
python3 scripts/books_extract.py --json; echo $?      # 0（打印 9 书统计）
python3 scripts/books_extract.py --search "farthingale"; echo $?  # 0
```

## 局限

- 纯文本无页码；所有页码标 UNCONFIRMED，只有章/段/行。
- 书为 1847—1919 年旧著，年代与文化判断需现代研究校正；已逐条标注现代纠正。
- 49559 为图录式文集，无章节切分，术语 hits 少；其图版未提取（只读文本）。
- 未使用任何受版权保护的现代注疏/译本；未下载或嵌入图像。
- 交叉验证依赖现有 197 张 SRC 卡（AAT/Met/FIT/V&A）；未新增外部博物馆请求（除既有卡片）。
