---
janitor:
  bucket: durable_memory
  persist: 1.83
  confidence: 0.77
  bucket_margin: 0.65
  contains_secret: 0.08
  safe_to_leave_in_git: 0.54
  action: frontmatter
  reason: normal vote
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  at: '2026-09-23T04:56:35Z'
---
# levelsio 用 AI agent 做出网页版视频编辑器

> **类型**: topic (创业案例)
> **来源**: [[entities/levelsio]] — status/2083654998404268188 + status/2084422532812222705
> **采集日**: 2026-08-08 / 2026-08-09
> **评分**: 用户 9 / 商业 8 / 传播 9 = 26

## 摘要

Pieter Levels（一人公司标杆）用 vibecoding 做出了网页版 Premiere/Capcut。核心不是 AI 生成 10 秒片段，而是**生成+剪辑闭环**在一个界面里。Agent 侧边栏让你动嘴就能剪视频。

## 详情

### 第一阶段：vibecode 出视频编辑器
- 原本"我绝不敢想做网页版 Premiere/Final Cut/Capcut"——太难了，从哪下手？
- AGI 摧毁护城河的讨论反而让他想 ship
- 结论：能用 AI 更快更好地发布，就该做更复杂的东西
- 直接用 vibecoding 做进了 Photo AI：全功能视频编辑器，能直接在编辑器里用你/你训练的模型生成视频
- 试做了"我作为数字游民抵达曼谷"的短片

### 第二阶段：Agent 侧边栏
- Cursor 式侧边栏，直接对 agent 说"按我的素材和故事剪"
- Agent 把当前状态发给 xAI，按你的叙事自动编辑
- 还能 [Send to video editor] 把生成的视频片段直接接进时间线
- 右键不满意的片段 -> [Regenerate] 改 prompt 原地替换

### 一人公司启示
- 原本"我绝不可能做网页版 Premiere/Capcut" -> vibecoding 直接做出来了
- 视频模型 likeness 够好，可生成"你本人演的短电影"
- 关键不是 AI 生成 10 秒片段，而是**生成+剪辑闭环**在一个界面里

### 可复制点
把"你本来懒得做的创作动作"包成对话式 agent。垂直版"AI 视频编辑 Agent"（口播/带货/旅行 vlog）比通用剪辑器易切入。

## 关联
- [[entities/levelsio]] — 一人公司标杆
- [[topics/26-startup-directions]] — 方向 #6 "build for the physical world"
- [[topics/5-solo-opportunities]] — 信号 3 "一人公司用 agent 做重活"
- [[concepts/copilot-to-loop-framework]] — "build agent for xyz" 的案例

## 来源
- [原推 1：vibecode 视频编辑器](https://x.com/levelsio/status/2083654998404268188) — 2026-08-08 采集
- [原推 2：Agent 侧边栏](https://x.com/levelsio/status/2084422532812222705) — 2026-08-09 采集
- [[sources/keep-candidates/KEEP候选-08-08]] — #64 评分记录
- [[sources/keep-candidates/KEEP候选-08-09]] — #5 精简版

## 变更记录
- 2026-08-08: 初始创建（详细版含原文+翻译+解读），来源 08-08 采集
- 2026-08-09: 合并 08-09 精简版（Agent 侧边栏阶段），更新格式为 wiki 页
