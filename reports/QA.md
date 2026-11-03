# QA 报告（P3.2 最终复验索引）

- 更新时间：2026-11-04 03:14；快照 **328 卡 / 45 例验收**；git HEAD `281e3b1`
- 详细独立验收：[P3-QA.md](P3-QA.md)；缺陷：[P3-DEFECTS.md](P3-DEFECTS.md)；历史：[P2.5-ACCEPTANCE.md](P2.5-ACCEPTANCE.md)

## 1. 机械验收（PASS）

| 项 | 命令 | 退出码 | 结果 |
|---|---|---|---|
| 结构校验 | `python3 scripts/validate.py` | 0 | 328/328；17/17 PASS；0 错误 0 警告 |
| 来源对账 | `python3 scripts/build_sources.py --check` | 0 | 174/174 一致（P3.2 CSV 已同步） |
| 验收 | `python3 scripts/run_acceptance.py` | 0 | **PASS 45/45**；query 命中 187、逐例 ≥1 |

## 2. 独立质量结论（P3.2）：PASS 19 / WARN 5 / FAIL 0 / HUMAN_UAT_PENDING 4

- **D2/D4/R1 全部关闭**：六类职业（护士/医生/警察/厨师/宇航员/婚礼）A 套匹配；同义词 T42–T45（巡警/民警/医师/宇航员）`occupation_match` 与 `no_cultural_mispick` PASS；雨具选择与 truthful warnings PASS；M1/M2/M4/M6/M7 关闭。
- **R2 查询层关闭**：P14「noir」返回 3 条且无 example；P02/T41 无同名和服重复。
- **R7（唯一条件项）**：独立 raw relevant@5 **3.92（98/125）<4.0**；剔除 P21 Mughal/P22 mourning jewelry 已知真实缺卡后 **4.26 ≥4.0**；precision **93.3%**、0 命中 **8%**；engineer 自评 4.0/95.2%/8%。
- **15 案例 rubric**：PASS 7 / WARN 8 / FAIL 0（P3.1：6/9/0）。
- **WARN 5**：R7 条件性、R8 单探针相关性、R3 数据层和服重复、R4 噪声 warning、R5 CSV 同步流程。

## 3. 结论

功能/结构/诚实性/回归全部 PASS，D2/D4/R1/R2 关闭；**发布门槛为 CONDITIONAL PASS**，唯一条件项 R7（raw 3.92 vs 调整 4.26）。若 lead 接受「已知 KB 缺口不计入门槛」，可进入发布；否则需再提升 P09/P10/P20 或补缺卡后复验。HUMAN_UAT_PENDING 4 项未完成前不得对外宣布全量 PASS。
