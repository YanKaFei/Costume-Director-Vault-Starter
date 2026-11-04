# P4-1 公版书籍索引（P4-BOOKS-INDEX）

- 生成：2026-11-04；worker：researcher（task-40）
- 许可门禁：`reports/P4-SOURCE-AUDIT.md`（P4-0）确认的 **Public Domain** 书籍；仅使用该审计列出的 5 本 GITenberg 镜像 + 4 本 Project Gutenberg 电子书。**未下载/未引用任何受版权保护的现代版本**。
- 解析工具：`scripts/books_extract.py`（Python 标准库，无第三方依赖）：`python3 scripts/books_extract.py --download` → `python3 scripts/books_extract.py`
- 说明：任务书写「8 本书」，审计实际列出 **5 GITenberg + 4 Gutenberg = 9 本**；本索引解析并登记全部 9 本（以审计清单为准）。

## 0. 总览

| # | PG# | 书名 | 作者/编者 | 年份 | 来源族 | 章节 | 正文行 | PD 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 34903 | Dress Design: An Account of Costume for Artists & Dressmakers | Talbot Hughes | 1919（PG 记录；正文题「Reprinted 1920」，丛书序 1913；首版年 UNCONFIRMED） | GITenberg | 8 | 19777 | Public domain in USA |
| 2 | 21534 | Textiles and Clothing | Kate Heintz Watson | 1907 | GITenberg | 39 | 8533 | Public domain in USA |
| 3 | 33020 | English Costume | Dion Clayton Calthrop | 1907 | GITenberg | 35 | 9746 | Public domain in USA |
| 4 | 48551 | Costume: Fanciful, Historical and Theatrical | Mrs. Aria（编）；Percy Anderson（绘） | 1906 | GITenberg | 20 | 6181 | Public domain in USA |
| 5 | 49559 | Modern Design in Jewellery and Fans | Charles Holme（编） | 1902 | GITenberg | 1 | 2915 | Public domain in USA |
| 6 | 76299 | A Dictionary of Men's Wear | William Henry Baker | 1908 | Gutenberg | 1 | 19779 | Public domain in USA |
| 7 | 56978 | The Book of the Feet: A History of Boots and Shoes | Joseph Sparkes Hall | 1847 | Gutenberg | 9 | 4672 | Public domain in USA |
| 8 | 76717 | The History of Fashion in France | Augustin Challamel（英译 Frances Cashel Hoey & John Lillie） | 1882 | Gutenberg | 34 | 11382 | Public domain in USA |
| 9 | 46949 | Chats on Costume | G. Woolliscroft Rhead | 1906 | Gutenberg | 10 | 6544 | Public domain in USA |

## 1. 逐书条目

### PG #34903 — Dress Design: An Account of Costume for Artists & Dressmakers

- 中文名：礼服设计：面向艺术家与裁缝的服饰史
- 作者/编者：Talbot Hughes；出版：Sir Isaac Pitman & Sons, Ltd.（伦敦；The Artistic Crafts Series of Technical Handbooks）；年份：1919（PG 记录；正文题「Reprinted 1920」，丛书序 1913；首版年 UNCONFIRMED）
- 文本：https://www.gutenberg.org/cache/epub/34903/pg34903.txt（HTTP 200，2026-11-04）
- 书目页：https://www.gutenberg.org/ebooks/34903（抽查 HTTP 200 + `Public domain in the USA`；2026-11-04 站点对部分请求间歇超时，不作唯一证据）
- GITenberg 镜像：https://github.com/GITenberg/Dress-designAn-Account-of-Costume-for-Artists--amp--Dressmakers_34903（审计 A12 条目；本网络下 4/5 个仓库页 HTTP 200，49559 页在 15s 超时但 PG 文本 200，未用仓库页作来源 URL）
- 来源卡：[[SRC-0061]]
- 目录/结构：按时代与「装饰/trimmings」分章：史前—10 世纪—15 世纪—16 世纪—17 世纪—18/19 世纪；第八章为 19 世纪与裁剪/装饰。
- 可支撑：16—19 世纪欧洲（以英国为主）服装装饰手法、裁片与结构描述；适合「装饰/裁剪/轮廓」术语线索。
- 质量与局限：作者为艺术教育者，表述带 1910 年代审美判断（如对 farthingale 的贬评），不可当作中立史实；无页码；图像未提取。

- 自动识别章节（前 18 个，完整见解析 JSON）：1. CHAPTER I；2. CHAPTER II；3. CHAPTER III；4. CHAPTER IV；5. CHAPTER V；6. CHAPTER VI；7. CHAPTER VII；8. CHAPTER VIII

### PG #21534 — Textiles and Clothing

- 中文名：纺织与服装
- 作者/编者：Kate Heintz Watson；出版：American School of Home Economics（芝加哥）；年份：1907
- 文本：https://www.gutenberg.org/cache/epub/21534/pg21534.txt（HTTP 200，2026-11-04）
- 书目页：https://www.gutenberg.org/ebooks/21534（抽查 HTTP 200 + `Public domain in the USA`；2026-11-04 站点对部分请求间歇超时，不作唯一证据）
- GITenberg 镜像：https://github.com/GITenberg/Textiles-and-Clothing_21534（审计 A12 条目；本网络下 4/5 个仓库页 HTTP 200，49559 页在 15s 超时但 PG 文本 200，未用仓库页作来源 URL）
- 来源卡：[[SRC-0062]]
- 目录/结构：纤维（棉/毛/亚麻/丝）—织造与组织—漂染印花—整理—织物名称—手缝/机缝—褶边/贴边/开襟—制版—七片裙/衬衫式女衫/领/袖—童装—保养。
- 可支撑：20 世纪初服装工艺教学：面料性能、缝制工序、七片裙与衬衫式女衫的结构要点；适合「构造/材料」卡。
- 质量与局限：1910 年代美国家政教育文本，工艺标准与当代不同；不含历史年代演变；页码未可靠保留。

- 自动识别章节（前 18 个，完整见解析 JSON）：1. Weaving；2. Fibers；3. Cotton；4. Wool；5. Flax；6. Silk；7. Modern Methods；8. Weaving；9. Weaves；10. Bleaching and Dyeing；11. Printing；12. Finishing；13. Cotton Goods；14. Linens；15. Woolens and Worsteds；16. Silks；17. Names of Fabrics；18. TEXTILES AND CLOTHING

### PG #33020 — English Costume

- 中文名：英国服装
- 作者/编者：Dion Clayton Calthrop；出版：Adam & Charles Black（伦敦）；年份：1907
- 文本：https://www.gutenberg.org/cache/epub/33020/pg33020.txt（HTTP 200，2026-11-04）
- 书目页：https://www.gutenberg.org/ebooks/33020（抽查 HTTP 200 + `Public domain in the USA`；2026-11-04 站点对部分请求间歇超时，不作唯一证据）
- GITenberg 镜像：https://github.com/GITenberg/English-Costume_33020（审计 A12 条目；本网络下 4/5 个仓库页 HTTP 200，49559 页在 15s 超时但 PG 文本 200，未用仓库页作来源 URL）
- 来源卡：[[SRC-0063]]
- 目录/结构：按英国君主在位期分章：William I 至 George IV（1066—1830），每章分「THE MEN / THE WOMEN」描述。
- 可支撑：英国 11—19 世纪初男/女装的时代描述与术语（tunic→doublet 演变、ruff、farthingale 等）；适合「时代地域/风格」线索。
- 质量与局限：通俗插画史（1907），年代与细节需与博物馆实物交叉；常以轶事与文学引文代替考据；无页码。

- 自动识别章节（前 18 个，完整见解析 JSON）：1. WILLIAM THE FIRST；2. WILLIAM THE SECOND；3. HENRY THE FIRST；4. STEPHEN；5. HENRY THE SECOND；6. RICHARD THE FIRST；7. JOHN；8. HENRY THE THIRD；9. EDWARD THE FIRST；10. EDWARD THE SECOND；11. EDWARD THE THIRD；12. RICHARD THE SECOND；13. THE END OF THE FOURTEENTH CENTURY；14. HENRY THE FOURTH；15. HENRY THE FIFTH；16. HENRY THE SIXTH；17. EDWARD THE FOURTH；18. EDWARD THE FIFTH

### PG #48551 — Costume: Fanciful, Historical and Theatrical

- 中文名：服装：奇幻、历史与戏剧
- 作者/编者：Mrs. Aria（编）；Percy Anderson（绘）；出版：Macmillan and Co., Limited（伦敦/纽约）；年份：1906
- 文本：https://www.gutenberg.org/cache/epub/48551/pg48551.txt（HTTP 200，2026-11-04）
- 书目页：https://www.gutenberg.org/ebooks/48551（抽查 HTTP 200 + `Public domain in the USA`；2026-11-04 站点对部分请求间歇超时，不作唯一证据）
- GITenberg 镜像：https://github.com/GITenberg/Costume-Fanciful-Historical-and-Theatrical_48551（审计 A12 条目；本网络下 4/5 个仓库页 HTTP 200，49559 页在 15s 超时但 PG 文本 200，未用仓库页作来源 URL）
- 来源卡：[[SRC-0064]]
- 目录/结构：按世纪分章（古典—19 世纪）+ 英国/外国农民 + 东方服饰 + Fancy Dress（第 15 章）+ Dominoes and Masks（第 16 章）+ Materials, the Corset, and the Crinoline（第 17 章）。
- 可支撑：戏剧/化装舞会服装与历史服装的区别、domino/面具、紧身衣与裙撑材料；适合「戏剧服装 vs 历史服装」「风格」卡。
- 质量与局限：1906 年舞台/化装视角，历史段落为通俗综述；「fancy dress」定义非学术定义；无页码。

- 自动识别章节（前 18 个，完整见解析 JSON）：1. CHAPTER I；2. CHAPTER II；3. CHAPTER III；4. CHAPTER IV；5. CHAPTER V；6. CHAPTER VI；7. CHAPTER VII；8. CHAPTER VIII；9. CHAPTER IX；10. CHAPTER X；11. CHAPTER XI；12. CHAPTER XII；13. CHAPTER XIII；14. CHAPTER XIV；15. CHAPTER XV；16. CHAPTER XVI；17. CHAPTER XVII；18. CHAPTER XVIII

### PG #49559 — Modern Design in Jewellery and Fans

- 中文名：现代珠宝与扇子设计
- 作者/编者：Charles Holme（编）；出版：Offices of "The Studio"（伦敦/巴黎/纽约）；年份：1902
- 文本：https://www.gutenberg.org/cache/epub/49559/pg49559.txt（HTTP 200，2026-11-04）
- 书目页：https://www.gutenberg.org/ebooks/49559（抽查 HTTP 200 + `Public domain in the USA`；2026-11-04 站点对部分请求间歇超时，不作唯一证据）
- GITenberg 镜像：https://github.com/GITenberg/Modern-Design-in-Jewellery-and-Fans_49559（审计 A12 条目；本网络下 4/5 个仓库页 HTTP 200，49559 页在 15s 超时但 PG 文本 200，未用仓库页作来源 URL）
- 来源卡：[[SRC-0065]]
- 目录/结构：导论 + 各国珠宝/扇子设计评述（法国、英国、奥地利、德国、比利时、丹麦）+ 工匠与设计师名录 + 图版说明。
- 可支撑：1900 前后珠宝/扇子的材料与工艺（金、珐琅、象牙、珍珠、宝石）与设计潮流；适合「配饰/材质」线索。
- 质量与局限：设计评论文集，非技术手册；图版本身未提取（仅文本）；无页码（图版编号有，但未核验）。

- 自动识别章节（前 18 个，完整见解析 JSON）：1. (whole text)

### PG #76299 — A Dictionary of Men's Wear

- 中文名：男士服饰词典
- 作者/编者：William Henry Baker；出版：William Henry Baker（克利夫兰）；年份：1908
- 文本：https://www.gutenberg.org/cache/epub/76299/pg76299.txt（HTTP 200，2026-11-04）
- 书目页：https://www.gutenberg.org/ebooks/76299（抽查 HTTP 200 + `Public domain in the USA`；2026-11-04 站点对部分请求间歇超时，不作唯一证据）
- 来源卡：[[SRC-0066]]
- 目录/结构：按字母排序的男装/面料/裁缝行话词典（约 5,391 个词条头），附美国独立民兵制服、礼服规则等附录。
- 可支撑：1908 年美国男装贸易术语与结构定义（blazer、sack coat、frock coat、waistcoat、trousers、tweed、denim…）；适合「单品/结构/材料术语」卡。
- 质量与局限：贸易词典，定义有时代/地域性（美国 1908），部分词义已变化（如 gabardine）；只覆盖男装；无页码，用词条定位。

- 自动识别章节（前 18 个，完整见解析 JSON）：1. (whole text)

### PG #56978 — The Book of the Feet: A History of Boots and Shoes

- 中文名：足部之书：靴鞋史
- 作者/编者：Joseph Sparkes Hall；出版：J. S. Redfield（纽约；据第二版伦敦版增补美国部分）；年份：1847
- 文本：https://www.gutenberg.org/cache/epub/56978/pg56978.txt（HTTP 200，2026-11-04）
- 书目页：https://www.gutenberg.org/ebooks/56978（抽查 HTTP 200 + `Public domain in the USA`；2026-11-04 站点对部分请求间歇超时，不作唯一证据）
- 来源卡：[[SRC-0067]]
- 目录/结构：古代鞋履—英国靴鞋史—外国靴鞋—行业起源—足部结构与鞋楦—鞋之诗—美国靴鞋史—制鞋名人传记—杂录。
- 可支撑：19 世纪中叶以前的靴鞋形制与史料汇编（含古代/中世纪引文）；适合「鞋履/时代」线索。
- 质量与局限：1847 年行业史，考古与史料引用需现代研究复核；带宣传/轶事成分；无页码。

- 自动识别章节（前 18 个，完整见解析 JSON）：1. CHAPTER I.；2. CHAPTER II.；3. CHAPTER III.；4. CHAPTER IV.；5. CHAPTER V.；6. CHAPTER VI.；7. CHAPTER VII.；8. CHAPTER VIII.；9. CHAPTER IX.

### PG #76717 — The History of Fashion in France

- 中文名：法国时装史
- 作者/编者：Augustin Challamel（英译 Frances Cashel Hoey & John Lillie）；出版：Sampson Low, Marston, Searle & Rivington（伦敦）；年份：1882
- 文本：https://www.gutenberg.org/cache/epub/76717/pg76717.txt（HTTP 200，2026-11-04）
- 书目页：https://www.gutenberg.org/ebooks/76717（抽查 HTTP 200 + `Public domain in the USA`；2026-11-04 站点对部分请求间歇超时，不作唯一证据）
- 来源卡：[[SRC-0068]]
- 目录/结构：导论 + 34 章：高卢/高卢-罗马—墨洛温—加洛林—中世纪—文艺复兴—17/18 世纪—大革命—19 世纪（至 1880 年代）。
- 可支撑：法国服饰通史（1882 年视角），适合「历史演变/时代」线索与 19 世纪史学样本。
- 质量与局限：1882 年旧史学，民族/进步叙事与部分年代判断已被现代研究修正；必须交叉验证；无页码。

- 自动识别章节（前 18 个，完整见解析 JSON）：1. CHAPTER I.；2. CHAPTER II.；3. CHAPTER III.；4. CHAPTER IV.；5. CHAPTER V.；6. CHAPTER VI.；7. CHAPTER VII.；8. CHAPTER VIII.；9. CHAPTER IX.；10. CHAPTER X.；11. CHAPTER XI.；12. CHAPTER XII.；13. CHAPTER XIII.；14. CHAPTER XIV.；15. CHAPTER XV.；16. CHAPTER XVI.；17. CHAPTER XVII.；18. CHAPTER XVIII.

### PG #46949 — Chats on Costume

- 中文名：服装漫谈
- 作者/编者：G. Woolliscroft Rhead；出版：T. Fisher Unwin（伦敦）；年份：1906
- 文本：https://www.gutenberg.org/cache/epub/46949/pg46949.txt（HTTP 200，2026-11-04）
- 书目页：https://www.gutenberg.org/ebooks/46949（抽查 HTTP 200 + `Public domain in the USA`；2026-11-04 站点对部分请求间歇超时，不作唯一证据）
- 来源卡：[[SRC-0069]]
- 目录/结构：十章：总览 / Tunic / Mantle / Doublet and Hose / Kirtle or Petticoat / Crinoline / Collars and Cuffs / Hats, Caps and Bonnets / 发须 / Boots and Shoes。
- 可支撑：按服装部件分章的通史：tunic、mantle、doublet & hose、kirtle、crinoline、collar/cuff、帽、鞋；适合「单品/结构/年代」线索。
- 质量与局限：通俗随笔，文学引文多、可核证细节少于学术著作；观点性语句需剔除；无页码。

- 自动识别章节（前 18 个，完整见解析 JSON）：1. I A GENERAL SURVEY；2. II THE TUNIC；3. III THE MANTLE；4. IV THE DOUBLET AND HOSE；5. V THE KIRTLE OR PETTICOAT；6. VI THE RISE AND FALL OF THE CRINOLINE；7. VII COLLARS AND CUFFS；8. VIII HATS, CAPS, AND BONNETS；9. IX THE DRESSING OF THE HAIR, MOUSTACHIOS, AND BE；10. X BOOTS, SHOES, AND OTHER COVERINGS FOR THE FEET

## 2. 质量分级与使用规则

| 级别 | 判据 | 用法 |
| --- | --- | --- |
| book_fact | 书内可定位原文 | 只能标「书中记载」；不得直接标 verified |
| 交叉验证 | book_fact + Met/FIT/V&A/AAT 独立佐证同一断言 | 可标 verified，并同时列 book + SRC 双方 |
| 现代纠正 | 现代研究/词义与本书记载不同 | 写明差异与年代，不覆盖书内原文 |
| candidate / interpretive | 无独立佐证或属作者判断 | 只作线索或设计建议，不得 verified |

## 3. 复现

```bash
python3 scripts/books_extract.py --download   # 仅下载审计确认的 9 本 PD 文本到 /tmp/p4books
python3 scripts/books_extract.py              # 解析并写 11-验收/P4-BOOKS/extracted/
python3 scripts/books_extract.py --search "farthingale"   # 带定位的全文检索
python3 scripts/books_extract.py --locate 46949:5155      # 行号 -> 章/段定位
```

网络限制（2026-11-04 实测）：GitHub/GITenberg 仓库页 4/5 HTTP 200，`Modern-Design-in-Jewellery-and-Fans_49559` 仓库页 15s 超时；Project Gutenberg 文本与书目页 9/9 HTTP 200。
