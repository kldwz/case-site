---
name: Canvas Student Insights with AI
一句话: Google Chrome 内置 AI 挑战赛荣誉提名：把学习平台的数据变成学生的个性化学习计划，13 个赞
创始人地区: 独立开发者（GitHub：onEnterFrame），提交于 Google Chrome Built-in AI Challenge
营收模式: 尚未商业化（黑客松参赛作品，无营收数据）
月收入估算: 未官方披露（赛事作品，尚无营收）
流量来源: 赛事作品页 + 教育科技场景；Devpost 官方作品页 13 个赞
可迁移点: ① 数据已经存在，只是没人读：Canvas 里有成绩、作业、进度，学生和老师却看不到"下一步该做什么" ② 别做新平台，做"已有平台的一层皮"：插件直接长在 Canvas 界面上，不需要用户换工具 ③ 教育场景的 AI 价值在"总结"而非"生成"：把散落的数据变成一句人话建议，比生成新内容更有用 ④ 三类用户一起满足：学生看进度、老师看全班、学校看风险，一个产品覆盖三个视角 ⑤ 用 Gemini + JavaScript 就够了：教育类产品的门槛在场景理解，不在技术
原文链接: https://devpost.com/software/canvas-student-insights-with-ai
数据口径: Devpost 官方作品页（devpost.com/software/canvas-student-insights-with-ai），2026-09-12 抓取：赛事 Google Chrome Built-in AI Challenge、奖项 Winner · Honorable Mention、13 likes、技术栈 gemini / instructure-canvas / javascript、源码 github.com/onEnterFrame/canvasChrome。无营收数据。
分类: AI 应用 / 教育科技 / 英文 / 浏览器扩展
类型: 获奖作品
证据等级: 平台数据可查
平台数据: Devpost 官方作品页：Winner · Honorable Mention · 13 likes（2026-09-12）
赛事: Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）
场景: 教育科技：把 Canvas 学习平台的数据变成学生能读懂的进度与学习计划
奖项: Winner · Honorable Mention（荣誉提名）
封面: /case-site/cases/canvas-insights/site.png
---

![Canvas Student Insights 作品页](/cases/canvas-insights/site.png)

# 数据早就在那儿了，只是没人替学生读一遍

> **赛事**：Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）
> **场景**：教育科技：把 Canvas 学习平台的数据变成学生能读懂的进度与学习计划
> **奖项**：Winner · Honorable Mention（荣誉提名）
> **出处**：[作品页](https://devpost.com/software/canvas-student-insights-with-ai) ｜ [赛事页](https://googlechromeai.devpost.com/) ｜ [源码](https://github.com/onEnterFrame/canvasChrome)

## 产品是什么

一个长在 Canvas（海外主流学习管理系统）上的 AI 插件：直接读取学生在这个平台里的进度、作业、成绩，给出**实时总结、可执行的分析和个性化学习计划**。

技术栈非常简单：Gemini + Instructure Canvas API + JavaScript。

## 它解决了什么

学习平台里躺着大量数据：哪些作业交了、哪些迟了、哪次测验分数掉了、这门课进度落后多少。但这些数据**对学生来说基本不可读**——它以表格和列表的形式存在，不会告诉你「你现在的状况」和「下一步该干什么」。

老师那边更糟：一个班几十个学生，谁掉了队很难第一时间发现。

## 这个解法妙在哪

1. **不做新平台，做现有平台的一层皮**。插件直接长在 Canvas 界面上，用户不需要换工具、不需要迁移数据——这是教育类工具最大的 adoption 障碍，它绕过去了。
2. **AI 的价值在总结，不在生成**。这类场景里，学生不需要 AI 写作文，需要 AI 把散落的数据变成一句人话：「你这周有两份作业逾期，先补数据结构那门」。
3. **一份数据，三种视角**：学生看自己的进度，老师看全班的风险名单，学校看整体趋势——同一套数据卖出三个价值。
4. **技术极简**：Gemini + Canvas API + JS，说明门槛在场景理解，不在工程复杂度。

## 团队与赛事

独立开发者（GitHub: onEnterFrame），提交于 **Google Chrome Built-in AI Challenge**，获 **Winner · Honorable Mention**，13 个赞。

## 这个案例能学到什么

① **找「数据已经存在但没人读」的地方**。这类机会不需要造数据，只需要把已有的东西翻译成人话。

② **别做新平台，做现有工具的插件**。用户换工具的成本是最大的落地障碍，长在别人界面上就绕开了。

③ **教育 AI 的正确用法是总结，不是生成**。帮学生看懂自己的状态，比帮他写作业有价值得多。

④ **一套数据服务三类用户**。学生、老师、学校三个视角，同一份数据三种卖法。

⑤ **教育类产品的门槛在场景理解**。技术简单不是缺点，说明你把力气花在了正确的地方。

## 来源与数据

- Devpost 官方作品页：`https://devpost.com/software/canvas-student-insights-with-ai`（2026-09-12 抓取：Winner · Honorable Mention、13 likes、技术栈 gemini / instructure-canvas / javascript）
- 赛事页：`https://googlechromeai.devpost.com/`
- 源码：`https://github.com/onEnterFrame/canvasChrome`
- 营收：赛事作品，无营收数据，本站不做估算

> 最好的 AI 教育产品不生成内容，它只是把本来就存在的数据，翻译成一句"你现在该干什么"。
