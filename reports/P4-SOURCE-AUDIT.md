# P4 开源资源与书籍许可审计（P4-0 许可门禁）

- 生成：2026-11-04 16:05（Asia/Shanghai）；verifier / task-38（P4-0 资源审查与许可门禁）
- 快照：363 卡（内容 166 + 来源 197）；git HEAD 见 `reports/STATUS.md`（本轮仅写 reports/，未改卡片/脚本）
- 范围：**16 个 GitHub 仓库 + 4 本 Project Gutenberg 电子书**（共 20 项）；大仓库只取元数据与 README/LICENSE，**未整包下载**
- 方法：`gh api`/GitHub REST 取仓库元数据（stars/archived/pushed/license/root files）；`raw.githubusercontent.com` 取 README/LICENSE/NOTICE；curl 取 Gutenberg 小说页与 `pg<id>.txt`；`fashionpedia.github.io/home/data_license.html` 取官方条款
- **候选区规则：本报告所有 PASS 均为「许可清晰、可进入候选整合」之意，不代表已核实为证据；20 项全部为 CANDIDATE 状态（未标 verified，未写入任何卡片）。**
- 配套矩阵：`reports/P4-LICENSE-MATRIX.csv`（20 行 × 14 列）

## 0. 总览

| 指标 | 结果 |
|---|---|
| 审计来源 | **20**（16 GitHub + 4 Gutenberg ebooks） |
| 顶层可访问 | **20/20**（HTTP 200 / gh 元数据成功） |
| 许可清晰、可候选整合（PASS） | **15** |
| 受限/需条件（WARN） | **2**（FashionStylist NC；Garments2Look 数据集许可未核实） |
| 受限/商业与再分发风险（RESTRICTED 类） | **3**（polyvore 数据条款不清；open-pose 图片非商业禁转发；DeepFashion2 无许可） |
| 顶层 INACCESSIBLE | **0** |
| 嵌入资源不可访问（许可因此未核实） | **3**：Garments2Look 数据集、Garments2Look LoRA、fashion-clip 权重（均在 HuggingFace；本网络 SSL 不可达） |
| 与现有 363 卡直接重叠 | **2** 个来源（Fashionpedia 3 张来源卡；Met Open Access 28 张卡）；DeepFashion2 仅间接提及 |
| 可立即私有研究使用 | 15 项 PASS + Garments2Look/fashion-clip 的**代码/本地部分**（数据集/权重除外） |
| 商业/公开传播阻断 | 5 项（见 §D） |

## A. GitHub 仓库逐项审计

> 状态定义：PASS=许可清晰可候选整合；WARN=可用但有明确条件；RESTRICTED=仅限受限场景；FAIL=不可用；INACCESSIBLE=无法访问。所有结论基于实际抓取的元数据/README/LICENSE（网络时间 2026-11-04 15:57–16:04）。

### A1. `cvdfoundation/fashionpedia` — **PASS（数据候选；图像排除）**
- 存在/结构：HTTP 200；180★/18 fork；last push **2020-06-05**（长期未更新，但为官方 canonical 数据仓）；README 指向 S3 图片/标注；**仓库无 LICENSE 文件**。
- 许可拆分：**软件** = BSD 风格（官方 data_license 页）；**数据/本体/网站** = **CC BY 4.0**（页面明文 "licensed under a Creative Commons Attribution 4.0 License"）；**图像** = Flickr/Unsplash/Burst/Freestocks/Kaboompics/Pexels 第三方，Fashionpedia 不拥有 → **不得复制/内嵌**。
- 私人/商业/再分发：私人研究 OK（署名）；本体/注释可商业使用（CC BY 署名）；再分发数据/本体需署名；图像全部禁止。
- 现有重叠：**直接 3 张来源卡**（SRC-0001 主页、SRC-0002 数据集、SRC-0003 许可证据）+ 本体已用于字典分层。
- 质量：本体质量高、类别/属性体系成熟；但 repo 无 LICENSE、2020 后未更新 → 以官方 data_license 页为准，避免把 repo 当维护活跃项目。
- 建议：仅用于**术语/本体/类别候选**；不引入图像；引用时署名 Fashionpedia + CC BY 4.0。

### A2. `metmuseum/openaccess` — **PASS（已采用；数据 CC0）**
- 存在：200；**1452★**；last push **2026-11-02**（活跃）；LICENSE 明确 **CC0-1.0**。
- 许可拆分：数据集 **CC0 1.0**（CSV UTF-8）；**图像不包含在数据集内**，仅当对象页有 CC0 图标时才可用；Met 商标/不得暗示背书；修改/转换须披露。
- 私人/商业/再分发：均允许（数据 CC0；建议署名、避免商标误导）。
- 现有重叠：**28 张卡**（Met 对象来源/卡片）；为现有最大直接来源之一。
- 质量：高（博物馆元数据、持续更新；文档说明 Excel/Mac UTF-8 处理细节）。
- 建议：继续作为**首选可核实对象数据**（CC0）；图像仍走逐图核验（H2）。

### A3. `freesewing/freesewing` — **PASS（MIT；维护迁移风险）**
- 存在：200；488★；**archived**（GitHub 镜像）；last push 2025-04；README 指向 **Codeberg 新家**。
- 许可：**MIT**（LICENSE 全文）；设计/文档随 repo（MIT）；站点图片未单独许可（不作为素材）。
- 私人/商业/再分发：MIT 允许（保留版权/许可声明）。
- 重叠：**0**。
- 质量：设计/制版文档体系强；但 GitHub 已归档、canonical 迁至 Codeberg → 采用时记录来源版本。
- 建议：候选用于**结构/制版术语**；优先 Codeberg 当前版本；不引用站点图片。

### A4. `freesewing/pattern` — **PASS（MIT）**
- 存在：200；9★；**archived 2021**；README 明确 "License: MIT"；LICENSE 全文 MIT。
- 许可：MIT（pattern 库）；无图像语料。
- 私人/商业/再分发：MIT（署名）。
- 重叠：0；质量：小而专的 pattern 库；归档后需确认是否被新仓库替代。
- 建议：候选（MIT）；采用前确认现行版本。

### A5. `recsys-benchmark/FashionStylist` — **WARN（CC BY-NC 非商业）**
- 存在：200；13★；last push 2026-07；LICENSE = **CC BY-NC 4.0**（"NonCommercial — You may not use the material for commercial purposes."）。
- 许可拆分：**软件+数据（Dataset/ CSV：1,000 outfits / 4,637 items，含中英文）** 均在 repo 内，按根 LICENSE 为 **CC BY-NC 4.0**；无独立数据许可；图像示例 assets 同 repo（NC）。
- 私人/商业/再分发：私人研究 OK；**商业禁止**；再分发需署名 + 非商业。
- 重叠：0；质量：2026 论文数据集、结构清晰（outfit/item id、中英 CSV、supplementary PDF）。
- 建议：**仅内部研究/非商业**；若要入产品，必须换许可或只借鉴字段结构（不复制内容）；标注 NC 阻断。

### A6. `xthan/polyvore-dataset` — **WARN/RESTRICTED（数据条款不清；图片不可用）**
- 存在：200；233★；last push 2023-12；LICENSE = **Apache-2.0**；README 说明 21,889 outfits、图片 URL 来自 Polyvore（站点被 SSense 收购，URL 已失效；镜像在 Kaggle）。
- 许可拆分：**代码/仓库文件 Apache-2.0**；**数据（JSON 注释）没有单独许可**（Apache-2.0 可解释覆盖 repo 文件，但数据集出处/第三方权利未清）；**图像** = 第三方 Polyvore 商品图，**无授权**且链接失效。
- 私人/商业/再分发：注释私人研究谨慎可用；商业/再分发**未清**；图像一律不可用/不可再分发。
- 重叠：0；质量：经典 outfit-compatibility 数据集，但维护停止（2023）、图像源已死。
- 建议：**只作方法论参考**，不导入数据/图像；如需注释，先法务确认 Apache 覆盖范围。

### A7. `patrickjohncyh/fashion-clip` — **PASS（代码 MIT）/ WARN（权重许可待查）**
- 存在：200；547★；last push 2025-01；LICENSE **MIT**；README 指向 HuggingFace 权重页（`patrickjohncyh/fashion-clip`）。
- 许可拆分：**代码 MIT**；**训练数据 Farfetch 未公开**（无数据可分发）；**模型权重**在 HF，**HF 页许可未能访问**（SSL 不可达）→ 未核实；README 声称 release weights & code as open source。
- 私人/商业/再分发：代码 MIT 可；模型按 HF 许可（**待核实**）；数据不可得。
- 重叠：0；质量：547★、有论文/Colab/教程；模型适合**风格/语义检索**候选。
- 建议：代码可候选；**权重使用前必须从 HF 页面确认 license**（阻断项 B-06）。

### A8. `Brilliant666/ai-costume-gallery-cn` — **PASS（数据候选；图像排除）**
- 存在：200；135★；active 2026-10-30；README 明示三层许可：**代码 MIT / 中文译文与结构化数据 CC BY 4.0 / 图片不授权**（"图片不授权"）。
- 私人/商业/再分发：数据可（CC BY 4.0 署名）；代码 MIT；**图像不可用**。
- 重叠：0；质量：中文术语/标签镜像（ai-costume-gallery.pages.dev），结构清晰（data/costume-zh.json）；维护活跃。
- 建议：**中文术语候选源**（数据层），图像排除；与 A1/A3 术语可交叉校验。

### A9. `hongye007/open-pose-costume` — **RESTRICTED（图片非商业/禁再分发；代码 MIT）**
- 存在：200；590★；very active（2026-11-03）；README 明确：**代码 MIT**；**自建素材（服饰/姿势/人像图）个人学习与非商业免费，不可商用；任何分发/再分发/转载/打包/转售须事先书面授权**；第三方参考图另有 SOURCES/NOTICES，仓库再分发获维护者确认，但**图片不适用 MIT**；仓库约 1.95GiB 图片资产。
- 私人/商业/再分发：私人非商业研究可；**商业禁止**；**图片再分发禁止**（除 repo 本身授权场景外）。
- 重叠：0；质量：活跃、文档详尽、可运行 web 应用；但素材权利最复杂。
- 建议：**仅内部非商业研究**；**不复制图片**；如用于 prompt 参考，必须只读链接并标注授权限制。

### A10. `switchablenorms/DeepFashion2` — **RESTRICTED / FAIL（无许可）**
- 存在：200；**2641★**；last push 2025-01；**无 LICENSE 文件**；README 无明确 license 条款；数据集 491K 图像（商业店铺 + 消费者照片）、801K 标注。
- 许可：**无任何明示许可 = 默认保留所有权利**；图像来自第三方电商/用户；不可商业、不可再分发、不可用于训练/产品（除作者书面许可）。
- 重叠：仅**间接**（Fashionpedia 来源卡提到其类别映射）。
- 质量：高影响力数据集，但许可缺失是硬阻断。
- 建议：**不导入**（数据/图像/标注均不）；如需，联系作者获取许可；仅可在报告中引用事实描述。

### A11. `ArtmeScienceLab/Garments2Look` — **WARN（代码 Apache-2.0；数据集/模型许可未核实）**
- 存在：200；42★；active 2026-10；LICENSE **Apache-2.0**（代码）；README 指向 **HF 数据集**（98,012 outfit 记录）与 **HF LoRA 模型**；README 未写数据集/模型许可。
- 许可拆分：**代码 Apache-2.0**；**数据集/图像/LoRA**：HF 页面不可达（SSL），**许可未核实**。
- 私人/商业/再分发：代码可；数据集/模型**未知**（不得假设 Apache 覆盖）。
- 重叠：0；质量：新（CVPR2026）、数据规模大、适合 try-on 研究；代码质量中。
- 建议：仅代码候选；**数据集/模型在使用前必须从 HF 核实 license**（阻断项 B-05）。

### A12–A16. GITenberg 5 本电子书镜像 — **PASS（PD 书籍候选）**
| 仓库 | 书/编号 | 许可 | 质量/维护 |
|---|---|---|---|
| `GITenberg/Dress-designAn-Account-of-Costume-for-Artists--amp--Dressmakers_34903` | Dress Design (#34903, 1919) | Public Domain（README）+ PG License（LICENSE 全文） | 静态镜像 2018，0★ |
| `GITenberg/Textiles-and-Clothing_21534` | Textiles and Clothing (#21534) | 同上；README 明文 "This book is in the Public Domain" | 静态 2018 |
| `GITenberg/English-Costume_33020` | English Costume (#33020) | 同上 | 静态 2018 |
| `GITenberg/Costume-Fanciful-Historical-and-Theatrical_48551` | Costume Fanciful (#48551) | 同上 | 静态 2018 |
| `GITenberg/Modern-Design-in-Jewellery-and-Fans_49559` | Jewellery & Fans (#49559) | 同上 | 静态 2018 |
- 共通：**书内容 PD in US**；**GITenberg/PG 文件再分发受 Project Gutenberg License 约束**（保留许可/商标条款）；**无图像资产**（纯文本）；仓库 2018 后未更新（静态镜像，非活跃项目）。
- 私人/商业/再分发：PD 下商业可用；若再分发 PG 制备文件需遵守 PG License；非美国地区需查当地法。
- 重叠：0（现有 363 卡无引用）；质量：可作为**历史/术语线索**，但需与博物馆/学术来源交叉核验（书籍本身为旧时综述）。

## B. Project Gutenberg 电子书（4 本）— **PASS（PD 候选）**

| ID | 标题/作者/年份 | 页面 | 文本 | 许可 | 质量/结构 |
|---|---|---|---|---|---|
| 76299 | A dictionary of men's wear — William Henry Baker, 1908 | 200 | 200（861KB / 20,156 lines） | Public domain in USA；PG License | PGDP 校对；词典体，适合术语候选 |
| 56978 | The Book of the Feet: A History of Boots and Shoes — Joseph Sparkes Hall（1847 版语境） | 200 | 200（285KB / 5,020 lines） | 同上 | 校对；鞋履史候选 |
| 76717 | The history of fashion in France — Augustin Challamel；trans. Frances Cashel Hoey & John Lillie（1882） | 200 | 200（608KB / 11,765 lines） | 同上 | 校对；法国服饰史（1882 史学，需谨慎） |
| 46949 | Chats on Costume — G. Woolliscroft Rhead（1920） | 200 | 200（327KB / 6,923 lines） | 同上 | 校对；通俗综述，适合线索 |

- 共通许可：PG 页头 **"This eBook is for the use of anyone anywhere in the United States…"** + **Public domain in the USA**；再分发 PG 文件须遵守 **Project Gutenberg License**（含商标条款）；非美国用户需查当地法。
- 图像：4 本均以纯文本为审计对象，**PG txt 不含图像**；插图权利不在本审计可用范围。
- 私人/商业/再分发：底层文本 PD（US）；商业使用文本可行；**PG 制备文件再分发需保留许可条款/署名**；不得使用 Project Gutenberg 商标暗示背书。
- 重叠：0（P3.5 的 Macbeth 用 PG #1533，不在本列表；已按 PD 处理）。
- 质量/建议：4 本均为 PGDP 校对文本、结构完整（章节/TOC/脚注）；建议作为**候选二级史料**，与博物馆/学术一手来源交叉核验后再进入卡片体系。

## C. 与现有 363 卡的重叠

| 来源 | 重叠 | 说明 |
|---|---|---|
| Fashionpedia | **直接 3**（SRC-0001/0002/0003） | 已在库；本体/许可页已用 |
| Met Open Access | **直接 28 卡** | 已在库（Met 对象）；CC0 数据 |
| DeepFashion2 | 间接 2 提及 | 仅 Fashionpedia 来源卡提及类别映射，无直接卡 |
| 其余 16 项（含 5 GITenberg + 4 ebooks） | **0** | 全新候选，无重复；接入不会造成重复卡 |

## D. 阻断项与建议分流

### 阻断项（不得进入候选整合）
1. **B-01 DeepFashion2**：无 LICENSE/无明示许可 + 第三方图像 → **禁止导入**（数据/图像/标注）；仅可作文献引用。
2. **B-02 FashionStylist**：CC BY-NC → **禁止商业使用**；只能非商业内部研究；不得进入商业发布物。
3. **B-03 open-pose-costume 图片**：非商业 + 禁止再分发 → 图片**不得复制/打包/再分发**；代码 MIT 可。
4. **B-04 polyvore-dataset**：数据条款不清 + 图像失效/无授权 → **不导入数据/图像**；仅方法论参考。
5. **B-05 Garments2Look 数据集/LoRA**：HF 许可不可达 → **未核实前不得使用**；代码 Apache-2.0 仅覆盖代码。
6. **B-06 fashion-clip 权重**：HF 模型卡许可不可达 → **未核实前不得使用权重**；代码 MIT 可。
7. **B-07 freesewing GitHub 归档/迁移**：非许可阻断，但**维护连续性风险**；采用时固定 commit/记录 Codeberg 替代。
8. **B-08 通用图片规则**：本审计所有来源的图片均**不得直接复制/内嵌**（与 Vault 现有 0 图片策略一致）；图片需逐图核验（H2）。

### 建议分流（candidate 通道）
- **可进入候选整合（PASS，15 项）**：Met Open Access（CC0，已用）、Fashionpedia（数据/本体 CC BY 4.0，图像排除）、freesewing + pattern（MIT，注意归档）、fashion-clip（代码 MIT；权重待 HF 核实）、ai-costume-gallery-cn（数据 CC BY 4.0；图像排除）、GITenberg 5 本（PD 书）、Gutenberg 4 本（PD 书）。
- **仅内部非商业研究**：FashionStylist（NC）、open-pose-costume（图片限制）、polyvore（数据条款待清）、Garments2Look（代码可用、数据待核实）。
- **禁止/待许可**：DeepFashion2（无许可）。
- **使用方式**：全部先入候选区（`source_kind` 标注 + `license_status` 按本矩阵），由 architect/researcher 核验事实后再决定是否建卡；**禁止把任何一项写成 verified**；图像一律 link-only/不引入。

### 对 Vault 的直接影响
- 本轮**不修改任何卡片/脚本**；363 卡与 197 来源不变；`validate`/`build_sources`/45 验收/quality_eval/9 workflow tests 不受影响（本任务不重跑，因仅写 reports/；如 lead 需要可复跑）。
- 建议 researcher 在 P4-1 中把 15 个 PASS 候选登记为 **P4-CAND**（不是 SRC），并优先：Met/Fashionpedia 术语、GITenberg/Gutenberg 书目、freesewing 制版；NC/无许可项只作参考链接。
- 下一步：对 8 本 PD 书抽取章节级候选断言（术语/结构），逐条标注「书 vs 现代研究」差异；对 Fashionpedia/ai-costume-gallery 仅抽类别/术语，不引图像。

## E. 附：审计方法与可复现命令

```bash
# GitHub 元数据（21 个端点）
gh api /repos/cvdfoundation/fashionpedia --jq '{stars,archived,pushed_at,license}'
# README/LICENSE（raw，无 rate-limit）
curl -sS -L https://raw.githubusercontent.com/metmuseum/openaccess/HEAD/LICENSE
# Gutenberg 电子书与文本
curl -sS -L -o ebook.html https://www.gutenberg.org/ebooks/76299
curl -sS -L -o pg76299.txt https://www.gutenberg.org/cache/epub/76299/pg76299.txt
# Fashionpedia 官方许可页
curl -sS -L -o fp_license.html https://fashionpedia.github.io/home/data_license.html
# HuggingFace（本网络不可达 → 许可未核实）
curl -sS -L https://huggingface.co/api/datasets/ArtmeScienceLab/Garments2Look   # SSL_ERROR_SYSCALL
```
- 网络限制：**HuggingFace 在本环境 SSL 不可达**（huggingface.co/api → SSL_ERROR_SYSCALL），因此 Garments2Look 数据集/LoRA 与 fashion-clip 权重许可标记为 **未核实**，未做任何假设。
- 书页/文本抓取时间：2026-11-04 15:57–16:04；GitHub 元数据时间 15:57–16:00。
- 证据留存：`/tmp/p4/`（repos.json、fetch_results.tsv、files/、ebook_*.html、pg*.txt、fp_license.html、git_license.txt、openpose_terms.txt、retry_*）。

## F. 结论

- **可访问性**：20/20 顶层可访问；0 顶层不可达；3 个嵌套 HuggingFace 资源不可达（许可未核实）。
- **可用（PASS，15）**：Met Open Access、Fashionpedia、freesewing×2、fashion-clip（代码）、ai-costume-gallery-cn（数据）、GITenberg×5、Gutenberg×4 —— 均可作为**候选**进入 P4 整合流程（署名/条款约束见矩阵）。
- **受限（WARN/RESTRICTED，5）**：FashionStylist（NC）、polyvore（数据条款不清/图像不可用）、open-pose-costume（图片非商业/禁转发）、DeepFashion2（无许可）、Garments2Look（数据集/LoRA 许可未核实）。
- **阻断**：DeepFashion2（无许可）与所有图像复制/内嵌；商业/公开传播前需按矩阵逐项确认（尤其 NC/无许可/HF 未核实项）。
- **候选区规则**：全部 20 项均为 CANDIDATE，未标 verified；未写任何卡片。
