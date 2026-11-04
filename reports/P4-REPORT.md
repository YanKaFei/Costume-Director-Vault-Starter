# P4 最终验收报告（书籍 / 结构 / 组合器 / 视觉 / Macbeth / 许可门禁）

- 生成：2026-11-04 16:24（Asia/Shanghai）；verifier / task-45（P4-6 最终独立验收）
- 快照：**399 卡**（内容 188 + 来源 211）；45 例验收；git HEAD `7f7a21b`（P4 commit）
- **门禁：PRIVATE-READY / PRIVATE-USE = YES（状态不变）；PUBLIC-READY = NO（BLOCKED，B1–B6 + P4 许可阻断）**
- 声明：本报告不采信 worker 自评；所有 PASS 均基于本轮独立复跑/抽检。**未修改卡片/脚本；未代填人工评分**。

## 0. 总览

| 交付域 | 独立结论 | 关键证据 |
|---|---|---|
| P4-0 许可审计 | **PASS（20 源，候选分流）** | 20/20 顶层可达；PASS 15 / WARN 2 / RESTRICTED 3；0 verified 误标（见 §1） |
| P4-1 公版书籍 | **PASS（9 本，31 条结论，15 条交叉验证）** | 9/9 PG 文本 HTTP 200；3/3 抽检定位回原文；页码 UNCONFIRMED；无现代版权文本（见 §2） |
| P4-2 结构 v1.2 | **PASS（42 可选字段，22 新卡，旧卡 0 破坏）** | validate 399/399；git 新增 22 内容卡 + 14 来源卡，旧卡 0 修改（见 §3） |
| P4-3 Outfit Composer | **PASS（9/9 + 独立 3 例）** | 独立跑 3 例：0 缺失 ID、0 未解析 SRC、A/B/C 项差 ≥2、连续性显式（见 §4） |
| P4-4 CC0 视觉索引 | **PASS（28 条，27 关联，0 下载）** | 28/28 `isPublicDomain=true`、图像 URL 200、Vault 内 0 图片（见 §5） |
| P4-5 Macbeth 验证 | **PASS（11/11 + 基线对比）** | 独立跑 11/11 exit 0；P4 指标相对 P3.5 提升；缺口/UNCONFIRMED 保留（见 §6） |
| 全回归 | **PASS（8 套）** | validate/build/45 acceptance/quality_eval(17/17)/9 workflow/9 composer/11 Macbeth；旧指标见 §7 |

## 1. P4-0 许可审计复核（reports/P4-SOURCE-AUDIT.md + LICENSE-MATRIX.csv）

- **20 源**（16 GitHub + 4 Gutenberg），顶层可访问 **20/20**；顶层 INACCESSIBLE 0；嵌入 HF 资源 3 个不可达（许可未核实）。
- 分流：**PASS 15**（Met CC0、Fashionpedia CC BY 4.0 数据、freesewing/pattern MIT、fashion-clip 代码 MIT、ai-costume 数据 CC BY 4.0、GITenberg×5、Gutenberg×4）；**WARN 2**（FashionStylist NC、Garments2Look 数据集许可未核实）；**RESTRICTED 3**（polyvore 数据条款不清、open-pose 图片非商业、DeepFashion2 无许可）。
- **无 verified 误标**：P4 新增来源卡仅来自审计 PASS/明确许可项（9 本 PD 书 + FreeSewing 2 + V&A 3）；受限/未核实来源未建卡（FashionStylist/DeepFashion2/polyvore/open-pose 均未进入 KB）。
- 矩阵逐列核对（20 行 × 14 列）：private/commercial/redistribution 与 decision 一致；本任务未看到许可矩阵被改写。

## 2. P4-1 公版书籍复核

- **9/9 本** PD 书（5 GITenberg + 4 Gutenberg）已解析；文本 HTTP 200；均含 PG 公有领域声明。
- **31 条术语/结构结论**：status 统计 **verified 15 / partial 11 / candidate 5**（15/31=48% 交叉验证，26/31=84% 部分+佐证），与交付声明一致。
- **3 条抽检回原文**（独立重建 body 行号）：
  - PG 76299 body[16668] = `=Waistcoat=—a short, sleeveless body garment worn between the coat and…`（与 glossary 引文一致）；
  - PG 76299 body[15902] = `=Trousers=—bifurcated garments for the lower limbs; called "pants" by…`（一致）；
  - PG 46949 body[3598] = `It is to be understood that the terms "collar" and "cuff" are here only…`（一致）。
- 页码：全部 **UNCONFIRMED**（纯文本无页码；仅有章/段/行定位）——已在 TERMS-GLOSSARY 标明。
- 无现代版权文本：仅使用 PG 公版文本（含 1882 年公版英译），未引用现代注疏/译本；未下载插图。
- 9 张来源卡 SRC-0061..0069 的 `rights_statement` 均写明 PD in USA + PG License；license_status 按 source 卡规则为 `not_applicable`（来源卡豁免）。

## 3. P4-2 结构 v1.2 复核

- `00-系统/数据字典-v1.2-扩展.md`：**42 个可选字段**（脚本统计文档表 42 行）；明确向后兼容：不修改 v1.1 必填/枚举/正文/证据规则，旧卡无需迁移。
- P4 commit 新增卡：**36 文件 = 22 内容卡 + 14 来源卡**
  - 内容卡 22：garment 5（手套/高跟鞋/帽子结构/胸针结构/手袋结构）、garment_part 14（STR-0012..0025）、material 3（MAT-0012..0014）；
  - 来源卡 14：9 本 PD 书（SRC-0061..0069）+ FreeSewing 2（SRC-0520/0521）+ V&A 3（SRC-0522..0524）。
- 新卡 optional 字段使用：22 张覆盖 **36/42** 可选字段（翻领/袖型/肩线/腰线/衣摆/门襟/纽扣/拉链/裁片/接缝/腰头/袖口/松量等；具体见卡片）。
- **旧卡 0 破坏**：`git show --name-status 7f7a21b` 中 01–09 目录**无 M（修改）条目**，仅新增；`validate.py` **PASS：399/399，来源卡 211，0 错误 0 警告**。
- 新卡全部 `evidence_status=verified`，含来源链接与正文证据边界（v1.2 未改变证据规则）。

## 4. P4-3 Outfit Composer 复核

- 官方套件：`python3 11-验收/P4-COMPOSER/test_outfit.py` → **PASS 9/9，exit 0**（独立重跑）。
- **我独立跑 3 例**（`scripts/outfit.py --input … --json`）：
  - `macbeth`：looks=3；items 覆盖 5 槽；A/B/C 两两项差 **2/2/4**；24 个 SRC 全部解析；0 编造 ID；`ids_all_exist/source_ids_resolve/abc_pairwise_ge_2/continuity_states_explicit=true`。
  - `rain_continuity`：looks=3；A/B/C 项差 **2/4/2**；21 SRC 全解析；连续性 states/anchors 显式；0 缺失 ID。
  - `conflict`：looks=1（不足 3 套，composer 以 warnings 明示冲突/缺口，未硬凑 A/B/C）；1 个真实 ID + 5 SRC 全解析；**未编造**。
- 结论：A/B/C 结构差异、槽位覆盖、连续性、证据可追溯均通过独立抽检；冲突案例以「少套数 + warnings」诚实降级，不伪造三套。

## 5. P4-4 CC0 视觉索引复核

- `visual-index.csv`：**28 行**，`rights_status` 全部 = `CC0 / Met Open Access (isPublicDomain=true)`，`public_domain_verified=28/28 true`。
- `verification-log.csv`：API 200 **28/28**、image_url 200 **28/28**、access_status=ok **28/28**。
- 关联：`related_card` 非空 **27/28**（1 条空白，见缺口）；`source_id` 为 SRC 或 MET-API（原型，未建独立 SRC 卡）。
- **0 下载/0 内嵌**：全库图片文件计数 **0**；README/`docs/VISUAL-REFERENCE.md` 明确「只存链接、不下载、image_url ≠ 许可、原型」。
- 结论：CC0 索引可用作**链接参考**；不构成图像再分发许可；1 条未关联卡与 MET-API 未建 SRC 为已知缺口。

## 6. P4-5 Macbeth 验证复核

- 官方套件：`python3 11-验收/P4-MACBETH/test_macbeth_p4.py` → **PASS 11/11，exit 0**（独立重跑）。
- 11 例覆盖：阶段变化 ×2、双人关系、全槽/配饰、历史证据缺口、极简 vs 复杂、特写、动作、视频连续性、中英术语检索、证据不足拒绝。
- 与 P3.5 基线对比（P4-MACBETH-COMPARISON.md）：P4 composer 指标 looks 3、avg_items **5.0**、max_abc_diff **4**、unique_src **21**，相对 P3.5 historical（looks 9、avg_items 1.0、max_abc_diff 0、unique_src 3）**槽位/A-B-C 差异/来源覆盖显著提升**；该对比用例 `continuity_states_explicit=false`（输入未提供跨场 states，属输入缺口而非 composer 回归）。
- 缺口与诚实性：11 例含 `historical_evidence_gap`、`evidence_insufficient_refusal` 通过；comparison 明示「No regression…evidence gaps explicit」。
- 人工评分：**无 P4 专用评分表**；现有 `11-验收/P3.5/Macbeth/HUMAN-SCORE.md` 18 行仍全空、`11-验收/P3.6/导演评分表.md` 18×7 全 NOT_SCORED → **保持 HUMAN_UAT_PENDING，未代填任何分数**。

## 7. 全回归（独立执行，P4 快照）

| 套件 | 命令 | 结果 |
|---|---|---|
| 结构校验 | `python3 scripts/validate.py` | **PASS**（399/399；来源卡 211；0 错误 0 警告） |
| 来源对账 | `python3 scripts/build_sources.py --check` | **PASS**（211/211；CSV 212 行；段位 SRC-0520..0524 已登记） |
| 验收 | `python3 scripts/run_acceptance.py` | **PASS 45/45**（exit 0） |
| 质量评估 | `python3 scripts/quality_eval.py --no-write` | **OVERALL PASS（17/17）** |
| Workflow | `python3 tests/test_workflow.py` | **9/9 OK**（106.8s） |
| Composer | `python3 11-验收/P4-COMPOSER/test_outfit.py` | **9/9 PASS**（exit 0） |
| Macbeth | `python3 11-验收/P4-MACBETH/test_macbeth_p4.py` | **11/11 PASS**（exit 0） |
| 旧检索/推荐指标 | quality_eval 对比 P3.6 | relevant@5 **4.16→4.16**、0-hit **0→0**、crash 0、example-in-A 0、warnings 1.0、A/B/C 0.9778、evidence 0.868 均不变；**precision 94.5%→92.9%（−1.6pp，阈值 0.8 仍 PASS）** |

**指标结论**：旧检索/推荐功能**无功能性回归**；唯一漂移为 precision −1.6pp（检索池从 363→399 卡后源卡排序稀释，仍在阈值内），列 WARN 观察，列入 NEXT-PLAN。

## 8. 发布门禁

| 状态 | 结论 |
|---|---|
| **PRIVATE-READY / PRIVATE-USE** | **YES（状态不变）**：P4 全部交付通过独立验收；技术/数据/质量门 PASS；版权场景 A/B 合规（0 图片/0 下载） |
| **PUBLIC-READY** | **NO（BLOCKED）**：B1–B6 未关闭 + **P4 新增许可阻断**（见 §9） |
| HUMAN_UAT_PENDING | **4 项未变**（Obsidian GUI、逐图版权、15 案例人工评分、62 draft 复核）；本轮未执行、未代填 |

## 9. P4 新增许可阻断（写入 RELEASE-GATE）

- **L1 DeepFashion2 禁入**：无 LICENSE/无明示许可 + 第三方图像 → 不得导入数据/图像/标注。
- **L2 FashionStylist 非商业**：CC BY-NC 4.0 → 仅内部非商业研究，禁止进入商业发布物。
- **L3 图片不复制**：所有审计来源图片一律不复制/不内嵌/不批量下载（Vault 现状 0 图片；含 open-pose、polyvore、Fashionpedia 图像）。
- **L4 HF 资源许可未核实**：Garments2Look 数据集/LoRA、fashion-clip 权重在 HuggingFace（本网络不可达）→ 使用前必须核实。
- **L5 polyvore 数据条款不清**：Apache-2.0 代码 ≠ 数据/clip 授权；仅方法论参考。
- **L6 open-pose 图片**：非商业 + 禁止再分发（除仓库自身授权场景）。
- 说明：P4 新来源卡（9 PD 书 + FreeSewing 2 + V&A 3）均有明确许可或 link_only 依据，未引入受限来源。

## 10. 残余风险与局限

1. **P4 专用 Macbeth 人工评分表缺失**：仅沿用 P3.5/P3.6 空表；建议 P4-7 补 `P4-MACBETH/HUMAN-SCORE.md` 18 套空表（不得代填）。
2. **P4 视觉 1 条未关联卡 + MET-API 未建 SRC**：原型缺口，不影响 0 图片政策。
3. **precision 小幅下降**（94.5%→92.9%）：非阻断，但与「检索池扩大」相关，需在 P5 观察。
4. **书籍结论 15/31 交叉验证**、5 条 candidate：进入卡片前需 architect 二次核实；年代/文化判断需现代研究校正（书为 1847–1919 旧著）。
5. **HF 许可未核实**与 **NC/无许可来源**：不得进入卡片/公开物。
6. **未执行人工 UAT**（B1–B4）：不得对外宣称公开可用。

## 11. 复现命令

```bash
python3 scripts/validate.py
python3 scripts/build_sources.py --check
python3 scripts/run_acceptance.py
python3 scripts/quality_eval.py --no-write
python3 tests/test_workflow.py
python3 11-验收/P4-COMPOSER/test_outfit.py
python3 11-验收/P4-MACBETH/test_macbeth_p4.py
# 独立 composer 抽检
python3 scripts/outfit.py --input 11-验收/P4-COMPOSER/fixtures/macbeth.json --json
python3 scripts/outfit.py --input 11-验收/P4-COMPOSER/fixtures/rain_continuity.json --json
python3 scripts/outfit.py --input 11-验收/P4-COMPOSER/fixtures/conflict.json --json
# 书籍抽检（body 行号）
python3 -c "import sys;sys.path.insert(0,'scripts');import books_extract as bx;h,b=bx.split_pg(open('/tmp/p4/pg76299.txt').read());print(b[16668])"
```
- 证据：`/tmp/p4_validate.txt`、`/tmp/p4_build.txt`、`/tmp/p4_acc.log`、`/tmp/p4_qeval.txt`、`/tmp/p4_wftest.log`、`/tmp/p4_composer_test.log`、`/tmp/p4_macbeth_test.log`、`/tmp/p4_outfit_*.json`。
- 版本：v1.0（2026-11-04，verifier/task-45）。
