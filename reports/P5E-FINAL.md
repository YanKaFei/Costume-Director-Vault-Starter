# P5-E 最终验收结论（P5E-FINAL）

- 定稿：2026-11-05 11:45（Asia/Shanghai）；verifier / task-92；快照：**HEAD `0e8d37d` + P5-E 工作区**（未提交；**458 卡 = 224 内容 + 234 来源；334 relations**）
- 依赖：`P5E-BASELINE`、`P5E-RELATION-ELIGIBILITY`、`P5E-SOURCE-RESEARCH`、`P5E-CANDIDATE-REVIEW`、`P5E-KNOWLEDGE-EXPANSION`、`P5E-AGENT-REGRESSION`、`P5E-GRAPH-COMPARISON`、`P5E-HUMAN-UAT`
- 声明：未改卡片/脚本；GUI 未执行，不得声称通过。

## 0. 结论摘要（PASS，附 WARN）

**P5-E 旧卡知识深化 + 定向关系通过最终验收：**
- **28 张旧卡深化**（20 material + 6 component + 2 style 解释）；**新增 26 条 typed relations**（20 uses_material + 6 may_have_part；全部 **medium/interpretive/review**）；**0 新增 high、0 新增卡、0 自动提升**；全部 target 真实/正文可见/主语类型合法。
- **独立抽样 30 条 = 100%（≥95%）**：26 条新增 + 4 条既有 high claim 逐条核对 target/结构化/可见/schema/subject/证据/置信。
- **覆盖率（E1 适用性分母）**：present **474/775 = 61.2%**；APPLICABLE **380**、REVIEW_REQUIRED **94**、INSUFFICIENT **301**、NOT_APPLICABLE **1017**；garment→material **39→53/92（42.4%→57.6%）**，garment_part→material **7→10/35（28.6%）**；component/style/outfit/narrative/claim 持平（component 17.4%、style 3.3%、outfit 59.8%、narrative 71.4%、claim 96.9%）。
- **来源可见率（单列）**：**370/478（77.4%）**，可见来源 **172/172**；P5-E 未改 source_ids，未变。
- **图谱对比**：P5-A 前 416 节点/66 分量/58 来源零可见/source_ids 299→可见 2 → 当前 **489 节点/60 分量/59 单点/370/478（77.4%）**；最大分量 335→399；typed 无可见 313→123。
- **回归**：validate 458/458、build 234、consistency **0 errors / 334**、acceptance **45/45**、composer **9/9**、workflow **9/9**、Macbeth **11/11**、relation_trace **6/6**、单元测试 **56/56**、candidate-review **5/5**；**quality_eval = PASS**（lead 复跑：relevant@5 4.16、precision 0.92、0-hit 0，`/tmp/p5e_quality.log`）。
- **Agent E2E**：official **3/3**、overlay **3/3**，五项全 true。
- **239 候选**：source_verifiable **39** / needs_human **163** / reject_or_rework **37**；0 写入/0 提升。
- **59 isolates / 38 draft / 6 flags**：保持；无自动提升。
- **门禁**：PRIVATE-READY/PRIVATE-USE = **YES（附 WARN：59 isolates/38 draft/6 flags、页码 UNCONFIRMED、GUI NOT_RUN）**；PUBLIC-READY = **NO（B1–B6 + L1–L6）**；**GUI = NOT_RUN/PENDING**。

## 1. 补足缺口（问题 1）

| 项 | 结果 |
|---|---|
| 深化旧卡 | **28 张**：20 材料/工艺（GAR-0077/0078/0057/0076/0022/0023/0024/0058/0060/0081/0084/0036/0061/0075/0066/0067/0080 + STR-0003/0005/0006）+ 6 部件/结构（GAR-0001/0002/0003/0008/0009/0012）+ 2 风格解释（STY-0001/0003，仅解释） |
| 新增关系 | **26 条**：uses_material 20（medium/interpretive/review）、may_have_part 6（medium/interpretive/review） |
| 新增卡/高置信 | **0 / 0**；未改 ID/evidence_status/review_status/source_ids |
| 覆盖 | garment→material **39→53/92**；part→material **7→10/35**；component 16/92 持平（6 条 may_have_part 原已被可见链接计入，现为 typed review） |
| 改动性质 | 28 卡正文**新增 51 行、删除 0 行**（additive），全部 target 出现在正文 Wikilink |

## 2. 新增可靠关系与抽样（问题 2）

- 26 条全部：target 真实、结构化依据（materials token / 正文 STR 链接）、正文可见、schema 允许、subject 类型合法（garment/part）、medium/interpretive。
- **独立抽样 30/30 = 100%**（26 新增 + 4 既有 high claim）；新增 **0 条 high**，不冒充强证据。
- 未发现 keyword/相似度硬连；未将 may_have_part 写成 has_part；style 仅解释。

## 3. 仍缺证据（问题 3）

- E1：**INSUFFICIENT_EVIDENCE 301/775（38.8%）**；fix 候选 **291**（177 actionable；其中材料候选 38）；**39 source_verifiable / 163 needs_human / 37 reject_or_rework**。
- 缺口：component 76/92 不足、material 39/92、style 89/92、accessory 25/56、outfit 37/92、narrative 10/35、claim 7/224；**silhouette 18/92 unknown**。
- 书籍：4 本背景书（0063/0065/0067/0068）未接卡；page **UNCONFIRMED**；E2 44 条可定位事实中仍有 6 类证据缺口（含 A/H/Y/T/X 廓形无审计来源）。
- 6 部分支撑候选、239 队列、59 isolates、38 draft、6 flags 均保留。

## 4. 覆盖实际变化（问题 4；E1 适用性分母）

| 维度（分母=适用） | E1 前（308） | **P5-E 后（334）** | 状态（后） |
|---|---:|---:|---|
| garment→component | 16/92（17.4%） | **16/92（17.4%）** | REVIEW 16 / INSUFF 76 |
| garment→material | 39/92（42.4%） | **53/92（57.6%）** | APP 9 / REVIEW 44 / INSUFF 39 |
| garment→silhouette（字段） | 74/92（80.4%） | **74/92（80.4%）** | APP 74 / INSUFF 18 |
| garment→style | 3/92（3.3%） | **3/92（3.3%）** | REVIEW 3 / INSUFF 89 |
| garment→footwear-accessory | 31/56（55.4%） | **31/56（55.4%）** | REVIEW 31 / INSUFF 25 |
| garment→outfit | 55/92（59.8%） | **55/92（59.8%）** | APP 55 / INSUFF 37 |
| LOOK→narrative | 25/35（71.4%） | **25/35（71.4%）** | APP 25 / INSUFF 10 |
| claim→source | 217/224（96.9%） | **217/224（96.9%）** | APP 217 / INSUFF 7 |
| **合计（8 维）** | **460/775（59.4%）** | **474/775（61.2%）** | APP 380 / REVIEW 94 / INSUFF 301 / N/A 1017 |
| garment_part→material（单列） | 7/35（20.0%） | **10/35（28.6%）** | +3 |

- 来源可见（单列）：**478 对 / 370 可见（77.4%）**，可见来源 172/172；P5-E 未改 source_ids。
- 结论：P5-E 的实际增量集中在 **material（+14 卡）**与 **part→material（+3）**；关系数 +26 但**高置信关系未增加**，不夸大历史事实。

## 5. GUI 是否验收（问题 5）

- **NOT_RUN / PENDING**：无 Obsidian GUI 运行、无截图、无签字；`P5E-HUMAN-UAT.md` 列 11 项（Vault 入口、MOC、Properties、Backlinks、Local Graph、关系可见性、孤立节点、搜索、坏链、性能、截图签字），**11/11 NOT_RUN**。
- 自动化预检通过不能替代 GUI；B1 保持 NOT_EXECUTED。

## 6. Agent 是否改善（问题 6）

- E2E：official **3/3**、overlay **3/3**；五项（skill/工具/结果/turn_end.completed/完整输出）全 true；官方/overlay 分开统计（`11-验收/P5E/e2e/validation-summary.json`）。
- relation_trace **6/6**；26 条新 review 关系正文可见，Agent 可检索并可区分 design/review；**无自动提升**；quality_eval 复跑 **PASS**（relevant@5 4.16、precision 0.92、0-hit 0）。
- 限制：document 的 approved anchors 模板为空，未虚构；design-only 过滤仍依赖 relation_trace/query 规则。

## 7. 新增风险（问题 7）

1. **26 条 medium/review 关系**：不是历史事实，不可当 high/verified；须人工复核或保留 review。
2. quality_eval 复跑 **PASS**（4.16/0.92/0；日志 `/tmp/p5e_quality.log`）。
3. **E1 eligibility.csv 为 E3 前快照**（308）；P5-E 后 334 未重新生成（本报告用“更新后”逻辑近似；如需正式档案应重跑 E1）。
4. 62 uncited（59 isolates + 3 未分类）、38 基线 draft、6 flags 未变；无自动提升。
5. 书籍 page UNCONFIRMED、4 本背景书未接入；版权：来源仅链接/ODC-BY、无新图片、无新增未审计 URL。
6. P5-E 工作区未提交；GUI 未验收；PUBLIC 门禁未解除。

## 8. 回归与证据

| 套件 | 结果 |
|---|---|
| validate 458 / build 234 / consistency 0 | **PASS**（独立 + E6 log） |
| acceptance | **PASS 45/45**（E6 log） |
| quality_eval | **PASS**（lead 复跑：4.16/0.92/0） |
| composer | **PASS 9/9**（E6 log） |
| workflow | **PASS 9/9**（E6 log） |
| Macbeth | **PASS 11/11**（E6 log） |
| relation_trace | **PASS 6/6**（本轮独立；E6 56/56 单元测试含其余） |
| security / lookbook / skill-sync / backup | **PASS（本轮独立）**；E6 log 56/56 单元测试 |
| human closeout | E6 log **PASS**（独立复跑本轮被终止 → 独立 NOT_RUN） |
| validate_outfits | **PASS 12/12 + 23 legacy**（本轮独立测试 EXIT 0） |
| candidate review | **PASS 5/5**（E6 log） |
| E2E | official **3/3**、overlay **3/3**，五项全 true |
| GUI | **NOT_RUN** |

## 9. 门禁

- **PRIVATE-READY / PRIVATE-USE = YES（附 WARN：59 isolates/38 draft/6 flags、页码 UNCONFIRMED、GUI NOT_RUN）**
- **PUBLIC-READY = NO（BLOCKED）**：B1 GUI NOT_EXECUTED、B2 逐图版权 NOT_RUN、B3 15 案例 NOT_SCORED、B4 62 draft、B5、B6；L1–L6 保持
- **HUMAN UAT = NOT_RUN/PENDING**（无截图/签字）

## 10. 建议

1. 提交 P5-E 工作区（28 卡 + 26 关系 + 报告/工具）。
2. 重跑 quality_eval（稳定环境）并留档；重生成 E1 eligibility（334 relations）。
3. 人工处理 6 flags、38 draft、59 isolates；按 P5E-HUMAN-UAT 做 GUI 验收（两人签字）。
4. 26 条 medium/review 关系逐条复核（可升级需新证据，不自动提升）。
5. 补充 4 本背景书接入/页码核验（如需），保持 0 图片、链接/ODC-BY 边界。


## 12. E1 表与最终覆盖口径

- `11-验收/P5E/eligibility.csv` 的 `relation_present` 生成于 E3 前（308 relations）；最终覆盖以 E3 后 **334 relations** 重算值（§2）为准；差异为 26 条 E3 new review relations，不改变适用性分母。
