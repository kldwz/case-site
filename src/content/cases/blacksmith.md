---
name: Blacksmith
一句话: 用裸金属游戏 CPU 把 CI 跑快 2 倍、便宜 60%：三个 Waterloo 校友 2 年半干到 5000 万美金 ARR，B 轮 4500 万、估值 5.5 亿
创始人地区: Aditya "JP" Jayaprakash（CEO，ex-Faire）+ Aayush Shah、Aditya Maru（均 ex-Cockroach Labs），三人为滑铁卢大学校友，2024 年创立，YC W24，总部旧金山
营收模式: 按用量计费（CI 分钟/任务），面向工程团队，替换 GitHub Actions 等托管 runners，更快更便宜
月收入估算: 约 5000 万美金 ARR（创立 2.5 年）、5000–6000+ 家公司使用、月处理 5000 万+ jobs；累计融资 5850 万美金（B 轮 4500 万 @ 5.5 亿估值，Peak XV 领投，2026-08 披露）
流量来源: 开发者口碑（Supabase/Clerk/Ashby/Mercury/Expensify 等标杆客户）+ YC 网络 + 技术博客/性能对比的「快又便宜」硬指标传播
可迁移点: ① 不做新平台，做「现有平台的更快更便宜替身」——替换摩擦极小 ② 用裸金属+游戏 CPU 这种「别人嫌麻烦」的硬件组合做出性能差 ③ 面向开发者，性能数字本身就是营销（快 2 倍/便宜 60% 一张图传遍 HN） ④ 三位校友合伙，技术互补（Faire 增长 + Cockroach 系统） ⑤ YC 仍是硬科技公司的强力跳板，W24 之后 2 年半就到 5000 万 ARR
原文链接: https://blacksmith.sh
数据口径: blacksmith.sh 官方、Y Combinator 公司页、MachineHerald 报道；ARR/公司数/jobs 量/B 轮金额为公开披露；「快 2 倍/便宜 60%」为公司对外性能宣称
分类: AI/开发者基础设施 / 按量计费 / 英文 / 开发者工具
封面: /case-site/cases/blacksmith/site.png
---

![Blacksmith 官网](/cases/blacksmith/site.png)

# Blacksmith：把 CI 跑快 2 倍、便宜 60%，三个校友 2 年半干到 5000 万美金 ARR

## 产品是什么

Blacksmith 解决的是每个工程团队都烦的事：**CI（持续集成）太慢、太贵**。

开发者每次 push 代码，GitHub Actions 这类托管 runners 要排队、要等、要烧钱。Blacksmith 直接提供**更快更便宜的 CI runners**——底层用的是裸金属服务器搭配游戏级 CPU（没错，就是打游戏那颗芯片），把构建和测试任务跑得比标准云快一大截。

它不做「又一个 CI 平台」逼你迁移，而是**直接替换你现有的 runners**。GitHub Actions / GitLab CI 的配置几乎不用改，把执行层换成 Blacksmith 就行。**替换摩擦极小，这是它增长的关键**。

## 怎么赚的钱

按用量计费（CI 分钟/任务数），客户为「跑得快 + 花得少」买单。硬指标很直白：

- **比 GitHub 标准 runners 快 2 倍、便宜 60%**。
- 创立 2.5 年，ARR 约 **5000 万美金**，5000–6000+ 家公司在使用，月处理 **5000 万+ 个 jobs**。
- 融资节奏：Seed 350 万（GV + YC）→ A 轮 1000 万 @ 6000 万估值 → **B 轮 4500 万美金 @ 5.5 亿估值（Peak XV 领投，2026-08 披露）**，累计 5850 万。

客户名单是开发者圈里有名的那批：Supabase、Clerk、Ashby、Mercury、Expensify。

## 流量从哪来

Blacksmith 几乎不打广告，靠的是开发者圈最管用的三样：

1. **标杆客户即广告**：Supabase、Clerk 这种「开发者偶像级」公司用了，其他团队会主动来问「你们用的啥」。
2. **性能数字自己会传播**：「快 2 倍、便宜 60%」配一张对比图，往 Hacker News 一发，技术人自己就转开了。
3. **YC 网络**：W24 批次的校友资源、引荐、背书，早期冷启动帮了大忙。

## 站长是谁

三个创始人是**滑铁卢大学校友**：

- **Aditya "JP" Jayaprakash（CEO）**，之前在 Faire 做增长，懂怎么把开发者产品卖出去。
- **Aayush Shah + Aditya Maru**，都来自 Cockroach Labs，系统/基础设施底子极厚——裸金属 + 游戏 CPU 这种「别人嫌麻烦」的硬件组合，就是这俩人捣鼓出来的。

技术互补很关键：一个懂增长，两个懂底层系统，三人刚好拼成「能造又能卖」的班底。

## 这个案例能学到什么

第一，**不做新平台，做「现有平台的更快替身」**。逼用户迁移到新 CI 平台成本极高、阻力巨大；直接替换 runners，配置都不用改，客户零心理负担就切过来了。**降低替换摩擦 = 增长加速器**。

第二，**用「别人嫌麻烦」的硬件做出性能差**。裸金属 + 游戏 CPU，运维复杂、一般人不想碰，但正因为没人做，Blacksmith 才拿到「快 2 倍/便宜 60%」的硬指标。

第三，**面向开发者，性能数字就是营销**。开发者不信情怀，信 benchmark。一张对比图胜过万言软文。

第四，**校友合伙、技术互补**。增长背景 + 系统背景的组合，比三个同工种凑一起稳得多。找合伙人先看「能不能补齐我的短板」。

第五，**YC 仍是硬科技公司的强力跳板**。W24 之后 2.5 年冲到 5000 万 ARR，说明「YC 背书 + 真实性能」这条路径对基础设施公司依然成立。

## 来源与数据

- 站点：https://blacksmith.sh
- 融资与估值：Y Combinator 公司页、MachineHerald 2026-08 报道
- ARR / 公司数 / jobs 量 / 性能宣称：blacksmith.sh 官方公开信息
- 客户名单：官方公示（Supabase、Clerk、Ashby、Mercury、Expensify 等）

## 一句话总结

> 三个滑铁卢校友用裸金属游戏 CPU 把 CI 跑快 2 倍、便宜 60%，替换摩擦趋近于零，2 年半干到 5000 万美金 ARR。
