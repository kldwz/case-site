---
name: Bland AI
一句话: 被 180 家机构拒绝后仍坚持自研全栈语音模型——给企业做能打三十分钟长电话的 AI 接线员，每周处理三百五十万通，累计融资超一亿美金
创始人地区: Isaiah Granet（CEO）与 Sobhan Nejad（联合创始人），2023 年创立，总部美国旧金山
营收模式: 面向受监管行业企业的语音 AI 平台，按通话分钟数计费，语音克隆与多语言等能力另计；公开定价自 299 美金每月起
月收入估算: 未披露营收；累计融资超过 1 亿美金——种子 12.5 万美金（YC，2023-06）、A 轮 1600 万美金（2024-08，Scale Venture Partners）、B 轮 4000 万美金（2025-01，Emergence Capital）、C 轮 5000 万美金（2026-06，Dell Technologies Capital）；约 112 名员工
流量来源: YC S23 起步 + 客户名单自带信任（Samsara、Kin Insurance、Mutual of Omaha、克利夫兰骑士队）+ 受监管行业的合规资质作为准入门槛 + 创始人被拒 180 次的逆袭叙事被 Fortune 报道
可迁移点: ① 在最难的地方自建壁垒——他坚持自研端到端语音模型，甚至不让客户接入 OpenAI 或 Anthropic，换来的是三十到四十五分钟的长电话能力 ② 合规不是成本而是准入证，SOC 2 Type II、HIPAA、PCI DSS、GDPR 直接把一大批对手挡在医疗与保险门外 ③ 挑通话量极大且高度重复的行业切入，医疗、保险、金融服务的电话场景天然高频且有明确 ROI ④ 先给自己做——创始团队是在上一家公司里被医疗沟通的低效刺痛才转做这个 ⑤ 融资被拒不等于判断错，被 180 家机构拒绝后仍拿到 Dell Technologies Capital 领投的 5000 万美金 C 轮 ⑥ 让天使投资人成为分销节点，Twilio 联创 Jeff Lawson、PayPal 联创 Max Levchin 站台在语音赛道里格外有分量
原文链接: https://www.bland.ai
数据口径: 融资——YC 种子 12.5 万美金（2023-06）、A 轮 1600 万美金（2024-08，Scale Venture Partners 领投）、B 轮 4000 万美金（2025-01，Emergence Capital 领投）、C 轮 5000 万美金（2026-06，Dell Technologies Capital 领投），累计约 1.06 亿美金；运营——每周处理约 350 万通电话，250 家以上企业客户，支持 40 多种语言，约 112 名员工；客户——Samsara、Kin Insurance、Mutual of Omaha、CNO Financial、克利夫兰骑士队、Better.com、University of Phoenix、Sears
类型: 收入案例
证据等级: 官方披露
分类: 语音 AI / 企业客服 / 受监管行业 / 美国
封面: /case-site/cases/bland-ai/site.png
---

![Bland AI 官网](/cases/bland-ai/site.png)

# Bland AI：被 180 家机构拒绝后，他们靠自研语音模型每周打三百五十万通电话

## 产品是什么

Bland AI 做的是**能替企业打电话的 AI 接线员**，呼入呼出都能接，规模可以拉到很大。

和一堆套壳的语音 Agent 不同，Bland **跑在自己的基础设施上**，用的是自研的端到端语音模型。这一点他们坚持得很硬——平台**不允许客户接入 OpenAI 或 Anthropic 的模型**，哪怕客户想。

代价是研发重，收益是能力边界：他们的通话可以持续 **30 到 45 分钟**，能完成相当复杂的任务。公开例子里有引导用户量血压、排查设备故障、判断是否需要转急诊这类医疗场景——这类电话对「断了就重来」的通用方案来说太长了。

平台包含：

- **Norm** — 用来搭建生产级 Agent 的构建器
- **Conversational Pathways** — 自研的脚本系统，用一棵提示树规定 Agent 在各种回应下怎么走
- **测试、可观测性与全渠道部署** — 覆盖语音、短信、网页聊天，支持 40 多种语言
- **集成** — Twilio、Salesforce、HubSpot、Genesys
- **合规** — SOC 2 Type II、HIPAA、PCI DSS、GDPR

## 怎么赚的钱

**按分钟计费**的用量模式，企业为呼入呼出通话付费，语音克隆、多语言等附加能力另外计价。公开定价自 299 美金每月起。

客户集中在**通话量极大、话术高度重复、且出错代价高**的行业：医疗、保险、金融服务、物流、地产。这些行业共同的特点是——电话多到人力扛不住，但又不像普通电商客服那样可以随便外包。

结果是每周约 **350 万通电话**，超过 **250 家企业客户**。

## 流量从哪来

第一，**合规资质本身就是获客渠道**。在医疗和保险里，HIPAA 不是加分项而是入场券。拿到这些认证，等于自动过滤掉一大批没有资质的小玩家。

第二，**客户名单的可信度外溢**。Samsara、Kin Insurance、Mutual of Omaha、CNO Financial、克利夫兰骑士队——在 B 端语音这个信任门槛极高的品类里，同行名单比功能对比有效得多。

第三，**YC 与豪华天使阵容**。种子轮来自 YC，天使里有 **Twilio 联创 Jeff Lawson** 和 **PayPal 联创 Max Levchin**。在语音赛道，这两个名字的分量不只是钱，更是渠道。

第四，**逆袭叙事上了 Fortune**。被 180 家机构拒绝之后拿到 Dell Technologies Capital 领投的 5000 万美金 C 轮——这个故事本身就是一次大规模曝光。

## 站长是谁

**Isaiah Granet**，Bland CEO，2022 年从圣路易斯华盛顿大学毕业；**Sobhan Nejad**，联合创始人。两人 2023 年在旧金山创立 Bland，出自 YC 的 S23 批次。

起点是他们此前的公司 **Intelliga Health**。在做医疗沟通产品时，他们被这个行业里低到离谱的效率反复刺痛——患者打不通电话、信息传不到、流程靠传真——然后意识到这不是医疗独有的问题，而是**整个企业电话系统的问题**。

他们的判断很朴素：人没法 24 小时在线，没法同时处理几百万通电话，也没法被训练成完全符合公司要求的语气和行为——**但 AI 可以，而且成本只是零头**。

从 pre-seed 到 B 轮只用了十个月，节奏快得反常。但同一时间线里也藏着被 180 家机构拒绝的记录——「快」是事后看的结果，不是当时的体感。

## 这个案例能学到什么

第一，**在别人不愿意自建的地方自建**。语音 Agent 最容易的做法是接通用大模型，Bland 偏不。自研带来的三十到四十五分钟长通话能力，正是医疗、保险这些高价值场景的硬性门槛。

第二，**把合规当护城河而不是负担**。SOC 2 Type II、HIPAA、PCI DSS、GDPR 听起来是成本，实际上是准入门槛——它替你挡掉了所有做不到的人。

第三，**挑「量极大且高度重复」的场景**。Bland 选的行业有个共同点：电话多到人力扛不住。在这种场景里，ROI 是客户自己能算出来的，不需要销售说服。

第四，**做自己被刺痛过的问题**。创始团队不是看到了市场报告，是在上一家公司里亲身被医疗沟通折磨。这种动机在长周期 B 端业务里特别抗打击。

第五，**被拒的次数不等于判断的质量**。180 家机构拒绝之后，Dell Technologies Capital 领投了 5000 万美金 C 轮。融资是找那一个懂你的人，不是说服所有人。

第六，**让投资人成为渠道节点**。Jeff Lawson 做 Twilio、Max Levchin 做 PayPal——在语音和支付这两个相邻赛道里，他们的背书比资金本身更值钱。

## 来源与数据

- 站点：https://www.bland.ai
- 融资：YC 种子 12.5 万美金（2023-06）、A 轮 1600 万美金（2024-08，Scale Venture Partners 领投）、B 轮 4000 万美金（2025-01，Emergence Capital 领投）、C 轮 5000 万美金（2026-06，Dell Technologies Capital 领投），累计约 1.06 亿美金；天使投资人包括 Jeff Lawson（Twilio 联创）、Max Levchin（PayPal 联创）、Piotr Dabkowski
- 运营：每周处理约 350 万通电话，250 家以上企业客户，支持 40 多种语言，约 112 名员工（2026 年初）
- 产品：自研端到端语音模型，不支持客户接入 OpenAI 或 Anthropic 模型；通话可持续 30 至 45 分钟；含 Norm 构建器、Conversational Pathways 脚本系统、测试与可观测性、全渠道部署
- 合规：SOC 2 Type II、HIPAA、PCI DSS、GDPR
- 客户：Samsara、Kin Insurance、Mutual of Omaha、CNO Financial Group、克利夫兰骑士队、Better.com、University of Phoenix、Sears
- 定价：按通话分钟计费，公开定价自 299 美金每月起
- 团队背景：Isaiah Granet（2022 年毕业于圣路易斯华盛顿大学）与 Sobhan Nejad 于 2023 年创立，出自 YC S23；此前的公司为 Intelliga Health

## 一句话总结

> 两个年轻人被医疗沟通的低效刺痛，转头去做企业电话的 AI 接线员。他们拒绝接入通用大模型，硬啃自研语音栈，换来能打三十到四十五分钟长电话的能力，以及医疗、保险这些高门槛行业的通行证。被 180 家机构拒绝之后，Dell Technologies Capital 领投了 5000 万美金 C 轮。如今他们每周处理三百五十万通电话——人类的电话，正在被一行行代码接走。
