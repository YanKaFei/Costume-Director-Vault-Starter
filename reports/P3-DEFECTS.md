# P3 缺陷登记（DEFECTS）— P3.1 复验后

- 更新时间：2026-11-04 02:47（Asia/Shanghai）；P3.1 复验（task-17）
- 快照：328 卡（内容 154 + 来源 174）；git HEAD `0345f05` + P3.1 工作区修改（未提交）
- 状态：**D2/D4 已关闭；但 query relevance 未达发布门槛 → 最终 FAIL 1 / WARN 5**；FIXED 8 项；RESOLVED-BY-QA 2 项
- 验证依据：`reports/P3-QA.md`（P3.1 复验章节）、`11-验收/测试结果/SUMMARY.md`（41 例）、`11-验收/测试结果/T31–T41.md`

## 1. P3 阻断缺陷（本轮验证）

| ID | 严重度 | 缺陷 | P3 状态 | **P3.1 状态** | 证据 |
|---|---|---|---|---|---|
| D2 | S2 | 职业服万能填充：护士/舞者/建筑师/教师等 A 套用警察制服+医生白袍+医疗鞋；warning 自称无职业卡 | OPEN | **FIXED（主项）** | T26/T31 急诊护士 A=护士制服 GAR-0036+白袍 GAR-0041+医疗鞋+徽章+手袋；T32 医生含白袍 GAR-0041；T33 警察=GAR-0042；T34 厨师=GAR-0043；T35 太空=连体工作服 GAR-0038+头盔 GAR-0039；T36 婚礼=布布长袍+gele；warnings 改为「无 X 专属卡，通用件替代且未用他职业制服」 |
| D4 | S1 | 虚假 warning「rainwear cards are missing」（风衣/雨衣卡存在） | OPEN | **FIXED** | T01/T02 使用 GAR-0045 风衣；T37 `rainwear_selected=PASS`、`warning_absent:rainwear_gap=PASS`；T38 室内同理 |
| D1 | S3 | SOURCES.csv 未随来源卡同步 | RESOLVED-BY-QA（P3） | **复发一次→已再次 RESOLVED-BY-QA** | P3.1 修 SRC-0046/47 后 CSV 2 行字段漂移（build --check FAIL）→ QA `--write` 重建后 PASS；须纳入发布步骤（见 NEXT-PLAN） |

## 2. P2.5 遗留错标（M1–M8）

| ID | 状态 | 证据/说明 |
|---|---|---|
| M1 GAR-0010「运动与童装」扩写 | **FIXED** | 卡片改述「页面提及 exercising/athletic activities 但未广泛采用；运动与童装的具体范围属 interpretive」 |
| M2 SRC-0046/0047 许可 | **FIXED** | license_status 改 `cc0`，note 说明「Commons Public domain；字典无 public_domain 值，按 cc0 记录」 |
| M3 假阴性「无覆盖」 | **FIXED（P3）** | 保持修复 |
| M4 C01 context 误导 | **FIXED** | C01 context_refs=`{}`（空）；T39 `context_refs_clean=PASS`，无 1770s/维多利亚引用 |
| M5 example 卡进 A | **FIXED（P3）** | 41/41 T 与 15 语义案例 A 套 example=0 |
| M6 GAR-0019 室内/雨景外层 | **FIXED** | T13/T38 A 无 anorak；T38 `no_arctic_indoor=PASS`；T01/T02 外层改用 GAR-0045 风衣 |
| M7 prompt 串文「worn in snow」 | **FIXED** | T13/T38 prompts 扫描 0 次「worn in snow」；41 例 `no_prompt_contamination=PASS` |
| M8 query 排序/重复 | **PARTIAL** | P07「1930s 上海」top5 现为 GAR-0031+LOOK-0008/0009/0012/0015（T40 `query_top5_contains:GAR-0031=PASS`）；P02 和服 top5 无同名重复（T41 `query_no_duplicate_names=PASS`）；**但 P14「noir」top5 仍含 example 卡（第 4/5 名），且 GAR-0001/GAR-0065 两张「和服」卡仍在库中**（仅查询层去重） |

## 3. P3.1 残余风险（WARN，不阻断但需 P4 处理）

| ID | 严重度 | 风险 | 证据/建议 |
|---|---|---|---|
| R1 | S2 | **职业同义词未全覆盖**：T33 用「警察」可匹配 GAR-0042，但我的合成案例「巡警」得到旗袍 GAR-0031+派克 GAR-0019（未匹配警察制服）；T32 医生 A 套仍含韩服 GAR-0064（白袍正确但内层不当） | 扩充 occupation hint 词表（巡警/女警/护士长/外科医生/厨师长/急诊医师…）；医疗场景对 one_piece 加领域白名单 |
| R2 | S3 | **example 卡仍在 query top5**（P14 noir：GAR-EXAMPLE-001 第 4、LOOK-EXAMPLE-001 第 5） | 建议 style/evidence 过滤时默认排除 example，或排序降权至 top5 之外 |
| R3 | S3 | **和服重复卡未在数据层合并**（GAR-0001/GAR-0065 同名，仅 name_en/periods/note 区分） | 保留可，但应在索引/字典标注 canonical；或合并为一张 |
| R4 | S4 | 噪声 warning「no upper_body/lower_body candidates retrieved」在 one_piece/set 场景反复出现 | 措辞改为「该槽位由 one_piece/set 覆盖」 |
| R5 | S3 | **质量自评与独立评分口径差异**：engineer `quality_eval` 报 relevant@5 3.84/94.1%，verifier 独立复评为 3.64/89.2%（严格人工 rubric） | 建议以独立 rubric 为准并在 release 说明；自评指标不得单独作为验收依据 |
| R6 | S3 | **SOURCES.csv 同步流程缺失**（D1 复发） | 把 `build_sources.py --write` 写入发布清单与 CI 式检查（每次改来源卡后执行） |

## 3.1 发布门槛 FAIL（唯一阻断项）

| ID | 严重度 | 问题 | 证据 |
|---|---|---|---|
| R7（FAIL） | S2（发布门槛） | **query relevance 未达 4.0 阈值** | verifier 独立 relevant@5=**3.64**；engineer `quality_eval.py --no-write` relevant@5=**3.92**（<4.0）→ **OVERALL FAIL / exit 1**；precision 独立 89.2%（自评 96.1%）、0 命中 12%。具体排序已修（P07 GAR-0031 第 1、P02/T41 去重），但 P09/P10 跨文化多词查询与 P14 example 残留拉低均值 |

## 4. 统计与优先级

- **FIXED：8 项**（D2 主项、D4、M1、M2、M4、M6、M7 + P3 的 F1/F2/F3/M3/M5 保持）
- **PARTIAL：1 项**（M8 查询层去重完成、数据层重复卡与 example top5 残留）
- **RESOLVED-BY-QA：2 次**（D1 CSV 漂移）
- **WARN/OPEN 残余：R1–R6（6 项，非阻断）+ R7（FAIL，唯一发布门槛阻断）**
- 优先级：**R7（query relevance ≥4.0）** > R1（职业同义词/医疗内层）> R2（example top5）> R6（CSV 同步）> R3/R4/R5。
- **发布门槛**：D2/D4 已关闭；R1/R2 建议在 P4 修复并回归；HUMAN_UAT_PENDING 4 项未完成前不得对外宣布全量 PASS。
