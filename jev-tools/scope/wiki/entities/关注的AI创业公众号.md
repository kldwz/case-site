---
title: 关注的 AI 创业公众号清单（反推）
created: 2026-09-05
source: 从 sources/mpwechat/ 已存文章反推 + 用户陈述
note: 本地存档只能反推部分关注；完整关注列表需用 WeChatMsg 解密本机微信数据库
janitor:
  bucket: needs_review
  persist: 1.28
  confidence: 0.35
  bucket_margin: 0.14
  contains_secret: 0.52
  safe_to_leave_in_git: 0.28
  action: frontmatter
  reason: low confidence or explicit needs_review
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  suggested_bucket: durable_memory
  at: '2026-09-23T04:56:34Z'
---

# 我关注的 AI 创业 / 独立开发公众号（反推版）

> 用途：喂给 `wechatDownload` 批量拉取进知识库（见 WorkBuddy/wechatDownload/wechat_pull.py）。
> 关联：[[10-indie-first-bucket-criteria]] ｜ [[为什么还没有拿到第一桶金-看看这10条准则]]

## 高置信（存档明确署名 / 正文中点名 / 已解析 __biz）

| 公众号 | 证据 | __biz | 主题 |
|---|---|---|---|
| **苍何** | `用WorkBuddy_Codex加Obsidian搭建自生长个人知识库.md` 署名「苍何」 | `MzU4NTE1Mjg4MA` | AI 工具链、Obsidian 知识库、独立开发 |
| **三此君** | 《为什么还没有拿到第一桶金》原文 `nick_name:'三此君'` | `Mzg2MzczOTM1Nw` | 独立开发 / 第一桶金方法论 |
| **陈天宇宙** | `wiki/bookmarks/bookmarks-2026-08-09.md` 收藏《陈天宇宙支付全集》 | `Mzg2MTg1NTM4NA` | 支付 / 创业 |
| **伍六七AI编程** | `挖到宝藏开源工具…` / `temp_article.md` 正文反复点名 | （待解析） | AI 编程、工具测评 |

## 中 / 低置信（按主题推断，号名未知，需你确认）

以下文章来自你关注的号，但存档里没有可靠署名，需你核对号名后回填到 `wechat_pull.config.json`：

| 已存文章 | 推断领域 | 疑似号类型 |
|---|---|---|
| 从0到1，我在Coze上打造财富测评Skill的真实历程 | Coze / AI 应用开发 | AI 应用开发者 |
| 我花10块钱，给自己的黄金交易配了个"顶级研究员" | AI 自动化 + 量化/交易情报 | 副业自动化博主 |
| 实测腾讯CodeBuddy Code：Claude Code平替 | AI 编程工具测评 | AI  Coding 测评号 |
| 用了7年为知笔记，几千篇笔记导出难住我 | 笔记/知识管理 | 效率工具号 |
| 花大价钱入手Screen Studio | 创作工具 | 创作者工具号 |
| 发现一个超牛的chrome插件，截图+录制一键搞定 | 浏览器插件 | 工具推荐号 |
| 为什么还没有拿到第一桶金-看看这10条准则 | 独立开发 / 第一桶金 | 独立开发方法论号 |
| 偶像的书《MAKE：初创者手册》被我用插件翻译 | 创业/读书 | 创业读书号 |
| 录屏踩坑后，我最终锁定了这款Mac神器 | Mac 创作工具 | （与苍何风格高度重合，疑似同一号） |

## 待办

- [ ] 在微信里核对"中/低置信"号的真实名称，回填 `wechat_pull.config.json` 的 `accounts`
- [ ] 用 WeChatMsg 解密本机微信，导出完整关注列表（含 `gh_` biz），补全本表
- [ ] 拉取方式：当前 macOS 14.4.1 跑不了本地 app（需 15.0+），先走云端兜底
      `python3 wechat_pull.py single <URL>` 把单篇/合集拉进 `sources/mpwechat/`；
      升级到 macOS 15 后再用 `batch` 做整号全量历史下载。
