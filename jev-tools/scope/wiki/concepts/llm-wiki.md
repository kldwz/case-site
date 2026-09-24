---
janitor:
  bucket: durable_memory
  persist: 1.95
  confidence: 0.88
  bucket_margin: 0.82
  contains_secret: 0.03
  safe_to_leave_in_git: 0.49
  action: frontmatter
  reason: normal vote
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  at: '2026-09-23T04:56:28Z'
---
# LLM Wiki：让 AI 持续维护、自生长的知识库

> **类型**: concept
> **来源**: [[sources/obsidian-llm-wiki-zi-growth]] — 苍何《用 WorkBuddy/Codex + Obsidian 搭建自生长个人知识库》
> **采集日**: 2026-08-31
> **评分**: 用户 9 / 商业 6 / 传播 7 = 22

## 摘要

LLM wiki 是 Karpathy 提出的一种知识库架构：不给 AI 一次性问答，而是给 AI 一份"长期工作"——持续维护一个知识库。每次加入资料，Agent 都检索现有页面、补充旧页、新建概念、建立双链，并保留分歧与来源。知识因此"自生长"。

## 详情

### 与 RAG 的本质区别

- **RAG / NotebookLM / 文件上传**：你提问 → 模型召回片段 → 临时拼答案 → 答完即散。同样问题问一百遍，重新拼一百遍，知识零积累。
- **LLM wiki**：你加入资料 → Agent 改知识库本身（新增/补充/连链）→ 知识库随输入持续演化。提问只是读取已沉淀的网。

### 三层架构

| 层 | 作用 | 旺旺 vault 对应 |
|----|------|----------------|
| Raw | 原始资料，只读不改 | `sources/`（raw-collect / keep-candidates / mpwechat） |
| Wiki | AI 整理的概念·实体·主题 | `wiki/`（concepts / entities / topics） |
| Schema | 规则层（AGENTS.md） | `SCHEMA.md` |

### 自生长的关键

每次处理必须"留下变化"：可能新增一个概念、补一条关联、或暴露一个待解问题。变化累积 → 真正属于自己的知识体系。

## 我的判断（AI 推理，待旺旺确认）

旺旺现有 vault 已是 LLM wiki 的实操版（SCHEMA + raw + wiki + log + 双链），只是之前没用"LLM wiki"这个名字，也没把"增量维护纪律"（每次 ingest 重算 index）固化。本文价值在于**提供了标准术语和 AGENTS.md 10 条规则范本**，可直接对照补全旺旺的 SCHEMA。

## 关联

- [[entities/karpathy]] — 方法源头人物（前 Tesla AI 总监）
- [[topics/self-growing-kb]] — 自生长知识库主题综述
- [[sources/obsidian-llm-wiki-zi-growth]] — 来源文章摘要
- [[concepts/agent-as-daily-sms]] — 旺旺已有：Agent 作为日常信息入口的思路，与"Agent 维护知识库"同源

## 来源

- [[sources/obsidian-llm-wiki-zi-growth]] — 本地摘要页
- [原文](https://mp.weixin.qq.com/s/6pkU-Ggx1KkM_7Blgpbdhw) — 微信公众号 苍何 2026-08-09

## 变更记录

- 2026-08-31: 初始创建
