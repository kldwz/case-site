---
name: Netris
一句话: 三个干了二十多年的网络工程师熬了八年，等 AI 集群把「网络配置」卡成瓶颈，做出 GPU 云的自动化与多租户层，a16z 领投 1500 万美金 A 轮，过去 12 个月 ARR 增长 800%
创始人地区: Alex Saroyan（CEO）、Tigran Martirosyan（软件工程）、Arsen Arakelyan（客户成功），总部美国加州圣克拉拉；2017 年成立
营收模式: 面向 neocloud、主权 AI 云与 AI 工厂的企业软件授权/订阅（NAAM 平台：网络自动化、抽象与多租户）；与 NVIDIA 深度绑定，生态伙伴含 Mirantis、Rafay、Red Hat、Spectro Cloud、vCluster、HPE
月收入估算: 未公开绝对营收；官方与 Forbes 口径为过去 12 个月 ARR 增长 800%，已在全球 35+ 个 AI 集群上线，覆盖约百万张 GPU 量级
流量来源: 与 NVIDIA 的深度合作（NVIDIA 两年前看 demo 后就向客户推荐）；a16z 领投带来的行业背书，参与本轮的 Martin Casado（Nicira 创始人、SDN 开创者）、Raghu Raghuram（前 VMware CEO）、Guido Appenzeller（加入董事会）；Futuriom 连续六年列入 Futuriom 50；客户案例驱动（Lightning AI、TensorWave、TELUS、Foxconn 系 Visionbay、Firmus、HPE）
可迁移点: ① 在风口到来前八年就进场，等风来——但前提是真的熬得住 ② 解决「没人愿意干的脏活」（多厂商网络配置），而不是最性感的 AI 部分 ③ 绑定生态里的权力中心（NVIDIA），让巨头替你销售 ④ 创始人即领域专家（25 年网络架构经验），客户是同行，说服成本极低 ⑤ 明确说「生成式 AI 不适合这个场景」，用反共识建立专业可信度
原文链接: https://netris.io
数据口径: 融资——2026 年 6 月宣布 1500 万美金 A 轮，Andreessen Horowitz（a16z speedrun）领投，GP Guido Appenzeller 加入董事会，Martin Casado 与 Raghu Raghuram 支持（Forbes 2026-06-25、Futuriom、a16z 系 LinkedIn 公告）；增长——官方称过去 12 个月 ARR 增长 800%（Forbes、Futuriom）；部署——全球 35+ 个 AI 集群上线，覆盖约 100 万张 GPU；客户——Lightning AI、STN、Boost Run、TensorWave、TELUS、DCAI、YOTTA、Foxconn 支持的 Visionbay.ai（台湾最大 GPU 集群）、Firmus（澳洲最大可再生主权 AI 工厂）、HPE；产品——NAAM（Network Automation, Abstraction, and Multi-Tenancy），把 VPC、负载均衡、弹性 IP、路由与租户隔离下沉为硬件级配置，支持 Ethernet、InfiniBand、NVLink/NVL72、BlueField DPU 与边缘网络；生态——NVIDIA、Mirantis、Rafay、Red Hat、Spectro Cloud、vCluster、HPE；创始人——Alex Saroyan（CEO，25+ 年大规模网络架构经验，曾任职 Orange、Ucom）、Tigran Martirosyan（软件工程，曾任职 Orange、Lycos）、Arsen Arakelyan（系统与网络工程、客户部署，曾任职 Orange、Sourcio）
类型: 收入案例
证据等级: 官方披露
分类: 基础设施 / AI 云网络 / 英文 / 美国
封面: /case-site/cases/netris/site.png
---

![Netris 官网](/cases/netris/site.png)

# Netris：熬了八年，等 AI 集群把「网络」卡成瓶颈

## 产品是什么

Netris 做的是 AI 云里最不性感、但现在最卡脖子的一层：**GPU 集群的网络自动化与多租户隔离**。

它把这套东西叫 **NAAM**——Network Automation, Abstraction, and Multi-Tenancy。

问题长这样：一个 AI 云同时跑在好几张网络结构之上——Ethernet、InfiniBand、NVL72 扩展结构、虚拟与边缘网络，每一张都有自己的控制平面。而且它从不停下来：**每次运营商新增、扩容或移除一个租户，这些结构就必须协同重配**。配错一次，整个集群可能宕机，或者一个租户的数据漏到另一个租户那里。

Netris 的解法是：把 VPC、负载均衡、弹性 IP、路由和**租户隔离**这些逻辑，**下沉成硬件级配置**——跨厂商、跨硬件（NVIDIA 和 AMD 服务器环境都支持），不需要为了某个厂商重构整个栈。

## 怎么赚的钱

**面向 neocloud、主权 AI 云和 AI 工厂的企业软件授权/订阅**。

2026 年 6 月，Netris 宣布 **1500 万美金 A 轮**，由 **Andreessen Horowitz（a16z speedrun）领投**，GP Guido Appenzeller 加入董事会，Martin Casado 和 Raghu Raghuram 也参与支持。

营收方面，官方口径是**过去 12 个月 ARR 增长 800%**。规模上，已在全球 **35+ 个 AI 集群**上线，覆盖约**百万张 GPU** 量级。

## 流量从哪来

第一，**NVIDIA 替它销售**。这是最关键的一条。据 Forbes 报道，NVIDIA 两年前看过 demo 后，就开始向自己的客户推荐 Netris。对一个基础设施 startup 来说，被生态里的权力中心推荐，比任何销售团队都有效。

第二，**a16z 的背书本身就是行业事件**。参与这轮的三个人——Martin Casado（Nicira 创始人，SDN 开创者，后被 VMware 收购）、Raghu Raghuram（后来做到 VMware CEO）、Guido Appenzeller——正是上一代数据中心网络革命的主导者。他们投 Netris，等于在说「AI 云需要同一场重新发明」。Forbes、Futuriom 都专门写了这件事。

第三，**客户名单就是最好的广告**。Lightning AI、TensorWave、TELUS、Foxconn 支持的 Visionbay.ai（台湾最大 GPU 集群）、Firmus（澳洲最大可再生主权 AI 工厂）、HPE——这些都是「把多租户 GPU 网络交给别人」的最高信任等级客户。

第四，**六年连续入选 Futuriom 50**。在基础设施圈子里，这种持续上榜意味着同行认可，而不是一次性曝光。

## 站长是谁

**Alex Saroyan**（CEO）、**Tigran Martirosyan**（软件工程）、**Arsen Arakelyan**（客户成功），2017 年成立，总部加州圣克拉拉。

三人都是老网络工程师：Saroyan 有 25+ 年大规模网络架构经验，曾在 Orange 做运营商与核心网，后来在 Ucom 负责核心网络；Martirosyan 曾在 Orange 和 Lycos 做软件工程；Arakelyan 曾在 Orange 和 Sourcio 做系统与网络工程，负责客户部署。

Saroyan 有一句话很能代表这家公司的气质——他直言**生成式 AI 不适合这个场景**，因为「AI 不是确定性的」。对网络变更管理来说，「持久且可重复」比「聪明」重要得多。

## 这个案例能学到什么

第一，**在风口到来前八年就进场，等风来**——但前提是你真熬得住。Netris 2017 年成立，前几年一直在找方向、重新定位，直到 AI 集群建设爆发才对上。这种「熬」不是被动等待，是持续把产品磨到能接住需求。

第二，**解决没人愿意干的脏活**。配置多厂商网络一点都不性感，但正因为没人愿意做，它才成了 AI 基建扩张的瓶颈，也才值钱。

第三，**绑定生态里的权力中心**。NVIDIA 的一句推荐，抵得过几十个销售。找到那个「你的客户都听他」的角色，让他替你说话。

第四，**创始人即领域专家，说服成本极低**。Saroyan 的客户是他的同行——同样被多厂商网络折磨了二十多年的人。这种对话不需要教育市场。

第五，**敢说反共识的话**。在一片「AI 改变一切」里，CEO 明确说「生成式 AI 不适合网络变更管理，因为它不确定」——这种专业判断反而建立了可信度。

## 来源与数据

- 站点：https://netris.io
- 融资：2026-06 宣布 1500 万美金 A 轮，a16z（speedrun）领投，Guido Appenzeller 加入董事会，Martin Casado 与 Raghu Raghuram 支持（Forbes 2026-06-25、Futuriom 2026-06）
- 增长：官方称过去 12 个月 ARR 增长 800%
- 部署：全球 35+ 个 AI 集群上线，覆盖约 100 万张 GPU
- 客户：Lightning AI、STN、Boost Run、TensorWave、TELUS、DCAI、YOTTA、Visionbay.ai（Foxconn 支持）、Firmus、HPE
- 产品：NAAM 平台，把 VPC、负载均衡、弹性 IP、路由与租户隔离下沉为硬件级配置；支持 Ethernet、InfiniBand、NVLink/NVL72、BlueField DPU、边缘网络
- 生态：NVIDIA、Mirantis、Rafay、Red Hat、Spectro Cloud、vCluster、HPE
- 创始人：Alex Saroyan（CEO，25+ 年网络架构，前 Orange/Ucom）、Tigran Martirosyan（前 Orange/Lycos）、Arsen Arakelyan（前 Orange/Sourcio）

## 一句话总结

> 三个干了二十多年的老网络工程师，2017 年就成立了 Netris，熬了八年、几经重新定位，直到 AI 集群建设把「多厂商网络配置」卡成整个行业的瓶颈——一个 AI 云同时跑在 Ethernet、InfiniBand、NVL72 等多张结构上，每加一个租户就得协同重配，配错一次可能整个集群宕机或数据串租户。Netris 把这些逻辑下沉成硬件级配置，做成 GPU 云的自动化与多租户层（NAAM）。NVIDIA 两年前看过 demo 就开始向客户推荐，a16z 领投 1500 万美金 A 轮，SDN 时代的三位老将（Casado、Raghuram、Appenzeller）站台。过去 12 个月 ARR 增长 800%，35+ 个 AI 集群上线。真正可迁移的那句话是：**别追最性感的活，去干那件没人愿意干、但一卡住整个行业就停摆的脏活**——而熬得住，是这种生意唯一的入场券。
