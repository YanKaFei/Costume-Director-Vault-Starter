# DRAFT-SIGNOFF-R1.1 — 62 张 draft 卡人工签核表（KQ-13）

- 生成：2026-11-05（Asia/Shanghai）；worker：researcher（task-56，R1.1-G）
- 依据：`reports/DRAFT-REVIEW.csv`（P3.5/P4 复核记录）+ 当前卡片 frontmatter（`review_status`/`evidence_status`/`source_ids`）。
- 当前状态：**62 张全部仍为 `review_status: draft`；0 张 reviewed**。本表**不修改任何卡片**，也不自动提升 evidence_status；只提供逐卡建议与签字栏。
- 数量：`REVIEWED-CANDIDATE` **45** + `STAY_DRAFT` **17**；签核要求：38 张「人工签核」、20 张「人工重配来源/重写断言后复评」、4 张「确认 example 身份」。
- 空白导演评分表（与 AUD-005 对应）：[`11-验收/P3.6/导演评分表.md`](../11-验收/P3.6/导演评分表.md)（NOT_SCORED，AI 不得代填）。

## 签核规则（人工执行，不可由脚本代签）

1. **REVIEWED-CANDIDATE**：人工确认来源与断言一致、无过度解读后，把 `review_status` 改为 `reviewed`；`evidence_status` 保持不变（不得自动提升）。
2. **需重配来源/重写断言**（20 张）：按“证据不足”清单先补来源或把断言降级为 interpretive，再复评。
3. **STAY_DRAFT**：保持 draft，说明原因（example 身份/缺来源/待设计决策）。
4. 签字后同步更新本表「结论/日期/签字人」，并在 `reports/DRAFT-REVIEW.csv` 追加复核记录；不得批量改卡。

## 汇总

| 指标 | 数量 |
| --- | --- |
| draft 卡总数 | 62 |
| REVIEWED-CANDIDATE（可人工签核） | 45 |
| STAY_DRAFT（保持 draft） | 17 |
| 当前 reviewed | 0 |
| 当前 still draft | 62 |
| 无记录（DRAFT-REVIEW 缺失） | 0 |
| 状态漂移（CSV 与卡不一致） | 0 |

## 逐卡清单与签字栏

| # | 卡 ID | 类型 | 名称 | evidence | review | 复核结论 | 建议动作 | 人工结论（DRAFT/REVIEWED/停留原因） | 签字人 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | GAR-EXAMPLE-001 | garment | 白色立领衬衫 | example | draft | STAY_DRAFT | 保持 draft；example 卡无需来源，但不得改为 verified；人工确认示例身份后方可 reviewed（evidence_s |  |  |  |
| 2 | LOOK-0001 | look | 洛可可沙龙女主人 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 3 | LOOK-0002 | look | 摄政时期乡间日装 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 4 | LOOK-0003 | look | 十六世纪欧洲宫廷男装 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 5 | LOOK-0004 | look | 奥斯曼晚期官员 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 6 | LOOK-0005 | look | 1900 南方庄园女主人 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 7 | LOOK-0006 | look | 1977 伦敦朋克青年 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 8 | LOOK-0007 | look | 当代雨夜调查者连续性造型 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 9 | LOOK-0008 | look | 1930 年代上海长衫知识分子 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 10 | LOOK-0009 | look | 1930 年代上海旗袍女性知识分子 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 11 | LOOK-0010 | look | 急诊科护士夜班职业装 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 12 | LOOK-0011 | look | 废弃空间站维修工 | interpretive | draft | REVIEWED-CANDIDATE | 先重配来源/重写断言，再复评 |  |  |  |
| 13 | LOOK-0012 | look | 1930 年代上海雨夜女记者 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 14 | LOOK-0013 | look | 加纳-英国婚礼新娘仪式造型 | interpretive | draft | REVIEWED-CANDIDATE | 先重配来源/重写断言，再复评 |  |  |  |
| 15 | LOOK-0014 | look | 1940 年代战后通勤女装 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 16 | LOOK-0015 | look | 上海银行家之妻：从晚宴到难民（身份下滑） | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 17 | LOOK-0016 | look | 1940 年代复员军人：从军装到平民通勤（身份上升） | interpretive | draft | REVIEWED-CANDIDATE | 先重配来源/重写断言，再复评 |  |  |  |
| 18 | LOOK-0017 | look | 1977 朋克青年到 1980 年代职业人（身份上升） | interpretive | draft | REVIEWED-CANDIDATE | 先重配来源/重写断言，再复评 |  |  |  |
| 19 | LOOK-0018 | look | 西非阿散蒂家庭节庆（kente 与 adinkra 的场合边界） | interpretive | draft | REVIEWED-CANDIDATE | 先重配来源/重写断言，再复评 |  |  |  |
| 20 | LOOK-0019 | look | 伦敦美术馆晚宴上的中国云肩与旗袍（东亚跨文化） | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 21 | LOOK-0020 | look | 伦敦南亚家庭庆典上的纱丽（南亚跨文化） | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 22 | LOOK-0021 | look | 当代雨夜调查者·四场连续性升级 | interpretive | draft | REVIEWED-CANDIDATE | 先重配来源/重写断言，再复评 |  |  |  |
| 23 | LOOK-0022 | look | 1940 年代战后通勤·三场连续性 | interpretive | draft | REVIEWED-CANDIDATE | 先重配来源/重写断言，再复评 |  |  |  |
| 24 | LOOK-EXAMPLE-001 | look | 雨夜调查者 | example | draft | STAY_DRAFT | 保持 draft；example 卡无需来源，但不得改为 verified；人工确认示例身份后方可 reviewed（evidence_s |  |  |  |
| 25 | PRD-0001 | period_region | 1770 年代英法服饰语境 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 26 | PRD-0002 | period_region | 1790 至 1810 英法新古典时代 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 27 | PRD-0003 | period_region | 1890 年代英美服饰语境 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 28 | PRD-0004 | period_region | 1920 年代美国与西欧 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 29 | PRD-0005 | period_region | 1930 年代美国好莱坞语境 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 30 | PRD-0006 | period_region | 1940 年代英美战时语境 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 31 | PRD-0007 | period_region | 1950 年代美英战后语境 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 32 | PRD-0008 | period_region | 1960 年代伦敦与美国 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 33 | PRD-0009 | period_region | 奥斯曼帝国晚期 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 34 | PRD-0010 | period_region | 拜占庭帝国晚期 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 35 | PRD-0011 | period_region | 1930 年代上海民国语境 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 36 | SCN-0001 | scene | 雨夜追查 | example | draft | STAY_DRAFT | 保持 draft；example 卡无需来源，但不得改为 verified；人工确认示例身份后方可 reviewed（evidence_s |  |  |  |
| 37 | SCN-0002 | scene | 1900 庄园早餐 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 38 | SCN-0003 | scene | 1977 银禧河船 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 39 | SCN-0004 | scene | 1930 年代上海知识分子对话 | interpretive | draft | STAY_DRAFT | 保持 draft；1930s 上海知识分子对话为虚构场景；来源仅支撑旗袍/长衫服饰语境，场景/人物不可由来源核实 |  |  |  |
| 40 | SCN-0005 | scene | 急诊夜班抢救 | interpretive | draft | STAY_DRAFT | 保持 draft；急诊夜班场景为虚构/设计推测；来源仅支撑护士制服类型 |  |  |  |
| 41 | SCN-0006 | scene | 废弃空间站维修 | interpretive | draft | STAY_DRAFT | 保持 draft；废弃空间站维修为虚构场景；来源（连体工作服/玩具头盔）证据间接 |  |  |  |
| 42 | SCN-0007 | scene | 上海雨夜后巷 | interpretive | draft | STAY_DRAFT | 保持 draft；上海雨夜后巷为虚构场景；来源仅支撑旗袍/盘扣服饰 |  |  |  |
| 43 | SCN-0008 | scene | 加纳英国婚礼 | interpretive | draft | STAY_DRAFT | 保持 draft；P3.5 narrator 已修 source 集（SRC-0106/0431/0144/0145，与加纳服饰对应）；但 |  |  |  |
| 44 | SCN-0009 | scene | 1940年代战后通勤 | interpretive | draft | STAY_DRAFT | 保持 draft；1940s 战后通勤为设计推测；来源支撑单品但不支撑场景 |  |  |  |
| 45 | SCN-0010 | scene | 伦敦美术馆晚宴 | interpretive | draft | STAY_DRAFT | 保持 draft；伦敦美术馆晚宴为虚构场景；来源支撑旗袍/云肩服饰 |  |  |  |
| 46 | SCN-0011 | scene | 伦敦南亚家庭庆典 | interpretive | draft | STAY_DRAFT | 保持 draft；伦敦南亚家庭庆典为虚构场景；来源支撑纱丽/细布（1902 婚礼纱），场景不可核实 |  |  |  |
| 47 | SCN-0012 | scene | 阿克拉家庭庆典 | interpretive | draft | STAY_DRAFT | 保持 draft；P3.5 narrator 已修 source 集（SRC-0106/0431/0144/0145，与加纳服饰对应）；但 |  |  |  |
| 48 | SCN-0013 | scene | 上海银行家晚宴 | interpretive | draft | STAY_DRAFT | 保持 draft；上海银行家晚宴为虚构场景；来源仅支撑旗袍服饰 |  |  |  |
| 49 | SCN-0014 | scene | 上海难民收容所 | interpretive | draft | STAY_DRAFT | 保持 draft；上海难民收容所为虚构/推测场景；SRC-0412 Utility 裙为间接参考，无难民服装来源 |  |  |  |
| 50 | SCN-0015 | scene | 1940年代复员站台 | interpretive | draft | STAY_DRAFT | 保持 draft；1940s 复员站台为设计推测；来源支撑单品但不支撑场景 |  |  |  |
| 51 | SCN-0016 | scene | 1980年代设计工作室 | interpretive | draft | STAY_DRAFT | 保持 draft；1980s 设计工作室场景，SRC-0155 为 1930s 概览，年代/场景关联弱 |  |  |  |
| 52 | STY-0001 | style | 新古典主义着装风格 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 53 | STY-0002 | style | 维多利亚丧服风格 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 54 | STY-0003 | style | 爵士时代摩登风格 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 55 | STY-0004 | style | 好莱坞魅惑造型 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 56 | STY-0005 | style | 黑色电影造型 | interpretive | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 57 | STY-0006 | style | 军装制服风 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 58 | STY-0007 | style | 朋克亚文化风格 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 59 | STY-0008 | style | 九十年代极简主义 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 60 | STY-0009 | style | 复古未来主义科幻街头 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 61 | STY-0010 | style | 时代剧历史考据造型 | verified | draft | REVIEWED-CANDIDATE | 人工签核后可置 reviewed（evidence 不变） |  |  |  |
| 62 | STY-EXAMPLE-001 | style | 克制的都市黑色电影造型 | example | draft | STAY_DRAFT | 保持 draft；example 卡无需来源，但不得改为 verified；人工确认示例身份后方可 reviewed（evidence_s |  |  |  |

## 备注

- 45 张 REVIEWED-CANDIDATE 的「建议动作」不构成 reviewer 结论；签核必须由人类完成（H4）。
- 20 张需重配来源/重写断言：优先处理涉及误标来源（如跨地域借用、年代近似）与 example 混用的卡。
- 本表与 `reports/DRAFT-REVIEW.csv` 逐行对应；若卡片状态变化，请同步两处，避免漂移。
