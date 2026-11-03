# P3 质量验收报告（P3.2 最终复验后）

- 验收人：`verifier`（独立复跑/复评；只写 reports/，未改卡片/脚本/`00-系统`）
- 时间：2026-11-04 03:04–03:15（Asia/Shanghai）；**P3.2 最终复验（task-19）**
- 快照：**328 张卡**（内容 154 + 来源 174）；git HEAD `281e3b1`（P3.2 commit）；**45 例验收**
- 环境：macOS，Python 3.9.6，PyYAML 6.0.3；网络可用；无 Obsidian GUI
- 声明：**不采信 engineer 自评分数**；所有指标为本人独立复算。不以 exit 0 / 45-45 PASS 代替质量结论。

## 0. 最终结论：PASS 19 / WARN 5 / FAIL 0 / HUMAN_UAT_PENDING 4（28 项）

| # | 项 | 判定 | 证据 |
|---|---|---|---|
| P1 | `validate.py` 结构校验 | **PASS** | 328/328；17/17 PASS；0 错误 0 警告 |
| P2 | `build_sources.py` 一致性 | **PASS** | CSV 174 行与来源卡一致（P3.2 已同步；`--check` exit 0；3 组重复 URL 已标 canonical） |
| P3 | 45 例验收 | **PASS** | `run_acceptance.py` exit 0；**PASS 45/45**；query 命中总 187、逐例 ≥1 |
| P4 | 回归用例 T31–T45 | **PASS** | 职业匹配（含同义词：巡警/民警/医师/宇航员）、雨具、室内禁极地派克、context、查询排序/去重全部 PASS |
| P5 | F1（historical 1940s–70s 崩溃） | **PASS** | 4/4 exit 0、3 looks |
| P6 | F2（period/region 假阴性） | **PASS** | 1580s 3 looks（16 世纪卡）；拜占庭 1 look + 诚实缺口声明；无假阴性措辞 |
| P7 | F3（未覆盖请求静默） | **PASS** | 6/6 探针 exit 0 且 warnings 3–8 条 |
| P8 | **D2 职业匹配（含同义词）** | **PASS** | 护士 T26/T31=GAR-0036+白袍 GAR-0041+医疗鞋 GAR-0044+徽章+手袋；医生 T32/T43=白袍+医疗鞋（**无韩服**）；警察 T33/T42/T45=GAR-0042；厨师 T34=GAR-0043；宇航员 T35/T44=连体工作服 GAR-0038+头盔 GAR-0039；婚礼 T27/T36=布布长袍 GAR-0005+gele GAR-0070；`occupation_match`/`no_occupation_mismatch`/`no_cultural_mispick` 全 PASS |
| P9 | **D4 rainwear 虚假 warning** | **PASS** | T01/T02 用 GAR-0045 风衣；T37 `rainwear_selected`+`warning_absent` PASS；41+ 例无「rainwear cards are missing」 |
| P10 | M4 context 过滤 | **PASS** | C01 context_refs={}；T39 `context_refs_clean` PASS |
| P11 | M6 室内/雨景极地派克 | **PASS** | T13/T38 A 无 GAR-0019；T38 `no_arctic_indoor` PASS |
| P12 | M7 prompt 串文 | **PASS** | T13/T38 prompts 无「worn in snow」；45 例 `no_prompt_contamination` PASS |
| P13 | M1 GAR-0010 断言 | **PASS** | 已改述「页面提及 exercising/athletic activities 但未广泛采用；运动与童装属 interpretive」 |
| P14 | M2 SRC-0046/47 许可 | **PASS** | `license_status: cc0` + note 映射说明 |
| P15 | M5 example 卡进 A | **PASS** | 45/45 T + 15 语义案例 A 套 example=0 |
| P16 | 证据可追溯 | **PASS** | 验收 checks `evidence_coverage` PASS；`missing_urls=[]`；编造=0 |
| P17 | warnings 覆盖/真实性 | **PASS** | 45/45 有 warnings；职业/文化/未来/年代/天气/冲突/身份类别齐备；无与实际库内卡矛盾的声明 |
| P18 | **R2 查询层 example/去重** | **PASS** | P14「noir」返回 3 条且全部非 example（`query_no_example_top` PASS）；P02 无同名和服重复；T41 `query_no_duplicate_names` PASS |
| P19 | 15 案例 6 维 rubric | **PASS（样本）** | **7 PASS / 8 WARN / 0 FAIL**（P3.1：6/9/0）；切题均值 1.33/2、差异 1.67、约束 1.00、证据 2.00、诚实 2.00、叙事 1.00；总分均值 9.0/12 |
| W1 | **R7 query relevant@5** | **WARN（条件性）** | 独立复评 **raw relevant@5=3.92（98/125）< 4.0**；**剔除 2 个已确认真实缺卡探针（P21 Mughal、P22 mourning jewelry）后=4.26（98/115→按 23 探针均 4.26）≥4.0**；precision **93.3%（98/105）**；0 命中 **8%（2/25）**。engineer 自评 4.0/95.2%/8%——差异来自标注严格度 |
| W2 | 单探针相关性缺口 | **WARN** | P09 3/5（PRD-0003/GAR-0031 仅部分相关）、P10 4/5（混入韩服 GAR-0064）、P20 4/5（Courrèges 外套部分相关）、P14/P24/P25 结果数仅 3–4 条；P21/P22 为已知真实 KB 缺口（0 命中） |
| W3 | 和服重复卡（数据层） | **WARN** | GAR-0001/GAR-0065 仍为两张「和服」卡（仅查询层去重；建议 canonical 标注或合并） |
| W4 | 噪声 warning | **WARN** | 「no upper_body/lower_body candidates retrieved」在 one_piece/set 场景重复出现（T27/T33/T42/T45 等） |
| W5 | SOURCES.csv 同步流程 | **WARN** | 本轮已同步（build PASS），但无自动化校验；历次曾两次漂移（D1），建议纳入发布步骤 |
| H1 | Obsidian GUI | **HUMAN_UAT_PENDING** | 无 GUI；仅结构层链接可达 |
| H2 | 逐图版权授权 | **HUMAN_UAT_PENDING** | 0 下载/0 内嵌；未逐图核验 |
| H3 | 语义评分签核 | **HUMAN_UAT_PENDING** | 本报告 rubric/评分需 lead 签核 |
| H4 | 62 张 draft 复核 | **HUMAN_UAT_PENDING** | `review_status: draft` 62 张 |

> **发布门槛结论：条件性通过（CONDITIONAL PASS）。**
> - R1（职业同义词/跨文化误配）、R2（查询 example/去重）、D2、D4、M1–M7 全部关闭；45/45 验收 + validate/build 全 PASS。
> - **R7 为唯一未闭合 WARN**：raw relevant@5 = 3.92 < 4.0（差 0.08），但剔除已确认的真实缺卡探针（Mughal/ mourning jewelry）后为 4.26 ≥ 4.0；precision 93.3%、0 命中 8% 均达标。
> - 是否放行取决于 lead 对「已知 KB 缺口（P21/P22）是否从门槛分母剔除」的决定；若要求 raw ≥4.0，则需再提升 P09/P10/P20 相关性或补 Mughal/哀悼珠宝卡。HUMAN_UAT_PENDING 4 项未完成前不得对外宣布全量 PASS。

## 1. 方法与真实命令

```bash
python3 scripts/validate.py                 # exit 0：328/328，17/17 PASS
python3 scripts/build_sources.py --check    # exit 0：174/174 一致（P3.2 已同步 CSV）
python3 scripts/run_acceptance.py           # exit 0：PASS 45/45，query 命中 187
python3 scripts/quality_eval_audit.py --quick  # F1/F2/F3 回归：4/4 exit0、1580s 3 looks、6/6 warnings
# 独立 query 探针：25 固定 + 6 未覆盖（/tmp/p32_query.json）
# 独立语义案例：C01–C10 + N1–N5 重跑（/tmp/p32cases/）；R1 职业验证取 acceptance raw T26/T27/T31–T36/T42–T45
# engineer 自评（仅对照，不采信）：11-验收/质量评估/SUMMARY.md（4.0/95.2%/8%）
```

## 2. R7 独立指标与逐探针缺口

| 指标 | engineer 自评 | **verifier 独立** | 门槛 |
|---|---|---|---|
| relevant@5（25 探针） | 4.0（100/125） | **3.92（98/125）** | ≥4.0（raw 未达，差 0.08） |
| relevant@5（剔除 P21/P22 已知缺卡） | — | **4.26（98/115 槽位；23 探针均 4.26）** | ≥4.0（达标） |
| precision | 95.2% | **93.3%（98/105）** | ≥90% PASS |
| 0 命中率 | 8% | **8%（2/25：Mughal、mourning jewelry）** | ≤20% PASS |

**逐探针相关性（relevant/5）**：P01 5、P02 5、P03 5、P04 5、P05 5、P06 4、P07 5、P08 5、P09 3、P10 4、P11 2/2、P12 3/3、P13 5、P14 3/3（example 已排除）、P15 5、P16 5、P17 5、P18 4、P19 5、P20 4、P21 0、P22 0、P23 5、P24 3、P25 3。
- 缺口归因：P09/P10/P20 属「部分相关」；P21/P22 为真实 KB 缺卡；P14/P24/P25 返回数少（n=3–4）拉低标准 relevant@5 分母。
- 未覆盖主题 6 探针：Q26 男鞋 1、Q27 拜占庭 5、Q28 非洲仪式 5、Q29 太空站 5、Q30 朋克 5、Q31 雨衣 1，全部 ≥1。

## 3. R1 职业匹配独立验证（六类 + 同义词）

| 场景 | A 套实际（acceptance raw） | 结论 |
|---|---|---|
| 护士 T26/T31 | GAR-0036 护士制服 + GAR-0041 白袍 + GAR-0044 医疗鞋 + GAR-0050 徽章 + GAR-0048 手袋 | **匹配** |
| 医生 T32/医师 T43 | GAR-0041 白袍 + GAR-0044 医疗鞋（+背心/牛仔基底；**无韩服**） | **匹配（R1 修好）** |
| 警察 T33/巡警 T42/民警 T45 | GAR-0042 警察制服 + GAR-0045 风衣 + GAR-0022 靴 | **匹配** |
| 厨师 T34 | GAR-0043 厨师服 + GAR-0014 牛仔裤 + GAR-0022 靴 | **匹配** |
| 宇航员 T35/T44 | GAR-0038 连体工作服 + GAR-0037 防护外套 + GAR-0039 安全头盔 | **匹配** |
| 婚礼 T27/T36 | GAR-0005 布布长袍 + GAR-0070 头巾 + GAR-0048 手袋 | **匹配** |
- T42–T45 的 `occupation_match` / `no_occupation_mismatch` / `no_cultural_mispick` 全部 PASS；warnings 仅 context/region/天气/风格缺口，无「有职业卡却称无卡」矛盾。

## 4. R2 查询 example/去重独立验证

- P14「--style-tag noir」→ **3 条**：LOOK-0007、LOOK-0021、STY-0005，**无 example 卡**（P3.1 时 example 在第 4/5 名）。
- P02「和服」→ GAR-0001、GAR-0066（obi）、SRC-0009、SRC-0028、SRC-0049，**无 GAR-0065 重复**；T41 `query_no_duplicate_names`/`query_no_example_top` PASS。
- 数据层仍有 GAR-0001/GAR-0065 两张「和服」卡（W3）。

## 5. 回归与结构

- F1：4/4 exit 0、3 looks；F2：1580s 3 looks（doublet/codpiece/意大利长袍）、Byzantine 1 look + 「no invented replacements」；F3：I1–I6 全部 exit 0 且 warnings 3–8。
- `validate.py` exit 0；`build_sources --check` exit 0（CSV 174 行一致）；`run_acceptance` exit 0，**45/45 PASS**，query 命中 187。
- 15 案例 rubric（7 PASS/8 WARN/0 FAIL）明细见 `reports/P3-QA.md` 历史表（本轮逐例复核：C02/C07/C08/C09/N1/N2/N3 PASS；C01/C03/C04/C05/C06/C10/N4/N5 WARN）。

## 6. 残余风险与 HUMAN_UAT_PENDING

**WARN（5 项）**：W1 R7 raw 3.92<4.0（调整后 4.26）；W2 单探针相关性缺口；W3 数据层和服重复卡；W4 噪声 warning 措辞；W5 CSV 同步流程未自动化。
**HUMAN_UAT_PENDING（4 项，不得写成 PASS）**：H1 Obsidian GUI；H2 逐图版权；H3 15 案例语义评分签核；H4 62 张 draft 复核。

## 7. 复现

```bash
python3 scripts/validate.py
python3 scripts/build_sources.py --check
python3 scripts/run_acceptance.py
python3 scripts/quality_eval_audit.py --quick
python3 scripts/quality_eval.py --no-write   # engineer 自评对照
```
- 原始证据：`/tmp/p32_query.json`、`/tmp/p32cases/`、`/tmp/p32_acc.log`、`11-验收/测试结果/raw/T31–T45.json`。
- 版本：v1.3（2026-11-04，verifier/task-19，P3.2 最终复验）。
