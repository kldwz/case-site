---
janitor:
  bucket: reference
  persist: 1.72
  confidence: 0.56
  bucket_margin: 0.31
  contains_secret: 0.03
  safe_to_leave_in_git: 0.46
  action: frontmatter
  reason: normal vote
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  at: '2026-09-23T04:56:34Z'
---
# 来源摘要：用 WorkBuddy/Codex + Obsidian 搭建自生长个人知识库

> **类型**: source
> **来源**: [[sources/mpwechat/用WorkBuddy_Codex加Obsidian搭建自生长个人知识库]] — 微信公众号（苍何，2026-08-09）
> **采集日**: 2026-08-31
> **关联概念**: [[concepts/llm-wiki]]、[[topics/self-growing-kb]]
> **关联实体**: [[entities/karpathy]]

## 摘要

作者基于 Karpathy 公开的 LLM wiki 方法，用 Agent（WorkBuddy / Codex）+ Obsidian 搭建能"自生长"的个人知识库。核心区别于 RAG：不是每次提问临时拼答案，而是让 AI 持续增量维护知识库，每次资料进来都留下变化。

## 核心内容

- **三层架构**：Raw（原始资料，只读）/ Wiki（AI 整理的概念·实体·主题）/ Schema（AGENTS.md 规定归档、更新、引用、冲突处理规则）
- **为什么 Obsidian**：本地化、Markdown 纯文本、Agent 可直接读写、双链图谱、Git 可追踪
- **Agent 职责**：新资料进 Raw 后检索现有 Wiki，补充旧页 / 建新页 / 建双链 / 记来源与冲突 / 更新 index 与 log
- **三种落地法**：① 直接提示词搭建 ② claude-obsidian 插件（ingest/retrieve）③ WeSight 知识大脑（内测）
- **AGENTS.md 10 条规则**：重点是 raw 只读、事实标来源、分歧保留不覆盖、log 只追加、信息不足先暂停提问

## 我的判断（AI 推理，待旺旺确认）

这套方法和旺旺现有 vault 的 SCHEMA/raw/wiki 三层思路高度一致，可直接对齐。差异点：作者用 `raw/` + 子分类（articles/papers/chats…），旺旺用的是 `sources/raw-collect` + `keep-candidates` + `mpwechat`，本质都是 Raw 层，命名不同而已。可把本文作为 vault 的"方法论参照"固化进 concepts。

## 相关页面

- [[concepts/llm-wiki]] — 什么是 LLM wiki
- [[topics/self-growing-kb]] — 自生长知识库主题综述
- [[entities/karpathy]] — 方法源头人物

## 来源

- [原推文/原文](https://mp.weixin.qq.com/s/6pkU-Ggx1KkM_7Blgpbdhw) — 采集 2026-08-31
- [[sources/mpwechat/用WorkBuddy_Codex加Obsidian搭建自生长个人知识库]] — 本地 Raw 副本

## 变更记录

- 2026-08-31: 初始创建（由本文整理）
