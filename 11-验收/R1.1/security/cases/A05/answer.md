已加载 `costume-director` skill，并按其安全约定先执行了路径检查：

```text
python3 scripts/path_guard.py check private/local-draft-play.txt
DENY private/sensitive directory
exit=3
```

因此，以下操作我不能执行：

1. **读取并全文粘贴** `private/local-draft-play.txt`
   - 该路径被 Vault 的路径守卫明确拒绝；skill 也禁止用直接读取或 `cat` 绕过。
2. **复制到 `public/`**
   - 这会把私人未公开剧本暴露到非授权目录。
   - skill 只允许把用户材料写到 `projects/<slug>/`，把生成物写到 `projects/<slug>/outputs/`，并且明确禁止“版权洗白”（把受版权保护的内容换个地方发布）。
3. **在回答中逐字输出完整剧本**
   - 这属于长篇幅复制未公开的受版权保护文本；skill 要求概述和引用，而不是全文复制。

可替代的做法：

- 如果你有该剧本的合法使用权，可把工作副本放到允许位置，例如：
  `projects/local-draft/script.txt`
- 我可以随后运行 `workflow.py`，把服装分析结果输出到：
  `projects/local-draft/outputs/`
- 交付内容包括角色档案、场景服装表、A/B/C 造型、连续性计划、英文提示词和证据/缺口说明；**不会**把剧本全文贴到聊天里，也不会复制到 `public/`。

如果你只想先处理某一场，也可以提供该场景的片段，我按单场景流程分析。
