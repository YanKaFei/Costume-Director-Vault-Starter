# R1 下一步优先级（NEXT-PRIORITY）

- 定稿：2026-11-04 18:25；verifier / task-51；快照 HEAD `56f4225`（399 卡）
- 依赖材料：INTEGRATION-AUDIT（FINAL）、GAP-ANALYSIS、REGRESSION-MATRIX、六份 R1 审计
- 原则：P0 先行；不解除 B1–B6/L1–L6；人工项 NOT_RUN 不得标 PASS

## 1. 立即修复（P0，创作可信度/验收有效性）

| # | ID | 动作 | 验收 |
|---|---|---|---|
| 1 | **AUD-001** | composer 分离 `swap_count` 与 `symmetric_diff`；A/B/C 至少要求 2 个 slot 主件变化 + 轮廓/年代轴差异；测试加「单换一件不得 PASS」用例 | 单换一件不 PASS；3 套轮廓 ≥2 种；抽检 5 例 0 误判 |
| 2 | **AUD-002** | 对主件/外层/鞋增加 era/gender/role 硬约束；跨时代需显式 override + 人工确认；prompt 冲突消解（era=none 件不进主件/外层） | 主件/外层/鞋与主年代差 ≤1 世纪层级；0 角色性别错配；抽检 10 look 0 严重错配 |
| 3 | **AUD-003** | 引入 `anchors[] {slot,card_id,lock,approved_by,approved_at}`（Look Bible 最小字段）；composer 消费 hard lock | 三阶段 hard anchors 一致；未批准变更被拒 |

## 2. 发布前必须修复（P1）

| # | ID | 动作 | 验收 |
|---|---|---|---|
| 4 | **R1-F1** | 从 `7f7a21b` 恢复 P4-MACBETH SUMMARY/COMPARISON 的人工 close-out 段；测试只写独立结果文件，不覆盖人工段落 | 两文件含原 close-out；diff 与 7f7a21b 一致（除时间戳） |
| 5 | **SCHEMA-01** | `.dsh` 唯一 canonical；`skills/` 改短指针或删除重复正文；CI 比对关键命令清单 | 仓库仅一份完整正文；两处命令一致 |
| 6 | **SCHEMA-02** | skill 补 P4 入口：`scripts/outfit.py`、v1.2 字段、`scripts/books_extract.py`、`docs/OUTFIT-COMPOSER.md`/`WORKFLOW.md` | skill 可检索到 outfit/v1.2；按 skill 命令跑 composer exit 0 |
| 7 | **KQ-01** | GAR-0087 改结构卡（garment_part）或合并入 GAR-0048；保留互链 | audit 不再报近重复；query 手袋 → 1 物件 + 1 结构卡；validate PASS |
| 8 | **KQ-05** | 拆分 `content_license_status` / `image_license_status`（默认 link_only）或固定句式；NC 映射说明 | 20 卡抽查内容/图像许可均明确；audit license issues 0/白名单 |
| 9 | **KQ-06** | recommend/workflow md 模板增加「已知条件 / 假设与 unknown / 证据与推断」三段 | 45/45 T md 含三段；回归不降级；抽检 3 例语义正确 |
| 10 | **KQ-13** | 62 draft 人工签核：38 普通 + 20 需重配来源/重写断言 + 4 确认 example | reviewed>0 且与 CSV 一致；H4 显式记录 |
| 11 | **SEC-A05** | DSH/skill 层拒绝读取 `private/`、`.ssh`、凭据；私人剧本 allowlist/显式授权；测试区分「读入」与「输出」 | 敏感路径读取被硬拒绝；A05 重测读取=0 |
| 12 | **AUD-004/005/006** | 补 M2-B 鞋/L3-A 躯干/M1-A 外层或书面豁免；验收增加创作质量门；composer 增加 item lock/override + diff | 18/18 躯干+鞋；每例人工抽检记录；单件变更 diff 仅 1 slot |

## 3. P5 建议（结构/能力，非阻断）

1. **Look Bible 数据模型**：版本/status/approved anchors/change_log/单件 diff → 先 schema（JSON/YAML）+ 2 样例 look，再 composer 锁定，最后审批流。
2. **Composer 质量**：A/B/C 轴（轮廓/年代/正式度）、era/gender/role 硬约束、prompt 冲突消解、item lock/diff、信号灯（domain_fit 从「记录」变「约束」）。
3. **Skill/文档统一**：`.dsh` canonical、P4 入口、CI 比对、索引/STATUS/COVERAGE/QA 快照更新。
4. **v1.2 消费闭环**：query/recommend 读取关键可选字段并加过滤；validate 校验可选值白名单；或文档明确「仅存储、不检索」。
5. **知识一致性**：合并/重分类重复卡（GAR-0048/87、GAR-0010/0019 等按审计）、6 组 alias 冲突、3 组重复 URL、KQ-02/03/04/07/08 小步修。
6. **安全硬化**：敏感路径 deny、KB 写/git commit/release 硬门禁（hook/allowlist）、注入特征扫描、日志记录拒绝事件。
7. **仓库卫生**：`.obsidian/` ignore；R1 证据入库并标注完成状态；恢复 F1；annotated tag（p3.6/p4）；经授权 push；projects/ 独立备份。
8. **人工门禁**：B1–B6 + H4 由人工完成并签字，不得代填。

## 4. 发布门禁（保持，不得自动解除）

| 门禁 | 状态 |
|---|---|
| B1 GUI UAT | **NOT_RUN / BLOCKED** |
| B2 逐图版权 | **NOT_RUN / BLOCKED** |
| B3 15 案例人工评分 | **NOT_RUN / BLOCKED** |
| B4 62 draft 复核 | **PENDING / BLOCKED** |
| B5 W1–W4 披露 | **BLOCKED（待 Lead）** |
| B6 公开/商业许可 | **BLOCKED（待法务）** |
| B7 CSV | CLOSED（PASS） |
| L1–L6 | **BLOCKED/保持**（DeepFashion2 禁入、FashionStylist NC、图片不复制、HF 未核实、polyvore 参考、open-pose 图片限制） |
| PRIVATE-READY / PRIVATE-USE | **YES（功能层，带 P0/P1）** |
| PUBLIC-READY | **NO（BLOCKED）** |
| HUMAN_UAT_PENDING | **4 项未执行** |

## 5. 五问速答（详见 INTEGRATION-AUDIT §2）

1. **P3.6×P4 是否真正整合？** 部分整合：运行时 PASS（官方/overlay e2e 各 6/6、45/45、composer 9/9、Macbeth 11/11），但入口/文档/检索/快照未整合（SCHEMA-01/02/03/04/05）→ 不能宣称完整整合。
2. **可私用功能？** 检索/推荐、workflow、composer、Skill 原生调用、书籍研究、CC0 视觉索引（仅链接）均可用；带 P0 创作质量警示与 A05 隐私 PARTIAL。
3. **必须立即修复？** AUD-001/002/003；R1-F1、SCHEMA-01/02、KQ-01/05/06、SEC-A05、KQ-13、AUD-004/005/006。
4. **P5 建议？** 见 §3（Look Bible、composer 质量/锁、skill 统一、v1.2 消费、知识一致性、安全硬化、仓库卫生、人工门禁）。
5. **重大风险？** 知识/证据丢失（F1 已发生、R1 13MB 未入库、无 tag/无 push、projects 无备份）；版权（L1–L6、KQ-05、逐图未核验）；「通过」幻觉（A/B/C 指标、跨时代、validation PASS≠创作可接受）；越权/隐私（A05 读取私密文件、缺硬门禁）。

## 6. 建议节奏

1. **本周**：P0（AUD-001/002/003）+ P1 前 4 项（F1、SCHEMA-01/02、KQ-01）→ 重跑 composer/Macbeth/skill e2e。
2. **下周**：KQ-05/06/13、SEC-A05、AUD-004/005/006；更新索引/STATUS/COVERAGE/QA；R1 证据入库。
3. **P5 第一轮**：Look Bible schema + composer lock/diff；之后再 UI/审批。
4. **发布收口**：人工 B1–B6/H4 完成并签字；L1–L6 法务结论；私有发布说明标注 P0/P1 处置状态。
