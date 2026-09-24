---
janitor:
  bucket: durable_memory
  persist: 1.85
  confidence: 0.76
  bucket_margin: 0.62
  contains_secret: 0.02
  safe_to_leave_in_git: 0.59
  action: frontmatter
  reason: normal vote
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  at: '2026-09-23T04:56:28Z'
---
# install .md 技能替代 .sh 脚本

> **类型**: concept (产品想法)
> **来源**: [[entities/karpathy]] — https://x.com/karpathy/status/2049903821095354523
> **采集日**: 2026-08-08
> **评分**: 用户 7 / 商业 7 / 传播 7 = 21

## 摘要

Karpathy 在 Sequoia 演讲里提出：把运维/安装步骤从"代码脚本"变成"人话说明书"，让 LLM 现场读、现场适配、现场排错。本质是把操作手册 AI 化。

## 详情

### 核心观点
> install .md skills instead of install .sh scripts. Why create a complex Software 1.0 bash script for e.g. installing a piece of software if you can write the installation out in words and say "just show this to your LLM". The LLM is an advanced interpreter of English and can intelligently target installation to your setup, debug everything inline.

> "you can outsource your thinking, but you cannot outsource your understanding"

### 机会
- 做"技能市场"——把常见运维/配置/部署步骤沉淀成 .md skills，普通人一键调用
- 这个想法和本 scout 的 skill 体系（SKILL.md/prompts）是同一个逻辑

### 警示
"不能外包理解"——AI 能干活，但你要懂它在干啥，否则出问题没法救。

## 关联
- [[entities/karpathy]] — 提出者
- [[strategy/行动卡-本周练手]] — 卡 B 就是实践这个理念
- [[topics/26-startup-directions]] — 方向 #12 "AI enablement"

## 来源
- [原推](https://x.com/karpathy/status/2049903821095354523) — 2026-08-08 采集
- [agent-native economy 演讲](https://x.com/karpathy/status/2049180863036813717)
- [[sources/keep-candidates/KEEP候选-08-08]] — 评分记录

## 变更记录
- 2026-08-08: 初始创建，来源 08-08 采集
