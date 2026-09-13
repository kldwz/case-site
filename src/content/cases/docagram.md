---
name: Docagram
一句话: Honorable Mention（Google Chrome 内置 AI 挑战赛）：把"画图"这件事交给浏览器自带的模型——成本为零，门槛归零。
创始人地区: 独立开发者/小团队参赛作品，提交于 Google Chrome Built-in AI Challenge
场景: 把内容可视化：用内置 AI 把文字/信息转成图解
营收模式: 尚未商业化（黑客松参赛作品，无营收数据）
月收入估算: 无收入（黑客松获奖作品）
流量来源: 赛事作品页 + 端侧/浏览器 AI 话题传播
原文链接: https://devpost.com/software/deverywhere
数据口径: Devpost 官方作品页（https://devpost.com/software/deverywhere），2026-09-13 抓取：赛事 Google Chrome Built-in AI Challenge（https://googlechromeai.devpost.com/）、奖项 Honorable Mention、36 likes、技术栈 gemini / prompt-api / react / shadcn / summary-api / tailwind / vite、源码 https://github.com/jtmuller5/docagram-react。无营收数据
分类: AI 应用 / 浏览器内置 AI / 英文
类型: 获奖作品
证据等级: 平台数据可查
平台数据: Devpost 官方作品页：Honorable Mention · 36 likes（2026-09-13）
赛事: Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）
奖项: Honorable Mention
封面: /case-site/cases/docagram/site.png
---

![Docagram 作品页](/cases/docagram/site.png)

> **赛事**：Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）
> **场景**：把内容可视化：用内置 AI 把文字/信息转成图解
> **奖项**：Honorable Mention
> **出处**：[作品页](https://devpost.com/software/deverywhere) ｜ [赛事页](https://googlechromeai.devpost.com/) ｜ [源码](https://github.com/jtmuller5/docagram-react)

# Docagram：把"画图"这件事交给浏览器自带的模型——成本为零，门槛归零。

## 它做了什么

一个"把什么都能画出来"的工具：用浏览器内置 AI 把信息转成可视化的图——概念关系、流程、结构，用图来表达。

## 这个解法妙在哪

1. **文字不如图直观**。很多内容（关系、流程、层级）用文字讲十句，不如画一张图。
2. **它把"画图"这件事交给了 AI**：你给它内容，它产出可视化，不需要你会用绘图工具。
3. **全部用内置 API（prompt-api、summary-api）实现**：不用自己训模型、不用付 API 费用，成本几乎为零。

## 技术怎么实现的

React + Vite + TailwindCSS + shadcn/ui；AI 能力全部来自 Chrome 内置的 Prompt API 与 Summary API（Gemini Nano）。前端负责内容输入与图形渲染。

## 团队与赛事

Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）（赛事页 https://googlechromeai.devpost.com/）。作品页获 **Honorable Mention** 徽章，36 个赞；源码公开在 GitHub。

## 这个案例能学到什么

1. **"文字讲解"之外永远有"画图"这个需求**。
2. **把专业工具的能力交给 AI 完成**（不用会画图，也能出图）。
3. **内置 API 让复杂功能变得便宜**。以前要调用付费模型，现在浏览器自带。
4. **纯前端 + 内置模型 = 零边际成本**。这类产品的可行性被彻底改变了。

## 来源与数据

- Devpost 官方作品页：`https://devpost.com/software/deverywhere`（2026-09-13 抓取：奖项 Honorable Mention、36 likes、技术栈 gemini / prompt-api / react / shadcn / summary-api / tailwind / vite）
- 赛事页：`https://googlechromeai.devpost.com/`
 - 源码：`https://github.com/jtmuller5/docagram-react`
- 赛事作品，无营收数据，本站不做估算

## 一句话总结

> 把"画图"这件事交给浏览器自带的模型——成本为零，门槛归零。