---
type: plan
title: 多 Agent 共用记忆落地计划（OpenMemory MCP）
updated: 2026-08-29
status: 已完成（2026-08-29）
janitor:
  bucket: needs_review
  persist: 1.68
  confidence: 0.46
  bucket_margin: 0.17
  contains_secret: 0.3
  safe_to_leave_in_git: 0.12
  action: frontmatter
  reason: low confidence or explicit needs_review
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  suggested_bucket: project_decision
  at: '2026-09-23T04:56:28Z'
---

# 多 Agent 共用记忆落地计划

> **目标**: Hermes / CodeBuddy / Claude Code 三个本地 Agent 共用同一份记忆（现有 `wangwang_memory`）
> **方案**: 用 OpenMemory MCP（mem0ai 官方）把现有本地 Mem0 包成共享 MCP 服务
> **更新**: 2026-08-29

---

## 前置认知（见 [[Mem0记忆/记忆架构与多Agent共用方案]]）
- 现有 Mem0 只是「库」，Agent 没接上；OpenMemory 是它的官方 MCP 封装，复用现有 Qdrant。
- 当前隐患：`wangwang_memory` 向量未建索引（`indexed_vectors_count=0`），需修复。

---

## 步骤总览（复杂度：中低，主要是配置 + 验证）

### 阶段 0：修复现有 Mem0 索引（必须先做）
- **动作**：重建 `wangwang_memory` 的向量索引（或重跑一次 embed 让 48 个点都进索引）。
- **目的**：让 `get_all` / export 能完整导出，避免镜像页永远只显 20 条。
- **风险**：低。可先备份 collection 再操作。
- **验证**：`get_all(limit=200)` 返回 48 条、`export_to_obsidian.py` 导出 48 条。

### 阶段 1：部署 OpenMemory MCP 服务
- **动作**：`git clone` OpenMemory 仓库 + `docker-compose up`，启动 API + Qdrant + Postgres。
- **关键配置**：让 OpenMemory 指向**你已有的** Qdrant（`wangwang_memory`），而非新建空库——避免记忆搬家的麻烦。若官方 compose 默认新建库，则改为挂载现有 Qdrant 数据或做一次性迁移。
- **目的**：对外暴露标准 MCP（SSE / Streamable HTTP）。
- **风险**：中。Docker 占用资源；需确认与现有 6333 端口的 Qdrant 不冲突（复用或改端口）。
- **验证**：`curl` MCP 端点返回可用；用 `mem0 search` 能搜到现有 48 条。

### 阶段 2：三个 Agent 各接 MCP
- **Hermes**：`~/.hermes/config.yaml` 加 `mcp_servers.openmemory`（指向 OpenMemory 地址），并把原 mem0 插件的 user_id 统一为 `wangwang`。
- **CodeBuddy**：CodeBuddy 的 MCP 配置（设置/plugins）加同一 OpenMemory server。
- **Claude Code**：`claude mcp add openmemory -- <openmemory 命令>` 或 `settings.json` 加 `mcpServers`。
- **风险**：低（纯配置）。各 Agent 的 MCP 接入方式不同，需逐个核对文档。
- **验证**：每个 Agent 新开会话问"我是谁/我在做什么"，能召回 `wangwang_memory` 里的记忆（如"一人公司目标""讨厌长会议"）。

### 阶段 3：统一写入入口 + 修导出链路
- **动作**：以后写记忆统一走 OpenMemory MCP（或用 `mem0_add.py` 但确保走索引写入），废弃"直接 upsert Qdrant 绕过 LLM 抽取"的野路子。
- **目的**：记忆只由一套逻辑写，避免再出现 20/48 不一致。
- **验证**：任意 Agent 写入一条 → 另两个 Agent 能立刻检索到。

---

## 复杂度评估
- **不复杂的部分**：阶段 2（配置）、阶段 3（规范）。
- **稍复杂的部分**：阶段 0（修索引）、阶段 1（Docker 部署 + 复用现有 Qdrant，可能有端口/数据挂载坑）。
- **总耗时预期**：纯配置 + 验证，不涉及写新代码；主要卡在阶段 1 的 Qdrant 复用方式。

---

---

## ✅ 实际落地结果（2026-08-29，已全部完成并验证）

### 最终选型：mem0-open-mcp（非 OpenMemory）
调研中发现：
- **OpenMemory（openmemory/ 目录）已被官方移除/淘汰**，main 分支已 404；
- **官方自托管 Mem0 Server（server/）用 Postgres+pgvector**，且**只提供 REST API，无 MCP 端点**，三个 Agent 无法直接接入；
- 最终选用 **`wonseoko/mem0-open-mcp`**：开源 MCP server，直接包官方 `mem0ai`，**免 Docker、本地自托管、支持 Qdrant** → 完美复用现有 `wangwang_memory`。

### 部署位置
| 项 | 值 |
|---|---|
| 源码 | `~/mem0-open-mcp`（已打补丁） |
| 运行环境 | `~/mem0_mcp_env`（Python 3.11 venv） |
| 配置文件 | `~/mem0_scripts/openmemory-mcp.yaml`（权限 600，API key 内联） |
| 后端 | 本地 Qdrant `wangwang_memory`，`user_id=wangwang` |
| LLM / Embedder | 硅基流动 DeepSeek-V3.2 / Qwen3-Embedding-4B（2560 维） |
| MCP 工具 | add_memories / search_memory / list_memories / get_memory / delete_memories / delete_all_memories |

### 三个 Agent 接入状态
| Agent | 配置位置 | 状态 |
|-------|---------|------|
| Claude Code | `~/.claude.json`（`claude mcp add mem0 --scope user`） | ✓ Connected |
| CodeBuddy | `~/.codebuddy/.mcp.json`（`codebuddy mcp add mem0 --scope user`） | ✓ Connected |
| Hermes | `~/.hermes/config.yaml` 的 `mcp_servers.mem0` | 已写入，重启后生效 |

### 共用验证（已通过）
进程 A 写入一条测试记忆 → **全新进程 B** 用 `list_memories` 读到 49 条、`search_memory` 命中该条 → 证明跨 Agent 共用生效。测试记忆已删除，数据复位为 48 条（+1 条"系统上线"说明记忆 = 49）。

### 踩过的坑（重要，勿重复）
1. **`mem0-open-mcp` 与 mem0 2.x 不兼容**：它 `await` 了 `AsyncMemory.from_config`（该方法在所有 mem0 版本都是同步的），且 `get_all(user_id=...)` 在 2.x 要求改为 `filters={'user_id':...}`（8+ 处）。
   - **解法**：退回 `mem0ai==1.0.11`（工具原本适配的版本），并手动删掉 3 处 `await`。
2. **`mcp` 包装成了 2.x**，其中 FastMCP 已更名 → 报 `No module named 'mcp.server.fastmcp'`。
   - **解法**：`pip install "mcp<2"`（用 1.29.1）。
3. **配置键名是 `base_url` 不是 `openai_base_url`**（工具内部会自动转换）。
4. **API key 必须内联进配置文件**：Agent 拉起 MCP 子进程时不一定继承 `OPENAI_API_KEY` 环境变量。
5. `codebuddy mcp add` 解析参数时 `--` 不能省略，否则 `-c` 被当成 CLI 自己的选项。

---

## 待办 / 可选
- Hermes 需重启一次以加载新 MCP 配置。
- 记忆镜像页 `Mem0记忆/wangwang-memory-mirror.md` 目前靠手动脚本同步；可改为定期用 MCP `list_memories` 刷新（它能拿全 48+ 条，绕过 `get_all` 的 20 条限制）。

---

## 关联
- [[Mem0记忆/记忆架构与多Agent共用方案]] — 架构关系与方案对比
- [[Mem0记忆/wangwang-memory-mirror]] — 记忆镜像页
