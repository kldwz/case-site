---
name: Reflexio
一句话: 让 AI Agent 从真实交互里「学到经验、记住教训」，免费引流、按用量订阅
创始人地区: 美国（联创 Yi Lu，前 Meta tech lead、UW 兼职教授；另两位联创 Guangyu Yang 等）
营收模式: SaaS 订阅制。官网 pricing：Free $0/月（100K tokens）+ Pro $299/月（10M tokens）+ BYOC 私有化自托管（custom）
月收入估算: 未官方披露
流量来源: ProductHunt 首发（首周 #2、274 upvotes）+ 开源 SDK/GitHub + 官网 SEO + 社区口碑
可迁移点: ① 面向 AI Agent 的「记忆/学习层」是 2025 新空位，比做通用模型工具更聚焦 ② 免费层 100K tokens 只够试用，Pro 直接 $299 锚定企业用量 ③ 把客户自己的日志变成产品卖点，零数据标注成本 ④ 开源 SDK 让开发者无痛接入，降低采用门槛
原文链接: https://www.reflexio.ai/
数据口径: 官网 pricing/Features 页实测 + ProductHunt 收录（2026-09-01）
分类: AI 基础设施 / Agent 学习 / SaaS / 英文
封面: /case-site/cases/reflexio/site.png
---

![Reflexio 官网首页](/cases/reflexio/site.png)

# Reflexio：让 AI Agent 不再重复犯错的行为学习平台

## 产品是什么

Reflexio 是一个 **AI Agent 行为学习平台**（官网定位 "LEARNING PLATFORM FOR AI AGENTS"）。它解决的是 Agent 的一个老毛病：**同一个错犯第二次**。

一个客服 Agent 第一次漏了客户的第二笔异常扣款，客户会再回来追问一遍；如果没有学习机制，这类错误会反复出现。Reflexio 的做法是把用户的纠正、失败的路径、成功的结局收集起来，转成 Agent 下次能复用的「行为规则」，而且**每一条都可见、可回滚**——不是把 Agent 变成一个黑盒，而是让它越用越不容易重复踩坑。

官网给了一个很直观的例子：没有 Reflexio，客服 Agent 只看到一笔 $49.99 的陌生扣款就回复退款，漏了同一窗口的 $9.99；有了 Reflexio，Agent 学会先搜完整扣款窗口、把所有陌生项一次性呈现并询问是否一起退——同一件事，一次对话就结束。

它支持编码 Agent、销售助理、数据分析师、招聘等多个场景，并提供 Python / REST / CLI 接入，还有针对 Codex、Claude Code、Cursor 的开源 skill。

## 怎么赚的钱

Reflexio 是典型的 **开发者工具 SaaS 订阅制**，三层定价锚定不同客群：

| 档位 | 价格 | 用量 |
|------|------|------|
| Free | $0/月 | 100K tokens / 月，给开发者试用接入 |
| Pro | $299/月 | 10M tokens / 月，面向真实业务量 |
| BYOC | 自托管（custom） | 数据不出企业，面向大客户 / 合规要求 |

这套设计的核心逻辑：**免费层只够把工具跑通，一旦 Agent 流量上量就自然跨进付费墙**——对 Agent 基础设施类产品，用户业务越大、用量越狠，付费越高，天然跟着客户成长收费。

具体收入官方未披露。

## 流量从哪来

- **ProductHunt 首发**：上线当周拿到 #2、274 upvotes、504 followers，冷启动靠社区首发引爆。
- **开源 SDK + GitHub**：reflexio 仓库和 Codex/Claude Code/Cursor 的集成 skill 放在 GitHub，开发者可自取、可 PR，形成开发者生态入口。
- **官网 SEO + 内容**：Features/Pricing/Docs/Blog 齐全，靠「Agent 学习/记忆」相关关键词承接搜索。
- **社区口碑**：AI Agent 开发者圈子小、传播快，一个「不重复犯错」的差异化点容易被口口相传。

无公开流量数字，渠道结构为定性判断。

## 这个案例能学到什么

第一，**给 Agent 做「记忆与学习层」，是比做通用工具更聚焦的空位**。大家都做模型、做编排，Reflexio 专攻「让 Agent 记住上次教训」——切口小，但每个做 Agent 的人都有这个痛点。

第二，**用量计费让客户替你长大**。免费层 100K tokens 是体验钩子，Pro 直接 $299 不是拍脑袋，是锚定「Agent 处理真实业务量的月 token 消耗」——产品跟客户的规模同步收费。

第三，**把客户自己产生的日志变成产品数据**。Reflexio 不需要手动标注数据，Agent 的每一次成功/失败对话就是训练素材，这是它能轻资产冷启动的关键。

第四，**开源接口降低采用门槛**。不给客户一套要重写架构的封闭系统，而是给 Codex/Claude Code 一行 skill、一个 SDK——接入成本越低，越多人敢试。

## 来源与数据

- 站点：https://www.reflexio.ai/（pricing/Features 页实测，2026-09）
- 来源：ProductHunt 收录（2026-09-01）+ 官网
- 定价：官网 pricing 页明码标价（Free / Pro $299 / BYOC custom）
- 创始人：官网 Blog/About 披露联创 Yi Lu（前 Meta tech lead、UW 兼职教授）
- 收入：官方未披露

## 一句话总结

> 不训练大模型，只给 Agent 装一套「会从错误里学习」的行为记忆层，免费试用、按用量订阅，让客户业务量越大付得越多。
