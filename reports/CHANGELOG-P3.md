# P3 更新日志（CHANGELOG）

- 版本：P3（commit `0345f05`，2026-11-04 02:24）
- 变更规模：**210 个文件，+35,255 / −9,489 行**（146 新增 / 64 修改）
- 基线：P2.5（commit `e848e08`，235 卡 / 18 例验收 / 142 来源）
- 终态：**328 卡（内容 154 + 来源 174）/ 30 例验收 / 174 来源**

## 1. 知识库扩充

| 类别 | P2.5 | P3 | 新增内容 |
|---|---|---|---|
| 总卡数 | 235 | **328** | +93 |
| garment | 36 | **71** | +35：职业服（护士/医生/警察/厨师/消防/军装）、雨具（风衣/雨衣/雨伞）、携带物（手提包/手杖）、徽章、Utility、1950s/1960s/1970s 单品、1930s 男鞋、跨文化传统服（科普特/文艺复兴/纱丽/韩服/和服/agbada/gele）、安全头盔等 |
| garment_part | 11 | 11 | — |
| material | 7 | **8** | +拜占庭 samite 丝绸 |
| pattern | 3 | 3 | — |
| look | 10 | **23** | LOOK-0010..0021：急诊护士、空间站维修、1930s 上海雨夜、加纳婚礼、1940s 通勤、身份弧线、西非节庆、跨文化晚宴/纱丽、当代四场连续性升级 |
| scene | 4 | **16** | SCN-0005..0016：急诊、空间站、上海后巷、加纳婚礼、1940s 通勤/复员、美术馆晚宴、南亚庆典、阿克拉节庆、银行家晚宴、难民收容所、1980s 工作室 |
| source | 142 | **174** | **+32（SRC-0400..0431）**：V&A 护士戏服/消防外套/雨衣/雨伞/手袋/手杖/徽章/Utility/鸡尾酒裙/童裙/迷你裙/厚底鞋/背带裤/男鞋/意大利丝袍/拜占庭 samite/寺庙纱丽/韩服/和服/obi/云肩/婚纱/agbada/gele + Met 军装大衣/科普特长袍 |
| style / period_region | 11 / 11 | 11 / 11 | 未扩充 |

- 证据分布：verified **282**、interpretive **42**、example **4**；`draft` 62 张（新增卡多为 draft，待人工复核）。

## 2. 脚本与验收

| 文件 | 变更 |
|---|---|
| `scripts/reco_norm.py` | **新增**：period/region 归一化（decade→century→era、region 层级）+ 近似证据层 |
| `scripts/recommend.py` | 修改（约 +40% 行）：兼容崩溃修复、period/region 归一化与近似声明、warnings 体系（职业/文化/未来/天气/冲突/身份弧线）、冲突检测（历史 vs 科幻拆分建议）、预算替代说明、prompt/context 过滤增强、brief 解析 |
| `scripts/query.py` | 修改：多词/`--phrase` 稳定化、排序与 example 卡处理改进 |
| `scripts/run_acceptance.py` | 修改：18 → **30 例**；新增 case 校验（历史年代层、跨文化、冲突、brief 解析、性别鞋履缺口） |
| `scripts/quality_eval.py` | **新增**：engineer 自评脚本（25 query 探针 + 30 推荐用例；其指标未覆盖语义缺陷，不作为验收依据） |
| `skills/costume-director/SKILL.md` | 更新到 P3 用法 |

## 3. 验收用例（18 → 30）

新增 T19–T30：1940s 战时职员、1950s 美国家庭、1960s 伦敦摄影师、1970s 伦敦朋克（historical mid-century 回归）、1580s 意大利宫廷舞者（F2 回归）、拜占庭帝国晚期宫廷（F2 回归）、太空站歌剧女伶、急诊科护士夜班、加纳英国跨文化婚礼、1930s 男职员雨夜（性别/鞋履缺口）、1930s 上海赛博朋克义体（冲突约束）、自由文本 brief 解析。

## 4. P2.5 缺陷修复（详见 `P3-DEFECTS.md`）

| 缺陷 | 状态 |
|---|---|
| F1 historical 1940s–70s 崩溃 | ✅ FIXED（4/4 exit 0） |
| F2 period/region 假阴性 | ✅ FIXED（1580s/拜占庭诚实输出） |
| F3 未覆盖请求静默 | ✅ FIXED（6/6 探针有 warnings；替代质量仍差 → D2） |
| M3 假阴性措辞 | ✅ FIXED |
| M5 example 卡进 A | ✅ FIXED（0/30、0/15） |
| M7 prompt 串文 / M8 query 排序 | ⚠️ PARTIAL |
| M1 / M2 / M4 / M6 | ❌ OPEN |
| 新发现 D2（职业服万能填充）、D4（虚假 rainwear 声明）等 | ❌ OPEN（详见缺陷登记） |

## 5. 验证结果（verifier 独立复跑）

- `validate.py` → exit 0（328/328，17/17 PASS，0 错误 0 警告）
- `run_acceptance.py` → exit 0，**PASS 30/30**，query 命中总 124、逐例 ≥1
- `build_sources.py --check` → 初始 **FAIL**（CSV 142 vs 174）→ QA `--write` 重建后 **PASS**（174 行）
- query 探针（独立复评）：relevant@5 **3.64/5**、precision **89.2%**、0 命中 **12%**（P2.5 3.0/86.2%/16%）
- 15 案例 6 维 rubric：PASS 1 / WARN 14 / FAIL 0；切题均值 **0.53/2**、诚实/证据 **2.0/2**
- 新增 32 来源 URL：**32/32 HTTP 200**，内容与卡名吻合
- 结论：**P3 数据与诚实性显著提升，但职业匹配（D2）与虚假 warning（D4）为 S1/S2 阻断缺陷，不得视为质量通过。**

## 6. 报表

- 新增：`reports/P3-QA.md`、`P3-COVERAGE.md`、`P3-DEFECTS.md`、`CHANGELOG-P3.md`、`NEXT-PLAN.md`
- 更新：`reports/STATUS.md`、`COVERAGE.md`、`QA.md`（反映 P3 终态）
- 重建：`reports/SOURCES.csv`（174 行 + 表头，P3 提交时遗漏同步）

---

# P3.1 更新（复验后，未提交工作区）

- 时间：2026-11-04 02:39–02:47；基于 HEAD `0345f05` 的工作区修复
- 触发：P3 独立 QA 的 D2/D4/M4/M6/M7 与 M1/M2、query 排序/去重缺陷

## 1. 脚本变更

| 文件 | 变更 |
|---|---|
| `scripts/recommend.py` | 新增 `OCCUPATION_HINTS`/`OCCUPATION_PROFILES` 与职业匹配逻辑（护士/医生/警察/厨师/太空/婚礼等）；职业服禁止跨职业顶替；rainwear 选择与「rainwear gap」措辞修正；context_refs 过滤；prompt 仅取已选 items 的短语；冲突检测与身份弧线 warning；curated occupational look 优先 |
| `scripts/reco_norm.py` | period/region 归一化与近似证据层增强 |
| `scripts/query.py` | 排序/去重：1930s 上海 GAR-0031 排名、同名和服去重、example 卡降权（top5 首名排除） |
| `scripts/run_acceptance.py` | 30 → **41 例**；新增 criteria：`occupation_match`、`no_occupation_mismatch`、`occasion_match`、`rainwear_selected`、`warning_absent:*`、`no_arctic_indoor`、`context_refs_clean`、`query_top5_contains`、`query_no_duplicate_names`、`query_no_example_top` 等 |
| `scripts/costume_lib.py` | 配套工具更新 |

## 2. 测试（30 → 41）

新增 T31 急诊护士职业匹配、T32 医生职业匹配、T33 警察职业匹配、T34 厨师职业匹配、T35 太空站维修工职业匹配、T36 加纳婚礼新郎跨文化、T37 1930s 上海雨具选择、T38 室内走廊不穿极地派克、T39 明末清初 context 清洁、T40 query 排序 1930s 上海、T41 query 和服去重。

## 3. 卡片与文档修正

- `GAR-0010`：删去无依据的「用于运动与童装」断言，改标 interpretive（M1 FIXED）。
- `SRC-0046`/`SRC-0047`：`license_status: cc0` + note 说明 Public domain 映射（M2 FIXED）。
- `GAR-0001`/`GAR-0065`：增加「查询去重提示」并区分 name_en/periods（查询层去重；数据层仍为两张卡，M8 部分）。
- `00-系统/来源规范.md`：补充 SRC 段位（0200..0299、0400..0499 等）。
- `reports/SOURCES.csv`：因 SRC-0046/47 字段变更再次漂移 → QA `build_sources --write` 重建为 174 行（D1 复发，已 RESOLVED-BY-QA）。

## 4. P3.1 独立复验结果

| 项 | 结果 |
|---|---|
| validate | exit 0（328/328，17/17 PASS，0 错误 0 警告） |
| build_sources --check | 首次 FAIL（2 行漂移）→ QA 重建后 PASS（174 行） |
| run_acceptance | exit 0，**PASS 41/41**，query 命中 178 |
| D2 职业匹配 | **CLOSED**（T26/T31/T32/T33/T34/T35/T36 + C02/N1 使用匹配卡；warnings 真实） |
| D4 rainwear 假 warning | **CLOSED**（T01/T02 用风衣；T37/T38 warning_absent PASS） |
| M1/M2/M4/M6/M7 | **CLOSED** |
| M8 查询排序/去重 | **PARTIAL→大部分关闭**（P07 GAR-0031 第 1、T40 PASS；T41 无重复名；P14 example 仍第 4/5） |
| query 指标（verifier） | relevant@5 3.64/89.2%/12%（与 P3 持平；具体排序改善） |
| quality_eval（engineer 自评复跑） | **exit 1，OVERALL: FAIL**：relevant@5=3.92 < 阈值 4.0（其余 15 项 PASS：precision 96.1%、0 命中 12%、崩溃 0、example-in-A 0、warnings 1.0、A/B/C 差异 0.976、证据覆盖 0.959、context 1.0、prompt 串文 0、occupation_mismatch 0 等） |
| 15 案例 rubric | **PASS 6 / WARN 9 / FAIL 0**（P3: 1/14/0）；切题均值 1.27/2 |

## 5. 残余风险（进入 P4）

**R7（FAIL/发布门槛）**：query relevance 未达 4.0（独立 3.64 / 自评 3.92，quality_eval OVERALL FAIL）——P3.1 唯一阻断项；R1 职业同义词/医疗内层（巡警未匹配、医生 A 含韩服）；R2 example 卡仍 in top5、和服数据层重复；R5 自评口径差；R6 SOURCES.csv 同步流程；15 案例中 9 例切题 0–1（覆盖限制，已诚实声明）。


---

# P3.2 更新（P3.2 最终修复）

- 时间：2026-11-04 02:50–03:05；commit `281e3b1`；工作区 clean
- 触发：P3.1 复验 R7（query relevance 3.64/3.92 < 4.0）、R1 职业同义词残余、R2 example top5

## 1. 变更

| 文件/对象 | 变更 |
|---|---|
| `scripts/query.py` | 扩展 QUERY_ALIASES（医师/巡警/民警/警官/宇航员/航天员/新郎/材质类）；新增 REGION_INTENT 区域意图加权（和服→japan、旗袍→china、纱丽→india、gele/agbada→nigeria 等）；**默认排除 example 卡**（`--include-example` 可恢复）；排序/去重增强 |
| `scripts/recommend.py` | 职业同义词/跨文化误配检查（`occupation_match`/`no_occupation_mismatch`/`no_cultural_mispick`）、医生内层约束、T42–T45 支持 |
| `scripts/run_acceptance.py` | 41 → **45 例**；新增 T42 巡警/ T43 医师/ T44 宇航员/ T45 民警同义词职业匹配（含 `no_cultural_mispick` 检查） |
| 测试 | T42–T45 新增；45/45 PASS |
| 报告 | `11-验收/质量评估/` 自评更新：relevant@5 4.0（100/125）、precision .952、0-hit 0.08 |

## 2. 独立复验结果（verifier）

| 项 | 结果 |
|---|---|
| validate / build_sources | exit 0 / exit 0（CSV 174 行已同步） |
| run_acceptance | exit 0，**PASS 45/45**，query 命中 187 |
| D2/R1 职业（含同义词） | **全部匹配**：护士 GAR-0036、医生白袍 GAR-0041（无韩服）、警察 GAR-0042（巡警/民警同）、厨师 GAR-0043、宇航员 GAR-0038/0039、婚礼 GAR-0005/0070 |
| D4/M4/M6/M7/M1/M2 | 保持关闭 |
| R2 | P14 返回 3 条全非 example；P02/T41 无同名重复；数据层和服重复卡仍在（WARN） |
| R7（独立） | raw relevant@5 **3.92（98/125）**；剔除 P21/P22 已知缺卡后 **4.26**；precision **93.3%**；0 命中 **8%**（engineer 自评 4.0/95.2%/8%） |
| 15 案例 rubric | **PASS 7 / WARN 8 / FAIL 0**（P3.1：6/9/0） |
| F1/F2/F3 回归 | 保持 PASS（4/4 exit0；1580s 3 looks；6/6 warnings） |

## 3. 残余风险（WARN 5）

R7（条件性放行：raw 3.92 <4.0、调整后 4.26）、R8 单探针相关性缺口、R3 数据层和服重复、R4 噪声 warning、R5 CSV 同步无自动化。**无 S1/S2 OPEN 缺陷；发布门槛为 CONDITIONAL PASS（R7 由 lead 决定接受已知缺口或继续提升）。**


---

# P3.3 更新（最终数据补充与 R7 关闭）

- 时间：2026-11-04 03:08–03:16；commit `fcebf79`；工作区 clean
- 触发：P3.2 复验 R7 raw relevant@5 3.92 < 4.0；P21 Mughal / P22 mourning jewelry 为真实缺卡；R3 和服同名、R4 噪声、R5 门禁未验证

## 1. 知识库变更

| 对象 | 变更 |
|---|---|
| GAR-0071 | 新增「莫卧儿 jama」（one_piece；mughal_empire/india；SRC-0450/0451/0452） |
| GAR-0072 | 新增「帕贾马裤」（lower_body；india/lucknow/gujarat；SRC-0453/0454） |
| GAR-0073 | 新增「维多利亚哀悼珠宝」（accessory；britain；SRC-0455/0456/0457） |
| GAR-0074 | 新增「哀悼戒指与胸针」（accessory；britain；SRC-0458/0459/0460） |
| SRC-0450..SRC-0460 | 新增 11 张 V&A 来源（11/11 HTTP 200，标题/对象与卡名吻合） |
| GAR-0065 | `name_zh` 改为「出口和服」、`name_en: export kimono`（文件名保留兼容双链）——R3 |
| 合计 | **343 卡（内容 158 + 来源 185）**；verified 297、interpretive 42、example 4；draft 62 |

## 2. 脚本/门禁变更

- `scripts/quality_eval.py`：新增 `check_sources_csv()` 质量门（R5），`sources_csv_sync` 阈值 1.0 纳入 OVERALL。
- `scripts/recommend.py`：移除「no upper_body/lower_body candidates」噪声 warning（R4）。
- `scripts/query.py`：P3.2 的区域意图/别名/example 排除策略保持；新增卡后 P21/P22 可检索。

## 3. 独立复验结果（verifier）

| 项 | 结果 |
|---|---|
| validate | exit 0（343/343，17/17，0 错误 0 警告） |
| build_sources --check | exit 0（185/185，CSV 186 行含表头） |
| run_acceptance | exit 0，**PASS 45/45** |
| **R7** | **raw relevant@5=4.16（104/125）≥4.0**；precision 94.5%；0 命中 0%（P21 3 命中、P22 2 命中，均相关）；与自评 4.16/0.945/0.0 一致 → **CLOSED** |
| R1/R2/R3/R4 | 全部 CLOSED（同义词六类匹配；P14 无 example；出口和服改名去重；噪声文案移除） |
| R5 | **实测有效**：注入 CSV 漂移→FAIL，恢复→PASS |
| 15 案例 rubric | **7 PASS / 8 WARN / 0 FAIL**（同 P3.2） |
| F1/F2/F3 | 保持 PASS |

## 4. 残余风险（WARN 4）

W1 rubric 8/15 切题 0–1（KB 覆盖限制）；W2 C01 明末清初选莫卧儿 jama（近似）；W3 filtered 查询结果数有限；W4 证据覆盖 0.94。**无 FAIL；发布门槛技术项 PASS，HUMAN_UAT_PENDING 4 项待完成。**
