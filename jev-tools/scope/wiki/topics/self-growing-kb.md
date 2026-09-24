---
janitor:
  bucket: durable_memory
  persist: 1.86
  confidence: 0.72
  bucket_margin: 0.56
  contains_secret: 0.03
  safe_to_leave_in_git: 0.43
  action: frontmatter
  reason: normal vote
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  at: '2026-09-23T04:56:35Z'
---
# 自生长个人知识库：主题综述

> **类型**: topic
> **来源**: [[sources/obsidian-llm-wiki-zi-growth]]（苍何，2026-08-09）、旺旺现有 vault 实践
> **采集日**: 2026-08-31

## 摘要

"自生长知识库"指一套让人持续往里丢资料、AI 自动织成知识网、且越用越准的系统。代表实现是 Karpathy 的 LLM wiki + Obsidian + Agent。旺旺的 `obsidian_workspace` vault 已是其实操版。

## 核心要素

### 1. 三层结构（Raw / Wiki / Schema）
- Raw 存证据（只读），Wiki 记理解（AI 维护），Schema 定规则（SCHEMA.md / AGENTS.md）
- 旺旺对应：`sources/` + `wiki/` + `SCHEMA.md`

### 2. Agent 增量维护（不是一次性问答）
- 每次新资料进来，Agent 检索现有 Wiki → 补充/新建/连链 → 更新 index + log
- 区别于 RAG：RAG 每次临时拼答案、零积累；LLM wiki 改的是知识库本身

### 3. 人的角色：验收而非织网
- 人负责输入高价值资料 + 关键判断（纠正 AI 记错的地方）
- 不用自己整理，但需偶尔扫 index / 图谱确认织得对

### 4. 工具选型（文章提及）
- Obsidian：本地化、Markdown、双链、Git 可追踪
- Agent 层：WorkBuddy / Codex / Claude Code
- 落地三档：手动提示词 → claude-obsidian 插件 → WeSight 知识大脑（内测）

## 与旺旺现有实践的对齐

| 维度 | 文章标准版 | 旺旺 vault |
|------|-----------|------------|
| Raw 层 | `raw/articles` `raw/chats` … | `sources/raw-collect` `keep-candidates` `mpwechat` |
| Wiki 层 | `wiki/concepts` `entities` `topics` | 同，且已有 45 页 |
| 规则层 | `AGENTS.md` | `SCHEMA.md`（2026-08-31 已修订） |
| 索引/日志 | `index.md` `log.md` | 同（2026-08-31 已校准 index 为 45 页） |

> 结论：旺旺不需要重搭，补"增量维护纪律"（每次 ingest 重算 index）即可对齐"自生长"。

## 关联

- [[concepts/llm-wiki]] — 核心概念定义
- [[entities/karpathy]] — 方法源头
- [[sources/obsidian-llm-wiki-zi-growth]] — 来源文章摘要
- [[concepts/agent-as-daily-sms]] — 同源思路：Agent 作为日常信息入口

## 来源

- [[sources/obsidian-llm-wiki-zi-growth]]
- [原文](https://mp.weixin.qq.com/s/6pkU-Ggx1KkM_7Blgpbdhw)

## 变更记录

- 2026-08-31: 初始创建
