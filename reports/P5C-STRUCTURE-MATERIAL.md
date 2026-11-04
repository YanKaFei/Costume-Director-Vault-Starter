# P5-C 结构 / 材质 / 配饰扩建与关系（task-72）

- 任务：P5-C 结构与材质扩建；日期 2026-11-05（Asia/Shanghai）
- 性质：只新增 `01-服装单品/`、`02-结构细节/`、`03-材质纹样/` 卡片；**未覆盖/修改任何既有卡片**；未改 `00-系统/05-09/scripts`；来源卡由 researcher（task-73/源审计）创建，本任务只引用
- 新来源：**SRC-0530..SRC-0552（23 张）**，均由 researcher 按 V&A 对象页/API + Getty AAT 记录 curl 200 核验；本任务不新建来源 ID
- 验证：`validate.py` **PASS 458/458**（来源卡 234，0 错误/0 警告）；`build_sources.py --check` **PASS**（CSV 与 234 来源一致）

## 1. 新增 18 张卡

### 结构（9，STR-0027..0035）
| ID | 名称 | 主要来源 | 证据 |
|---|---|---|---|
| STR-0027 | 领口形态（square/round/high） | SRC-0530/0531/0533/0535 | verified（实例）；typology 说明为解释性 |
| STR-0028 | 青果领/披肩领 | SRC-0532/0539 | verified（对象著录 shawl collar） |
| STR-0029 | 泡泡袖 | SRC-0533 | verified（long puffed and pleated sleeves） |
| STR-0030 | 里布与衬（lining/interlining/facing） | SRC-0534/0540 | verified（V&A 实例 + AAT 定义） |
| STR-0031 | 填充与绗缝 | SRC-0541/0542 | verified（AAT 定义） |
| STR-0032 | 褶裥与抽褶 | SRC-0543/0544/0531/0533 | verified（AAT 定义 + 实例） |
| STR-0033 | 口袋结构 | SRC-0545/0532 | verified（AAT + 袋盖实例） |
| STR-0034 | 拖尾 | SRC-0546/0535 | verified（AAT + rounded train 实例） |
| STR-0035 | 廓形与比例 | SRC-0530/0531/0533/0535/0536 | **interpretive**（实例对比；无权威 A/H/Y/T/X 分类） |

### 材质（5，MAT-0015..0019；与 MAT-0012/0013 物性卡分开）
| ID | 名称 | 主要来源 | 证据 |
|---|---|---|---|
| MAT-0015 | 羊毛织物 | SRC-0547/0534/0204 | verified |
| MAT-0016 | 亚麻织物 | SRC-0548/0539/0486 | verified |
| MAT-0017 | 皮革 | SRC-0549/0489/0538 | verified（鞣制工艺细分不在 AAT 范围，卡内标 interpretive/限制） |
| MAT-0018 | 丝绸 | SRC-0013/0423/0530/0535 | verified（材质族；组织另见 MAT-0012/0014） |
| MAT-0019 | 现代合成纤维与防水涂层 | SRC-0550/0417/0406 | verified（现代边界明确；前现代防水不覆盖） |

### 配饰/鞋履（4，GAR-0088..0091）
| ID | 名称 | 主要来源 | 证据 |
|---|---|---|---|
| GAR-0088 | 晚装长手套（opera-length） | SRC-0538 | verified |
| GAR-0089 | 腰封/束腰带（waspie） | SRC-0536 | verified（1940s New Look 语境） |
| GAR-0090 | 项链与耳环 | SRC-0551/0552/0455/0457 | verified（AAT 定义 + jet 实例） |
| GAR-0091 | 乐福鞋（loafers） | SRC-0537 | verified（1970s 黑色皮革） |

共同：8 节正文、`source_ids` 全部解析、`## 来源链接` 列出全部来源、`## 相关卡片` 链到既有单品/结构/材质；未把物性卡 MAT-0012/0013 当材料。

## 2. 关系（新卡内 `relations`）

**新卡共 52 条关系**：`claim_supported_by` **47** + `uses_material` **5**；全部 target/source_id 可解析；无 `may_have_part`/`ensemble_with` 硬连，无 unsupported 关系。
- 5 条材料关系：STR-0027→MAT-0018（silk georgette）、STR-0029→MAT-0001（muslin）、STR-0034→MAT-0018（silk）、GAR-0088→MAT-0017（kid leather）、GAR-0091→MAT-0017（leather）。
- 其余为 claim→source（47 条），来源均为真实 SRC-0530..0552 或既有 SRC-0013/0204/0406/0417/0423/0455/0457/0486/0489。
- 每张新卡另有 `## 相关卡片` 导航链接到既有内容卡（4–5 条/卡），但**不把这些导航链接写成事实关系**；正式关系只到来源/材料。
- 关系证据/置信：新卡 17 张 verified + STR-0035 interpretive；source claim 以 high 为主，material 关系统一 medium（符合 v2 `uses_material` 上限）。

## 3. 覆盖变化（本任务新增卡口径）

| 指标 | 任务前 | 任务后 |
|---|---:|---:|
| 内容卡 | 206 | **224**（+18） |
| GAR | 88 | **92**（+4 配饰/鞋） |
| STR | 26 | **35**（+9 结构） |
| MAT（material） | 11 | **16**（+5 材质） |
| 来源卡 | 234（含 researcher 新 23） | **234**（task-72 不新建来源） |
| 新卡 relations | — | **52**（47 claim +5 material） |

- 结构缺口覆盖：领口/青果领/泡泡袖/里布衬/填充绗缝/褶裥抽褶/口袋/拖尾/廓形 9 项；材质缺口：羊毛/亚麻/皮革/丝绸/合成+涂层 5 项；配饰缺口：长手套/腰封/项链耳环/乐福鞋 4 项。
- 来源归属：SRC-0530..0552（23 张）为 researcher/task-73 创建并核验；task-72 只引用，**未新建来源卡**，故来源总数保持 234。
- 组件覆盖限制：**未改既有 garment→component 字段/关系**（任务禁止覆盖旧卡）；新结构卡通过正文相关链接提供导航，但既有 88 张 garment 的正式 component 关系不变。若需提升矩阵的 garment→component 百分比，需要另任务在既有 garment 上补真实关系（不能靠新建结构卡自动提高）。
- 材质覆盖：新 MAT-0015..0019 补齐材质实体卡，使“材料实体 vs 物性卡（MAT-0012/0013）”分层；未把属性卡当材料。

## 4. 验证与证据

```bash
python3 scripts/validate.py
# 卡片总数: 458；frontmatter 通过: 458；来源卡: 234
# 错误级失败项: 0；警告: 0 -> PASS
python3 scripts/build_sources.py --check
# PASS（CSV 与全部来源卡一致；234 来源）
```

- 新卡均通过 8 节正文、source_ids 解析、来源链接提及全部 source_ids；
- 新来源卡由 researcher 创建并 curl 200 核验（V&A 对象页+API；AAT .nt+页面 Note）；本任务未新建/修改来源卡；
- 未修改既有卡片；未改 `00-系统/05-09/scripts`；`00-系统/索引.md`/`11-验收/P5/source-audit.csv` 计数更新不在本任务范围，需 owner 重建（source-audit 仍为 211 白名单，本任务新增 23 来源尚未进入白名单）。

## 5. 缺口 / 风险

1. **既有 garment→component 关系未提高**（任务不允许改旧卡）；新结构卡只在正文“相关卡片”导航。后续若需矩阵提升，应另任务在既有 garment 上补带来源的真实关系。
2. `STR-0035 廓形与比例` 明确 interpretive：A/H/Y/X 不是本库可证史实分类；仅按 V&A 实例（1820s/1870s/1920s/1940s）对比。
3. 皮革鞣制工艺（植鞣/铬鞣）、鱼尾摆特殊剪裁、现代涂层具体聚合物没有直接来源；卡内已标限制/interpretive，不用作强断言。
4. 新卡 `relations` 主要是 claim/material；未把新建结构卡与既有 garment 做 `may_have_part` 硬连（P5-B 规则：共现候选不得当结构事实）。
5. `11-验收/P5/source-audit.csv` 仍为 211 白名单；新 SRC-0530..0552 未进入 researcher 的 whitelist/register（researcher 已说明 task-73 外）；下游使用新来源前需 owner 重建 register/audit。
6. 未跑 GUI/workflow/acceptance；本报告只覆盖 validate/build + 静态卡面检查。
