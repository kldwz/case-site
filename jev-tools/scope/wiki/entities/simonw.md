---
janitor:
  bucket: needs_review
  persist: 1.69
  confidence: 0.54
  bucket_margin: 0.39
  contains_secret: 0.05
  safe_to_leave_in_git: 0.52
  action: frontmatter
  reason: low confidence or explicit needs_review
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  suggested_bucket: durable_memory
  at: '2026-09-23T04:56:33Z'
---
# simonw (Simon Willison)

> **类型**: entity (person)
> **身份**: Datasette 创始人，llm/shot-scraper 等 CLI 工具作者
> **追踪源**: X @simonw
> **关注动机**: learn 用 LLM 做实事（AI Engineer 实操）
> **标签**: 实操密度极高 / 无水分
> **加入关注清单**: 2026-09-13（核心 10 人清单）

## 摘要

关注 AI 工具实用化和安全问题。本期贡献了 PDF 转 Markdown 的刚需信号，以及多篇关于 AI agent 安全事件的技术分析。

## 关键观点汇总

### AI 工具
- [[concepts/pdf-to-markdown]] — PDF 转 Markdown 是 Accenture 大头 token 支出（评分 24）

### 安全分析
- OpenAI-HuggingFace 事件详细时间线分析
- "Felony humble-bragging"：AI agent 逃逸事件正在变成营销/PR 炒作
- Codex Desktop / GPT-5.6 Sol Ultra 构建游戏实验（Raccoon Heist -> Moonlight & Mayhem）

### 实用技巧
- ChatGPT mobile 长按发送按钮可调 effort（"slingshot"）
- 消费者模型名 vs API 模型名混淆问题

## 采集统计
- 08-08: 1 条 KEEP（PDF 转 Markdown）
- 08-09: 1 条 KEEP（#9 PDF 转 Markdown 精简版）

## 来源
- [[sources/raw-collect/原始采集-08-08]] — 08-08 原始采集
- [[sources/raw-collect/原始采集-08-09]] — 08-09 原始采集

## 变更记录
- 2026-08-09: 初始创建，汇总 08-08 + 08-09 采集内容
- 2026-09-13: 列入用户核心关注 10 人清单，补关注动机与标签
