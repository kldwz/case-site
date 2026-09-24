---
type: architecture-note
title: 记忆架构：Mem0 库 → 本地实例 → OpenMemory MCP 封装
updated: 2026-08-29
janitor:
  bucket: project_decision
  persist: 1.66
  confidence: 0.71
  bucket_margin: 0.63
  contains_secret: 0.25
  safe_to_leave_in_git: 0.26
  action: frontmatter
  reason: normal vote
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  at: '2026-09-23T04:56:26Z'
---

# 记忆架构与多 Agent 共用方案

> **类型**: architecture-note
> **更新**: 2026-08-29
> **目标**: 本地多 Agent（Hermes / CodeBuddy / Claude Code）共用同一份记忆

---

## 一、三者关系（关键认知）

```
Mem0 项目 (github.com/mem0ai/mem0, Apache 2.0)
   │  只是「库/SDK」：Memory() 实例可 add/search
   ▼
本地实例 (~/mem0_scripts + Qdrant collection "wangwang_memory", user_id=wangwang)
   │  你已经在用，但只有脚本在用，Agent 没接上
   ▼
OpenMemory MCP (mem0ai 官方 MCP 封装，docker-compose: API+Qdrant+Postgres)
   │  把上面的实例包成标准 MCP 服务，对外暴露 SSE/HTTP
   ▼
各 Agent 加一个 MCP 配置 → 共用同一份记忆
```

**结论**：不用换技术，只是把已有的 Mem0 用 OpenMemory 包成共享服务。

---

## 二、当前真实状态（2026-08-29 核查）

- Qdrant `wangwang_memory` collection 共 48 个点，全部 `user_id=wangwang`。
- `indexed_vectors_count = 0` → 向量未建索引，导致 `get_all` / `export_to_obsidian` 只能看到 20/48 条（**隐患，需修**）。
- `m.add()` 对「清单式长文本」返回空 results、不写库（LLM 事实抽取丢弃）——上一轮写 X 账号时是直接 upsert Qdrant 点绕过的。
- 三个 Agent 默认都没接 Mem0：
  - **Hermes** 有 mem0 插件能力，但 `wangwang_memory` 里无 `hermes-user` 数据 → 未指向本库。
  - **CodeBuddy** trace 里出现过 `wangwang_memory`，但默认记忆目录未接 → 非持久共享。
  - **Claude Code** 配置里无任何 mem0/qdrant 引用 → 未接。

---

## 四、阶段0已完成（2026-08-29）：索引真相澄清

- **重建了 `wangwang_memory`**：原 10 个零向量点已补算 2560 维 embedding（用现有 embedder），collection 删除重建为带 `hnsw_config` + `bm25` 稀疏向量槽的正确 schema，48 个点全量导入。
- **`indexed_vectors_count` 仍为 0 是正常的**：Qdrant 1.19 默认 `full_scan_threshold=10000`，点数（48）远低于阈值时**故意不建 HNSW 索引**，改用全量扫描，检索结果完全准确，不影响使用。这不是故障。
- **Mem0 `get_all` 恒返回 20 条是其自身分页限制**（与 limit 参数无关），不影响 `search` 语义检索，也不影响记忆共享。镜像页改用 Qdrant 直接全量读取（48 条）重写。
- **备份**：`~/mem0_backup/` 下有 snapshot（310MB）+ points JSON（48 点含向量），可随时回滚。

---

## 三、候选开源方案对比（多 Agent 共用维度）

| 项目 | 后端 | 多 Agent 共用 | 本地 | 与你现状 |
|------|------|--------------|------|---------|
| **OpenMemory MCP**（mem0ai 官方） | Qdrant+Postgres(Docker) | ✅ 标准 MCP | ✅ | **复用现有 Qdrant+Mem0，迁移最低** |
| **mcp-memory-service**（doobidoo） | SQLite-vec/Milvus | ✅ 25+ 客户端, X-Agent-ID 隔离 | ✅ | 轻量但不复用 Qdrant |
| **agentmemory**（rohitg00） | 纯 SQLite | ✅ Hook 自动捕获 | ✅ | 召回最高 95.2%，偏 Coding Agent |
| Mem0（库，已在用） | Qdrant+LLM | 需自建服务暴露 | ✅ | 即当前 `wangwang_memory` |
| Zep CE / Cognee / Letta | 各自 DB | 需部署服务 | ✅ | 时序/图谱/状态机，非必需 |

**选定方向**：OpenMemory MCP（复用现有投入，改造最小）。

---

## 四、关联
- [[Mem0记忆/wangwang-memory-mirror]] — 记忆镜像页（人看）
- [[entities/x-ai-accounts]] — 已写入的 X 关注账号清单
