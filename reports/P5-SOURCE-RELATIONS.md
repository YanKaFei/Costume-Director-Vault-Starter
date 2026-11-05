# P5-A 来源引用核验与孤岛归因（SOURCE-RELATIONS）

- 生成：2026-11-05 01:24（Asia/Shanghai）；worker：researcher（task-62，P5-A）
- **基线：git HEAD `1acb4d3`（clean，400 卡 = 189 内容 + 211 来源）**；审计对象 = 211 张来源卡。
- 只读声明：本任务**不修改任何卡片/脚本**，只写 `reports/P5-SOURCE-RELATIONS.md` 与 `11-验收/P5/source-audit.csv`。
- **并发状态（审计后更新）**：审计期间 P5 迁移（engineer/task-60）曾把 29 张卡写入损坏的 frontmatter（缺结束 `---`，`validate.py` 371/400 FAIL）；已报告 engineer 并修复，**当前 `validate.py` PASS 400/400（0 错误 0 警告）**。本报告仍以 clean HEAD `1acb4d3` 为基线计算；复核当前工作区（含迁移后的 `relations:` 元数据）：**143 个来源被 source_ids 引用，与基线 0 差异**，故 CSV 分类对当前状态同样有效。若迁移后续改动 `source_ids`，需按 §11 重跑。
- 迁移工具产物（engineer）同目录存在：`11-验收/P5/RELATION-CANDIDATES.csv`、`REVIEW-QUEUE.csv`、`migration-report.json`；本文件与其不重叠（本文件=来源侧 whitelist/blacklist）。
- 机读台账：`11-验收/P5/source-audit.csv`（211 行 × 20 列，每卡一行；`migration_class` 供迁移工具直接过滤）。

## 0. 总览

| 分类（relation_verdict） | 数量 | 含义 | migration_class |
|---|---|---|---|
| **connected（已连接）** | **143** | 被内容卡 `source_ids` 直接引用 | `whitelist_connected` |
| **legitimately-independent（合理独立）** | **49** | 词典/背景/实践/图像许可，或当前无匹配卡片（覆盖缺口）；不应强行连接 | `whitelist_independent` |
| **should-connect（应连接但未连接）** | **7** | 未被引用，但有证据支持的跨分类关系候选（已逐条回读原文） | `action_should_connect` |
| **needs-citation（需补充引用）** | **9** | 仅被正文 wikilink 引用（P4 公版书研究笔记），未进 `source_ids` | `action_needs_citation` |
| **merge-or-deprecate（可合并/可弃用，不删除）** | **3** | 与 canonical 同 URL 的重复来源卡 | `blacklist_duplicate` |
| 合计 | **211** | | |

方向核验（来源卡正文 `## 相关卡片` → 内容卡）：**142** 张来源卡声明了相关卡；其中 **119** 全部被对向 `source_ids` 证实、**20** 部分证实、**3** 完全未证实（重复卡，见 §5）；其余 69 张未声明相关卡（词典/背景/图像许可等）。

## 1. 方法

1. **source_ids 入向**：读取 189 张内容卡 frontmatter 的 `source_ids`，按精确 `SRC-xxxx` 统计（`validate.py` 已保证 100% 可解析）。
2. **wikilink 入向**：扫描全部 `.md`（内容卡、`06-时代地域/书籍研究`、`11-验收`、`reports`、`docs` 等；排除来源卡自身文件）中的 `[[SRC-xxxx]]`。
3. **来源→内容方向**：解析来源卡正文 `## 相关卡片` 的 `[[GAR/STR/MAT/STY/PRD/LOOK/SCN-xxxx]]`，逐条检查目标卡是否反向引用该来源（`source_ids` 含此 SRC）。这是**形式核验**；内容级支撑只在 §3 的 7 条候选上逐条回读双方原文。
4. **重复判定**：规范化 URL（去 protocol/www/尾斜杠）分组；canonical 以卡内 already-declared 备注为准（SRC-0022/0036/0115）。
5. **should-connect 判定（不凭 URL/关键词）**：候选必须同时满足 (a) 来源卡 `可支撑事实` 明确覆盖内容卡某一断言或实例；(b) 内容卡正文存在对应主张；(c) 人工回读双方原文确认（6 条 high/medium + 1 条 low 仅建议 review）。仅凭 token/URL 相似的不进入 action 列表。

## 2. 已连接（143）— 白名单

- 来源类型分布：academic_reference 69、museum_collection 69、reference_work 3、dataset 1、industry_framework 1。
- 说明：这些来源卡的 URL/许可/HTTP 已验证（见 `reports/SOURCES.csv` 与各自卡内验证记录）；迁移工具可直接把它们作为已有 `source_ids` 关系保留，**无需新建关系**。
- 例外：canonical 重复组中的 3 张非 canonical 卡（0163/0175/0157）见 §5，不因“已连接”而复制新关系。

## 3. 应连接但未连接（7）— 迁移候选（需人工确认）

| # | 来源 | 目标卡 | 置信度 | 证据（双方原文要点） | 迁移动作 |
|---|---|---|---|---|---|
| 1 | SRC-0037 V&A 风衣博客 | **GAR-0045 风衣** | high | 卡正文写「Burberry 1880 年推出 gabardine…防水与透气」；博文明确讲 19 世纪亚麻 smock 受潮收缩防水「与 gabardine 相同原理」并主题为 trench coat | 加 `source_ids`（补充 gabardine 原理/历史语境），不改正文事实 |
| 2 | SRC-0050 Cleveland 腰带 c.1375–1400 | **GAR-0080 腰带** | high | 卡定义「中世纪—早期近代固定衣物/挂载…带扣可极尽装饰」；CMA 实物为 1375–1400 银鎏金带扣+银线腰带，正好是该时段实例 | 加 `source_ids`（示例来源） |
| 3 | SRC-0029 Met 马甲 1615–20 | **GAR-0008 马甲** | high | 卡覆盖 17–20 世纪马甲形制；Met 1615–20 亚麻/丝/金属马甲提供 17 世纪初实例 | 加 `source_ids`（实例） |
| 4 | SRC-0030 Met 马甲 1780–1800 | **GAR-0008 马甲** | high | 卡写「18 世纪盛行刺绣」；Met 1780–1800 丝+棉马甲提供 18 世纪末实例 | 加 `source_ids`（实例） |
| 5 | SRC-0059 V&A 保持干燥简史 | **GAR-0047 雨伞** | medium | 卡写雨伞是携带式防雨工具与身份配饰（1927 实例）；博文提供防雨/伞的历史语境与 1929 地铁海报例 | 加 `source_ids`（历史语境） |
| 6 | SRC-0028 Met 和服 ca.1910 | **GAR-0001 和服** | medium | 卡以 Met 19 世纪和服为锚点并区隔 1910–30 出口款；Met ca.1910 和服可作为早期 20 世纪通用和服实例（注意 `isPublicDomain=false`，仅元数据） | 加 `source_ids`（实例；许可字段保持 link_only） |
| 7 | SRC-0041 V&A kantha 走针 | **GAR-0063 纱丽** | low（review） | kantha 博文以 tussar 纱丽为例讲刺绣工艺；纱丽卡讲的是缠裹形制——仅工艺语境 | **不自动迁移**；建议转 REVIEW-QUEUE，若建「刺绣/工艺」卡再挂 |

> 迁移工具只需消费 `migration_class=action_should_connect` 且 `confidence in (high,medium)` 的 6 条；`low` 的 SRC-0041 保留在 review。

## 4. 需补充引用（9）— P4 公版书（wikilink-only）

- SRC-0061..0069（9 本 PD 书）当前只被 `06-时代地域/书籍研究/书籍研究-历史服饰术语与结构.md`、`11-验收/P4-BOOKS/TERMS-GLOSSARY.md`、`reports/P4-BOOKS-INDEX.md` 以 wikilink 引用，**没有进入任何内容卡 `source_ids`**。
- 原因：P4-1 的 31 条结论落在研究笔记，尚未迁入卡片；按证据规则，书上说法只能作 **book_fact**（章/段/行定位，页码 UNCONFIRMED），不能单独支撑 `verified`。
- 迁移建议（不是自动白名单）：若把书籍结论迁入卡片，候选关系（需重写断言 + 标 book_fact）：
  - SRC-0066《男士服饰词典》→ GAR-0008 马甲 / GAR-0002 达布里特 / GAR-0016 班扬袍（词条定位在 `11-验收/P4-BOOKS/TERMS-GLOSSARY.md`）；
  - SRC-0067《足部之书》→ GAR-0022 威灵顿靴 / GAR-0035 女式皮鞋 / GAR-0010 鞋履类；
  - SRC-0068《法国时装史》→ PRD-0001/PRD-0002（法国语境，需标 book_fact）；
  - SRC-0063《英国服装》→ PRD-0003（1890 年代英美语境，需标 book_fact）；
  - SRC-0069《服装漫谈》→ GAR-0002 达布里特 / GAR-0016 相关结构卡；
  - SRC-0061/0062/0064/0065 与现有卡对应较弱（Dress Design/Textiles/Costume Fanciful/Jewellery-Fans），建议保留为背景研究，不强行连接。
- 结论：这 9 张卡**不是** orphan；分类为 needs-citation（补引用或保持背景），不进自动迁移白名单。

## 5. 可合并/可弃用（3）— 黑名单（不删除）

| 重复卡 | canonical | 依据 | 处理 |
|---|---|---|---|
| SRC-0163 | **SRC-0022** | 同一 FIT 拜占庭晚期服饰页 URL | 卡内已写 canonical；迁移工具不新建关系，引用统一到 0022 |
| SRC-0175 | **SRC-0036** | 同一 Screen Ireland Booklet 5 PDF URL | 同上；引用统一到 0036 |
| SRC-0157 | **SRC-0115** | 同一 FIT 1950–1959 页 URL | 同上；引用统一到 0115 |

- 另有 3 张 canonical 卡（0022/0036/0115）保持 connected（被内容卡引用），不是黑名单。
- 方向核验中 3 张“完全未证实”即这三张重复卡：它们的 `相关卡片` 指向的内容卡已改用 canonical，属于预期现象，不是新缺陷。

## 6. 合理独立（49）— 白名单（不强行连接）

| 子类 | 数量 | 说明/代表 |
|---|---|---|
| 词典/本体（AAT/Fashionpedia） | 22 | 术语分层与定义背景，内容卡用页面级来源承载具体断言；不强制 `source_ids` |
| 背景/方法 | 4 | SRC-0015 FIT 时间线、SRC-0017 研究方法、SRC-0042 CSA、SRC-0043 Costume Society |
| 行业实践 | 3 | SRC-0033 CDG 定义、SRC-0034 Design Details、SRC-0035 Screen Ireland 入口页（PDF 由 SRC-0036 承担） |
| 图像/许可参照 | 5 | SRC-0045..0049 Wikimedia Commons 文件：只作视觉/许可参照，不是事实断言来源 |
| 覆盖缺口/无匹配卡 | 15 | SRC-0018/0019/0020（FIT 19 世纪个案）、SRC-0023/0024/0025（Met 1855/1885/1886-88 连衣裙）、SRC-0026/0027（束身衣/婚礼束身衣）、SRC-0031（体操服）、SRC-0032（运动套装）、SRC-0038（Undressed 展）、SRC-0039（羽毛帽）、SRC-0040（护身衬衫）、SRC-0044（Museum at FIT）、SRC-0060（印度防染印花） |

- 覆盖缺口 15 张不是“坏来源”，而是当前无对应内容卡：若要连接，应先建卡（束身衣、19 世纪中后期连衣裙、体操/运动服、羽毛帽、贴身护身衣等），而不是把它们挂到不相关的卡上。
- 明确**不要交叉连接**的例子：SRC-0060（印度 resist block printing）≠ MAT-0008（日本 katazome 型染）——两者是不同传统，仅词面相似；SRC-0033/0034/0035（实践/方法）不应挂到具体服饰史卡。

## 7. 方向核验（来源→内容，142 张声明）

| 结果 | 数量 | 说明 |
|---|---|---|
| 全部证实（yes） | 119 | 来源卡 `相关卡片` 均反向出现在目标卡 `source_ids` |
| 部分证实（partial） | 20 | 部分目标卡未引用该来源；多为“来源卡列了宽泛相关卡，但卡片只引用了更具体的页面级来源” |
| 完全未证实（no） | 3 | 均为 canonical 重复卡（见 §5），预期 |

部分证实的例子与处理建议（**不自动改卡**，交 engineer/architect 在迁移中决定）：
- SRC-0101（Medici collar）声明 GAR-0015 法式长袍，但 GAR-0015 只引 SRC-0116；Medici collar 与 robe à la française 无直接领型关系 → 建议从来源卡的“相关卡片”移除该链接或说明只是宽泛同代参照（不属证据关系）。
- SRC-0162（费兹帽/奥斯曼）声明 GAR-0027、STY-0006；两卡分别引 SRC-0128、SRC-0162? 需核对——若内容卡并未使用该页断言，保持来源卡单侧语义为“背景”而非 `cites`。
- SRC-0201/0203/0204/0205/0206 等 V&A 卡声明了未被引用的邻近卡（如 GAR-0033/GAR-0008/GAR-0031）：属于“来源卡提示可配合卡”，不是已建关系；迁移工具不应据此创建关系（与 architect 的 `context_includes` 规则一致：只从结构化 `PRD.key_garments`/`source_ids` 派生）。
- 其余 16 条 partial 见 CSV 的 `declared_uncited_cards` 列。

## 8. 分组专项检查

### 8.1 P4 书籍来源 SRC-0061..0069
- 9/9 存在、wikilink 引用可见（研究笔记/术语表/索引），但 `cited_by_source_ids_count=0` → **needs-citation**（见 §4），不是 orphan。
- 原因：P4-1 结论尚未迁入内容卡；迁移时须按 book_fact + 章/段/行（页码 UNCONFIRMED）写入，不可直接 verified。

### 8.2 FreeSewing / V&A 结构来源 SRC-0520..SRC-0524
- 5/5 均已 connected：`SRC-0520`→STR-0021/STR-0025；`SRC-0521`→STR-0025；`SRC-0522`→GAR-0083；`SRC-0523`→GAR-0085；`SRC-0524`→GAR-0084。方向一致，无需动作。

### 8.3 Met API 来源（17 张 URL 含 metmuseum）
- connected 7；should-connect 3（SRC-0028→GAR-0001、SRC-0029/0030→GAR-0008）；independent 7（0018/19/20 非 Met；Met 中 0023/0024/0025/0026/0027/0031/0032 属覆盖缺口；另有 page-level Met 卡已连接）。
- 说明：Met API 卡的强项是「馆藏元数据 + isPublicDomain」，适合实例级补充；不要把 API URL 当作图像许可本身（图像仍逐件核验，见 0-图片策略）。

### 8.4 独立专题（拜占庭/莫卧儿/南亚/日本/奥斯曼）的跨分类关系
逐卡核对结果：**已有关系均已连接，无需新增**：
- 拜占庭：PRD-0010↔SRC-0022、MAT-0011↔SRC-0423、GAR-0061↔SRC-0421（均已 connected）；
- 莫卧儿/南亚：GAR-0071↔SRC-0450/0451/0452、GAR-0072↔SRC-0453/0454、GAR-0063↔SRC-0424、LOOK-0020/SCN-0011↔SRC-0424/0102（connected）；
- 日本：GAR-0001↔SRC-0100、GAR-0065↔SRC-0426、GAR-0066↔SRC-0427、MAT-0008↔SRC-0147（connected）；
- 奥斯曼：GAR-0027↔SRC-0128、PRD-0009/LOOK-0004↔SRC-0162（connected）。
- 可新增（review 级，非迁移就绪）：SRC-0041（kantha）→GAR-0063（见 §3 #7）；书籍→PRD（见 §4）。
- **不应新增**：SRC-0060（印度防染）→MAT-0008（日本型染）；SRC-0040（护身衬衫，中东/南亚宗教服饰）→任何纱丽/和服卡。

## 9. 给迁移工具的白/黑名单（engineer/architect 使用）

| migration_class | 数量 | 用法 |
|---|---|---|
| `whitelist_connected` | 143 | 保留现有 `source_ids` 关系；无需新建 |
| `whitelist_independent` | 49 | 不强行建关系；词典/背景/图像许可/覆盖缺口 |
| `action_should_connect` | 7（6 条 high/medium 可迁移，1 条 low 转 review） | 见 §3 表；迁移后需重跑 `validate.py`/`build_sources.py` |
| `action_needs_citation` | 9 | P4 书：只有把书籍结论迁入卡片时才加 `source_ids`（book_fact）；否则保持研究笔记背景 |
| `blacklist_duplicate` | 3 | 不新建关系；引用统一到 canonical（0022/0036/0115） |

## 10. 限制

- 本次为**基线审计**（HEAD `1acb4d3`）：P5 迁移正在工作区进行且当前 frontmatter 损坏，未纳入；迁移完成后应以新状态重跑本 CSV（脚本/方法相同）。
- `should-connect` 仅 7 条，全部人工回读双方原文；其余“相似度”候选未升级，避免 URL/关键词式误连。
- 方向核验是形式核验（声明 vs `source_ids`），不判断断言真值；内容级支撑以 `should-connect` 的 7 条为准。
- 未改任何卡片/脚本；CSV 每行含 `notes`/`evidence_relation_candidates` 供人工复核。

## 11. 复现

```bash
# 基线导出（HEAD，只读）
rm -rf /tmp/p5base && mkdir -p /tmp/p5base && git archive HEAD | tar -x -C /tmp/p5base
# 本报告 CSV 由 /tmp/p5_baseline.py 生成（读取 /tmp/p5base 与 scripts/audit_knowledge.py 的解析器）
python3 /tmp/p5_baseline.py        # 生成 11-验收/P5/source-audit.csv
# 交叉核对
python3 scripts/validate.py        # HEAD 基线应为 PASS 400/400
python3 scripts/build_sources.py   # PASS（CSV 212 行）
```

---

## P5-C 刷新（task-78，2026-11-05 02:05）

- **基线推进**：`11-验收/P5/source-audit.csv` 由 211 行扩到 **234 行**（+23 新来源 SRC-0530..0552）。分类：
  - `whitelist_connected` **167**（原 143 + 23 新来源 + SRC-0013 由 MAT-0018 引用）
  - `whitelist_independent` **48**（原 49，SRC-0013 转 connected）
  - `action_should_connect` **7**（SRC-0028/29/30/37/41/50/59，未强制迁移）
  - `action_needs_citation` **9**（P4 书 SRC-0061..0069）
  - `blacklist_duplicate` **3**（SRC-0157/0163/0175，canonical 不变）
- **新增 23 张全部 connected**：10 张 V&A 对象（SRC-0530..0539）+ 13 张 Getty AAT（SRC-0540..0552），均被 P5-C 新内容卡的 `source_ids` 引用（23/23，0 未用来源）。
- **语义单点刷新**：65 → **有效 64**；SRC-0013（AAT silk）已由 `MAT-0018 丝绸` 引用，从单点列表移除；其余分类保留（legit_reference 33 / future_topic 14 / evidence_missing_expression 16 / no_verifiable_relation 1），见 `11-验收/P5C/isolates.csv`。
- **9 本 P4 书状态不变**：仍只在 `06-时代地域/书籍研究` 等研究文档被 wikilink 引用，未进内容卡 `source_ids`；保持 `action_needs_citation`，不强制引用（若迁入卡片须 book_fact + 章/段/行，页码 UNCONFIRMED）。
- **来源可见率口径（单独统计，不与关系覆盖率混算）**：
  - content 卡 224；有 `source_ids` 的卡 199；`source_ids` 引用对 **346**；
  - 正文 wikilink 可见对 **196/346 = 56.6%**；正文任意 SRC 文本可见对 **346/346 = 100%**（engineer 链接修复后）；唯一可见来源 **147/167**；零 wikilink 可见卡 **52**（多为 draft LOOK/STY）。
  - 关系覆盖率（relations 覆盖等）见 `reports/P5C-RELATION-COVERAGE.md`，本 CSV 不混入该指标。
- 复核：`validate.py` 与 `build_sources.py` 未受影响（本任务只改报表/CSV，不改卡片）。

---

## P5-D 书籍应用刷新（2026-11-05 10:35，lead 批准后）

> 本节取代 §4 的「9 本 P4 书全部 needs-citation」历史状态；§4 保留为当时快照。

- **`11-验收/P5/source-audit.csv` 234 行分类更新**：
  - `whitelist_connected` **172**（P5-C 167 + 本次 5 本书转 connected）
  - `whitelist_independent` 48
  - `action_should_connect` 7（SRC-0028/29/30/37/41/50/59，未迁移）
  - `action_needs_citation` **4**（仅剩 SRC-0063/0065/0067/0068，背景）
  - `blacklist_duplicate` 3（SRC-0157/0163/0175）
- **书籍状态（9 本）**：
  - **已 connected 5 本（book_fact 已进卡 source_ids + 正文可见链接）**：
    - SRC-0061 PG34903 → STR-0010（1 卡）
    - SRC-0062 PG21534 → MAT-0012/15/16/18、STR-0016/17/18/20/30/32（10 卡）
    - SRC-0064 PG48551 → STR-0006（1 卡）
    - SRC-0066 PG76299 → GAR-0008/11/17/33/77、MAT-0015（6 卡）
    - SRC-0069 PG46949 → GAR-0079（1 卡；**卡仍 interpretive**，书源不升级）
  - **仍 needs-citation/背景 4 本**：SRC-0063 PG33020、SRC-0065 PG49559、SRC-0067 PG56978、SRC-0068 PG76717（仅研究文档 wikilink；不强制引用）。
- 应用台账：`11-验收/P5D/book-source-application.csv`（18 卡/19 组）；备份 `11-验收/P5D/backup-20261105-102725/`；报告 `reports/P5D-BOOK-EVIDENCE.md` §9。
- 校验：`validate.py` PASS 458/458；`build_sources.py` PASS 234/234；`relation_consistency.py` relations=284, errors=0。
- **注意（未在本轮更新）**：`11-验收/P5C/isolates.csv` 仍按 task-78 为 64 条，其中含 9 本书；本次 5 本已 connected，若按 task-78 口径刷新，**有效 isolates 应为 59**（剩余 4 本书 + 其他 55）。待 lead 确认后可由我补刷 isolates/coverage 附录。
