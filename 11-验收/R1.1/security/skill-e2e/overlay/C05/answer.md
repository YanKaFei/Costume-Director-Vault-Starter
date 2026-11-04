## 检索结果对比（`scripts/query.py … --json`，默认排除 example）

**1. 旗袍 / qipao — 召回完全相同（各 10 条，ID 集与排序一致）**
- 核心：GAR-0031（verified；SRC-0200、SRC-0201，均 V&A 旗袍实物）；来源卡 SRC-0200、SRC-0201
- 衍生：LOOK-0009、LOOK-0019、LOOK-0012、LOOK-0015（interpretive）、PRD-0011（verified）、STR-0011、STR-0016
- 首条得分均 8.6。卡内中英文名严格对译，双语命中等价。

**2. 立领 / stand collar — 各 10 条，交集 7 条，侧翼差异大**
- 共有：GAR-0031（SRC-0200/0201）、GAR-0032 长衫（SRC-0202）、LOOK-0008/0009/0012/0019、PRD-0011
- 仅「立领」：GAR-0002 达布里特（SRC-0103）、GAR-0007 衬衫式女衫（SRC-0108）、GAR-0041（interpretive，无 SRC）——中文正文含"立领"成词
- 仅「stand collar」：STR-0001 美第奇领（SRC-0101，得分 5.5）、GAR-0076 斗篷（SRC-0482/0483）、LOOK-0003——命中 standing/stand-up collar 及英文提示词短语

**3. 腰带 / belt — 各 10 条，交集 8 条，排序不同**
- 共有：GAR-0080（verified；SRC-0487、SRC-0488）、SRC-0050（CMA，1375–1400）、SRC-0427、SRC-0487、SRC-0488、GAR-0040（SRC-0404）、GAR-0042、GAR-0045（SRC-0405）
- 仅「腰带」：GAR-0066 和服腰带（SRC-0427，高分 8.4）、GAR-0001 和服（SRC-0100）
- 仅「belt」：GAR-0057 Courrèges（SRC-0417）、GAR-0075 束腰长袍（SRC-0480/0481），均靠英文段 "belt at waist"；GAR-0066 降为 4.2

## 召回差异原因
1. **双语共索引**：卡片中英文名同卡，主命中高度重叠；标题精确匹配约 8.4–8.6 分，正文提及仅 2–3 分。
2. **形态变化不对称**：英文需覆盖 stand/standing/stand-up、belt/belted/girdle，中文靠子串成词（立领、和服腰带），故侧翼卡不同。
3. **语种写作偏向**：西方服饰的英文提示词块只被英文词召回；中式单品中文叙述只被中文词召回。
4. **知识库结构缺口**：无独立"立领"STR 卡（最接近为 STR-0001），该词被迫散落在 garment/look 卡中。

（约 560 字）
