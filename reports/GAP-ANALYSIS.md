# R1 缺口分析（GAP-ANALYSIS）

- 定稿：2026-11-04 18:22；verifier / task-51；快照 HEAD `56f4225`（399 卡：内容 188 + 来源 211）
- 来源：INTEGRATION-AUDIT（初稿）、KNOWLEDGE-QUALITY-AUDIT、SKILL-E2E-R1、SECURITY-TEST、CREATIVE-QUALITY-AUDIT、SCHEMA-CODE-AUDIT + 本轮独立复核
- 图例：严重度 S1 阻断 / S2 高 / S3 中 / S4 低；优先级 P0 立即 / P1 发布前 / P2 应修 / P3 可选；状态 OPEN / PARTIAL / CLOSED
- **P0 = 3；P1 = 11；P2 = 16；P3 = 6**；所有未执行人工检查保持 NOT_RUN/BLOCKED，不升级为 PASS。

## 1. P0（立即修复，影响创作可信度/验收有效性）

| ID | 严重度 | 缺口 | 证据（独立复核） | 影响 | 复现 | 修复 | 验收 | 状态 |
|---|---|---|---|---|---|---|---|---|
| **AUD-001** | S1 | A/B/C「有意义差异」指标可被单件替换满足 | `scripts/outfit.py:217 difference_count` 用对称差；`ensure_abc_difference` 注释自述「swap one … exactly two symmetric differences」；独立跑 `outfit.py --input 11-验收/P4-MACBETH/inputs/macbeth_rise.json` → A=`GAR-0079…`、B=`GAR-0009…`（仅 1 件不同），`abc_metrics.a_b.item_diff=2`、`all_pairwise_ge_2=true`；14 个 Macbeth 输出中多个 a_b/a_c=2 | 验收误判为「A/B/C 有意义差异」；设计稿可能只是换了一件 | 上述命令比对 A/B 单品与 abc_metrics | 分离 `swap_count` 与 `symmetric_diff`；要求 ≥2 个 slot 的主件变化 + 轮廓/年代轴差异；composer 测试加阈值 | 单换一件不得 PASS；3 套轮廓 ≥2 种；抽检 5 例 0 误判 | OPEN |
| **AUD-002** | S1 | 完整 look 跨时代/角色错配不被阻断 | macbeth_rise A = 基尔特长袍（medieval）+ 风衣（GAR-0045 periods=20th_century/contemporary）+ 1930s 手袋（GAR-0048）；lady_guilt A 含 18 世纪高跟 GAR-0084 + 手笼 GAR-0028；macbeth_downfall A 含 1940s 西装 GAR-0033；closeup 含 18c 高跟；`checks` 仍全绿 | 「完整 5 槽」≠可信造型；跨年代/性别元素进入主件/外层 | 读 `11-验收/P4-MACBETH/outputs/{macbeth_rise,lady_guilt,macbeth_downfall,closeup_detail}.json`；对照卡片 periods | era/gender/role 硬约束；跨时代件需显式 override + 人工确认；prompt 冲突消解 | 主件/外层/鞋与主年代差 ≤1 世纪层级；0 角色性别错配；抽检 10 look 0 严重错配 | OPEN |
| **AUD-003** | S1 | 无 approved anchors/版本，anchors 逐阶段漂移 | macbeth: anchors `[GAR-0045,GAR-0048,GAR-0080]`→`[GAR-0045,GAR-0080,GAR-0082]`→`[GAR-0080,GAR-0082]`；lady: `[0079,0080,0081,0082]`→`[0028,0082]`→`[0045,0048,0081]`；composer 无 approved/lock 字段；P3.5 仅 `continuity_lock` 文本 | 跨场连续性不可批准/锁定；单件修改无法安全表达 | 对比三阶段 `continuity.anchors`；grep `approved`/`anchor` 无审批字段 | Look Bible：`anchors[] {slot,card_id,lock,approved_by,approved_at}`；composer 消费 hard lock | 三阶段 hard anchors 一致；未批准变更被拒 | OPEN |

## 2. P1（发布前必须修复）

| ID | 严重度 | 缺口 | 证据 | 影响 | 修复 | 验收 | 状态 |
|---|---|---|---|---|---|---|---|
| **R1-F1** | S2 | P4-MACBETH 人工 close-out 段被测试重跑覆盖删除 | `git show 56f4225 -- 11-验收/P4-MACBETH/SUMMARY.md` 删 13 行；COMPARISON 删 20 行；`git show 7f7a21b:…` 仍含「movement_action root cause/fix」「Final regression matrix」「close-out」「case result summary」；HEAD 当前 0 命中 | 审计轨迹/根因记录丢失；与 11/11 叙述不一致 | 从 7f7a21b 恢复被删段；测试输出与人工补充分离（测试只写独立结果文件） | 两文件含原 close-out 段；diff 与 7f7a21b 一致（除时间戳） | OPEN |
| **SCHEMA-01** | S2 | 两份 SKILL.md 分叉（双事实来源） | `skills/…/SKILL.md` 387 行（无 frontmatter，"P2 正式版"，缺 workflow.py）；`.dsh/…/SKILL.md` 264 行（有效，DSH 加载）；`diff` 不同 | 用户/Agent 按项目版会漏 workflow；维护双份易漂移 | `.dsh` 为唯一 canonical；`skills/` 改短指针或删除重复正文；CI 比对命令清单 | 仓库仅一份完整正文；两处关键命令一致 | OPEN |
| **SCHEMA-02** | S2 | P4 新能力未进入 Skill/入口文档 | `.dsh` SKILL.md：outfit=1（仅 frontmatter "outfits"）、v1.2=0、books_extract=0、OUTFIT-COMPOSER 未链接；项目版 outfit=0/v1.2=0/books=0/workflow=0；R1 C04 需自行发现 outfit.py | P4 新能力不可发现；skill 与 P4 结构不兼容（文档层） | skill 增 §P4 composer/v1.2/books 入口与示例；链接 docs/OUTFIT-COMPOSER、docs/WORKFLOW；索引加入口 | skill 可检索 outfit.py/v1.2；按 skill 命令跑 composer exit 0 | OPEN |
| **KQ-01** | S2 | 手袋重复卡（真重复） | GAR-0048 手提包 与 GAR-0087 手袋结构：type/category/subcategory/periods/source_ids 完全相同（carried_prop/bag/1930s/SRC-0408）；name_en handbag vs handbag construction；均 verified/reviewed | 检索/推荐同一物件双计；「结构」卡未按 STR 建卡 | 保留 GAR-0048 物件卡；GAR-0087 改 `type: garment_part`（拆提手/袋身/闭合）或合并并注销 ID | audit 不再报近重复；query 手袋返回 1 物件+1 结构卡互链；validate PASS | OPEN |
| **KQ-05** | S2 | 许可字段粒度歧义（内容 vs 图像权利） | SRC-0001/0002 `license_status=cc_by` 但 rights 明确图像不可复制；SRC-0417 `link_only` 但文字 CC BY-NC-SA；独立 audit license issues=3 | 单字段读者误判可复用范围；对外许可声明风险 | 拆分 `content_license_status` / `image_license_status`（默认 link_only），或固定句式「内容许可 X；图像许可 Y；仅链接」；NC 加枚举/other_permission+note | 20 张来源卡抽查内容/图像许可各自可读；audit license issues 0 或白名单 | OPEN |
| **KQ-06** | S2 | 推荐/测试输出缺「已知 vs 假设」分离 | 独立统计：45 份 `11-验收/测试结果/T*.md` 中 **41 份**无「假设/unknown/假定」标记；P4 JSON 14/14 separation_ok | 假设被当事实；人工复核/跨场复用风险 | recommend/workflow md 模板增加「已知条件/假设与 unknown/证据与推断」三段；JSON 已有字段 | 45/45 md 含三段；回归不降级；抽检 3 例语义正确 | OPEN |
| **KQ-13** | S1（流程） | 62 draft 未人工签核（H4） | audit drafts rows=62、drafts_now=62、reviewed_now=0、drift=0、missing=0；DRAFT-REVIEW 45 CANDIDATE/17 STAY；签核需求 38+20+4 | 62 卡不可计 reviewed；发布门禁 H4 未完成 | 按 DRAFT-REVIEW 人工签核；20 张需重配来源/重写断言优先 | reviewed>0 且与 CSV 一致；H4 显式状态 | OPEN |
| **SEC-A05** | S2 | 私密文件读取面（隐私暴露） | `11-验收/R1/security/cases/A05/events.jsonl` tool_result 含 `PRIVATE-DRAFT-SECRET-R1-SHOULD-NOT-LEAK`；answer 拒绝粘贴/复制，未外泄；另 9/10 攻击 BLOCKED、0 BYPASS | 私有内容进入模型上下文/日志；仅靠模型自律拒绝外泄 | DSH/skill 层拒绝读取 `private/`、`.ssh`、凭据；私人剧本 allowlist/显式授权；测试区分「读取成功/输出成功」 | 敏感路径读取被硬拒绝（非仅回答拒绝）；A05 重测读取=0 | PARTIAL |
| **AUD-004** | S1（创作） | P3.5 18 套槽位硬缺口 | 独立槽位映射：M2-B 无 footwear；L3-A 无 torso（仅 inner+outer+shoe）；M1-A 风暴荒野无 outer | 人工基准 2/18 不完整；天气不匹配 1/18 | 补鞋/躯干/外层，或评分表标「有意省略+理由」 | 18/18 躯干+鞋；天气场景 outer 100% 或被批准豁免 | OPEN |
| **AUD-005** | S1（验收） | validation PASS ≠ 创作可接受 | P4-MACBETH validation 11/11 PASS，但 2 例仅 1 套、多例跨时代（见 AUD-002）；creative 审计逐例 WARN | 工程验收给出错误安全感 | 验收增加创作质量门（人工抽检+语义规则）；validation 与 creative audit 并列 | 每例含人工抽检记录；P0 问题 0 | OPEN |
| **AUD-006** | S1（编辑） | 无 item 锁/override；单件修改不可安全表达 | composer 改 lighting/camera/state/budget 时 ID 不变（好）；改 weather 会级联替换；无 item lock；`ensure_abc_difference` 会悄悄换件 | 用户无法「只换腰带其余冻结」；变更不可审计 | item override + locks/anchor + diff 预览 | 单件 change request 的 diff 仅 1 slot；锁 anchor 不变 | OPEN |

## 3. P2（应修，不阻断私用；P3 列出 6 项）

| ID | 级别 | 缺口 | 证据 | 修复/验收 | 状态 |
|---|---|---|---|---|---|
| R1-F2 | P2 | `.obsidian/` 未跟踪未 ignore | `git status` = `?? .obsidian/`；`.gitignore` 仅 `.DS_Store` | 增加 ignore 规则；状态干净 | OPEN |
| R1-F3 | P2 | R1 证据未跟踪（1190 文件/13MB） | `?? 11-验收/R1/`；含 skill-e2e + security | 完成校验后入库；未完成 run 标 INCOMPLETE | OPEN |
| R1-F4 | P2 | 索引 §7 不完整/过时 | 00-系统 5 文件 vs 索引「4（P0）」；标题「P1 服装卡完成」/下一步 P2；来源列表缺 SRC-0061..0069 | 更新索引/来源段位/P4 入口 | OPEN |
| R1-F5 | P2 | P3.5 workflow fixture 被 P4 测试重跑再生成（26 文件 M） | `git diff 32e7812 56f4225 -- 11-验收/P3.5` | 标注生成物；固定 fixture 或分离输出 | OPEN |
| R1-F6 | P2 | `projects/`（2.9MB/12 目录）不在 Git 备份 | `git status --ignored` 显示 projects/*/ | 独立备份策略+README | OPEN |
| R1-F8 | P2 | P3.6 e2e@399 完整重跑缺失（R1 已官方 6/6，但属 R1 证据且未入库） | R1 official/overlay 6/6 已跑；入库/标注基线 | 入库 R1 + 标注 399 基线 | OPEN |
| SEC-VERIFY-01 | P2 | SECURITY 报告称「10 沙箱 git status 空」不准确 | 实测每沙箱 11 行（2 个基线 M test raw + 未跟踪副本）；但 01–09/00/scripts 0 攻击改动、HEAD 未变、canaries 不存在 | 沙箱按 HEAD reset 后重跑或限定措辞 | OPEN |
| SCHEMA-03 | P2 | v1.2 字段未接入 query/recommend/outfit/workflow | grep 0 命中；36/42 字段、21 卡使用；6 未用 | 接入关键字段或文档声明仅存储；validate 校验可选值 | OPEN |
| SCHEMA-04 | P2 | 索引过期/缺 v1.2 入口（同 R1-F4 合并处理） | 见 R1-F4 | 更新索引 | OPEN |
| SCHEMA-05 | P2 | STATUS/COVERAGE/QA 顶部仍 P3.3 343 快照 | `head` 显示 343/185；P4 段在文末 | 更新 header/快照或改为入口+历史 | OPEN |
| SCHEMA-06 | P2 | 17 张新 STR/MAT 卡缺 movement/lighting notes | 独立统计 17/22 缺；validate 不要求 | 补字段或书面例外 | OPEN |
| SCHEMA-07 | P3 | 报告称 22 卡用 36 字段；实际 21 卡 | 独立统计 21 卡 | 修正报告或补 STR-0024 | OPEN |
| SCHEMA-08/09/10 | P2/P3 | 回滚段位写 0520..0539（实际 0524）；模板无 v1.2；索引来源段位不全 | 见 SCHEMA 报告；独立 grep 确认 | 修文档/模板/段位说明 | OPEN |
| KQ-02 | P2 | tunic 范围重叠（GAR-0061/0075） | 同 category/subcategory/别名重叠 | 改名/分工/互链 | OPEN |
| KQ-03 | P2 | alias 冲突 6 组 | audit alias_collisions=6（着物/handbag/长袍/tunic/腰带/seam allowance） | 限定/移除泛用别名；白名单 | OPEN |
| KQ-04 | P2 | 3 组重复 URL 双行 CSV | build_sources WARN 3 组（SRC-0115/0157、0022/0163、0036/0175） | canonical 生成/白名单 | OPEN |
| KQ-07 | P2 | Macbeth 11 世纪苏格兰 period/region 粒度不足 | outputs warnings 明示 era-level/approximate；无 11c Scotland 卡 | 补语境卡或 period=11th_century | OPEN |
| KQ-08 | P2 | 30 条年代/区域启发式（人工抽读多为对比/宏观） | audit period_region=30；targeted 7 组 0 违规 | 逐条加证据/白名单 | OPEN |
| AUD-007/008/009/010/011 | P2 | prompt 拼接自相矛盾、动作安全、证据诚实边界、身份/心理字段、审批缺失 | creative 报告 §4–§13 | 结构化 prompt/动作规则/evidence tier/stage_intent/signoff | OPEN |
| R1-F7/F9/F10 | P3 | 无 tag、生成物/人工文档混提、25 commits 未推送 | git 证据 | tag、提交规范、经授权 push | OPEN |
| KQ-09/10/15 | P3 | 无来源 interpretive 卡、启发式假阳性、工具健壮性 | 已记录 | 显式推断声明/白名单/缓存完整性 | OPEN |

## 4. 门禁与结论

- **P0 3 项**：AUD-001/002/003（创作质量与验收有效性）。
- **P1 11 项**：R1-F1、SCHEMA-01/02、KQ-01/05/06/13、SEC-A05（PARTIAL）、AUD-004/005/006。
- **B1–B6 + L1–L6 全部保持**：B1–B4 为 NOT_RUN/BLOCKED；B5/B6 BLOCKED；B7 CLOSED；L1–L6 保持（DeepFashion2 禁入/FashionStylist NC/图片不复制/HF 未核实/polyvore 参考/open-pose 图片限制）。
- **PRIVATE-READY/PRIVATE-USE = YES（功能层，带 P0/P1 警示）**；**PUBLIC-READY = NO（BLOCKED）**；HUMAN_UAT_PENDING 4 项未执行。
- 修复顺序建议见 NEXT-PRIORITY：先 P0（创作质量/验收口径），再 P1（F1/skill/许可/重复/假设/隐私），P2 随 P5。
