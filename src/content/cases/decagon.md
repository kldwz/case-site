---
name: Decagon
一句话: 给企业做 AI 客服 agent（对话/邮件/语音），按解决量计费，2025 年底 ARR 约 4400 万美金、2026 年中冲到 1 亿美金，估值 45 亿
创始人地区: Jesse Zhang（CEO，Harvard CS，前 Lowkey 被 Niantic 收购）+ Ashwin Sreenivas（CTO，Stanford CS，Helia 卖 Scale AI），2023 年 8 月旧金山创立
营收模式: 按对话 / 按解决量计费（per-conversation / per-resolution），面向大企业客服中心，办成一件事收一份钱
月收入估算: ARR 约 4400 万美金（2025 年底）；Sacra 估 2026 年 7 月达 1 亿美金；2026 年 1 月 2.5 亿美金 D 轮（Coatue + Index 领投）、估值 45 亿美金；2025 年 6 月 C 轮 1.31 亿 @ 15 亿估值
流量来源: PLG（自助试用）+ 大客户销售，100+ 企业客户含 Notion / Duolingo / Avis Budget / Deutsche Telekom / Block / Chime / Hertz / Oura
可迁移点: ① 把"按座位收费"换成"按解决量收费"，客户只为结果买单，也倒逼你把准确率做上去 ② 客服 agent 的真正壁垒是"接系统"（调 API 办退款/改订单），不是会聊天 ③ 语音用 ElevenLabs 等现成引擎、自己只做编排，避免重资产自研 ④ 大客户先用一个高痛场景（退款/密码）打穿，再横向铺开 ⑤ 哈佛/斯坦福+被收购经历的创始人组合，融资和签单都自带信用背书
原文链接: https://decagon.ai
数据口径: Sacra 2025–2026 公司报告、TechCrunch/Fortune 融资报道、decagon.ai 官网客户页；ARR/估值/客户均可交叉验证
分类: AI Agent / 企业服务 / 客服 / 英文
封面: /case-site/cases/decagon/site.png
---

![Decagon 官网](/cases/decagon/site.png)

# Decagon：两个斯坦福/哈佛毕业生用 AI 客服 agent 把 ARR 做到 4400 万美金

## 产品是什么

**Decagon** 给企业做"AI 客服 agent"——不是套个 ChatGPT 的客服机器人，是能同时跑**对话、邮件、语音**三个渠道、而且能自己调后台 API 真把事办了的"数字员工"。

比如用户说"我要退上个月那单"，Decagon 不是回一段模板话术，而是**真的去订单系统查、去支付系统退、再去发确认邮件**。它把企业的知识库、CRM、工单系统全接上，遇到搞不定的再平滑转人工。Decagon Voice 还跟 ElevenLabs 合作，把语音也做成自然对话。

说白了，它抢的是传统客服 BPO 和 Zendesk 那类"人力堆出来的支持中心"的活。

## 怎么赚的钱

**按解决量计费（per-resolution）**——客户只为"AI 真办成的一件事"付钱，不是按坐席买年费。

这招妙在两头通吃：对客户来说，比养一队客服或买 Zendesk 席位便宜，而且**不成功不花钱**；对 Decagon 自己来说，定价模型逼着它把"首次解决率"当命根子——AI 办不成，它自己也不赚钱。2025 年底 ARR 约 4400 万美金，Sacra 估 2026 年 7 月冲到 1 亿美金。

融资节奏很猛：2025 年 6 月 C 轮 1.31 亿美金、估值 15 亿；2026 年 1 月 D 轮 2.5 亿美金（Coatue + Index 领投）、估值 45 亿美金。从 2023 年 8 月创立到 45 亿估值，不到 3 年。

## 流量从哪来

1. **PLG 自助试用**：企业 IT/支持负责人登录 decagon.ai 配一个 agent，几小时跑通一条客服流，先小场景用起来。
2. **大客户销售**：Notion、Duolingo、Avis Budget、Deutsche Telekom、Block、Chime、Hertz、Oura 等 100+ 企业，靠"先打穿一个高痛场景（退款/密码重置），再横向铺开"的路径签单。
3. **Proactive Agents**：Decagon 推"主动 agent"——系统发现异常订单主动联系用户，把客服从"被动接电话"变成"主动触达"，这成了它撬动大客户的差异化卖点。

## 站长是谁

**Jesse Zhang（CEO）**，Harvard 计算机，之前做的社交 startup Lowkey 被 Niantic（Pokémon GO 那家）收购；**Ashwin Sreenivas（CTO）**，Stanford 计算机，创业项目 Helia 卖给了 Scale AI。

两个创始人都有"被大厂收购"的退出经历，等于**既懂怎么从 0 做产品，又懂怎么把公司卖个好价钱**。这种组合在融资圈特别吃香——Decagon 能这么快拿到 Coatue/Index 的钱，创始人的履历和退出记录是隐性的信用背书。

## 这个案例能学到什么

第一，**把"按座位收费"换成"按解决量收费"**。传统 SaaS 卖坐席年费，客户买完用不用都付钱；Decagon 按解决量收，客户只为结果买单。**这既是筛选器（敢承诺就说明真有底气），也是信任状（客户觉得你跟它站一边）**。

第二，**客服 agent 的真正壁垒是"能接系统"，不是"会聊天"**。LLM 人人都有，难的是把订单、支付、CRM 的 API 接稳、把权限和审计做好。**接系统的深度 = 替换成本 = 护城河**。

第三，**语音别自研，拿现成的拼**。Decagon Voice 直接接 ElevenLabs 的语音引擎，自己只做编排和路由。**在"不是核心差异点"的环节用现成方案，把精力压在真正拉开差距的地方**。

第四，**大客户先打穿一个场景，再横向扩张**。别一上来说"我替你管全部客服"，先拿"退款"或"密码重置"这种高频高痛的场景做出 ROI，再谈铺开。**小切口、大证明、慢扩张**。

第五，**创始人组合自带融资杠杆**。一个 Harvard+被收购、一个 Stanford+被收购，这种背景让顶级基金敢在 A 轮就下重注。**对个人开发者来说，教训是：你的"退出经历/大厂背景"本身就是可变现的资产，写案例、聊合作时别藏着**。

## 来源与数据

- 站点：https://decagon.ai
- ARR / 估值 / 融资：Sacra 公司报告（2025–2026）、TechCrunch / Fortune 融资报道
- 客户名单：decagon.ai 官网客户页（Notion / Duolingo / Avis Budget 等）
- 产品能力：Decagon Voice / Proactive Agents 官方介绍

## 一句话总结

> 两个被大厂收购过的斯坦福/哈佛毕业生，用"按解决量收费 + 真接系统"的 AI 客服 agent，3 年把 ARR 干到 1 亿美金、估值 45 亿。
