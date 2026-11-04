# projects/ — 用户项目隔离区

这里放**用户自己的**剧本、角色资料、选角笔记和 workflow 生成结果。
知识库目录（`01-` … `11-`）是共享资产，请不要把用户材料写进去。

## 目录约定

```text
projects/
  <project-slug>/
    script.txt            # 用户剧本/场次（原文，勿改知识库）
    meta.json             # 人物/时代/地域/风格/预算/stages
    characters/           # 角色资料、参考、casting notes
    outputs/              # workflow.py / recommend.py 的输出
      character-dossier.md
      scene-costume-table.csv
      full-looks.md
      prompts.md
      continuity-plan.md
      fact-evidence-inference.md
      workflow-result.json
```

## 使用

```bash
cd /Users/coffee/Desktop/Costume-Director-Vault-Starter
python3 scripts/workflow.py \
  --script projects/<slug>/script.txt \
  --meta projects/<slug>/meta.json \
  --out projects/<slug>/outputs
```

- `--out` 必须位于 Vault 内；`projects/<slug>/outputs` 是推荐位置。
- 生成结果中的 `GAR-*`/`SRC-*` 只来自知识库脚本，不得手改/伪造。
- 用户材料默认被 `projects/.gitignore` 忽略，不污染仓库。
- 需要共享/归档时，由项目负责人在 `projects/<slug>/` 内自行创建 README 摘要；
  不要把用户隐私内容提交到知识库。
