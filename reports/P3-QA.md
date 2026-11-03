# P3 质量验收报告（P3.1 复验后）

- 验收人：`verifier`（独立复跑/复评；只写 reports/，未改卡片/脚本/`00-系统`）
- 时间：2026-11-04 02:35–02:55（Asia/Shanghai）；**P3.1 复验轮（task-17）**
- 快照：**328 张卡**（内容 154 + 来源 174）；git HEAD `0345f05` + P3.1 工作区修改（scripts/测试/卡片修正，未提交）；41 例验收
- 环境：macOS，Python 3.9.6，PyYAML 6.0.3；网络可用；无 Obsidian GUI
- 输入：P3 baseline（`P2.5-ACCEPTANCE.md`、本报告 P3 版历史）、engineer P3.1 修复、architect 卡片修正、本人独立探针
- 声明：**不以 exit 0 / 41-41 PASS 代替质量结论**；GUI/逐图版权/签核/draft 复核未通过，保持 HUMAN_UAT_PENDING。

## 0. 最终结论：PASS 17 / WARN 5 / FAIL 1 / HUMAN_UAT_PENDING 4（27 项）

| # | 项 | 判定 | 证据 |
|---|---|---|---|
| P1 | `validate.py` 结构校验 | **PASS** | 328/328 卡；17/17 检查 PASS；0 错误 0 警告 |
| P2 | `build_sources.py` 一致性 | **PASS（修复后）** | P3.1 改 SRC-0046/47 后 CSV 2 行漂移（FAIL）→ QA `--write` 重建 174 行后 PASS（D1 复发，流程风险保留） |
| P3 | 41 例验收 | **PASS** | `run_acceptance.py` exit 0；**PASS 41/41**；query 命中总 178、逐例 ≥1 |
| P4 | 新增回归用例 T31–T41 | **PASS** | 职业匹配 5 例、跨文化婚礼、雨具选择、室内禁极地派克、context 清洁、query 排序/去重，逐项验收判定 PASS（见 §7） |
| P5 | F1 崩溃回归（historical 1940s–70s） | **PASS** | 4/4 exit 0、3 looks（P2.5：4/4 exit 1） |
| P6 | F2 period/region 假阴性回归 | **PASS** | 1580s 意大利（T23/C08）exit 0、3 looks 使用 doublet/codpiece/文艺复兴长袍；拜占庭（T24）exit 0、1 look + 缺口声明；无「no wardrobe candidates」假措辞 |
| P7 | F3 证据不足诚实性 | **PASS** | 6/6 未覆盖探针均有 3–10 条 warnings；不再静默 |
| P8 | **D2 职业匹配** | **PASS（主项）** | T26/T31 急诊护士 A=护士制服 GAR-0036+白袍 GAR-0041+医疗鞋 GAR-0044+徽章+手袋；T32 医生含 GAR-0041；T33 警察=GAR-0042；T34 厨师=GAR-0043；T35 太空=连体工作服 GAR-0038+头盔 GAR-0039；T36 婚礼=布布长袍+gele；warnings 已改为「无 X 专属卡，通用件替代且未用他职业制服」 |
| P9 | **D4 rainwear 虚假 warning** | **PASS** | T01/T02 外层改用 GAR-0045 风衣；T37 `rainwear_selected=PASS`、`warning_absent:rainwear_gap=PASS`；扫描 41 例 warnings 无「rainwear cards are missing」 |
| P10 | M4 context 过滤 | **PASS** | C01 context_refs=`{}`；T39 `context_refs_clean=PASS`（refs=0） |
| P11 | M6 室内/雨景极地派克 | **PASS** | T13/T38 A 套无 GAR-0019；T38 `no_arctic_indoor=PASS` |
| P12 | M7 prompt 串文 | **PASS** | T13/T38 prompts 无「worn in snow」；41 例 `no_prompt_contamination=PASS` |
| P13 | M1 GAR-0010 断言 | **PASS** | 已改述为「页面提及 exercising/athletic activities 但未广泛采用；运动与童装属 interpretive」 |
| P14 | M2 SRC-0046/47 许可 | **PASS** | `license_status: cc0`，note 说明字典无 public_domain 的映射 |
| P15 | M5 example 卡进 A | **PASS** | 41/41 T + 15 语义案例 A 套 example=0 |
| P16 | evidence 可追溯 | **PASS** | 41 例 `looks with evidence=3/3`；`missing_urls=[]`；编造=0 |
| P17 | warnings 覆盖与真实性 | **PASS** | 41/41 有 warnings；职业/文化/未来/年代/天气/冲突/身份弧线类别齐备；未再发现与实际库内卡矛盾的声明 |
| F1 | **query 相关性未达发布门槛** | **FAIL** | 独立复评 relevant@5 **3.64/5**（< 4.0 发布门槛）；engineer `quality_eval.py --no-write` 亦报 relevant@5 **3.92 < 4.0**、**OVERALL: FAIL（exit 1）**。precision 独立 89.2%（自评 96.1%）、0 命中 12%。P07/P02 排序与去重已修复，但总体 relevance 未达阈值 |
| W2 | example top5 / 数据层重复卡 | **WARN** | P14「noir」top5 现为 LOOK-0007/LOOK-0021/STY-0005/GAR-EXAMPLE-001/LOOK-EXAMPLE-001（example 降至第 4/5）；P07/T40 已修复（GAR-0031 第 1）；P02/T41 查询无同名重复，但 GAR-0001/GAR-0065 两张和服卡仍在库 |
| W3 | 15 案例 6 维 rubric | **WARN** | **6 PASS / 9 WARN / 0 FAIL**；切题均值 **1.27/2**（P3 0.53）、差异 1.73、约束 1.00、证据 2.00、诚实 2.00、叙事 1.00；太空/未来/身份下滑案例仍偏弱（诚实声明） |
| W4 | 职业同义词/内层匹配残余 | **WARN** | 合成「巡警」案例得到旗袍+派克（未匹配 GAR-0042）；T32 医生 A 含韩服 GAR-0064（白袍正确、内层不当） |
| W5 | SOURCES.csv 同步流程 | **WARN** | D1 再次复发（本轮已重建）；须把 `build_sources --write` 纳入发布步骤 |
| W6 | 证据覆盖不均 | **WARN** | 部分用例 items with source_ids 8/12（T31）等；example/设计推断件无来源属预期，但覆盖率应公开披露 |
| H1 | Obsidian GUI | **HUMAN_UAT_PENDING** | 无 GUI；仅结构层链接可达 |
| H2 | 逐图版权授权 | **HUMAN_UAT_PENDING** | 0 下载/0 内嵌；未逐图核验 |
| H3 | 语义评分签核 | **HUMAN_UAT_PENDING** | 本报告 rubric/评分需 lead 签核 |
| H4 | 62 张 draft 复核 | **HUMAN_UAT_PENDING** | `review_status: draft` 62 张 |

> **结论：D2 与 D4 均已关闭，但 P3.1 未完全通过发布前质量门槛——查询相关性未达 4.0 阈值（独立 3.64 / engineer 自评 3.92，`quality_eval` 判 OVERALL FAIL），故保留 1 项 FAIL；其余 17 项 PASS、5 项 WARN、4 项 HUMAN_UAT_PENDING。**

## 1. 方法与真实命令

```bash
python3 scripts/validate.py                 # exit 0：328/328，17/17 PASS，0 错误 0 警告
python3 scripts/build_sources.py --check    # P3.1 后首次：exit 1（SRC-0046/47 两行漂移）
python3 scripts/build_sources.py --write    # QA 重建 174 行
python3 scripts/build_sources.py --check    # exit 0（RESULT: PASS）
python3 scripts/run_acceptance.py           # exit 0：PASS 41/41，query 命中 178
python3 scripts/quality_eval.py --no-write  # engineer 自评复跑（仅作对照，不作为验收依据）
python3 scripts/quality_eval_audit.py --quick  # 回归探针（F1/F2/F3）
# 独立探针：/tmp/p31_audit.py（30 T + 10 C + 5 N + 9 D2 合成案例 + 4 crash），结果 /tmp/p31_results.json
# query：25 固定探针 + 6 未覆盖探针，结果 /tmp/p31_query.json
```

## 2. D2/D4 关闭证据（独立复跑）

| 场景 | A 套实际单品（节选） | 结论 |
|---|---|---|
| T26 急诊科护士 / T31 急诊护士职业匹配 / C02 ER nurse / 合成 NURSE | GAR-0036 护士制服 + GAR-0041 医生白袍 + GAR-0044 医疗工作鞋 + GAR-0050 制服徽章 + GAR-0048 手提包 | **职业匹配**，无警察/厨师顶替 |
| T32 医生职业匹配 | GAR-0041 医生白袍 + GAR-0044 医疗鞋（另含 GAR-0064 韩服，见 W4） | 白袍匹配；内层残余 |
| T33 警察职业匹配 | GAR-0042 警察制服 + GAR-0045 风衣 + GAR-0022 靴 | **匹配** |
| T34 厨师职业匹配 | GAR-0043 厨师服 + GAR-0014 牛仔裤 + GAR-0022 靴 | **匹配** |
| T35 太空站维修工 / C09 / N2 火星技师 | GAR-0038 连体工作服 + GAR-0037 防护外套 + GAR-0039 安全头盔 + GAR-0022 靴 | 职业/环境基座匹配 |
| T36/T27/C07/N3 加纳婚礼 | GAR-0005 布布长袍 + GAR-0070 头巾（gele）+ GAR-0048 手袋 + GAR-0035 鞋 | 文化/场合匹配 |
| T01/T02/T37 1930s 上海雨 | GAR-0031 旗袍 + **GAR-0045 风衣** + GAR-0035 鞋 / GAR-0047 雨伞 | rainwear 已选；`rainwear_gap` warning 不再出现 |
| T13/T38 室内走廊 | GAR-0007/0010/0017/0023，无 GAR-0019 极地派克；prompt 无「worn in snow」 | **M6/M7 关闭** |
| C01 明末清初 | A 仍为欧洲 doublet/codpiece/mule（KB 无明制卡，属诚实的近似）；context_refs=`{}` | M4 关闭；切题仍低（W3） |

## 3. 回归（F1/F2/F3 保持修复）

- F1：historical 1940s/50s/60s/70s → 4/4 exit 0、3 looks（`/tmp/p31_results.json.crash`）。
- F2：1580s（T23/C08）→ 3 looks 使用 16 世纪卡；拜占庭（T24）→ 1 look + 「looks are missing required layers … no invented replacements」诚实声明；无假阴性措辞。
- F3：6 个未覆盖探针全部 exit 0 且 warnings ≥3（I1 10、I2 8、I3 6、I4 5、I5 3、I6 4）；无静默。
- M3/M5 保持修复。

## 4. Query 指标（独立复评，对比 P2.5/P3）

| 指标 | P2.5 | P3 | **P3.1（verifier 独立）** |
|---|---|---|---|
| relevant@5 | 3.0 | 3.64 | **3.64**（91/125） |
| precision | 86.2% | 89.2% | **89.2%**（91/102） |
| 0 命中率 | 16%（4/25） | 12%（3/25） | **12%**（3/25：spacesuit/Mughal/mourning） |
| 具体排序 | — | P07 缺 GAR-0031；P14 example 第 1/4 | **P07 GAR-0031 第 1（T40 PASS）；P02/T41 无同名重复；P14 example 降至第 4/5（仍残留）** |

- 未覆盖主题 6 探针：Q26 男鞋 1、Q27 拜占庭 5、Q28 非洲仪式 5、Q29 太空站 5、Q30 朋克 5、Q31 雨衣 1 → 全部 ≥1 命中。
- **engineer `quality_eval.py --no-write` 独立重跑结果：exit 1；relevant@5=3.92（阈值 4.0）→ FAIL；precision=96.1%、0 命中 12%、崩溃率 0、example-in-A 0、warnings 覆盖 1.0、A/B/C 差异 0.976、证据覆盖 0.959、context 清洁 1.0、prompt 串文 0、occupation_mismatch 0、rainwear_false_claim 0、arctic_indoor 0 → 其余 15 项 PASS，OVERALL: FAIL（仅 relevant@5 未达阈值）。**
- 采用两者的较小值：**relevant@5 以独立 3.64 为准（<4.0）→ 记为 FAIL**；precision 同时披露独立 89.2% 与自评 96.1%（评分标准不同，见 P3-DEFECTS R5）。

## 5. 15 案例 6 维语义 rubric（P3.1 重评）

维度 0–2：切题/差异/约束/证据/诚实/叙事；≥10 PASS，7–9 WARN，≤6 FAIL。

| 案例 | 切题 | 差异 | 约束 | 证据 | 诚实 | 叙事 | 总分 | 判定 | 说明 |
|---|---|---|---|---|---|---|---|---|---|
| C01 明末清初文人 | 0 | 2 | 1 | 2 | 2 | 1 | 8 | WARN | 欧洲单品近似、无明制卡；诚实声明 |
| C02 急诊护士 | 2 | 2 | 1 | 2 | 2 | 1 | **10** | **PASS** | 护士制服+白袍+医疗鞋+徽章 |
| C03 零重力歌剧女伶 | 0 | 2 | 1 | 2 | 2 | 1 | 8 | WARN | 布布长袍+靴；未来基底仍缺（已警告） |
| C04 1920s 表现主义 | 1 | 2 | 1 | 2 | 2 | 1 | 9 | WARN | 1930s Utility+风衣混搭；风格卡缺 |
| C05 富太→难民 | 1 | 0 | 1 | 2 | 2 | 1 | 7 | WARN | 1 套贯穿三场；弧线未建模已警告 |
| C06 夜班信使连续性 | 1 | 1 | 1 | 2 | 2 | 2 | 9 | WARN | 状态连续性正确；职业为达希基+牛仔 |
| C07 加纳-英国婚礼 | 2 | 2 | 1 | 2 | 2 | 1 | **10** | **PASS** | 布布长袍+gele 文化匹配 |
| C08 1580s 意大利舞者 | 2 | 2 | 1 | 2 | 2 | 1 | **10** | **PASS** | 16 世纪 doublet/codpiece/长袍 |
| C09 低预算太空站 | 2 | 2 | 1 | 2 | 2 | 1 | **10** | **PASS** | 连体工作服+头盔+防护外套 |
| C10 1930s+义体冲突 | 1 | 2 | 1 | 2 | 2 | 1 | 9 | WARN | 冲突已警告；外层非义体 |
| N1 ER 创伤护士 | 2 | 2 | 1 | 2 | 2 | 1 | **10** | **PASS** | 同 C02 |
| N2 火星技师 | 1 | 2 | 1 | 2 | 2 | 1 | 9 | WARN | 工装近似；未来基底缺 |
| N3 加纳婚礼新郎 | 2 | 2 | 1 | 2 | 2 | 1 | **10** | **PASS** | 布布长袍+gele |
| N4 爵士名媛→女工 | 1 | 0 | 1 | 2 | 2 | 1 | 7 | WARN | 1 套贯穿；弧线未建模已警告 |
| N5 1920s+义体冲突 | 1 | 2 | 1 | 2 | 2 | 1 | 9 | WARN | 冲突警告；外层为风衣 |

**汇总：PASS 6 / WARN 9 / FAIL 0**（P3：1/14/0）；均值：切题 **1.27**、差异 1.73、约束 1.00、证据 2.00、诚实 2.00、叙事 1.00；总分均值 9.0/12。

## 6. 复跑与结构（独立）

| 项 | 结果 |
|---|---|
| `validate.py` | exit 0；328/328；17/17 PASS；0 错误 0 警告 |
| `build_sources.py --check` | 首次 exit 1（SRC-0046/47 rights/note 漂移）→ `--write` 后 exit 0；`SOURCES.csv` 174 行 + 表头 |
| `run_acceptance.py` | exit 0；**PASS 41/41，FAIL 0/41**；query 命中 178、逐例 ≥1；SUMMARY 与实测一致（41 例） |
| `quality_eval.py --no-write` | **exit 1；OVERALL: FAIL**（仅 relevant@5 3.92 < 4.0；其余 15 项 PASS，precision 96.1%、0-hit 12%、崩溃 0、example-in-A 0、warnings 1.0、A/B/C 0.976、evidence 0.959、context 1.0、contamination 0、occupation_mismatch 0、rainwear_false_claim 0、arctic_indoor 0） |
| 新测试 T31–T41 | 全部 PASS；关键断言：`occupation_match`/`no_occupation_mismatch`（T31–T35）、`occasion_match`/`region_evidence`（T36）、`rainwear_selected`/`warning_absent:rainwear_gap`（T37/T38）、`no_arctic_indoor`（T38）、`context_refs_clean`（T39）、`query_top5_contains:GAR-0031`（T40）、`query_no_duplicate_names`/`query_no_example_top`（T41） |

## 7. 残余风险与 HUMAN_UAT_PENDING

**残余风险（WARN，不阻断；详见 P3-DEFECTS §3）**
1. R1 职业同义词/内层：合成「巡警」→旗袍+派克；T32 医生含韩服。
2. R2 example 卡仍在 P14 top5 第 4/5；数据层和服重复卡未合并。
3. R5 自评 vs 独立评分口径差（3.84/94.1% vs 3.64/89.2%）。
4. R6 SOURCES.csv 同步流程缺失（D1 复发）。
5. 15 案例中 9 例切题仍 0–1（KB 覆盖限制，已诚实声明）。

**HUMAN_UAT_PENDING（不得写成 PASS）**
- H1 Obsidian GUI 打开/渲染/链接跳转
- H2 逐图版权授权核验
- H3 15 案例语义评分人工签核
- H4 62 张 `review_status: draft` 人工复核

## 8. 复现

```bash
python3 scripts/validate.py
python3 scripts/build_sources.py --check
python3 scripts/run_acceptance.py
python3 scripts/quality_eval_audit.py --quick    # F1/F2/F3 回归
python3 scripts/quality_eval_audit.py            # 回归 + query 探针 + 15 案例
python3 scripts/quality_eval.py --no-write       # engineer 自评对照
```
- 原始证据：`/tmp/p31_results.json`（推荐逐例）、`/tmp/p31_query.json`（query 探针）、`/tmp/p31_acc.log`（41 例）、`/tmp/p31_qeval.txt`（自评对照）。
- 版本：v1.2（2026-11-04，verifier/task-17，P3.1 复验）。
