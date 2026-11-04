# QA 报告（P3.3 最终复验索引）

- 更新时间：2026-11-04 03:26；快照 **343 卡 / 185 来源 / 45 例验收**；git HEAD `fcebf79`
- 详细独立验收：[P3-QA.md](P3-QA.md)；缺陷：[P3-DEFECTS.md](P3-DEFECTS.md)；历史：[P2.5-ACCEPTANCE.md](P2.5-ACCEPTANCE.md)

## 1. 机械验收（PASS）

| 项 | 命令 | 退出码 | 结果 |
|---|---|---|---|
| 结构校验 | `python3 scripts/validate.py` | 0 | 343/343；17/17 PASS；0 错误 0 警告 |
| 来源对账 | `python3 scripts/build_sources.py --check` | 0 | 185/185 一致（CSV 186 行含表头） |
| 验收 | `python3 scripts/run_acceptance.py` | 0 | **PASS 45/45** |
| 质量评估 | `python3 scripts/quality_eval.py --no-write` | 0 | **OVERALL PASS**：relevant@5 4.16、precision .945、0 命中 0、CSV gate PASS |

## 2. 独立质量结论（P3.3）：PASS 24 / WARN 4 / FAIL 0 / HUMAN_UAT_PENDING 4

- **R7 关闭**：独立 raw relevant@5 **4.16（104/125）≥4.0**；precision **94.5%**；0 命中 **0%**；P21 Mughal 3 命中（GAR-0071/SRC-0450/GAR-0072）、P22 mourning jewelry 2 命中（GAR-0073/GAR-0074）均相关；与 engineer 自评一致。
- **R1/R2/R3/R4/R5 全部关闭**：六类职业含同义词匹配；P14 无 example、P02/T41 无同名重复；GAR-0065 改名「出口和服」；噪声 warning 移除；R5 质量门经「漂移→FAIL→恢复→PASS」实测有效。
- **D2/D4/M1–M7/F1–F3** 保持关闭；45/45、validate、build 全 PASS。
- **15 案例 rubric**：7 PASS / 8 WARN / 0 FAIL（切题均值 1.33/2）。
- **WARN 4**：W1 rubric 覆盖限制、W2 C01 跨文化近似、W3 filtered 结果数有限、W4 证据覆盖 0.94。

## 3. 结论

**技术/数据/质量门 PASS**（R7 关闭、R1–R5 关闭、45/45 验收、validate/build/quality_eval 全 PASS）。发布仍需完成 **HUMAN_UAT_PENDING 4 项**（Obsidian GUI、逐图版权、语义评分签核、62 draft 复核）；完成前不得对外宣布「全量 PASS」。


---

## 4. P3.6 Skill 原生调用验收（2026-11-04 15:56，task-37）

- 快照：363 卡（内容 166 + 来源 197）；45 例验收；9 workflow tests；HEAD `7afe02b`。
- **机械验收**：validate **PASS**（363/363，17/17）；build_sources **PASS**（197/197，CSV 198 行）；acceptance **PASS 45/45**；quality_eval **OVERALL PASS（17/17）**；workflow tests **9/9 OK**。
- **Skill 原生调用**：独立 2 次 Vault-cwd headless 请求 exit 0，事件含 `skill(costume-director)` + `<skill_content>` + bash `scripts/query.py`；答案 ID/SRC 全解析、0 编造。
- **10 例 e2e**：10/10 通过（skill+脚本调用、ID/SRC 0 缺失、无 stderr/错误；T07 同会话、T08 缺口诚实、T09 冲突拒绝、T10 连续性与 prompts）。
- **安全**：commit 纯新增（无既有卡/脚本修改）；projects 隔离；未推送（ahead 22）；无许可改动；注入策略有文档但未运行时验证。
- **导演材料**：18/18 审阅完整；评分表 18×7 NOT_SCORED（无数字分）；OBSIDIAN-UAT 为 HUMAN_UAT_PENDING/NOT_TESTED。
- **结论**：**PRIVATE-USE VERIFIED = YES；PUBLIC-READY = NO（BLOCKED，B1–B6）**；HUMAN_UAT_PENDING 4 项未变；兼容性 caveat（DeepSeek 402 / Doubao overlay）已披露。
- 详见 `reports/P3.6-REPORT.md`。


---

## 5. P4 最终验收（2026-11-04 16:26，task-45）

- 快照：399 卡（内容 188 + 来源 211）；45 acceptance；9 workflow；9 composer；11 Macbeth；HEAD `7f7a21b`。
- **机械门禁**：validate **PASS** 399/399（0 错误 0 警告）；build_sources **PASS** 211/211（CSV 212 行）；acceptance **PASS 45/45**；quality_eval **OVERALL PASS（17/17）**。
- **P4 专项**：许可审计 20 源分流（PASS 15/WARN 2/RESTRICTED 3，无 verified 误标）；9 本 PD 书/31 结论（15 verified，3/3 抽检原文行一致，页码 UNCONFIRMED）；结构 v1.2（42 可选字段、22 新卡、旧卡 0 破坏）；composer 9/9 + 独立 3 例（0 缺失 ID/0 未解析 SRC/A-B-C 差异/连续性）；视觉 28/28 CC0、27 关联、0 下载；Macbeth 11/11 + P3.5 基线对比（looks/avg_items/abc_diff/unique_src 提升）。
- **回归指标**：relevant@5 4.16 持平、0-hit 0 持平、recommend 指标全持平；**precision 94.5%→92.9%（−1.6pp，仍 ≥0.8）** → WARN 观察，非阻断。
- **门禁**：PRIVATE-READY/PRIVATE-USE = YES（不变）；PUBLIC-READY = NO（BLOCKED B1–B6 + L1–L6）；HUMAN_UAT_PENDING 4 项未执行、未代填。
- 详见 `reports/P4-REPORT.md`。
