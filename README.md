# Costume Director Knowledge System — Obsidian Starter

这是 **Obsidian 可浏览、AI 可检索** 的服装/造型知识库与启动包（半成品→持续维护型），不是完成的服装史。用 Obsidian “打开本地文件夹作为仓库”即可浏览；Agent 通过仓库内脚本检索/组合造型并给出有来源约束的提示词。

## 当前状态（R1.2，2026-11-05）

| 项 | 值 |
|---|---|
| 卡片 | **458 = 224 内容 + 234 来源** |
| 关系 | **345（high 262 / medium 83）**；relation_consistency **0 errors** |
| 校验 | validate **458/458 PASS**、build_sources **234 PASS**、graph **typed_unresolved 0 / unresolved 0** |
| 来源可见 | source_ids **478/478（100%）**；MOC **224/224 内容 + 234/234 来源** |
| draft | 79（其中 38 基线 draft 待人工；未自动提升） |
| GUI | **NOT_RUN / HUMAN_UAT_PENDING**（11 项见 `reports/R1.2-GUI-UAT.md`） |
| quality_eval | **NOT_RUN**（最近一次超时；旧 PASS 不作当前证据） |
| E2E | engineer report：official **3/3**、overlay **3/3** 五项全 true（selected runs；早期探索失败不计） |
| 发布门禁 | PRIVATE-USE = **YES（附 WARN/P1）**；PUBLIC = **NO（B1–B6、L1–L6 未关闭）** |

## 快速开始

1. **Obsidian**：Open folder as vault → 本目录；从 `00-系统/MOC/README.md` 进入导航。
2. **校验**（仓库根）：
   ```bash
   python3 scripts/validate.py                 # 458/458
   python3 scripts/build_sources.py --check    # 234 sources / CSV
   python3 scripts/relation_consistency.py     # 0 errors / 345 relations
   python3 scripts/graph_analyze.py --root .   # 0 unresolved / 748 typed
   ```
3. **Agent/检索**：`scripts/query.py`、`recommend.py`、`outfit.py`、`relation_trace.py`；`skills/costume-director/` 为统一 skill。
4. **验收/回归**：`scripts/run_acceptance.py`（45）、`scripts/quality_eval.py`、`tests/test_workflow.py`、`11-验收/P4-MACBETH/test_macbeth_p4.py`。
5. **备份**：`python3 scripts/backup_restore.py backup --dest <仓库外目录>` → `verify` → `restore`；详见 `reports/R1.2-MAINTENANCE.md`。

## 目录

- `00-系统/`：数据字典、关系类型 v3、MOC 导航、来源规范
- `01-服装单品/`、`02-结构细节/`、`03-材质纹样/`、`05-风格体系/`、`06-时代地域/`、`07-剧情场景/`、`09-造型组合/`：知识卡
- `04-来源/`：来源卡（234；canonical/deprecated 规则）
- `10-提示词模板/`：生图/视频提示词接口
- `scripts/`、`tests/`、`11-验收/`：工具、测试、验收证据
- `reports/`：STATUS/QA/COVERAGE/RELEASE-GATE/各阶段报告
- `config/obsidian/`：可移植 Obsidian 配置模板（dry-run/apply/restore）

## 数据安全（重要）

- `projects/` 为**私有生产目录**：git 忽略、主备份排除；**当前无独立私有备份（P1）**——请立即单独加密备份。
- 全量备份请放**仓库外**并保留 verify/restore 记录；`/tmp` 仅临时。
- 不下载/嵌入版权不明图片；书源 page 多为 UNCONFIRMED；0 图片策略。
- 不得向公网上传本地剧本/私人项目；GUI 验收前 PUBLIC 门禁保持 BLOCKED。

## 关键参考

- [Fashionpedia](https://fashionpedia.github.io/home/index.html) · [Getty AAT](https://www.getty.edu/research/tools/vocabularies/aat/) · [FIT Fashion History Timeline](https://fashionhistory.fitnyc.edu/) · [Met Open Access](https://github.com/metmuseum/openaccess) · [Costume Designers Guild](https://costumedesignersguild.com/what-is-costume-design/)

## 当前限制

- GUI 人工验收未执行（仅默认前后截图，见 `reports/obsidian-graph/`）。
- quality_eval 当前未通过（超时）；E2E engineer report：official 3/3、overlay 3/3 五项全 true（selected runs；早期探索失败不计）。
- 6 flags、38 draft、59 isolates、18 候选（16+2）仍待人工/审批；不自动提升。
- 详细状态与门禁见 `reports/STATUS.md`、`reports/RELEASE-GATE.md`、`reports/R1.2-FINAL.md`。
