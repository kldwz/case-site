---
janitor:
  bucket: reference
  persist: 1.49
  confidence: 0.56
  bucket_margin: 0.4
  contains_secret: 0.03
  safe_to_leave_in_git: 0.5
  action: frontmatter
  reason: normal vote
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  at: '2026-09-23T04:56:26Z'
---
# 用 WorkBuddy / Codex + Obsidian 搭建自生长的个人知识库实战

> 原始来源：微信公众号文章（苍何，2026-08-09）
> 原文链接：https://mp.weixin.qq.com/s/6pkU-Ggx1KkM_7Blgpbdhw
> 采集日：2026-08-31
> 说明：本文件为 Raw 层原始资料，内容原文保留，AI 整理后的结构化知识见 `wiki/` 对应页面。

---

## 核心观点

作者基于 Karpathy 公开的 LLM wiki 知识库构建方法，用 WorkBuddy / Codex + LLM wiki + Obsidian 搭了一套能"自生长"的个人知识库。核心不是 RAG 那种"每次提问临时拼答案"，而是给 AI 一份长期工作：持续维护知识库，每次加入资料都留下变化（新增概念、补关联、暴露待解问题），累积成自己的知识体系。

## 什么是 LLM wiki（三层架构）

- **Raw 层**：保存文章、论文、聊天记录等原始资料（只读，不修改）
- **Wiki 层**：沉淀 AI 整理出的概念、实体、主题
- **Schema 层**：规定 AI 如何归档、更新、引用、处理冲突（即 AGENTS.md）

一句话：Raw 保存证据，Wiki 记录理解，Schema 负责定规则。

## 为什么是 Obsidian

- 完全本地化、数据自主，Vault 就是普通文件夹，Markdown 纯文本
- Agent 可直接读目录、建页、改链、维护索引，变更可用 Git 追踪
- 双链、反向链接、知识图谱帮助发现核心节点和孤立页面
- 同时承担存储底座、人机操作界面、知识观察窗口三种角色

## Agent（WorkBuddy / Codex）做什么

新资料进 Raw 后，Agent 先理解内容、识别概念/实体/主题，再与现有 Wiki 对照：已有知识补充、新内容建页、相关建链；分歧保留来源/时间/适用范围；同步更新索引与变更日志。增量维护，不重建。

## 实战：三层目录模板

```
my-wiki/
├── AGENTS.md          # Schema 规范层
├── index.md           # 全局索引/站点地图
├── log.md             # 变更日志（只追加）
├── raw/               # 原始资料层（只读）
│   ├── articles/      # 剪藏文章、网页
│   ├── papers/        # 论文、报告
│   ├── books/         # 书籍、划线、笔记
│   ├── chats/         # 有价值的 AI 对话记录
│   ├── notes/         # 灵感碎片
│   └── meetings/      # 会议纪要
└── wiki/              # Wiki 层（AI 全权维护）
    ├── sources/       # 来源摘要页（一份 raw 对应一页）
    ├── concepts/      # 概念页
    ├── entities/      # 实体页（人物、公司、工具）
    └── topics/        # 主题综述页
```

## 三种搭建方法

1. **直接搭建法**：在 Agent 中打开 Vault，用一段详细提示词让 Agent 按三层架构建好结构、AGENTS.md、模板。粗暴但需懂提示词工程，AGENTS.md 要不断调。
2. **claude-obsidian 插件**：开源项目，把初始化/入库/索引/检索封装成 Agent Skill，用 ingest / retrieve 指令即可，门槛降低。
3. **WeSight 知识大脑**：把入库、更新、查询整合进 Obsidian 内部，一键加入笔记、Chat 时选"基于知识库"模式，内测中。

## 为什么是"自生长"

来自知识结构的持续增量更新。每次新资料进 Raw，Agent 按 Schema 检索现有 Wiki、补充旧页、建新节点、建双链、记来源与冲突。每次处理都留下可复用结构化结果，知识库随输入演化。Obsidian 提供载体和可视化，Agent 提供理解与编排，人负责输入高价值资料和关键判断。

## AGENTS.md 关键规则（作者给出）

1. 处理新资料前先检索现有 Wiki，判断补充还是新建
2. raw/ 是事实来源，禁止改写/删除/移动
3. 每份 Raw 在 wiki/sources/ 建对应摘要页，保留原链接
4. 概念/实体/主题用独立页面 + 双链，不堆一篇
5. 事实性内容标注来源；无法确认的写"待核实"
6. 新旧分歧同时保留说法、来源、时间、适用范围，不直接覆盖
7. 每次只更新受影响页，同步双链、index、log
8. log.md 只追加：日期、来源、新建/更新页、待确认事项
9. 不擅自删文件；同名先读并合并
10. 信息不足或影响整体结构时暂停并提问

## 给你的建议（作者原文结尾）

不需要一开始搭完美系统。先建三层目录，放一篇真实资料，让 Agent 完成第一次增量更新，再据实际使用调 Schema。只要每次输入都留下可复用结果，知识库就开始生长了。
