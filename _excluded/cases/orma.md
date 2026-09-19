---
name: Orma
一句话: Best Hybrid AI App (Chrome Extension)（Google Chrome 内置 AI 挑战赛）：给浏览器装一层记忆，让你可以跟自己读过的东西对话。
创始人地区: 独立开发者/小团队参赛作品，提交于 Google Chrome Built-in AI Challenge
场景: 浏览器记忆层：把浏览过的网页抓下来，之后可以用自然语言跟自己的浏览历史对话
营收模式: 尚未商业化（黑客松参赛作品，无营收数据）
月收入估算: 无收入（黑客松获奖作品）
流量来源: 赛事作品页 + 端侧/浏览器 AI 话题传播
原文链接: https://devpost.com/software/orma
数据口径: Devpost 官方作品页（https://devpost.com/software/orma），2026-09-13 抓取：赛事 Google Chrome Built-in AI Challenge（https://googlechromeai.devpost.com/）、奖项 Best Hybrid AI App (Chrome Extension)、56 likes、技术栈 chrome / googlenano / openai / react / tailwindcss。无营收数据
分类: AI 应用 / 浏览器内置 AI / 英文
类型: 获奖作品
证据等级: 平台数据可查
平台数据: Devpost 官方作品页：Best Hybrid AI App (Chrome Extension) · 56 likes（2026-09-13）
赛事: Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）
奖项: Best Hybrid AI App (Chrome Extension)
封面: /case-site/cases/orma/site.png
---

![Orma 作品页](/cases/orma/site.png)

> **赛事**：Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）
> **场景**：浏览器记忆层：把浏览过的网页抓下来，之后可以用自然语言跟自己的浏览历史对话
> **奖项**：Best Hybrid AI App (Chrome Extension)
> **出处**：[作品页](https://devpost.com/software/orma) ｜ [赛事页](https://googlechromeai.devpost.com/)

# Orma：给浏览器装一层记忆，让你可以跟自己读过的东西对话。

## 它做了什么

Orma 给浏览器加了一层「记忆」：你照常上网，它在后台把你读过的内容抓下来、结构化，之后你可以直接问它——「我上周看的那篇讲 X 的文章说了什么？」「把我看过的关于 Y 的内容总结一下」。

## 这个解法妙在哪

1. **它解决的是"读过就忘"**。我们每天读大量网页，但搜索引擎搜不到"我读过的内容"，收藏夹也是只进不出。
2. **定位成"记忆层"而不是"书签"**。书签存的是地址，它存的是内容，而且能对话。
3. **混合架构是现实最优解**：轻量理解用浏览器内置模型（Google Nano），重任务交给 OpenAI——成本和能力两头占。
4. **数据是自己的**：浏览历史存在本地，这既是隐私卖点，也是产品成立的前提。

## 技术怎么实现的

浏览器扩展（Chrome）+ React + TailwindCSS；理解层调用 Google Nano（浏览器内置模型）与 OpenAI；数据存在本地。前端抓取与结构化页面内容，再交给模型做理解和问答。

## 团队与赛事

Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）（赛事页 https://googlechromeai.devpost.com/）。作品页获 **Best Hybrid AI App (Chrome Extension)** 徽章，56 个赞。

## 这个案例能学到什么

1. **"读过就忘"是每个人的痛点**，但几乎没有产品真的解决它。
2. **记忆层比书签高一个维度**。存地址没用，能对话才有价值。
3. **混合模型架构是当下的现实最优解**：轻任务本地、重任务云端。
4. **本地存储既是隐私优势，也是产品前提**。
5. **"跟自己的历史对话"这个说法，一句话就能让人听懂。**

## 来源与数据

- Devpost 官方作品页：`https://devpost.com/software/orma`（2026-09-13 抓取：奖项 Best Hybrid AI App (Chrome Extension)、56 likes、技术栈 chrome / googlenano / openai / react / tailwindcss）
- 赛事页：`https://googlechromeai.devpost.com/`

- 赛事作品，无营收数据，本站不做估算

## 一句话总结

> 给浏览器装一层记忆，让你可以跟自己读过的东西对话。