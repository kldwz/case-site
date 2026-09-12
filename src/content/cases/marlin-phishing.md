---
name: Marlin（反钓鱼检测）
一句话: Google Chrome 内置 AI 挑战赛网络安全赛道第三名：五人团队做的反钓鱼工具，22 个赞
创始人地区: 五人团队（Elvis Huỳnh、Dylan Vu、Aaron Ang、Priyansh Shah、Charlie Weinberger），提交于 Google Chrome Built-in AI Challenge
营收模式: 尚未商业化（黑客松参赛作品，无营收数据）
月收入估算: 未官方披露（赛事作品，尚无营收）
流量来源: 赛事作品页 + 网络安全这个赞助商赛道；Devpost 官方作品页 22 个赞
可迁移点: ① 赞助商赛道是"送分题"：主办方单独设了网络安全奖，等于明说"我需要这类作品"，跟着给钱的人做 ② 钓鱼攻击是"人"的问题不是"系统"的问题：最弱的一环永远是点开链接的那个人，产品就盯着这一环 ③ 五人团队能在一周内出完整产品，靠的是分工明确：前端 React/TS、后端 FastAPI、爬虫 BeautifulSoup、模型 Mixtral ④ 抓包式分析（BeautifulSoup 解析页面）比训练模型更快出效果：工程上先跑通，再谈智能 ⑤ 演示视频比代码更能拿奖：安全类项目的价值要用"看，它拦住了"来证明
原文链接: https://devpost.com/software/marlin
数据口径: Devpost 官方作品页（devpost.com/software/marlin），2026-09-12 抓取：赛事 Google Chrome Built-in AI Challenge、奖项 Winner · 3rd Place（Cybersecurity：Reinventing Digital Defense 赞助赛道）、22 likes、技术栈 beautiful-soup / chrome / fastapi / kindo-ai / mixtral / pydantic / python / react / tailwind / typescript、团队 Elvis Huỳnh / Dylan Vu / Aaron Ang / Priyansh Shah / Charlie Weinberger、源码 github.com/rf-peixoto/phishing_pot。无营收数据。
分类: AI 应用 / 网络安全 / 英文 / 浏览器扩展
类型: 获奖作品
证据等级: 平台数据可查
平台数据: Devpost 官方作品页：Winner · 3rd Place（网络安全赞助赛道）· 22 likes（2026-09-12）
封面: /case-site/cases/marlin-phishing/site.png
---

![Marlin 作品页](/cases/marlin-phishing/site.png)

# Marlin：五个人、一周，把「最弱的一环」补上

## 产品是什么

一个反钓鱼工具：检测你正在访问的页面，判断它是不是钓鱼网站，并给出警示。

技术栈是一个标准的小团队分工配置：`BeautifulSoup`（解析页面）+ `FastAPI`（后端）+ `React`/`TypeScript`（前端）+ `Mixtral`（模型判断）+ `Pydantic`（数据校验）。

## 它解决了什么

网络安全的投入大多花在「系统」上：防火墙、入侵检测、端点防护。但绝大多数成功的攻击根本不碰系统——**它们骗人点链接**。

钓鱼邮件、仿冒登录页、假客服页面，技术上毫无难度，成功率却高得离谱。 weakest link（最弱一环）从来不是服务器，是人。

## 这个解法妙在哪

1. **盯着「人」这一环做产品**。不跟防火墙抢市场，只做「在你点下去之前提醒你」这一件事。
2. **先工程、后智能**。用 BeautifulSoup 把页面结构扒出来做规则判断，比训练一个模型更快见效——比赛里这是正确顺序。
3. **五人分工明确**：前端、后端、爬虫、模型、集成各管一摊，一周能出完整可演示的产品。
4. **安全类项目靠演示取胜**。「看，它把这个假登录页拦住了」——一个 30 秒的录屏胜过一千行代码说明。

## 团队与赛事

五人团队：Elvis Huỳnh、Dylan Vu、Aaron Ang、Priyansh Shah、Charlie Weinberger。提交于 **Google Chrome Built-in AI Challenge** 的网络安全赞助赛道（Cybersecurity: Reinventing Digital Defense），获 **3rd Place**，22 个赞。

## 这个案例能学到什么

① **赞助商赛道是明牌**。主办方单独设奖的领域，等于公开告诉你「我需要这类作品」——跟着给钱的人做，命中率最高。

② **安全产品要盯人，不盯系统**。绝大多数攻击成功在「人点了链接」这一步，产品机会就在这一步。

③ **小团队靠分工不靠加班**。前端 / 后端 / 爬虫 / 模型 / 集成五条线并行，一周出完整产品。

④ **先跑通再谈智能**。规则 + 解析能解决 80% 的问题时，就别急着训模型。

⑤ **安全类项目的价值要用画面证明**。一段「它拦住了钓鱼页」的录屏，比任何技术说明都有说服力。

## 来源与数据

- Devpost 官方作品页：`https://devpost.com/software/marlin`（2026-09-12 抓取：Winner · 3rd Place（Cybersecurity 赞助赛道）、22 likes、技术栈 beautiful-soup / chrome / fastapi / kindo-ai / mixtral / pydantic / python / react / tailwind / typescript）
- 赛事页：`https://googlechromeai.devpost.com/`
- 源码：`https://github.com/rf-peixoto/phishing_pot`
- 营收：赛事作品，无营收数据，本站不做估算

> 主办方单独设了奖的赛道，就是明摆着的需求——参赛时先看赞助商想要什么，往往比自己想点子更快命中。
