---
name: NeuThera（药物发现工具包）
一句话: 黑客松第三名：用生成式模型从头设计药物分子，449 个赞，把 AI 制药流程做成了工具链
创始人地区: 参赛团队 Redomic，提交于 Windows on Snapdragon AI Hackathon（收录自该赛事 Devpost 作品库）
营收模式: 尚未商业化（黑客松参赛作品，无营收数据）
月收入估算: 未官方披露（赛事作品，尚无营收）
流量来源: 赛事作品页 + AI 制药这个高关注赛道；Devpost 官方作品页 449 个赞
可迁移点: ① 比赛的胜负手常常是"整合"而非"发明"：它把 chemberta、deeppurpose、DrugBank、ChEMBL 等现成模型和数据库串成一条流水线 ② 做工具链而不是做一个 Demo：目标是"可复用的药物发现流程"，评委看到的是工程完整度 ③ 图检索 + 分子指纹 + 生成模型三件套：这是当下 AI 制药的标准范式，照着搭就能出成果 ④ 选高价值赛道：制药是 AI 落地里最被看好的方向之一，评委和媒体天然关注 ⑤ 数据来源要写得清清楚楚（DrugBank / ChEMBL / BioSNAP），可信度是科研类项目的生命线
原文链接: https://devpost.com/software/neuthera-drug-discovery-platform
数据口径: Devpost 官方作品页（devpost.com/software/neuthera-drug-discovery-platform），2026-09-12 抓取：奖项 Winner · Third Place、449 likes、技术栈含 arango / biomart / biopython / biosnap / chemberta / chembl / deeppurpose / drugbank / faiss、源码 github.com/Redomic/NeuThera-Drug-Discovery-Toolkit；收录自 Windows on Snapdragon AI Hackathon 作品库（wos-ai.devpost.com）。无营收数据。
分类: AI 应用 / AI 制药 / 英文 / 科研工具
类型: 获奖作品
证据等级: 平台数据可查
平台数据: Devpost 官方作品页：Winner · Third Place · 449 likes（2026-09-12）
封面: /case-site/cases/neuthera/site.png
---

![NeuThera 作品页](/cases/neuthera/site.png)

# NeuThera：不发明新模型，把现成的 AI 制药工具串成一条流水线

## 产品是什么

一个 AI 药物发现工具包：从零开始设计（de novo）候选药物分子。它集成了多个当前最好的生成模型，配合图结构检索和分子指纹技术，走完「检索已知化合物 → 生成新分子 → 评估性质」的完整链路。

技术栈里能看到 ChemBERTa、DeepPurpose、DrugBank、ChEMBL、BioSNAP、FAISS、ArangoDB 等一长串名字——这不是炫技，而是这条流水线的真实组成。

## 它解决了什么

药物发现的痛点不是「没有一个好模型」，而是**流程断裂**：数据库在一处、模型在一处、评估在另一处，每一步都要人工搬运和转换格式。

NeuThera 做的是把这些环节接起来：检索（FAISS / ArangoDB）→ 生成（ChemBERTa 等）→ 评估（DeepPurpose）→ 数据（DrugBank / ChEMBL / BioSNAP），形成一条能跑通的工具链。

## 这个解法妙在哪

1. **它赢在整合，不在发明**。黑客松只有几天，训一个 SOTA 模型不现实，但把已有的 SOTA 串成流水线完全可行——这正是比赛的现实打法。
2. **做工具链，不做 Demo**。评委看到的不是「一个能生成分子的网页」，而是「一整套可复用的流程」，工程完整度立刻拉开差距。
3. **数据来源写全**：DrugBank、ChEMBL、BioSNAP 都标得清清楚楚。科研类项目的可信度就建立在这个清单上。

## 团队与赛事

参赛团队 Redomic，作品获 **Winner · Third Place**，449 个赞，源码公开于 GitHub（NeuThera-Drug-Discovery-Toolkit）。本条目收录自 Windows on Snapdragon AI Hackathon 的 Devpost 作品库。

## 这个案例能学到什么

① **整合也是一种创新**。把散落各处的工具串成流水线，价值不比训一个新模型小，而且在时间有限时更现实。

② **工程完整度比单点效果更容易拿奖**。流程能跑通、数据可追溯、组件可替换，这些是评委最看重的。

③ **标准范式可以直接复用**：图检索 + 分子指纹 + 生成模型，是当下 AI 制药的通用解法，照着搭就有结果。

④ **选高关注度赛道**。AI 制药是最容易被理解和关注的 AI 落地方向之一，天然有评委缘和媒体缘。

⑤ **来源清单就是可信度**。科研类项目把数据来源列全，可信度立刻上一个台阶。

## 来源与数据

- Devpost 官方作品页：`https://devpost.com/software/neuthera-drug-discovery-platform`（2026-09-12 抓取：Winner · Third Place、449 likes、技术栈 arango / biomart / biopython / biosnap / chemberta / chembl / deeppurpose / drugbank / faiss）
- 赛事作品库：`https://wos-ai.devpost.com/`
- 源码：`https://github.com/Redomic/NeuThera-Drug-Discovery-Toolkit`
- 营收：赛事作品，无营收数据，本站不做估算

> 一周做不出新模型，但一周足够把十个现成模型串成一条流水线——比赛比的是整合速度，不是发明能力。
