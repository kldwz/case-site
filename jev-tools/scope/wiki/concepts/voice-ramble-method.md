---
janitor:
  bucket: durable_memory
  persist: 1.82
  confidence: 0.94
  bucket_margin: 0.9
  contains_secret: 0.03
  safe_to_leave_in_git: 0.56
  action: frontmatter
  reason: normal vote
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  at: '2026-09-23T04:56:29Z'
---
# 语音 ramble 工作法

> **类型**: concept (AI工作流)
> **来源**: [[entities/karpathy]] — https://x.com/karpathy/status/2079610838143623371
> **采集日**: 2026-08-08 / 2026-08-09
> **评分**: 用户 9 / 商业 6 / 传播 9 = 24

## 摘要

脑子乱、懒得打字时，对着 AI 叨叨 10 分钟就能理清思路。Karpathy 的方法：切到 /voice，stream-of-consciousness 瞎聊，LLM 极擅长把混乱长语音重建得比你开头还清楚。

## 详情

### 做法
- 切到 /voice，stream-of-consciousness 瞎聊 10 分钟，啥都行
- 有时声明"切到语音识别，错别字见谅"
- 有时变成几轮小采访
- LLM 极擅长把混乱长语音重建得比你开头还清楚 -> mind meld 更好，之后要改的更少

### 原理
很多人用 AI 写不出好东西，是因为懒得把需求说清楚。Karpathy 的方法反其道而行：不要求你说清楚，而是让你乱说，LLM 帮你理清。

## 我的判断

最低门槛的"AI 陪想"用法，今天就能用。适合写方案前先口头梳理。

可直接做成内容选题/短视频钩子："为什么你对着 AI 说话比打字更好用"。也适合做成小工作流产品（语音转结构化笔记）。

## 关联
- [[entities/karpathy]] — 提出者
- [[concepts/agent-as-daily-sms]] — 同属"低门槛 AI 工作流"
- [[topics/26-startup-directions]] — 方向 #12 "AI enablement" 的具体应用

## 来源
- [Karpathy 原推](https://x.com/karpathy/status/2079610838143623371) — 2026-07-21
- [[sources/keep-candidates/KEEP候选-08-08]] — 评分记录
- [[sources/keep-candidates/KEEP候选-08-09]] — #8 精简版

## 变更记录
- 2026-08-08: 初始创建，来源 08-08 采集
- 2026-08-09: 合并 08-09 精简版，更新格式为 wiki 页
