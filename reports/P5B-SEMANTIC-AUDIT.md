# P5-B 语义关系纠错与五级证据分类

- 任务：task-65（P5-B 第一阶段语义纠错）；日期 2026-11-05（Asia/Shanghai）
- 基线：HEAD `afcd9ec`（P5-A：400 卡 / 211 来源 / 201 条 cards `relations`）+ 本任务工作区
- 输入：`reports/P5-SEMANTIC-REVIEW.md`（4 MISLINK + 8 WEAK）、`reports/P5-GRAPH-QA.md`、`reports/P5-RELATION-MIGRATION.md`、`11-验收/P5/SEMANTIC-SPOTCHECK.csv`
- 输出：本报告 + `reports/P5B-RELATION-CORRECTIONS.csv`（39 行；`card_id,old,new,evidence,action,status` + 审计字段）+ `00-系统/关系类型.md` v2 规则
- 性质：只改卡片 frontmatter 的 `key_garments`/`relations`；**不改正文/来源事实、不删除卡片、不新增来源**；无依据不替换。

## 0. 结论

| 项 | 结果 |
|---|---|
| 4 条 MISLINK | **2 closed（修复）+ 2 rejected（候选拒绝，未进入正式关系）** |
| 8 条 WEAK | **1 closed（移除越级正式关系）+ 6 review_queue（隔离，禁止历史使用）+ 1 rejected（example 排除）** |
| 同类模式（key_garments 40 对） | 明确年代冲突 **6 对已修正**（5 移除 + 1 替换）；**6 对 flag review**（不删除，保留待人工核） |
| uses_material | 正式关系 2 条 high 越级 → **降 medium/review**；候选 18 条指向物性卡 MAT-0013 → **rejected**；pattern 目标 0 |
| may_have_part | 31 条候选；**1 条语义冲突 rejected**（codpiece→collar）；30 条保持 review；0 条升格 `has_part` |
| context_includes | 45 条 high 候选；**2 条上游 key_garments 修正**（移除/替换）；其余保持“语境级 indirect”，禁止当逐件史实 |
| 五级证据分类 | 已写入 `00-系统/关系类型.md` §2.1；修正记录覆盖 unsupported_conflict 23 / indirect_interpretation 10 / later_influence 1 / creative_inference 5 / direct_evidence 0 |
| 验证 | `validate.py` PASS 400/400（0 errors/0 warnings）；`build_sources --check` PASS；卡片删除 0；来源卡编辑 0 |

## 1. 五级证据分类（`00-系统/关系类型.md` §2.1）

| 等级 | 定义 | 本任务典型 | Agent 边界 |
|---|---|---|---|
| `direct_evidence` | 来源直接陈述且 scope 覆盖断言 | pilot claim_supported_by（本次无修正） | 可用于历史判断（仍须 high/verified+scope） |
| `indirect_interpretation` | 来源只支持语境/类比/材料族 token | context_includes、uses_material token | 必须 hedge“语境/候选”；不得说成逐件史实 |
| `later_influence` | 来源/实例晚于目标年代 | GAR-0045→SRC-0405（2014 实例） | 只能作实例/影响，不能证明早期历史 |
| `creative_inference` | LOOK 组合、ensemble、may_have_part、风格标签 | GAR-0002/0003→STR-0001；LOOK-0001→STY-0010 | 只作设计建议；不得进入历史/结构事实 |
| `unsupported_conflict` | 年代/地域/类型/语义冲突 | PRD-0007→GAR-0006；PRD-0010→MAT-0003；GAR-0013→STR-0001；MAT-0013 物性卡 | 移除/拒绝；禁止参与历史判断 |

> 说明：`direct_evidence` 在“修正记录”中为 0 是正常的——它代表没有出错的直接证据关系（28 条 pilot claim 未改），不是分类缺失。

## 2. 4 条 MISLINK 逐条关闭

| # | ID | card / 关系（old） | 证据 | 修正（new） | 等级 | 状态 |
|---|---|---|---|---|---|---|
| 1 | MISLINK-01 | PRD-0007.key_garments 含 GAR-0006 | PRD-0007=1950s；GAR-0006 periods=1960s/1970s/contemporary；GAR-0006 已在 PRD-0008(1960s) | 移除 GAR-0006：`[GAR-0014, GAR-0006, GAR-0023]` → `[GAR-0014, GAR-0023]` | unsupported_conflict | **closed** |
| 2 | MISLINK-02 | PRD-0010.key_garments 含 MAT-0003 | PRD-0010=拜占庭晚期；MAT-0003=16–19c 欧洲 passementerie；MAT-0011=拜占庭 samite（SRC-0423） | 替换 MAT-0003→MAT-0011：`[GAR-0009, MAT-0003]` → `[GAR-0009, MAT-0011]` | indirect_interpretation（语境） | **closed** |
| 3 | MISLINK-03 | candidate REL-0640 GAR-0002→MAT-0013 (uses_material, medium) | MAT-0013 是“克重与垂坠”物性卡；token linen 命中 fiber_content ≠ 使用材料 | 候选 rejected；规则 v2 排除 MAT-0012/0013 与 pattern 卡 | unsupported_conflict | **rejected**（候选，未入正式 relations） |
| 4 | MISLINK-04 | candidate REL-0614 GAR-0013→STR-0001 (may_have_part, medium) | codpiece 与 Medici collar 仅 LOOK-0003 共现；无结构关系 | 候选 rejected；不再作为 part 候选 | unsupported_conflict | **rejected**（候选，未入正式 relations） |

## 3. 8 条 WEAK 逐条关闭

| # | ID | card / 关系 | 证据/问题 | 修正/隔离 | 等级 | 状态 |
|---|---|---|---|---|---|---|
| 5 | WEAK-05 | candidate GAR-0002→STR-0001 may_have_part | 同 LOOK 共现；无 part_ids | 保留 review；禁止升格 has_part | creative_inference | review_queue |
| 6 | WEAK-06 | candidate GAR-0003→STR-0001 may_have_part | 同上 | 保留 review | creative_inference | review_queue |
| 7 | WEAK-07 | formal GAR-0033→SRC-0155 claim_supported_by high | SRC-0155=1930–39 概览，不能覆盖 GAR-0033 的 1940s；同卡 SRC-0204=1940s | 移除该正式 relation；保留 SRC-0204；SRC-0155 仍在 source_ids 作背景，正文不动 | indirect_interpretation | **closed** |
| 8 | WEAK-08 | candidate GAR-0002→GAR-0024 ensemble_with | LOOK-0003 共现；设计搭配非历史 | 保留 design/review；不迁移 | creative_inference | review_queue |
| 9 | WEAK-09 | candidate LOOK-0001→STY-0010 in_style | exact STY ID，但 1770s LOOK 的“历史考据剧”标签是设计标签 | 保留 design/review；不迁移 | creative_inference | review_queue |
| 10 | WEAK-10 | candidate LOOK-EXAMPLE-001→GAR-0014 appears_in_look low | example LOOK + low 不得迁移 | 排除出迁移（候选保留演示） | creative_inference | **rejected** |
| 11 | WEAK-11 | formal GAR-0020→MAT-0001 uses_material high | uses_material 最高 medium；token 关联非 canonical material | 关系降 `confidence=medium; rule=R-MAT-TOKEN`，保留 review；合并到单一 `relations:` 列表 | indirect_interpretation | review_queue |
| 12 | WEAK-12 | formal GAR-0045→SRC-0405 claim_supported_by high | SRC-0405=2014 Burberry 蕾丝风衣实例，不能单独支撑通用风衣历史 | 降 `evidence=interpretive; confidence=medium`，保留实例 | later_influence | review_queue |

## 4. 同类模式扫描

### 4.1 key_garments 年代/地域（11 PRD，40 个 key_garments 对）

- 方法：对 PRD 与目标卡的 `periods` 做区间归一（decade→区间、世纪/era→区间、`contemporary` 宽标签单独标注）；不做关键词或颜色推断。
- **明确冲突 6 对（已修正，均记录在 CSV）**：
  1. PRD-0007→GAR-0006（1950s vs 1960s+）**移除**
  2. PRD-0010→MAT-0003（拜占庭 vs 16–19c）**替换 MAT-0011**
  3. PRD-0003→GAR-0012（1890s vs early/mid19c）**移除**
  4. PRD-0005→GAR-0007（1930s vs 1890s/Edwardian）**移除**
  5. PRD-0006→GAR-0017（1940s vs 18–19c）**移除**
  6. PRD-0006→GAR-0011（1940s vs mid/late19c/early20c）**移除**
- **6 对 flag review（不删除，待人工核）**：PRD-0004→GAR-0007（1920s 边界）、PRD-0007→GAR-0023（moccasin/region）、PRD-0006→GAR-0022（contemporary 宽标签）、PRD-0008→GAR-0014、PRD-0008→MAT-0004（邻接十年）、PRD-0011→GAR-0033（republican era 宽标签）。
- 扫描中 `PRD-0006` 现仅保留 `[GAR-0022]`（flag，未删）；`PRD-0001/0002/0009` 的多数差异属年代区间/语境级可解释，不强行修改。

### 4.2 uses_material 指向物性/纹样卡

- 正式 `relations`：**2 条 high 越级** — GAR-0020→MAT-0001、PRD-0002→MAT-0001，均降 `medium/R-MAT-TOKEN`，保留 review（CSV WEAK-11 / SCAN-MAT-02）。
- 候选 CSV：**18 条 uses_material 目标为 MAT-0013（物性卡）**（含 REL-0640），全部在修正 CSV 标 `rejected`；`MAT-0012` 与 pattern 卡（MAT-0005/6/7）目标 0 条。
- 规则 v2：`MAT-0012/0013`（material_property）与 pattern 卡不得作为 `uses_material` 目标；仅真实 material/fiber/trim/metal 卡；上限 medium。

### 4.3 may_have_part 仅 LOOK 共现

- 候选 31 条全部为 LOOK 共现；**1 条语义冲突 rejected**（GAR-0013 codpiece→STR-0001 collar），其余 30 条保持 review；**0 条**提升为 `has_part` 或写入正式 `relations`。
- 正式 relations 中没有 may_have_part（P5-A 只迁移了 high claim/style/material）。

### 4.4 context_includes 宏观语境 vs 逐件史实

- 候选 45 条 high `context_includes`；本任务修正 2 条上游 key_garments（PRD-0007 移除、PRD-0010 替换），其余 **43 条仅作语境级 `indirect_interpretation`**，不得作为逐单品历史证明，不得直接迁移。
- 规则 v2 要求 target 的 periods/regions 与 PRD 兼容；不兼容即 rejected。其余 43 条需 P5-A 重生成候选后按新规则复判。

## 5. 修正记录/不删除证据

- 卡片编辑：**9 个文件的 frontmatter**（9 files changed, +8/−10 行，均为 key_garments/relations 行；正文与 source_ids 未改）。
- 未删除任何卡片；未修改任何 `04-来源` 来源卡；未新增来源；未把任何关系升级为 `has_part`。
- 完整 old/new/evidence/action/status：`reports/P5B-RELATION-CORRECTIONS.csv`（39 行：closed 6 / review_queue 13 / rejected 20；等级 unsupported 23 / indirect 10 / creative 5 / later 1）。
- `reports/P5B-RELATION-CORRECTIONS.csv` 为后续迁移/回归的唯一纠错依据；P5-A 候选 CSV 未改（不在本任务写范围）。

## 6. 规则更新（`00-系统/关系类型.md` v2）

1. 五级证据分类与 Agent 使用边界（§2.1）。
2. `uses_material` 排除 `material_property`（MAT-0012/0013）与 pattern（MAT-0005/6/7）；最高 medium。
3. `may_have_part`/`ensemble_with` 仅 review/design，永非 `has_part`/历史搭配；语义不通直接 rejected。
4. `context_includes` 需 period/region 兼容；只做语境级间接解释。
5. `claim_supported_by` 检查来源 scope：后世/实例来源标 `later_influence` 并降 medium；背景来源不得替代主证据。
6. `in_style` 标 creative_inference（设计标签，非史实风格）。
7. 纠错/迁移协议：修正写入 `reports/P5B-RELATION-CORRECTIONS.csv`；rejected/unsupported 不得进入 Agent 历史判断。

## 7. 验证

```bash
python3 scripts/validate.py
# 卡片总数: 400；frontmatter 通过: 400；来源卡: 211
# 错误级失败项: 0；警告: 0
# RESULT: PASS
python3 scripts/build_sources.py --check
# RESULT: PASS（CSV 与全部来源卡一致）
```

- 卡片删除：0；来源卡编辑：0；正文改动：0（diff 仅 frontmatter 关系/key_garments）。
- 修正 CSV：39 行，字段 `card_id,old,new,evidence,action,status` + `audit_id,evidence_level,relation_type,rationale,source_ids,file`。

## 8. 剩余风险 / 未闭合

1. **P5-A 候选 CSV 未更新**（不在写范围）：仍含 45 条 context_includes、18 条 MAT-0013 uses_material、codpiece may_have_part 等 rejected 行；下游必须以本报告/修正 CSV 过滤，或重跑 P5-A 生成器（规则 v2）。
2. **6 对 key_garments flag review** 仍未定论（PRD-0004/0006/0007/0008/0011），未删除；需人工/领域 owner 决定。
3. **PRD-0006 仍保留 GAR-0022**（contemporary 宽标签，flag）；如有更合适 1940s 卡可替换，但不做 coverage 驱动补链。
4. **MOC 未改**（不在写范围）：`00-系统/MOC/时代地域.md` 的 key_garments 计数可能滞后；MOC 只是导航，不作为关系事实。
5. **关系字符串未写 `evidence_level`**：卡片 `relations` 仍只有 evidence/confidence/rule；五级分类在 schema/修正 CSV/文档，迁移工具与 Agent 需按规则映射，不能只看字符串。
6. **workflow/GUI 未运行**：本任务为静态语义纠错；`workflow` 当前树 hang（P5-GRAPH-QA 已记 NOT_RUN），Agent headless 未重跑；不得宣称端到端 PASS。
7. **direct_evidence 修正数 0**：不代表 direct 关系全部正确；pilot 28/34 claim 已由 P5-A 抽检 PASS，其余 claim 关系仍属 P5-A 覆盖范围，未做全量重审。

8. **迁移工具重跑风险**：`scripts/relation_migrate.py` 若再次按 `source_ids` 全量生成，可能重新添加已移除的 GAR-0033→SRC-0155、或把 GAR-0045→SRC-0405 重新标 high，并可能覆盖本任务降级；后续迁移必须读取 `reports/P5B-RELATION-CORRECTIONS.csv` 的 rejected 列表并应用 v2 scope 规则，或先更新迁移器的排除表，再重跑。
