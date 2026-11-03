# P3 缺陷登记（DEFECTS）— P3.3 最终复验后

- 更新时间：2026-11-04 03:24（Asia/Shanghai）；P3.3 最终复验（task-22）
- 快照：343 卡（内容 158 + 来源 185）；git HEAD `fcebf79`；45 例验收
- 状态：**FAIL 0 / WARN 4（残余）/ FIXED 16 / RESOLVED-BY-QA 2**
- 发布门槛：**技术/数据/质量门 PASS**；HUMAN_UAT_PENDING 4 项未完成前不得对外宣布「全量 PASS」

## 1. 已关闭的阻断/严重缺陷（FIXED 16）

| ID | 严重度 | 缺陷 | 状态 | 证据 |
|---|---|---|---|---|
| F1 | S1 | historical 1940s–70s 崩溃 | FIXED | 4/4 exit 0、3 looks |
| F2 | S1 | period/region 假阴性 | FIXED | 1580s 3 looks；Byzantine 1 look + 诚实声明 |
| F3 | S2 | 未覆盖请求静默 | FIXED | 6/6 探针 warnings 3–8 |
| D2 | S2 | 职业服万能填充/矛盾 warning | FIXED | 六类职业 A 套匹配；同义词 T42–T45 PASS |
| D4 | S1 | 虚假 rainwear warning | FIXED | T01/T02 用 GAR-0045；T37/T38 `warning_absent:rainwear_gap` PASS |
| M1 | S3 | GAR-0010 断言扩写 | FIXED | 改述 + interpretive |
| M2 | S3 | SRC-0046/47 许可错标 | FIXED | cc0 + note 映射 |
| M3 | S1 | 假阴性措辞 | FIXED | 近似/缺口声明 |
| M4 | S2 | C01 context 误导 | FIXED | context_refs={}；T39 PASS |
| M5 | S2 | example 卡进 A | FIXED | 45/45 + 15 案例 example=0 |
| M6 | S2 | GAR-0019 室内/雨景 | FIXED | T13/T38 无；T38 `no_arctic_indoor` PASS |
| M7 | S2 | prompt 串文 | FIXED | T13/T38 无「worn in snow」 |
| **R1** | S2 | 职业同义词/医疗内层误配 | **CLOSED** | 巡警/民警→GAR-0042（T42/T45）、医师→白袍 GAR-0041（T43，无韩服）、宇航员→GAR-0038/0039（T44） |
| **R2** | S3 | query example 排序/和服重复 | **CLOSED** | P14 无 example；P02/T41 无同名重复 |
| **R3** | S3 | 和服同名（数据层） | **CLOSED** | GAR-0065 `name_zh: 出口和服` / `name_en: export kimono`（文件名保留兼容）；P02/T41 通过 |
| **R4** | S4 | warning 噪声「no upper/lower candidates」 | **CLOSED** | 文案已移除；T27/T31–T36/T42–T45 warnings 扫描 0 命中 |

## 2. R7（上一轮唯一 FAIL）— 已关闭

| 指标 | P3.2 | **P3.3（独立）** | 门槛 | 状态 |
|---|---|---|---|---|
| raw relevant@5 | 3.92（98/125） | **4.16（104/125）** | ≥4.0 | **CLOSED（PASS）** |
| precision | 93.3% | **94.5%（104/110）** | ≥0.8/0.9 | PASS |
| 0 命中率 | 8%（2/25） | **0%（0/25）** | ≤20% | PASS |
| P21 Mughal | 0 命中 | **3 命中**（GAR-0071/SRC-0450/GAR-0072，均相关） | ≥1 | PASS |
| P22 mourning jewelry | 0 命中 | **2 命中**（GAR-0073/GAR-0074，均相关） | ≥1 | PASS |

- 与 engineer 自评（4.16/0.945/0.0）**一致**；本轮为独立复算，非采信自评。
- 提升来源：P3.3 新增 GAR-0071 莫卧儿 jama、GAR-0072 帕贾马裤、GAR-0073 维多利亚哀悼珠宝、GAR-0074 哀悼戒指与胸针 + SRC-0450..0460（11 张 V&A 来源，11/11 HTTP 200）。

## 3. R5 CSV 同步质量门 — 实测有效

- 实现：`scripts/quality_eval.py::check_sources_csv()` 调用 `build_sources.py --check`，阈值 `sources_csv_sync=1.0`，纳入 OVERALL。
- 实测：注入 1 行 CSV 漂移（SRC-0001 note 追加 `[QA-DRIFT]`）→ build_sources --check **exit 1 / RESULT: FAIL**；`check_sources_csv()` 返回 `(1, FAIL…)` → 质量门判 FAIL；恢复备份后返回 `(0, PASS)`、build exit 0、CSV 186 行。**质量门真实有效（CLOSED）**。

## 4. 残余风险（WARN 4 项，非阻断）

| ID | 严重度 | 问题 | 说明/建议 |
|---|---|---|---|
| W1 | S3 | 15 案例中 8 例 rubric WARN（切题 0–1）：明制、未来基底、身份弧线 wardrobe-stage、跨文化仪式礼服 | KB 覆盖限制，已诚实声明；P4 补卡或 rubric 分层处理 |
| W2 | S3 | C01 明末清初 A 套选莫卧儿 jama GAR-0071（跨文化近似） | 有 region/period warnings；建议为明/清补卡或提高 region 硬约束 |
| W3 | S4 | P14/P24/P25 等 filtered 查询仅 3–4 条 | example 已排除、库内条目少；非排序错误 |
| W4 | S4 | 证据覆盖 0.94 | example/设计推断件无来源属预期；验收阈值 0.65 已 PASS |

## 5. 统计与发布门槛

- **FAIL 0；FIXED 16；CLOSED R7/R1/R2/R3/R4/R5；WARN 4；HUMAN_UAT_PENDING 4。**
- **发布门槛：PASS（技术/数据/质量门）**——validate、build_sources、45/45 acceptance、quality_eval OVERALL PASS（relevant@5 4.16、precision 0.945、0-hit 0、CSV gate PASS）全通过。
- **发布条件**：HUMAN_UAT_PENDING 4 项（Obsidian GUI、逐图版权、语义评分签核、62 draft 复核）必须完成并留档；W1–W4 建议列入 P4 改进但不阻断。
