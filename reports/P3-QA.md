# P3 质量验收报告（P3.3 最终复验后）

- 验收人：`verifier`（独立复跑/复评；只写 reports/，未改卡片/脚本/`00-系统`）
- 时间：2026-11-04 03:16–03:25（Asia/Shanghai）；**P3.3 最终复验（task-22）**
- 快照：**343 张卡**（内容 158 + 来源 185）；git HEAD `fcebf79`（P3.3 commit）；**45 例验收**
- 环境：macOS，Python 3.9.6，PyYAML 6.0.3；网络可用；无 Obsidian GUI
- 声明：**不采信 engineer 自评**；所有指标为本人独立复算（与自评一致处标注）。不以 exit 0 / 45-45 PASS 代替质量结论。

## 0. 最终结论：PASS 24 / WARN 4 / FAIL 0 / HUMAN_UAT_PENDING 4（32 项）

| # | 项 | 判定 | 证据 |
|---|---|---|---|
| P1 | `validate.py` | **PASS** | 343/343；17/17 PASS；0 错误 0 警告 |
| P2 | `build_sources.py --check` | **PASS** | 185/185 一致（CSV 186 行）；3 组重复 URL canonical |
| P3 | 45 例验收 | **PASS** | `run_acceptance.py` exit 0；**PASS 45/45**；query 命中 187+ |
| P4 | T31–T45 回归 | **PASS** | 职业匹配/同义词/雨具/室内派克/context/查询排序去重全 PASS |
| P5 | F1（historical 1940s–70s 崩溃） | **PASS** | 4/4 exit 0、3 looks |
| P6 | F2（period/region 假阴性） | **PASS** | 1580s 3 looks；Byzantine 1 look + 诚实声明 |
| P7 | F3（未覆盖请求静默） | **PASS** | 6/6 探针 exit 0 且 warnings 3–8 条 |
| P8 | D2/R1 职业匹配（含同义词） | **PASS** | 护士 GAR-0036、医生白袍 GAR-0041（无韩服）、警察 GAR-0042（巡警/民警同）、厨师 GAR-0043、宇航员 GAR-0038/0039、婚礼 GAR-0005/0070；T42–T45 `occupation_match`/`no_cultural_mispick` PASS |
| P9 | D4 rainwear 虚假 warning | **PASS** | T01/T02 用 GAR-0045；T37/T38 `rainwear_selected`+`warning_absent` PASS |
| P10 | M4 context 过滤 | **PASS** | C01 context_refs={}；T39 `context_refs_clean` PASS |
| P11 | M6 室内/雨景极地派克 | **PASS** | T13/T38 无 GAR-0019；T38 `no_arctic_indoor` PASS |
| P12 | M7 prompt 串文 | **PASS** | T13/T38 无「worn in snow」；45 例 `no_prompt_contamination` PASS |
| P13 | M1 GAR-0010 断言 | **PASS** | 改述 + interpretive |
| P14 | M2 SRC-0046/47 许可 | **PASS** | cc0 + note 映射说明 |
| P15 | M5 example 卡进 A | **PASS** | 45/45 T + 15 语义案例 A 套 example=0 |
| P16 | 证据可追溯 | **PASS** | 验收 `evidence_coverage` PASS；`missing_urls=[]`；编造=0 |
| P17 | warnings 覆盖/真实性 | **PASS** | 45/45 有 warnings；类别齐备；无与库内卡矛盾的声明 |
| P18 | R2 查询 example/去重 | **PASS** | P14 无 example；P02 无同名和服重复；T41 PASS |
| P19 | **R7 query relevant@5（独立）** | **PASS** | **raw relevant@5 = 4.16（104/125）≥4.0**；precision **94.5%（104/110）**；**0 命中 0/25 = 0%**；P21 Mughal 3 命中（GAR-0071/SRC-0450/GAR-0072）、P22 mourning jewelry 2 命中（GAR-0073/GAR-0074）均相关。与 engineer 自评 4.16/0.945/0.0 一致 |
| P20 | **R3 和服同名去重** | **PASS** | GAR-0065 `name_zh: 出口和服` / `name_en: export kimono`（文件名保留兼容双链）；P02 返回 GAR-0001「和服」+ GAR-0065「出口和服」，无同名重复；T41 `query_no_duplicate_names` PASS |
| P21 | **R4 warning 噪声** | **PASS** | recommend.py 已无「no upper_body/lower_body candidates」文案；T27/T31–T36/T42–T45 等 warnings 中 0 命中该噪声 |
| P22 | **R5 CSV 同步质量门** | **PASS（实测）** | `quality_eval.check_sources_csv()` 在人工注入 1 行 CSV 漂移时返回 exit 1 + `RESULT: FAIL`，恢复后返回 exit 0 + `RESULT: PASS`；质量门有效（见 §6） |
| P23 | 新增来源抽样 | **PASS** | SRC-0450..SRC-0460 共 **11/11 HTTP 200**（curl -m 10 -L），页面标题/对象与卡名逐条吻合（jama/angarkha/farshi paijama/churidar/jet necklace/brooch/mourning ring/Princess Alice brooch/hair brooch） |
| P24 | 15 案例 6 维 rubric（抽样重评） | **PASS（样本）** | **7 PASS / 8 WARN / 0 FAIL**；切题均值 1.33/2、差异 1.67、约束 1.00、证据 2.00、诚实 2.00、叙事 1.00 |
| W1 | rubric 覆盖限制 | **WARN** | 8/15 案例仍 WARN（C01/C03/C04/C05/C06/C10/N4/N5），切题 0–1：明制、未来基底、身份弧线 wardrobe-stage、跨文化仪式礼服仍受 KB 覆盖限制（诚实声明，非错误） |
| W2 | C01 跨文化近似误配 | **WARN** | 1644 明末清初 A 套选莫卧儿 jama GAR-0071（印度），属近似而非明制；有 region/period warnings，但仍是「最近证据」示例 |
| W3 | filtered 查询结果数有限 | **WARN** | P14/P24/P25 等返回 3–4 条（example 已排除；覆盖有限，非排序错误） |
| W4 | 证据覆盖 0.94 | **WARN** | 部分 example/设计推断件无来源（属预期；验收 `evidence_coverage` 仍 PASS ≥0.65） |
| H1 | Obsidian GUI | **HUMAN_UAT_PENDING** | 无 GUI；仅结构层链接可达 |
| H2 | 逐图版权授权 | **HUMAN_UAT_PENDING** | 0 下载/0 内嵌；未逐图核验 |
| H3 | 语义评分签核 | **HUMAN_UAT_PENDING** | 本报告 rubric/评分需 lead 签核 |
| H4 | 62 张 draft 复核 | **HUMAN_UAT_PENDING** | `review_status: draft` 62 张 |

> **发布门槛结论：PASS（技术/数据/质量门全部通过）。**
> - R7 已关闭：独立 raw relevant@5 = **4.16（≥4.0）**、precision 94.5%、0 命中 0%；P21/P22 已真实命中且相关。
> - R3/R4/R5 全部关闭（R5 质量门已用「注入漂移→FAIL→恢复→PASS」实测有效）。
> - D2/D4/R1/R2/M1–M7/F1–F3 全部关闭；45/45 验收、validate、build_sources 全 PASS。
> - **发布仍不得写「全量 PASS」**：HUMAN_UAT_PENDING 4 项（GUI/逐图版权/语义签核/62 draft 复核）未完成，必须在发布前完成并留档。

## 1. 方法与真实命令

```bash
python3 scripts/validate.py                 # exit 0：343/343，17/17 PASS
python3 scripts/build_sources.py --check    # exit 0：185/185 一致（CSV 186 行含表头）
python3 scripts/run_acceptance.py           # exit 0：PASS 45/45
python3 scripts/quality_eval.py --no-write  # exit 0：OVERALL PASS；relevant@5=4.16、precision=.945、0-hit=0
python3 scripts/quality_eval_audit.py --quick  # F1/F2/F3 回归
# 独立 query 探针（25+6）：/tmp/p33_query.json
# 独立语义案例：C01–C10 + N1–N5（/tmp/p33cases/）
# 新增来源抽样：SRC-0450..0460 curl -m 10 -L → 11/11 200，页面标题与卡名吻合
```

## 2. R7 独立指标（逐探针）

| 指标 | engineer 自评 | **verifier 独立** | 门槛 | 结论 |
|---|---|---|---|---|
| relevant@5（25 探针） | 4.16（104/125） | **4.16（104/125）** | ≥4.0 | **PASS** |
| precision | 0.945 | **94.5%（104/110）** | ≥0.8/0.9 | PASS |
| 0 命中率 | 0.0 | **0%（0/25）** | ≤0.2 | PASS |

**逐探针 relevant/5**：P01 5、P02 5、P03 5、P04 5、P05 5、P06 4、P07 5、P08 5、P09 3、P10 5、P11 2/2、P12 3/3、P13 5、P14 3/3（无 example）、P15 5、P16 5、P17 5、P18 4、P19 5、P20 4、**P21 3**（GAR-0071/SRC-0450/GAR-0072）、**P22 2**（GAR-0073/GAR-0074）、P23 5、P24 3、P25 3。
- P21/P22 此前为 0 命中，P3.3 新增莫卧儿 jama/帕贾马裤/维多利亚哀悼珠宝/哀悼戒指胸针卡与 11 张来源后已真实命中且相关。
- 剩余不足 5 的探针均属「结果数少于 5（example 排除/库内条目少）」或「部分相关」，非排序错误；无 0 命中。

## 3. R1 职业匹配独立验证（六类 + 同义词）

| 场景 | A 套实际 | 结论 |
|---|---|---|
| 护士 T26/T31 | GAR-0036+白袍 GAR-0041+医疗鞋 GAR-0044+徽章+手袋 | 匹配 |
| 医生 T32/医师 T43 | GAR-0041 白袍+医疗鞋（无韩服） | 匹配 |
| 警察 T33/巡警 T42/民警 T45 | GAR-0042+风衣 GAR-0045+靴 | 匹配 |
| 厨师 T34 | GAR-0043+牛仔裤+靴 | 匹配 |
| 宇航员 T35/T44 | GAR-0038 连体工作服+防护外套+头盔 GAR-0039 | 匹配 |
| 婚礼 T27/T36 | GAR-0005 布布长袍+gele GAR-0070 | 匹配 |

## 4. R2/R3/R4 复核

- **R2**：P14「--style-tag noir」→ LOOK-0007、LOOK-0021、STY-0005（3 条，无 example）；P02/T41 无同名重复。
- **R3**：GAR-0065 已改名「出口和服 / export kimono」（文件名保留兼容）；P02 结果中 name_zh 与 GAR-0001 不同名，去重通过；T41 PASS。
- **R4**：`no upper_body/lower_body candidates` 文案已移除；T27/T31–T36/T42–T45 的 warnings 扫描 0 命中。

## 5. 15 案例 6 维 rubric（重评）

PASS 7 / WARN 8 / FAIL 0（P3.2 同为 7/8/0）。PASS：C02 急诊护士、C07 加纳婚礼、C08 1580s、C09 太空站、N1 ER 护士、N2 火星技师、N3 加纳新郎；WARN：C01、C03、C04、C05、C06、C10、N4、N5（多因 KB 无对应基底/仪式/未来服，均有 warnings）。切题均值 1.33/2、差异 1.67、约束 1.00、证据 2.00、诚实 2.00、叙事 1.00。

## 6. R5 质量门实测（注入漂移 → 恢复）

| 步骤 | 结果 |
|---|---|
| 备份 `reports/SOURCES.csv`（186 行） | — |
| 人工给 SRC-0001 的 note 追加 `[QA-DRIFT]` | build_sources --check → **exit 1**；`[FAIL] 共有行的字段一致: 1 行有差异`；`RESULT: FAIL` |
| `quality_eval.check_sources_csv()`（漂移时） | 返回 `(1, '[FAIL] …RESULT: FAIL…')` → 质量门将其映射为 `sources_csv_sync=0` → OVERALL FAIL |
| 恢复备份后 | `check_sources_csv()` → `(0, 'RESULT: PASS…')`；build --check exit 0；CSV 186 行 |

结论：**R5 同步质量门真实有效**（不是仅文档声明）。

## 7. 新增来源抽样（≥10 要求超额）

- SRC-0450..SRC-0460 共 11 条（3 个段位？均为 V&A）：莫卧儿 jama、Bharatpur jama、勒克瑙 angarkha、farshi paijama、古吉拉特 churidar、1870s jet 项链、jet 胸针、19 世纪雕花 jet 项链、William Pitt 哀悼戒指、Princess Alice 哀悼胸针、19 世纪发丝哀悼胸针。
- **11/11 HTTP 200**；页面 `<title>` 与卡名逐条吻合；对应新卡 GAR-0071 莫卧儿jama、GAR-0072 帕贾马裤、GAR-0073 维多利亚哀悼珠宝、GAR-0074 哀悼戒指与胸针。

## 8. 残余风险与 HUMAN_UAT_PENDING

**WARN（4 项，不阻断）**：W1 15 案例中 8 例切题 0–1（KB 覆盖限制，已诚实声明）；W2 C01 明末清初使用莫卧儿 jama（跨文化近似）；W3 P14/P24/P25 等 filtered 结果数有限；W4 证据覆盖 0.94（example/设计推断件无来源属预期）。
**HUMAN_UAT_PENDING（4 项，不得写成 PASS）**：H1 Obsidian GUI；H2 逐图版权；H3 15 案例语义评分签核；H4 62 张 draft 复核。

## 9. 复现

```bash
python3 scripts/validate.py
python3 scripts/build_sources.py --check
python3 scripts/run_acceptance.py
python3 scripts/quality_eval.py --no-write
python3 scripts/quality_eval_audit.py --quick
```
- 原始证据：`/tmp/p33_query.json`、`/tmp/p33cases/`、`/tmp/p33_acc.log`、`/tmp/p33_qeval.txt`、`/tmp/ev33/results.tsv`（11 URL）。
- 版本：v1.4（2026-11-04，verifier/task-22，P3.3 最终复验）。


---

## 10. P3.5 最终验证补记（2026-11-04 14:00，task-28）

- 快照 363 卡（内容 166 + 来源 197）；HEAD `04778f8`。
- `validate.py` PASS（363/363）；`run_acceptance.py` **45/45 PASS**；`tests/test_workflow.py` **8/8 PASS**；
  **`build_sources.py --check` FAIL：缺 12 行 SRC-0480..SRC-0491**；**`quality_eval` OVERALL FAIL，仅 `sources_csv_sync=0` FAIL**（其余 16 项 PASS：relevant@5 4.16、precision 0.945、0-hit 0、evidence_coverage 0.868……）。
- workflow：fixture Macbeth 通过（scenes=3、stages rise/fall、IDs 真实、exit 0）；真实案例 meta `"1-3"` 引用导致 stage 全 unassigned（D2，S-id 修正后分配正确）；案例 workflow-run 为旧产物。
- LOOK 修复 7 张（非 9）：LOOK-0011/0013/0016/0017/0018/0021/0022；URL 抽验 26/26 200；DRAFT-REVIEW 更新 45/17；未改卡片。
- Macbeth 案例：18 套 × 2 角色 × 3 阶段 × A/B/C；50 ID 0 缺失；EVIDENCE 18 行 + 8 缺口；HUMAN-SCORE 18 行全空；6 组 SRC 抽样 200。
- **发布门禁：PRIVATE-READY = YES（条件修 D1）；PUBLIC-READY = NO（BLOCKED）**；HUMAN_UAT_PENDING 4 项不变。
- 详细报告：`reports/P3.5-REPORT.md`；门禁：`reports/RELEASE-GATE.md`。
