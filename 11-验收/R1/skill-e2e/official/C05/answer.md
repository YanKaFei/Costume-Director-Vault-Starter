## 结果（各 10 条，默认上限）
旗袍/qipao：**两条查询的 ID、分数、排序完全一致**——GAR-0031·SRC-0200/0201（8.6）、LOOK-0009·SRC-0200/0201/0205（8.2）、SRC-0200/0201（7.68）。

立领：GAR-0031、GAR-0032·SRC-0202（3.15）、LOOK-0009、LOOK-0012（3.0）。

stand collar：LOOK-0019、STR-0001·SRC-0101（5.5）、GAR-0031（3.15）、GAR-0076·SRC-0482/0483（3.15）。

腰带：GAR-0066·SRC-0427、GAR-0080·SRC-0487/0488（8.4）、SRC-0050/0427/0487/0488（7.68）。

belt：GAR-0080（8.4）、SRC-0050/0487/0488（7.68）、GAR-0066（4.2）。

## 差异
1. **别名只扩中→英，英文不反查**：旗袍扩展出 qipao 和 cheongsam，所以与 qipao 查询的 ID、分数、排序完全相同；立领则依靠 stand collar 和 stand-up collar 命中 prompt_en。
2. **英文多词未加引号会被拆开**：stand collar 被拆成 stand 和 collar 后取平均分；其中 collar 在 name_en 字段上的权重为 8，因此把 LOOK-0019、STR-0001 的得分提高到 5.5。加 `--phrase` 后只返回 5 条，而且还会漏掉写作 stand-up collar 的 GAR-0031。
3. **字段权重差异**：name 字段权重为 8，高于 prompt_en 的 3，更高干 body 的 1。腰带查询因为命中 GAR-0066 的中文名，得分 8.4；belt 只命中它的 subcategory 字段，得分跌至 4.2；此外，立领查询还会把 GAR-0002/0007/0041 等只在 body 中有弱匹配的卡一并带出。
