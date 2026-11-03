---
id: SRC-0100
type: source
name_zh: 大都会艺术博物馆开放数据：19 世纪日本和服
name_en: 'The Met Open Access object data: Japanese kimono (19th century)'
category: source
subcategory: museum_collection
aliases: []
periods: []
regions: []
style_tags: []
colors: []
materials: []
source_ids: []
evidence_status: verified
review_status: reviewed
license_status: cc0
url: 'https://collectionapi.metmuseum.org/public/collection/v1/objects/125953'
publisher: The Metropolitan Museum of Art
date_accessed: 2026-11-04
rights_statement: The Met Open Access；该对象 isPublicDomain=true。元数据与图像权利分开核验；本卡不内嵌图片。
source_kind: museum_collection
note: curl 实测：HTTP 200（objects/125953 JSON）；人类可读页本次核验 HTTP 429（Met 限流），以 API 数据为核验对象（2026-11-04）；可支撑主题见正文。
tags: [costume, source, museum_met]
---
# SRC-0100 大都会艺术博物馆开放数据：19 世纪日本和服

## 定义
大都会艺术博物馆 Open Access 馆藏对象的 JSON 元数据接口，返回 objectID、标题、年代、文化、材质、尺寸、分类、入藏信息与公共领域状态。

## 结构要点
- 发布机构：The Metropolitan Museum of Art
- 来源类型：museum_collection
- 页面/接口：https://collectionapi.metmuseum.org/public/collection/v1/objects/125953
- 核验命令：`curl -sS -m 10 -L <url>`（2026-11-04）

## 视觉辨识
来源卡不适用；本卡仅登记文字/数据来源，不内嵌图片。若页面含图片，其权利与文字数据分开核验，本 Vault 只保留原始 URL。

## 适用条件
可支撑：该馆藏对象为 Kimono（和服）、文化 Japan、年代 19th century、材质 silk、尺寸 170.5 × 122.2 cm、分类 Main dress-Womenswear、入藏号 C.I.53.22.10、公共领域。

## 不适用条件
不能支撑：和服的一般定义、结构术语、穿着礼仪、纹样寓意；也不能证明该对象曾被某部影视剧或某位演员使用。

## 提示词短语
- （来源卡不适用；请引用相关卡片的 prompt_en。）

## 来源链接
- https://collectionapi.metmuseum.org/public/collection/v1/objects/125953（实测：HTTP 200（objects/125953 JSON）；人类可读页本次核验 HTTP 429（Met 限流），以 API 数据为核验对象，2026-11-04）

## 相关卡片
- [[GAR-0001-和服]]
