# P5-A 覆盖缺口矩阵（P5-COVERAGE-GAPS）

- 生成：2026-11-05 01:24；verifier / task-63；基线：最终树 400 卡（内容 189 + 来源 211）
- 性质：**只做缺口矩阵与建议，不扩卡**；数字由卡片 frontmatter 统计（`type/category/subcategory`）。

## 1. 内容覆盖（189 内容卡）

| 类型 | 数量 | 主要子类 | 覆盖判断 |
|---|---|---|---|
| garment | 88 | one_piece 23、outerwear 12、accessory 11、footwear 9、upper_body 8、headwear 7、lower_body 6、carried_prop 5、specialised 4、inner_layer 3 | 基础面广；鞋履/配饰/头饰仍偏薄 |
| garment_part | 26 | construction 26：领 4、袖 4、腰线 5、闭合 3、门襟 2、长度 2、层搭 2、肩 1、接缝 1、装饰 1、袋结构 1 | 结构覆盖中等；缺「里布/衬/填充、褶裥、开衩、口袋、裤裆结构」细化 |
| material | 11 | woven 4、dye 3、trim 2、fiber 1、metal 1 | **明显不足**：无 leather/fur/finish/knit/waterproof 独立卡 |
| pattern | 3 | — | **最大缺口**（条纹/格纹/印花/提花/刺绣等缺失） |
| look | 23 | — | 覆盖 1930s 上海、麦克白、加纳婚礼、护士等；历史/非西方专题仍少 |
| scene | 16 | — | 与 LOOK 配对尚可；缺法庭/宴会/战场等细分 |
| style | 11 | historical 3、cinematic 4、occupational 1、subculture 1、fictional 1、art_movement 1 | 电影类型/亚文化可再扩 |
| period_region | 11 | 1770/1790/1890/1920/1930/1940/1950/1960 英美、上海、奥斯曼、拜占庭 | **无 11 世纪苏格兰/中世纪盛期/18 世纪法国宫廷等**；非西方仅奥斯曼/拜占庭/莫卧儿（garment 内） |

## 2. 关系与来源覆盖（P5-A 后）

| 指标 | 数值 | 缺口/说明 |
|---|---|---|
| 有 `relations` 的内容卡 | 142/189（75.1%） | 47 卡无关系：38 draft（look 22/scene 15/style 1）+ 9 低优先 |
| `source_ids` 有可见 SRC 链接 | 193/299 对（64.5%）；143/143 被引用来源可见 | 106 对仍在 38 draft 卡；非 draft 全覆盖 |
| 来源未引用 | **68/211** | vocabulary 19、museum 12、academic 10、reference 9、other 8、image 5、industry 4、dataset 1；含 9 本 P4 书源 |
| 语义分量单点来源 | 65 | 28 无关系 + 27 背景 + 9 书源 + 1 书源；多为真实未引用/独立参考 |
| 导航覆盖 | MOC 9 页：88 GAR / 26 STR / 14 MAT+PAT / 32 鞋履配饰 / 11 PRD / 11 STY / 23+16 LOOK+SCN / 211 SRC | 导航层已全覆盖 |

## 3. 优先缺口（建议顺序，不扩卡）

| 优先 | 缺口 | 建议 |
|---|---|---|
| **P1** | pattern 仅 3；material 无 leather/fur/finish/knit/waterproof | 先补「常用面料族 + 纹样族」最小集（各 3–5 卡），优先被现有 88 garment 引用 |
| **P1** | 9 本 P4 书源未被内容卡引用（只在研究文档） | 按书源结论建最少 1–2 张内容卡或建立「书籍来源 MOC 关系」的可审计关系（不硬连） |
| **P2** | 鞋履 9 / 配饰 11 / 头饰 7 偏薄 | 补 20 世纪鞋履/包袋/头饰各 2–3 卡，与 1930s 上海/战时/当代专题配对 |
| **P2** | period_region 缺 11 世纪苏格兰/中世纪盛期/18 世纪法国宫廷 | 先补 Macbeth/历史专题所需语境卡（与 P3.5/P4 案例对应） |
| **P3** | 38 draft look/scene/style 未迁移关系 | 人工复核后按审核队列补关系，不自动迁移 |
| **P3** | 65 来源单点（28 无关系/27 背景/9 书源） | 分类处理：背景源保留独立并标注用途；可接入来源按 source-audit class 接入 |

## 4. 结论

- 内容面：**基础广、细分薄**（pattern/material/鞋履配饰/历史语境最明显）。
- 关系面：P5-A 后「机器引用不可见」基本修复（143/143 来源可见、75% 内容卡有 relations）；剩余缺口集中在 **draft 卡（38）** 与 **未被引用的参考源（68）**，属真实独立或待人工接入。
- 不建议用「硬连/猜测关系」提高连通率；应按 MOC/审核队列逐步接入。
