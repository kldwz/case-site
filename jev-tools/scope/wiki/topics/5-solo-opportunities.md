---
janitor:
  bucket: needs_review
  persist: 1.11
  confidence: 0.46
  bucket_margin: 0.25
  contains_secret: 0.02
  safe_to_leave_in_git: 0.55
  action: frontmatter
  reason: low confidence or explicit needs_review
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  suggested_bucket: log_entry
  at: '2026-09-23T04:56:35Z'
---
# 5 个可单干机会（周报精选）

> **类型**: topic (产品想法/周报精选)
> **来源**: [[weekly/周报-2026-08-09]]
> **筛选原则**: 一人能干、不融资、能先收钱；排除训练模型/大团队/牌照

## 摘要

从两日 KEEP 共 17 条中筛出 5 个"一个人能干、不融资、能先收钱"的方向。最稳入口是语音接电话和工具存活清单，最高杠杆是营销 agent 代投。

## 5 个机会

### 机会 1：本地商家"语音接电话 agent"
- 目标用户：5pm 后漏接单的本地商家（维修/家政/诊所）
- 痛点：漏接 = 直接丢钱，请人不值
- MVP：语音 LLM + 日历 API，先 3 家免费跑一周
- 收费：¥300-800/月
- 难度：低（套 API，不碰模型）
- 关联：[[topics/26-startup-directions]] 方向 #7

### 机会 2：小商家"营销 agent 代投"轻服务
- 目标用户：月营销预算<¥2000 的小店/个体
- MVP：手动串接 3 客户跑 2 周看 ROI
- 收费：¥499/月 + 消耗抽成
- 难度：中（需接 FB/小红书数据）
- 关联：[[concepts/marketing-agent-loop]]

### 机会 3：AI 工具"存活清单"订阅
- 目标用户：想用 AI 但怕踩坑的普通职场人
- MVP：每周 newsletter + 简单站
- 收费：免费引流 + ¥19/月去广告
- 难度：低
- 关联：[[topics/futuretools-dead-filtering]]

### 机会 4：PDF->可读 单功能工具
- 目标用户：烦 PDF 的任何人
- MVP：网页表单 + LLM 转换
- 收费：¥0.5/次或¥9/月
- 难度：低
- 关联：[[concepts/pdf-to-markdown]]

### 机会 5：垂直软件 AI-native 重做（Yoast 类）
- 目标用户：站点主/小商家
- MVP：选 1 个插件做 AI-first 版
- 收费：¥39-99/月
- 难度：中
- 关联：[[topics/26-startup-directions]] 方向 #14

## 顾问排序
- **最稳**：机会 1 + 3（下周可有付费用户）
- **最高杠杆**：机会 2（需先搞定数据授权）
- **别碰**：需训练模型、需大团队、需牌照的方向

## 关联
- [[weekly/周报-2026-08-09]] — 来源周报
- [[topics/26-startup-directions]] — 26 个方向全集
- [[strategy/副业作战地图]] — 旺旺的执行计划
- [[strategy/行动卡-本周练手]] — 本周可动手的任务

## 来源
- [[weekly/周报-2026-08-09]] — 周报精选
- [[sources/keep-candidates/KEEP候选-08-08]] + [[sources/keep-candidates/KEEP候选-08-09]] — 原始 KEEP

## 变更记录
- 2026-08-09: 初始创建，来源周报-2026-08-09
