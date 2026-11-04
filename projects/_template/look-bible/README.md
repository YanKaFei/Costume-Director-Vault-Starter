# Look Bible（项目级，R1.1-E / AUD-003）

Look Bible 是**项目级**的已批准服装清单，放在 `projects/<slug>/look-bible/`，不写入 `01–09` 公共知识卡。它解决跨场次 anchor 漂移：批准后的 hard anchor 不因单件修改而被静默覆盖。

## 文件

| 文件 | 作用 |
|---|---|
| `look-bible.json` | 主数据：looks、status、version、slots、approved_anchors、change_log、approvals |
| `versions/<look_id>/v<N>.json` | 每次变更的不可变快照（用于 item-level diff） |
| `signature.example.json` | 审批签名文件示例（真实审批必须替换为 human reviewer 的签名） |
| `examples/aud-004-slotfix.json` | AUD-004 P3.5 槽位修复示例（M2-B 鞋、L3-A 躯干层） |
| `README.md` | 本说明 |

## 状态机

```
Draft --propose--> Proposed --approve(reviewer+signature)--> Approved
```

- **Draft**：可自由增删 slot。
- **Proposed**：已提交人工评审；不允许自动批准。
- **Approved**：`approved_anchors.hard` 冻结；单件变更必须走 `patch`，只产生 item patch，不得重写整 Look。
- **Agent 不得自行 Proposed→Approved**：`approve` 必须同时提供 `--reviewer` 与 `--signature-file`；签名 JSON 的 `role` 必须为 `human`/`reviewer`，且 reviewer 不能是 agent/ai/bot 等身份。批准记录写入 `approvals[]`（含 reviewer、signature sha256、时间）。

## Anchors

每个 slot：
```json
{"card_id":"GAR-0075","lock":"hard","note":"..."}
```
- `hard`：批准后冻结；任何改变该 slot `card_id` 的 patch 都会被拒绝。
- `soft`：批准后仍可 patch，但会记录 change_log + 新版本；需重新评审。

## 命令

```bash
python3 scripts/lookbook.py init --project my-film
python3 scripts/lookbook.py add --project my-film --look MAC-M1-A --character MAC \
  --slot torso --card GAR-0075 --lock hard --rationale "approved silhouette"
python3 scripts/lookbook.py add --project my-film --look MAC-M1-A --slot footwear --card GAR-0081 --lock soft
python3 scripts/lookbook.py propose --project my-film --look MAC-M1-A
python3 scripts/lookbook.py approve --project my-film --look MAC-M1-A \
  --reviewer "human-reviewer" --signature-file projects/my-film/look-bible/signature.json
python3 scripts/lookbook.py patch --project my-film --look MAC-M1-A --slot footwear --card GAR-0081 --note "approved alternative"
python3 scripts/lookbook.py diff --project my-film --look MAC-M1-A --from 3 --to 4 --json
python3 scripts/lookbook.py validate --project my-film --vault .
```

退出码：0 成功；1 校验/审批/冻结冲突失败；2 argparse 参数错误。`diff` 输出 `item_patch[]`（仅变更的 slot），不重写整 Look。

## AUD-004 槽位修复（示例）

`examples/aud-004-slotfix.json` 记录：
- **M2-B**：补 `footwear = GAR-0081`（皮靴，15 世纪伦敦皮革踝靴，analogue）。
- **L3-A**：补 `torso = GAR-0079`（基尔特长袍，interpretive，作为 chemise 外的躯干层）。
两处均使用既有卡、不改叙事；实际 `11-验收/P3.5` 文件按任务写入范围保持只读，采用迁移补丁方式应用。

## AUD-004 迁移命令

```bash
python3 scripts/lookbook.py migrate-aud004 --project _template
```

## 回滚

Look Bible 是项目级 JSON；把 `look-bible.json` 与 `versions/` 恢复到上一个 git 版本即可（`git checkout -- projects/<slug>/look-bible/`）。公共卡不受影响。
