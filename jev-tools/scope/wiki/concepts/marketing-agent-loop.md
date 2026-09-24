---
janitor:
  bucket: durable_memory
  persist: 1.86
  confidence: 0.93
  bucket_margin: 0.9
  contains_secret: 0.03
  safe_to_leave_in_git: 0.54
  action: frontmatter
  reason: normal vote
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  at: '2026-09-23T04:56:28Z'
---
# 营销 Agent 自动跑广告闭环

> **类型**: concept (创业案例/AI工作流)
> **来源**: [[entities/gregisenberg]] — https://x.com/gregisenberg/status/2081814601851900221
> **采集日**: 2026-08-08 / 2026-08-09
> **评分**: 用户 8 / 商业 10 / 传播 9 = 27

## 摘要

营销 agent 是新的 coding agent。gregisenberg 给出了完整可跑的闭环栈：Perplexity 挖痛点 -> Nano Banana 出图 -> 视觉模型审品牌 -> HeyGen 出 UGC 视频 -> loop 读 FB 数据自优化。小商家请不起代运营，agent 能 80% 替代。

## 详情

### 闭环栈（已全部跑通）
1. Perplexity 抓 Reddit 真实痛点
2. Nano Banana 出 on-brand 静态素材
3. 视觉模型按品牌规范审核
4. HeyGen 出 AI UGC 视频
5. loop 读 Facebook 数据：杀输家、放量赢家、复制成功

### 点名的可抄机会
- Yoast（~$15M ARR）只给你红绿点让你自己改 SEO；AI 版直接帮你改。需求已验证、无 AI-native 竞品、几千站长月付
- 同理：WooCommerce、WP Forms 的 AI-first 版本

### 原文要点
> Marketing agents are the NEW coding agents.
> It's code in the cloud that makes decisions off your live business data on a loop.
> Coding agents changed who gets to build software. Marketing agents change who gets to grow a company.

### 扩展思考
1. 他说的 stack 每个工具你能不能试用？先挑 1 个做个小实验
2. "AI-first 版本旧插件"这个套路可复制到哪些你熟悉的旧软件？
3. 机会：垂直版营销 agent（只做电商/本地服务/Newsletter 增长）
4. 警示：所有营销渠道都被 AI slop 淹没，差异化在"真实痛点+品牌一致性"

## 我的判断

营销 agent 是继编码 agent 后的最大红利。壁垒不在技术，在"接好你自己的业务数据"。对一人公司来说，可以先做成"营销 agent 代运营"服务（卖结果不卖工具），再逐步产品化。

## 关联
- [[entities/gregisenberg]] — 提出者
- [[concepts/copilot-to-loop-framework]] — "build agent for xyz" 框架的具体应用
- [[concepts/agent-as-daily-sms]] — 营销 agent 可先做成每日推送
- [[topics/26-startup-directions]] — 方向 #13 "agency everyone resents"
- [[topics/5-solo-opportunities]] — 机会 2 "营销 agent 代投"

## 来源
- [原推](https://x.com/gregisenberg/status/2081814601851900221) — 2026-08-08/09 采集
- [masterclass 视频](https://youtube.com/watch?v=mD7JpNHLT70)
- [[sources/keep-candidates/KEEP候选-08-08]] — #106 评分记录
- [[sources/keep-candidates/KEEP候选-08-09]] — #4 精简版

## 变更记录
- 2026-08-08: 初始创建（原文件名：营销Agent自动跑广告闭环.md + 创业方向-营销Agent.md）
- 2026-08-09: 合并 08-09 精简版 + 08-08 创业方向页，整合为完整概念页
