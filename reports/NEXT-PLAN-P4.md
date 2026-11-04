# 下一步计划（NEXT-PLAN-P4，进入 P5）

- 基准：2026-11-04 16:26；399 卡（内容 188 + 来源 211）；HEAD `7f7a21b`
- 现状：P4 全交付独立验收 PASS；**PRIVATE-READY/PRIVATE-USE = YES**；**PUBLIC-READY = NO（BLOCKED）**；HUMAN_UAT_PENDING 4 项未执行
- 原则：公共发布先清 B1–B6 + P4 许可阻断；质量/覆盖改进不得破坏旧 CLI/JSON/退出码契约

## 1. 公共发布阻断（必须关闭，不得跳过）

| # | 阻断 | 状态 | 解除条件 |
|---|---|---|---|
| B1 | Obsidian GUI UAT | NOT_EXECUTED | 按 `reports/OBSIDIAN-UAT-CHECKLIST.md` 执行 + 两人签字 |
| B2 | 逐图版权核验 | NOT_EXECUTED | 逐图记录许可（当前 0 图片/0 下载；视觉索引仅链接） |
| B3 | 15 案例人工评分 | NOT_SCORED | `11-验收/P3.5/人工评分表.md` 完成 + Lead 签字 |
| B4 | 62 draft 人工复核 | PENDING | 45 REVIEWED-CANDIDATE 签核；17 STAY_DRAFT 处置 |
| B5 | W1–W4 披露 | 待 Lead | 发布说明写明已知缺口/example/interpretive 语义 |
| B6 | 公开/商业许可复核 | PENDING | FIT CC BY-NC-SA、other_permission、link_only 图像逐条；法务签字 |
| **L1** | **DeepFashion2 禁入** | 保持 | 不导入；如需要，联系作者取得书面许可 |
| **L2** | **FashionStylist 非商业** | 保持 | 仅内部非商业；商业产品不得使用 |
| **L3** | **图片不复制/不内嵌** | 保持 | 所有来源图片只链接；引图前逐图授权 |
| **L4** | **HF 资源许可未核实** | 待核实 | Garments2Look 数据集/LoRA、fashion-clip 权重：网络可达后核实 |
| **L5** | **polyvore 数据条款不清** | 保持 | 仅方法论参考；不得导入数据/图像 |
| **L6** | **open-pose 图片非商业/禁转发** | 保持 | 仅内部非商业研究；不复制图片 |

## 2. P5 优先级（非阻断改进）

| # | 任务 | 验收标准 |
|---|---|---|
| 1 | **书籍结论落地**：把 31 条术语结论的 15 条 verified 候选纳入卡片/词典（需 architect 二次核实 + 现代研究校正） | 新增卡片均含书内定位 + 独立佐证；candidate/partial 不升级 |
| 2 | **Composer 硬化**：P4-MACBETH 对比用例 `continuity_states_explicit=false`（输入未给 states）→ 在测试输入补跨场 states 或文档强调必填 | Macbeth 对比 11 例与 composer 9 例保持 PASS；无假状态 |
| 3 | **视觉索引补全**：1 条无关联卡；MET-API 是否建 SRC 或明确「链接型索引」政策 | 28/28 关联或政策文档化；0 图片不变 |
| 4 | **检索 precision 观察**（94.5%→92.9%）：评估新增 399 卡后的权重/过滤，不破坏旧契约 | relevant@5 ≥4.0、precision 回到 ≥0.94（或书面接受） |
| 5 | **P4 专用 Macbeth 人工评分空表**：补 `11-验收/P4-MACBETH/HUMAN-SCORE.md`（18 套 7 维，空白） | 空表 + 签名栏，不代填 |
| 6 | 覆盖扩展：pattern 3/11→≥6/11、material 补齐 leather/fur/metal/finish；AAT 19 张接入 | 缺口核销；来源引用率 ≥85% |
| 7 | draft 复核：62 → 0（或明确保留策略） | review_status 更新 + 人工签字 |
| 8 | P5 验收基线：399 卡 + 所有测试 + 指标对比归档 | 与本报告格式一致 |

## 3. 发布清单（P5 收口）

- [ ] B1–B6 + L1–L6 全部关闭或书面接受
- [ ] HUMAN_UAT_PENDING 4 项完成并留档（GUI/逐图版权/15 案例评分/draft）
- [ ] 8 套回归全 PASS（validate/build/45 acceptance/quality_eval/9 workflow/9 composer/11 Macbeth）
- [ ] 旧指标：relevant@5 ≥4.0、precision ≥0.94（或接受）、0-hit ≤20%、recommend 0 崩溃
- [ ] 许可：P4 审计 20 源分流保持；新增来源先审计后建卡
- [ ] reports 与 commit 一致（P4-REPORT/P4-COVERAGE/P4-REGRESSION/CHANGELOG-P4/NEXT-PLAN-P4/RELEASE-GATE/STATUS/QA/COVERAGE/SOURCES.csv）

## 4. 建议节奏

1. 第 1 批（1–2 天）：书籍 verified 结论入卡、视觉政策补全、composer 输入补齐。
2. 第 2 批：precision 观察与必要微调（不改旧 CLI 契约）、覆盖扩展。
3. 收尾：B1–B6 人工/法务门禁 + 发布签字。
