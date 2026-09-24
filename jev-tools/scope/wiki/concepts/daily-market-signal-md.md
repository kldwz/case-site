---
janitor:
  bucket: durable_memory
  persist: 1.93
  confidence: 0.91
  bucket_margin: 0.87
  contains_secret: 0.05
  safe_to_leave_in_git: 0.49
  action: frontmatter
  reason: normal vote
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  at: '2026-09-23T04:56:27Z'
---
# 每日市场信号 Markdown 工作流

> **类型**: concept (AI工作流)
> **来源**: [[entities/gregisenberg]] — status/2083954605533065561 + status/2084011714278777200
> **采集日**: 2026-08-08 / 2026-08-09
> **评分**: 用户 8 / 商业 8 / 传播 8 = 24

## 摘要

每家公司该有一个每天自动更新的 `what_the_market_is_telling_us.md`，从 Stripe/PostHog/Intercom 等真实信号源聚合"本周客户行为变了什么"。本质是让 agent 每天早上写一份带证据的产品决策建议。

## 详情

### 信号源（接上 MCP/API 即可）
1. Stripe — 谁付费/升级/降级/流失
2. PostHog — 用户真在干嘛
3. Intercom/Plain — 客服投诉
4. Granola/Gmeet — 销售电话转录
5. HubSpot/Salesforce — CRM/丢单原因
6. Linear/Jira/GitHub — bug 与需求
7. Ideabrowser MCP — 外部市场信号

### 核心原则
价值不在"本周发生了啥"，而在"什么变了"：
- 流失用户都提到 setup 困惑且没邀队友 -> 是激活问题不是定价问题
- 升级用户付费前都碰了同一功能 -> 把它往前推
- 销售电话突然输给以前能赢的竞品 -> 需要调查

### 原文要点
> The fastest way to PMF is understanding customers better than anyone else, and the highest signal customer insight is usually a change in behavior.

### 扩展思考
1. 这 7 个工具哪些你有？哪些能接 API？先列一张"我的数据源清单"
2. 核心不是"摘要发生了什么"，而是"什么变了"——这是判断 PMF 的关键
3. 机会：做"给小团队的 AI 增长助理"模板/产品，按效果计费

## 我的判断

这是 gregisenberg 今天最值钱的一条。小老板用 AI 做"穷人版 BI"，不养数据分析师。本质是"让 agent 每天早上写一份带证据的产品决策建议"。

## 关联
- [[entities/gregisenberg]] — 提出者
- [[concepts/marketing-agent-loop]] — 同作者方法论，营销 agent 是执行层
- [[topics/26-startup-directions]] — 方向 #9 "LLM-search land grab" 和 #12 "AI enablement"
- [[topics/5-solo-opportunities]] — 机会 3 "AI 工具存活清单"同属"每日推送"模式

## 来源
- [原推 1](https://x.com/gregisenberg/status/2083954605533065561) — 2026-08-08 采集
- [原推 2](https://x.com/gregisenberg/status/2084011714278777200) — 2026-08-09 采集
- [[sources/keep-candidates/KEEP候选-08-08]] — #90 评分记录
- [[sources/keep-candidates/KEEP候选-08-09]] — #3 精简版

## 变更记录
- 2026-08-08: 初始创建（详细版含原文+翻译+解读），来源 08-08 采集
- 2026-08-09: 合并 08-09 精简版，更新格式为 wiki 页
