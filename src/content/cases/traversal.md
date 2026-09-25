---
name: Traversal
一句话: 哥伦比亚教授带着因果机器学习研究下海做的「AI SRE」——自动侦测、排查、修复生产事故，把平均恢复时间（MTTR）砍掉 85%，出道就拿 Sequoia
  与 Kleiner Perkins 领投的 4800 万美金
创始人地区: Anish Agarwal（CEO，哥伦比亚大学运筹学教授、MIT 博士）+ Raj Agrawal、Ahmed Lone（哥伦比亚硕士）、Raaz
  Dwivedi（康奈尔理工副教授）等联创，2024 年创立于纽约
营收模式: 面向财富 500 强与金融机构的 B2B 企业级 SRE 平台，按企业部署订阅（具体定价未公开），主打「减少停机损失」的高 ROI
月收入估算: 未披露绝对营收；2025 年 6 月出 stealth 即宣布 4800 万美金种子 + A 轮，由 Sequoia 与 Kleiner Perkins
  联合领投；2026 年 3 月获 American Express（Amex Ventures）战略投资并达成合作
流量来源: 学术圈顶级声誉（创始人团队来自 Columbia/MIT/UC Berkeley，研究因果机器学习）+ Sequoia/KP 双星领投的强背书 + 企业客户（American
  Express、DigitalOcean、Eventbrite 等）标杆 + 「vibe coding 越多、系统越难调试」的时代红利
可迁移点: ① 把博士论文变成产品——因果推断解决「找根因」这个监控工具 decades 没解决的难题，研究壁垒即商业壁垒 ② 不做又一个仪表盘，而是做「自主排查
  + 修复」的 agent，直接替 on-call 工程解放 ③ 卡住「AI 写代码越多、系统越难debug」的时机，痛点随 vibe coding 爆发而放大
  ④ 安全优先架构 + 灵活部署，才能进金融机构这种最保守的客户 ⑤ 学术创业要「在场」——团队全在纽约，面对面把研究转产品的速度拉满
原文链接: https://www.traversal.com
数据口径: 融资——2025 年 6 月出 stealth、4800 万美金种子+A 轮、Sequoia 与 Kleiner Perkins 领投（TechCrunch/Cornell/Traversal
  官方）；2026 年 3 月 Amex Ventures 战略投资（Traversal 官方稿）；MTTR 降 85%（官方口径）；客户（American Express/DigitalOcean/Eventbrite）（官方与报道）；创始人学术背景（Columbia/Cornell
  报道）
类型: 收入案例
证据等级: 官方披露
分类: AI SRE / 运维智能体 / 英文 / 美国
封面: /case-site/cases/traversal/site.png
---


![Traversal 官网](/cases/traversal/site.png)

# Traversal：哥伦比亚教授把博士论文变成「AI SRE」，出道就拿 Sequoia 领投的 4800 万

## 产品是什么

Traversal 做的是 **AI SRE（站点可靠性工程）agent**——说白了，就是替 on-call 工程师自动**侦测、排查、修复生产事故**。

传统监控工具（Datadog、Splunk、Grafana 那类）只是把遥测数据画成仪表盘，真出事了还是得人去「垃圾堆里翻线索」。Traversal 的 agent 直接分析日志、指标、调用链和代码变更，在几分钟里定位「真正的根因」，甚至自动把修复建议或修复动作执行掉。

官方口径下，它把企业客户的**平均恢复时间（MTTR）砍掉 85%**。

## 怎么赚的钱

面向**财富 500 强与金融机构**的 B2B 企业级 SRE 平台，**按企业部署订阅**（具体定价未公开），主打「减少一次停机就值回票价」的高 ROI。

公司 2024 年才创立，但 2025 年 6 月一出 stealth 就宣布 **4800 万美金种子 + A 轮，由 Sequoia 与 Kleiner Perkins 联合领投**——两家顶级机构同时下注，本身就是最强信任章。2026 年 3 月又拿到 **American Express（Amex Ventures）的战略投资**，并达成技术合作。

## 流量从哪来

Traversal 的获客是**学术声誉 + 机构背书 + 时代红利**的组合：

1. **创始团队学术光环**：CEO Anish Agarwal 是哥伦比亚大学教授、MIT 博士，团队来自 Columbia/MIT/UC Berkeley，研究因果机器学习——这种背景在基础设施圈极稀缺。
2. **Sequoia + KP 双星领投**：两家顶级 VC 同时领投，客户一听就信。
3. **标杆客户**：American Express、DigitalOcean、Eventbrite 等都在用。
4. **时代红利**：「vibe coding」让 AI 写代码越来越多，系统出毛病时人越来越没上下文——Traversal 要解决的痛点正被这股潮放大。

## 站长是谁

**Anish Agarwal** 是 Traversal 的 CEO 兼联合创始人，哥伦比亚大学工业工程与运筹学助理教授、MIT 博士，研究因果机器学习（从大数据里找真正的因果关系）。

他的创业起点很戏剧：一位哥伦比亚硕士生 Ahmed Lone 主动给他发「冷邮件」聊研究，两人一拍即合。联创还包括 Raj Agrawal（Agarwal 在 MIT 读博时认识）、Raaz Dwivedi（康奈尔理工副教授）。一支以学术为主、全员在纽约的团队，把因果推断的研究转成了产品。

## 这个案例能学到什么

第一，**把博士论文变成产品**。根因分析几十年来是运维界的老大难，传统工具只会报「症状」。Traversal 用因果机器学习真正找「病因」——**研究壁垒就是商业壁垒**，别人想抄得先发几年论文。

第二，**不做又一个仪表盘，做能动手的 agent**。监控工具已经够多了，Traversal 的差异化是「自主排查 + 修复」，直接把 on-call 工程师从救火里解放出来。

第三，**卡住时代的痛点放大点**。"vibe coding" 越流行，AI 生成的代码越多，系统出事时人越没上下文——这个痛点正随潮流爆发，Traversal 正好站在浪上。

第四，**安全优先 + 灵活部署，才进得了保守客户**。金融客户最在意数据和部署安全，Traversal 用安全优先架构敲开了 American Express 这种门。

第五，**学术创业要「在场」**。团队全在纽约、面对面协作，把「研究转产品」的速度拉满。纽约的创业氛围成了隐形的加速器。

## 来源与数据

- 站点：https://www.traversal.com
- 融资：2025 年 6 月出 stealth、4800 万美金种子+A 轮、Sequoia 与 Kleiner Perkins 领投（TechCrunch/Cornell/Traversal 官方）；2026 年 3 月 Amex Ventures 战略投资（Traversal 官方稿）
- MTTR 降 85%：官方口径
- 客户（American Express/DigitalOcean/Eventbrite）：官方与报道
- 创始人学术背景：Columbia/Cornell 报道

## 一句话总结

> 一个哥伦比亚教授把因果机器学习的博士研究变成「AI SRE」产品，自动排查修复生产事故、把恢复时间砍掉 85%，出道就拿 Sequoia 与 Kleiner Perkins 领投的 4800 万美金——证明最硬的商业壁垒，有时候就是一篇别人抄不来的论文。
