# P3 缺陷登记（DEFECTS）

- 更新时间：2026-11-04 02:42（Asia/Shanghai）
- 快照：328 卡；git HEAD `0345f05`；验证方式见 `reports/P3-QA.md`
- 状态图例：**FIXED** / **PARTIAL** / **OPEN** / **RESOLVED-BY-QA**（QA 交付时修复的报表问题）
- 严重度：S1 阻断（错误/崩溃/虚假证据声明）、S2 严重（切题/约束错误）、S3 一般（标签/文档/一致性）、S4 轻微

## 1. P2.5 FAIL 回归项

| ID | 严重度 | 缺陷 | P2.5 状态 | P3 状态 | 证据 |
|---|---|---|---|---|---|
| F1 | S1 | historical 1940s–70s `KeyError: 'evidence'` 崩溃 | FAIL | **FIXED** | 4/4 输出现 exit 0、3 looks（P3-QA §2） |
| F2 | S1 | period/region 未归一化 → 假阴性「no wardrobe candidates」 | FAIL | **FIXED** | 1580s（T23/C08）与拜占庭（T24）exit 0 + 近似/缺口声明；无假声明 |
| F3 | S2 | 未覆盖请求静默套用无关单品（warnings=[]） | FAIL | **FIXED（诚实性）** | 6/6 探针均有 3–8 warnings；但**替代单品质量仍差**（见 D2） |

## 2. P2.5 错标 M1–M8

| ID | 严重度 | 缺陷 | 状态 | 证据/说明 |
|---|---|---|---|---|
| M1 | S3 | GAR-0010 `## 来源链接` 称「用于运动与童装」，FIT bloomers 页 0 次 sport/children | **OPEN** | 卡片原文未改；应改 interpretive 或删从属断言 |
| M2 | S3 | SRC-0046/SRC-0047 `license_status: not_applicable`，rights=Public domain | **OPEN** | 应为 cc0/public domain |
| M3 | S1 | 假阴性「no wardrobe candidates」措辞 | **FIXED** | 1580s/拜占庭改为近似/缺口声明 |
| M4 | S2 | C01 context 引用 1770s 英法/维多利亚丧服（请求 1644 明末清初） | **OPEN** | context 仍 STY-EXAMPLE-001/STY-0002/PRD-0001/SCN-0004 |
| M5 | S2 | example 卡进 A 套且无标记 | **FIXED** | 30/30 T + 15 案例 A 套 example=0 |
| M6 | S2 | GAR-0019 派克大衣被用作室内/雨景外层 | **OPEN** | T10 look2/3、T13 look2/3；T10 prompt 含 Arctic anorak |
| M7 | S2 | prompt 串文（「worn in snow」等） | **PARTIAL** | T13 室内走廊仍 2 处；T14 雪景合理；neon 为输入光照 |
| M8 | S3 | query example 卡排序靠前 / GAR-0031 掉出 1930s 上海 top5 / 和服重复卡 | **PARTIAL** | 徽章、风衣/雨衣检索已修复；P14 仍 example 第 1/4，P07 仍无 GAR-0031，GAR-0001/GAR-0065 同名和服 |

## 3. P3 新发现缺陷

| ID | 严重度 | 缺陷 | 状态 | 证据 |
|---|---|---|---|---|
| D1 | S3 | `reports/SOURCES.csv` 未同步 P3 新来源（142 行 vs 174 来源卡，缺 32 行） | **RESOLVED-BY-QA** | QA `build_sources --write` 重建 174 行；`--check` PASS。需把重建纳入发布步骤防复发 |
| D2 | **S2（P3 主缺陷）** | **职业服万能填充**：当代/职业请求 A 套普遍为 警察制服 + 医生白袍 + 医疗工作鞋，且 warning 声称「no occupational garment cards match X」，与库内已有 护士制服 GAR-0036/医生白袍 GAR-0041/厨师服 GAR-0043 矛盾 | **OPEN** | T04 舞者、T15 建筑师、T18 小学教师、T26/C02/N1 急诊护士、T05/C03/N2 太空、C07/T27 婚礼均如此；切题维度均值 0.53/2（P3-QA §3.2） |
| D3 | S3 | 重复内容卡：GAR-0001 与 GAR-0065 均为「和服 kimono / specialised traditional_regional」，仅来源不同 | **OPEN** | 应对齐或合并/canonical 标注；query P02 同时返回两卡 |
| D4 | **S1** | **虚假 warning**：「outerwear GAR-0037 has no documented weather protection; rainwear cards are missing」——但库内已有 GAR-0045 风衣、GAR-0046 雨衣（tags 含 rain） | **OPEN** | T01/T02（1930s 上海雨）；应改为「雨具卡年代/地域不匹配」准确措辞 |
| D5 | S4 | 噪声 warning：「no upper_body candidates retrieved / no lower_body candidates retrieved」在 one_piece/set 场景反复出现，易误读 | **OPEN** | T03/T04/T05/T06/T12/T15/T18/T24/T26/T27 等 |
| D6 | S3 | `11-验收/质量评估/` 自评 OVERALL PASS 与其指标未覆盖的 S1/S2 缺陷不一致（relevant@5 3.84 vs 独立复算 3.64；F1/F2 语义 FAIL 不计入其指标） | **OPEN（流程）** | P3-QA §3.1/§5；建议自评不得单独作为验收依据 |

## 4. 已确认修复（保留记录）

- F1 崩溃、F2 假阴性、F3 静默（诚实性）、M3、M5：见 §1/§2。
- 新增能力（非缺陷）：period/region 归一化与近似声明、warnings 覆盖（30/30）、A/B/C 差异度量（27/27 全 ≥2 件）、冲突检测（C10/T29/N5：历史 vs 科幻拆分建议）、身份弧线未建模声明（C05/N4/T03）、跨文化婚礼仪式询问（C07/T27）、未来基底缺口声明（C03/T25/N2）。

## 5. 统计与优先级

- **OPEN 缺陷：M1、M2、M4、M6、D2、D3、D4、D5、D6 = 9 项**；**PARTIAL：M7、M8 = 2 项**；FIXED 5 项（F1/F2/F3/M3/M5）；RESOLVED-BY-QA 1 项（D1）。
- **S1 阻断：D4（虚假证据声明）**；**S2 严重：D2（职业填充）、M4、M6、M7、M8 部分**。
- 建议排期：D4 → D2 → M4/M6/M7 → M1/M2/D3/D5/D6。
