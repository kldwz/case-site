---
name: B2B SaaS OS
一句话: 卖一套「多租户 B2B SaaS 基础设施」源码模板，一次买断 $249，不再重复造轮子
创始人地区: Wendel Andrady（X @WendelAndrady），海外，单人
营收模式: 数字产品一次买断（$249 lifetime，更新包含，无订阅无分成），Gumroad 收款
月收入估算: 未官方披露（IndieHackers 显示 pre-scale，验证定价阶段）
流量来源: IndieHackers/ProductHunt 开发者社区发布 + 官网 SEO（B2B SaaS boilerplate 关键词）+ X/Twitter build in public + 免费 demo 引流
可迁移点: ① 把「反复要做的脏活」打包成一次买断模板，卖时间给同行 ② 单人多产品线成本趋近零：写一次源码卖给 N 个人 ③ 用 live demo + 文档立信任，模板类产品先让人验货 ④ 明确授权边界（一次购买、客户可用、不可转售）消除合规顾虑
原文链接: https://andrady.co/
数据口径: 官网 Pricing/License 页实测 + Gumroad checkout（2026-09）
类型: 收入案例
证据等级: 第三方估算
分类: 开发者工具 / 模板一次买断 / 英文
封面: /case-site/cases/b2bsaasos/site.png
---

![B2B SaaS OS 官网首页](/cases/b2bsaasos/site.png)

# B2B SaaS OS：把每个 SaaS 都要重写的脏活，打包成 $249 一次卖断

## 产品是什么

B2B SaaS OS 是一套**多租户 B2B SaaS 的基础设施源码模板**，技术栈 Next.js 15 + Supabase + Stripe。它把「每一个 B2B SaaS 启动时都要从头搭一遍」的部分预先接好线，买下来直接当起点：

- **组织 / 多租户**：Org、成员、RBAC 权限矩阵
- **PostgreSQL RLS**：行级安全策略已配置（多租户数据隔离的关键）
- **Supabase Auth**：登录注册
- **Stripe 计费**：订阅/结算已接好
- **API keys、audit logs、用量限制** 等 B2B 客户常要的东西

官网首页 12 节，从架构哲学、RLS 示例、权限矩阵到 Stripe 事件处理都有讲，还挂了一个 **live demo** 让人先体验再买。目标用户是「不想把前两个月花在重复搭基础设施」的 B2B SaaS 开发者/小团队。

## 怎么赚的钱

**数字产品一次买断**，官网和 Gumroad 明码标价：

> **$249 one-time**——"yours forever, updates included"（一次购买、永久所有、更新包含）。

无订阅、无席位费、无分成。授权规则写得很清楚：**不限项目数、可给你的客户使用，但不可转售**。

这个模式对一个单人开发者（Wendel Andrady）的价值在于**边际成本趋近于零**：源码模板写好一次，每多卖一份都是纯利润，不像 SaaS 要持续维护服务器和用户支持。它本质是把「写代码的时间」卖了 N 次。

IndieHackers 上该项目标 pre-scale，创始人还在验证「模板里哪些部分是用户愿意付费的」，定价仍处于早期验证阶段。

## 流量从哪来

- **IndieHackers / ProductHunt 开发者社区**：这类「我做了一个能省你几个月的模板」内容在开发者社区天然有传播力。
- **官网 SEO**：「B2B SaaS boilerplate / Next.js Supabase Stripe template」是开发者搜模板的高意图关键词。
- **X (Twitter) build in public**：创始人分享搭建过程，吸引关注同类问题的开发者。
- **live demo 转信任**：模板类产品最怕「买回来货不对板」，可交互 demo 直接让人验货，提升转化。

无公开流量数字，渠道为定性判断。

## 这个案例能学到什么

第一，**把「你反复要做的脏活」打包卖掉**。B2B SaaS 的租户/权限/计费，是每个团队启动都要重写一遍的重复劳动。谁把它做成开箱即用的模板，谁就卖时间给同行。对买方省 1–2 个月，对卖方是一次劳动卖 N 次。

第二，**单人产品可以选「模板买断」而非「SaaS 订阅」**。SaaS 要持续维护、要扛 uptime、要养客服；买断模板交付即完成，更新可选做——对想用最小维护成本赚钱的单人开发者，这是被低估的模式。

第三，**给足 demo 和文档，是卖虚拟产品的信任基石**。源码这东西看不见摸不着，live demo + 详细 feature/授权说明，让买家在付款前就能验货，是这类高客单数字产品转化率的关键。

第四，**把授权边界写清楚（不可转售但可商用）**。模糊的授权会让企业买家犹豫「买来能不能给客户用」，白纸黑字消除顾虑，反而促进成交。

## 来源与数据

- 站点：https://andrady.co/（Pricing/License 页实测）
- 收款：Gumroad（andradyy.gumroad.com/l/b2b-saas-os，$249）
- 来源：IndieHackers 收录（B2B SaaS OS）+ 官网核实
- 定价：官网明码标价 $249 一次买断
- 创始人：Wendel Andrady
- 收入：官方未披露

## 一句话总结

> 每个人都要踩一遍的 B2B SaaS 基建坑，被他打包成开箱即用的源码模板——$249 一次买断，写一次代码卖 N 次，单人也能做。
