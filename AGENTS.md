# AGENTS.md — Costume Director Knowledge System

本目录（`/Users/coffee/Desktop/Costume-Director-Vault-Starter`）是唯一允许写入的项目根；面向 DeepSeek Harness / Agent 的服装与造型知识库。详细任务以 `TASKS/` 与 `reports/STATUS.md` 为准；本文件是当前实际命令与规则。

## 当前状态（R1.2，2026-11-05）

- **458 卡 = 224 内容 + 234 来源；345 relations（high 262 / medium 83）**
- validate **458/458 PASS**；build_sources **234 PASS**；relation_consistency **0 errors**；graph **typed_unresolved 0 / unresolved 0 / typed_edges 748**
- source_ids 可见 **478/478（100%）**；MOC **224/224 + 234/234**；59 isolates（+3 dup=62 uncited）；38 基线 draft；6 flags 待人工
- **GUI = NOT_RUN / HUMAN_UAT_PENDING**；quality_eval 当前 **NOT_RUN**（超时；不作 PASS）；**E2E engineer report official 3/3、overlay 3/3 五项全 true**（早期探索失败不计）
- 门禁：PRIVATE-USE **YES（WARN/P1）**；PUBLIC **NO（B1–B6、L1–L6）**

## 必须遵守

1. 唯一根目录；不新建第二套系统（无独立 DB/外部 wiki/影子卡）；不复制 skill/命令副本。
2. 不删除既有笔记、不覆盖来源原件、不下载/嵌入版权不明图片、不上传本地剧本/私有项目。
3. 文件 UTF-8 Markdown + Obsidian YAML frontmatter；固定 ID；事实/解释/design 分层；不伪造证据/HTTP/来源。
4. `projects/` 私有：git 忽略、主备份排除；**不进入公开 git/远程**；需独立加密备份。
5. `medium/review` 不自动升 high/verified；draft 不自动提升；6 flags 不自动关闭；不以卡数/全连通率为目标。
6. 每阶段更新 `reports/STATUS.md`、`reports/QA.md`、`reports/COVERAGE.md`、`reports/RELEASE-GATE.md`；GUI 未验收不得写 PASS。

## 常用命令（仓库根）

```bash
python3 scripts/validate.py
python3 scripts/build_sources.py --check
python3 scripts/relation_consistency.py
python3 scripts/graph_analyze.py --root .
python3 scripts/run_acceptance.py
python3 scripts/quality_eval.py --no-write
python3 tests/test_workflow.py
python3 11-验收/P4-MACBETH/test_macbeth_p4.py
python3 scripts/outfit.py ...          # 造型/提示词
python3 scripts/relation_trace.py ...  # 关系路径检索
python3 scripts/query.py ...           # 检索
```

## Obsidian 配置（跨设备）

- 模板：`config/obsidian/app.recommended.json`、`graph.recommended.json`
- 脚本：`python3 scripts/obsidian_config.py --diff`（默认 dry-run）；`--apply` 前备份 `.obsidian`；`--restore` 回滚 app/graph；不覆盖主题/插件/快捷键/workspace。
- 验收：`tests/test_obsidian_config.py` 6/6；隔离 488 节点/0 零度/1 分量；GUI 仍需人工 11 项（`reports/R1.2-GUI-UAT.md`）。

## 备份/维护

- `python3 scripts/backup_restore.py backup --dest <仓库外目录>` → `verify` → `restore`；排除 projects/.obsidian/sandbox；**P1：私有 projects 需单独备份**；`/tmp` 仅临时。
- 维护 8 步：发现→许可→事实提取→去重→关系校验→人工审核→自动测试→入库；详见 `reports/R1.2-MAINTENANCE.md`。
- 建议 R1.2 后进入维护模式：停止大规模扩卡；优先 GUI 人工、私有备份、quality 已 PASS（4.2/0.921/0）、E2E 3/3+3/3 收口、6 flags/38 draft 人工结论。

## 当前限制

- GUI 未验收；quality NOT_RUN；E2E 保留失败尝试；PUBLIC 门禁未解除；书源 page UNCONFIRMED；4 本背景书未接卡。
- 遇到阻塞/权限问题：报告 BLOCKED，继续离线结构工作，不编造完成证据。
