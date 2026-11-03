# P3 缺陷登记（DEFECTS）— P3.2 最终复验后

- 更新时间：2026-11-04 03:12（Asia/Shanghai）；P3.2 最终复验（task-19）
- 快照：328 卡（内容 154 + 来源 174）；git HEAD `281e3b1`；45 例验收
- 状态：**FAIL 0；WARN 5（残余）；FIXED 12 项；RESOLVED-BY-QA 2 次**
- 发布门槛：**条件性通过（CONDITIONAL PASS）**——全部阻断缺陷关闭；R7 raw 指标差 0.08，调整后达标（见 §3）

## 1. P3/P3.1 阻断缺陷（全部关闭）

| ID | 严重度 | 缺陷 | 状态 | 证据 |
|---|---|---|---|---|
| F1 | S1 | historical 1940s–70s `KeyError: 'evidence'` 崩溃 | **FIXED** | 4/4 exit 0、3 looks |
| F2 | S1 | period/region 假阴性「无覆盖」 | **FIXED** | 1580s 3 looks；Byzantine 1 look + 诚实声明 |
| F3 | S2 | 未覆盖请求静默套用 | **FIXED** | 6/6 探针 3–8 warnings |
| D2 | S2 | 职业服万能填充/自相矛盾 warning | **FIXED（含同义词）** | 护士/医生/警察/厨师/宇航员/婚礼六类 A 套匹配；巡警/民警/医师/宇航员同义词 T42–T45 PASS；医生无韩服；`occupation_match`/`no_occupation_mismatch`/`no_cultural_mispick` 全 PASS |
| D4 | S1 | 虚假「rainwear cards are missing」 | **FIXED** | T01/T02 用 GAR-0045；T37/T38 `warning_absent:rainwear_gap` PASS |
| M1 | S3 | GAR-0010「运动与童装」扩写 | **FIXED** | 改述 + interpretive |
| M2 | S3 | SRC-0046/47 许可错标 | **FIXED** | cc0 + note 映射说明 |
| M3 | S1 | 假阴性措辞 | **FIXED** | 保持 |
| M4 | S2 | C01 context 误导引用 | **FIXED** | context_refs={}；T39 `context_refs_clean` PASS |
| M5 | S2 | example 卡进 A 套 | **FIXED** | 45/45 + 15 案例 A 套 example=0 |
| M6 | S2 | GAR-0019 室内/雨景外层 | **FIXED** | T13/T38 无；T38 `no_arctic_indoor` PASS |
| M7 | S2 | prompt「worn in snow」串文 | **FIXED** | T13/T38 扫描 0；45 例 `no_prompt_contamination` PASS |

## 2. R1/R2 状态（P3.2）

| ID | 缺陷 | 状态 | 证据 |
|---|---|---|---|
| R1 | 职业同义词/医疗内层误配 | **FIXED** | 巡警/民警→GAR-0042（T42/T45）；医师→白袍 GAR-0041（T43，无韩服）；宇航员→GAR-0038/0039（T44）；六类职业 A 套全部匹配 |
| R2 | query example 排序 / 和服重复 | **FIXED（查询层）/ WARN（数据层）** | P14 返回 3 条全非 example；P02/T41 无同名重复；但 GAR-0001/GAR-0065 两张和服卡仍在库（W3） |

## 3. 残余风险（WARN 5 项；R7 为条件性）

| ID | 严重度 | 问题 | 证据/建议 |
|---|---|---|---|
| R7（WARN，条件性） | 发布门槛 | **query relevant@5 独立 raw=3.92（98/125）< 4.0 差 0.08**；剔除已确认真实缺卡探针（P21 Mughal、P22 mourning jewelry）后=4.26 ≥4.0；precision 93.3%、0 命中 8% 均达标；engineer 自评 4.0/95.2%/8% | 是否放行取决于 lead 对「已知 KB 缺口是否从门槛分母剔除」的决定；若要求 raw ≥4.0，需提升 P09（3/5）/P10（4/5）/P20（4/5）相关性或补 Mughal/哀悼珠宝卡 |
| R8 | S3 | 单探针相关性缺口：P09/P10/P20 部分相关；P14/P24/P25 返回数仅 3–4 条 | 见 P3-QA §2 逐探针表 |
| R3 | S3 | 数据层和服重复卡（GAR-0001/GAR-0065） | 建议 canonical 标注或合并 |
| R4 | S4 | 噪声 warning「no upper_body/lower_body candidates」在 one_piece/set 场景重复 | 措辞改为「由 one_piece/set 覆盖」 |
| R5 | S3 | SOURCES.csv 同步无自动化（历次两次漂移 D1） | 将 `build_sources --write/--check` 纳入发布步骤 |

> 无 OPEN 的 S1/S2 阻断缺陷；本轮 P3.2 commit 中 `SOURCES.csv` 已随 SRC-0046/47 更新同步（build --check PASS），D1 未复发。

## 4. 统计与优先级

- **FIXED：12 项**（F1、F2、F3、D2、D4、M1–M7）；**RESOLVED-BY-QA：2 次**（D1 CSV 漂移）。
- **WARN：5 项**（R7 条件性、R8、R3、R4、R5）。
- 优先级：R7（lead 决定放行/继续改进）> R8 > R3 > R4/R5。
- **发布门槛**：功能/结构/诚实性/回归全部 PASS；R7 为唯一条件项（raw 3.92 vs 调整 4.26）；HUMAN_UAT_PENDING 4 项未完成前不得对外宣布全量 PASS。
