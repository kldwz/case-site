---
janitor:
  bucket: needs_review
  persist: 1.36
  confidence: 0.5
  bucket_margin: 0.27
  contains_secret: 0.05
  safe_to_leave_in_git: 0.57
  action: frontmatter
  reason: low confidence or explicit needs_review
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  suggested_bucket: log_entry
  at: '2026-09-23T04:56:31Z'
---
# emollick (Ethan Mollick)

> **类型**: entity (person)
> **身份**: Wharton 教授，AI 与教育/工作研究专家
> **追踪源**: X @emollick
> **关注动机**: learn AI science

## 摘要

从学术视角分析 AI 对工作的影响。本期贡献了 LLM 理财建议研究和 computer-use 演示。他对 AI 安全事件（Astra/Mythos 模型）也有深度评论。

## 关键观点汇总

### AI 与工作
- [[topics/llm-financial-advice]] — 普通人听 LLM 理财建议反而更划算（评分 23）
- [[concepts/codex-control-bluetooth]] — Codex 控制电脑开关蓝牙（评分 20）

### AI 安全
- Astra 模型被列为首个"critical"网络安全模型
- Vingean soft take-off scenario 正在发生
- AI benchmark 分数都有隐含星号（harness 限制）

### 新书
- "Co-Existence"（10 月 20 日出版）：关于如何与有时比我们更聪明的 AI 共存共事

## 采集统计
- 08-08: 2 条 KEEP（LLM 理财, Codex 蓝牙）
- 08-09: 0 条 KEEP（内容多为书讯/安全恐慌/情绪帖，被 IGNORE）

## 来源
- [[sources/raw-collect/原始采集-08-08]] — 08-08 原始采集
- [[sources/raw-collect/原始采集-08-09]] — 08-09 原始采集

## 变更记录
- 2026-08-09: 初始创建，汇总 08-08 + 08-09 采集内容
