---
type: concept
title: 生产级上下文工程 vs Day8 教学版
created: 2026-08-12
tags: [agent, context-engineering, day8, 一人公司]
janitor:
  bucket: durable_memory
  persist: 1.91
  confidence: 0.96
  bucket_margin: 0.94
  contains_secret: 0.02
  safe_to_leave_in_git: 0.59
  action: frontmatter
  reason: normal vote
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  at: '2026-09-23T04:56:28Z'
---

# 生产级上下文工程 vs Day8 教学版

> **类型**: concept (Agent 上下文工程 / 学习地图)
> **来源**: 旺旺在 Day8（上下文工程）学完最小范式后追问"生产级怎么做" + 讲解梳理
> **采集日**: 2026-08-12
> **关联**: [[concepts/production-vs-tutorial-memory]]（记忆篇对照）、[[entities/ai-bloggers]]、Day8/Day9 笔记

## 摘要

Day8 写的 `08_context_assembly.py` 是"教学版上下文工程"：检索记忆→取 top_k=5→每条截断 80 字→拼成一段塞 prompt。它让人看懂"为什么要裁剪、裁剪省多少"，但生产级不是"写个 truncate 函数"。本文把"教学版 vs 生产级"差距地图固化，标注旺旺还差哪几层。

## 教学版（Day8 已掌握）

```
检索记忆 → 取 top_k=5 → 截断 80 字 → 拼成一段 markdown 塞进 prompt
```
- 只有"记忆"单来源
- 裁剪=全局 top_k + 分数截断
- 压缩=字符串截断（丢信息）
- 纯文本、每轮全量重装

## 生产级差距（6 块）

### 1. 多来源汇聚（教学版只有记忆一路）
真实 Agent 上下文来自多路 fan-in，要统一编排：
- 系统提示（人写死）
- 用户当前输入
- 检索记忆（Mem0）
- 检索知识（RAG，将来 RAGFlow）
- 工具调用结果（Day9 MCP 返回）
- 历史对话（压缩后）
- 工作记忆（当前任务状态）
生产里是个多路汇聚器，不是单路检索。

### 2. 裁剪不是"取 top_k"那么傻
- **按任务定向取**：在写代码就取代码记忆，聊偏好就取偏好，非无脑全局 top_k
- **预算分配 budget allocation**：总窗口切好——系统提示 5k / 历史 30k / 检索 20k / 工具结果 40k，不抢位
- **重排 rerank**：交叉编码器重排，比 embedding 余弦更准，最相关的真排最前

### 3. 压缩用真摘要，不是截断
- 长对话/文档喂**小模型做摘要**（便宜 LLM 把 50 轮压成 10 句）
- **结构化保底**：名字/约束/关键决策抽成 JSON 字段，永不被压掉
- 分级压缩：最近 3 轮原文、更早压摘要、再早只留索引

### 4. 结构化上下文，不是纯文本
教学版是一段 markdown。生产常是结构化块，模型对边界更敏感、程序易读易调：
```
<user_profile>{JSON}</user_profile>
<recent_dialog>{压缩摘要}</recent_dialog>
<retrieved_docs>{带引用片段}</retrieved_docs>
<tool_results>{结构化}</tool_results>
```

### 5. 动态 vs 静态上下文
- 常驻上下文（profile、系统提示，不变）+ 临时上下文（本轮检索/工具结果，用完可丢）
- 省成本省延迟，而非每轮重装全量

### 6. 可观测 + 评估（未碰）
- 回溯：答错能查"哪条上下文带偏"
- 压测：窗口 80%/100% 时效果掉多少
- 成本监控：每轮上下文多少 token / 延迟

## 落地优先级（旺旺路线）

| 优先级 | 动作 | 现状 | 成本 |
|--------|------|------|------|
| 高 | 多来源汇聚（工具结果/RAG 接进上下文） | 只有记忆 | 低 |
| 高 | 预算分配（别让某路撑爆窗口） | 无 | 低 |
| 中 | 真摘要替代截断 | 截断 | 中（调小模型） |
| 中 | 结构化上下文块 | 纯文本 | 低 |
| 低（做产品才要） | rerank / 可观测 / 评估 | 无 | 高 |

## 易错点钉死
1. "塞得越多越好"是反直觉坑——lost-in-the-middle：模型忽视中间内容。
2. **记忆 ≠ 上下文**：记忆在外部（可能几万条），上下文是当前这轮真正喂模型的那段（有限），桥接靠"检索+裁剪"。
3. 截断会丢信息：关键事实（名字/偏好/约束）必须保底保留，不能压没。
4. 裁剪 top_k 不是拍脑袋：按场景调，且配合 rerank。

## 和课程闭环
- **Day7 记忆/RAG**：提供原材料
- **Day8**：教"怎么装车"（教学版），本文是其生产级延展
- **Day9 MCP**：引入"工具结果"新上下文来源 → 多来源汇聚第一块雏形（记忆+工具结果两路）
- **[[concepts/production-vs-tutorial-memory]]**：记忆篇对照，本文是上下文篇对照，两篇并列

## 关联
- [[concepts/production-vs-tutorial-memory]] — 生产级记忆 vs Day7 教学版
- [[entities/ai-bloggers]] — 旺旺关注博主总表（含 Mem0/上下文工程信源）
- Day8-上下文工程（笔记）、Day9-通信协议（待写）
