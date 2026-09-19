---
name: BrowseGraph（浏览器内 GraphRAG）
一句话: Google Chrome 内置 AI 挑战赛"最佳混合 AI 应用"：在浏览器里跑 GraphRAG，把你看过的网页连成知识图，40 个赞
创始人地区: 独立开发者（GitHub：talperetz），提交于 Google Chrome Built-in AI Challenge
营收模式: 尚未商业化（黑客松参赛作品，无营收数据）
月收入估算: 未官方披露（赛事作品，尚无营收）
流量来源: 赛事作品页 + GraphRAG 这个技术热点；Devpost 官方作品页 40 个赞
可迁移点: ① 把服务器上的热门技术搬到浏览器里：PGlite + pgvector 让 Postgres 和向量检索跑在前端，这是当下的技术红利 ② "你浏览过的一切都是你的知识库"：这个定位比"又一个 AI 搜索"清晰得多 ③ 混合 AI 的正确用法：小任务用本地模型、重任务用云，成本和体验两头占 ④ 图可视化（reactflow）让抽象能力一眼看懂：技术再强，看不懂就等于不存在 ⑤ 数据不出浏览器，隐私叙事天然成立——这是端侧方案的白送优势
原文链接: https://devpost.com/software/browsegraph
数据口径: Devpost 官方作品页（devpost.com/software/browsegraph），2026-09-12 抓取：赛事 Google Chrome Built-in AI Challenge、奖项 Winner · Best Hybrid AI App (Chrome Extension)、40 likes、技术栈 cmdk / pglite / pgvector / react / reactflow / tailwind、源码 github.com/talperetz/browsegraph。无营收数据。
分类: AI 应用 / 浏览器扩展 / 英文 / 知识管理
类型: 获奖作品
证据等级: 平台数据可查
平台数据: Devpost 官方作品页：Winner · Best Hybrid AI App (Chrome Extension) · 40 likes（2026-09-12）
赛事: Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）
场景: 知识管理：在浏览器里跑 GraphRAG，把浏览过的网页连成知识图
奖项: Winner · Best Hybrid AI App (Chrome Extension)（最佳混合 AI 应用）
封面: /case-site/cases/browsegraph/site.png
---

![BrowseGraph 作品页](/cases/browsegraph/site.png)

# BrowseGraph：把 GraphRAG 塞进浏览器，你看过的网页就是你的知识库

> **赛事**：Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）
> **场景**：知识管理：在浏览器里跑 GraphRAG，把浏览过的网页连成知识图
> **奖项**：Winner · Best Hybrid AI App (Chrome Extension)（最佳混合 AI 应用）
> **出处**：[作品页](https://devpost.com/software/browsegraph) ｜ [赛事页](https://googlechromeai.devpost.com/) ｜ [源码](https://github.com/talperetz/browsegraph)

## 产品是什么

一个 Chrome 扩展：把你浏览过的网页自动连成一张**知识图谱**，并在浏览器本地完成检索——基于 GraphRAG（图结构 + 检索增强生成）的思路，但整套东西跑在你的浏览器里。

技术栈很能说明问题：**PGlite**（浏览器里的 Postgres）+ **pgvector**（向量检索）+ **ReactFlow**（图可视化）+ React。

## 它解决了什么

我们每天读大量网页，但这些内容读完就散了：收藏夹里躺着几百条，搜索引擎搜不到「我上周看过那个讲 X 的文章」，更别说把这些内容关联起来。

知识库工具能解决这个问题，但前提是你**主动剪藏、主动整理**——大多数人坚持不过两周。

## 这个解法妙在哪

1. **零主动操作**：你照常浏览，它在后台把内容接成图，不需要你改变任何习惯。
2. **把服务器技术搬到浏览器**：PGlite + pgvector 让「浏览器里跑一个带向量检索的数据库」成为现实。这是近两年才出现的技术红利，谁先用谁占便宜。
3. **图可视化让能力可见**：用 ReactFlow 把关联画出来，用户一眼就懂「它把我的浏览历史连起来了」——抽象能力必须被看见才算存在。
4. **数据不出浏览器**：本地存储 + 本地检索，隐私叙事天然成立，这是端侧方案的白送优势。

## 团队与赛事

独立开发者（GitHub: talperetz），提交于 **Google Chrome Built-in AI Challenge**，获 **Winner · Best Hybrid AI App (Chrome Extension)**，40 个赞。

## 这个案例能学到什么

① **紧跟基础设施的迁移红利**。当 Postgres 能跑进浏览器，一整类「必须上云」的产品就变成了纯前端项目。

② **定位要一句说清**。「你浏览过的一切都是你的知识库」，比「又一个 AI 搜索」清晰得多。

③ **混合是当下 AI 应用的现实最优解**：轻任务本地、重任务云端，成本和体验两头都占。

④ **把抽象能力可视化**。图结构画出来，用户才理解你做了什么。

⑤ **端侧方案的隐私叙事是白送的**。数据不出设备，这句话对一部分用户就是决定性因素。

## 来源与数据

- Devpost 官方作品页：`https://devpost.com/software/browsegraph`（2026-09-12 抓取：Winner · Best Hybrid AI App (Chrome Extension)、40 likes、技术栈 cmdk / pglite / pgvector / react / reactflow / tailwind）
- 赛事页：`https://googlechromeai.devpost.com/`
- 源码：`https://github.com/talperetz/browsegraph`
- 营收：赛事作品，无营收数据，本站不做估算

> 当数据库能跑进浏览器，"这个产品必须有个后端"这句话就不成立了——基础设施每次搬家，都会空出一批新产品位。
