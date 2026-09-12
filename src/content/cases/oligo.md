---
name: Oligo Security
一句话: CTO 发现 Instagram 能被一个开源库攻破，三个以色列前国防军网络军官据此创业——用运行时行为画像堵开源漏洞，9 个月内拿下 2800 万美金
创始人地区: Nadav Czerninski（联合创始人兼 CEO）、Gal Elbaz（联合创始人兼 CTO，前 Check Point）、Avshalom Hilu（联合创始人兼 CPO），总部以色列特拉维夫，另在纽约设办公室
营收模式: 企业级运行时应用安全与可观测性平台订阅，按受保护的主机与工作负载收费
月收入估算: 公司未公开披露 ARR；2023 年 2 月出 stealth 时累计融资 2800 万美金（种子轮 + A 轮），成立 9 个月内完成
流量来源: CTO 亲自发现 Instagram 开源库漏洞作为产品原点与传播钩子 + eBPF 库级运行时行为画像的技术差异化 + 以色列网安天使天团背书（Snyk 的 CTO、Check Point 联合创始人 Shlomo Kramer、Mellanox 创始人、Dome9 与 SafeBreach 创始人）+ Lightspeed、Ballistic Ventures、TLV Partners 领投
可迁移点: ① 最好的产品原点是创始人亲手挖出的洞——Gal Elbaz 2020 年发现 Instagram 可被开源库滥用攻陷，这个故事比任何市场分析都有说服力 ② 别在噪音上加噪音——传统 SCA 工具的毛病是海量误报，Oligo 只在「库的行为偏离既定权限」时告警，把警报工作量砍掉约 85% ③ 从「检测漏洞」转向「检测行为」——漏洞库永远追不完，但一个库该干什么不该干什么是可以被画像的 ④ 把性能开销做成产品前提——他们的 eBPF 引擎在库级别工作，既精准又不影响应用稳定性，这是能进生产环境的硬门槛 ⑤ 早期把行业里的关键人物变成投资人——Snyk 的 CTO、Check Point 的创始人都在天使名单里，这些人既是钱也是渠道
原文链接: https://www.oligo.security
数据口径: 融资——2023 年 2 月出 stealth 时累计 2800 万美金，种子轮由 TLV Partners 领投，A 轮由 Lightspeed Venture Partners 与 Ballistic Ventures 参与，成立 9 个月内完成（Business Wire 官方通稿、Globes、FinSMEs、Calcalist）；投资人——Lightspeed Venture Partners、Ballistic Ventures、TLV Partners、Shlomo Kramer（Cato Networks 联合创始人兼 CEO、Check Point 联合创始人）、Eyal Waldman（Mellanox 创始人）、Adi Sharabani（Snyk CTO）、Eyal Manor（前 Google Cloud 总经理、Twilio 首席产品与工程官）、Zohar Alon（Dome9 创始人）、Guy Bejerano（SafeBreach 联合创始人）、Shai Morag（Ermetic 联合创始人）、Ofer Ben-Noon 与 Ohad Bobrov（Talon Cyber Security 联合创始人）；基金包括 Cyber Club London、Kmehin Ventures、OperAngels（Business Wire、Calcalist、TLV Partners 投资笔记）；技术——基于自研 eBPF 引擎的动态库级分析与行为监控，为每个开源库建立合法行为画像，偏离时告警或阻断，客户响应安全警报的工作量减少约 85%（Business Wire、FinSMEs）
分类: 企业安全 / 开源供应链安全 / 英文 / 以色列
封面: /case-site/cases/oligo/site.png
---

![Oligo Security 官网](/cases/oligo/site.png)

# Oligo Security：Instagram 能被一个开源库攻破

## 产品是什么

Oligo Security 做的是**运行时应用安全与可观测性**（Runtime Application Security）。核心场景是：堵住开源代码库里的漏洞。

现代软件有 **80% 到 90% 的代码来自开源**。这既带来了效率，也带来了巨大的攻击面。2022 年是个转折点——Log4Shell 漏洞波及数亿台设备，随后 Text4Shell、Spring4Shell、OpenSSL、PyTorch 以及 colors 和 faker 这类小包的投毒接踵而来。

当时市面上的 SCA（软件成分分析）工具解决不了这个问题，原因有两个致命伤：**噪音极大**，大量误报；**没有运行时上下文**，无法判断一个漏洞在你的应用里到底有没有被真正触达。

Oligo 换了个思路：**不看漏洞清单，看库的实际行为**。

它的自研 **eBPF 引擎**会为每个正在运行的开源库建立「合法行为画像」，形成知识库。一旦某个库的活动偏离了它应有的权限策略——比如一个图片处理库突然去读环境变量——就判定为可疑，立即告警或阻断。

这样做的直接收益是精准：它只在真正偏离时报警。官方数据称，客户**响应安全警报的工作量减少约 85%**。

## 怎么赚的钱

**企业级平台订阅**，按受保护的主机与工作负载收费。

公司没有披露 ARR。融资节奏很快：**2022 年成立，2023 年 2 月出 stealth 时已经拿到 2800 万美金**（种子轮加 A 轮），整个过程只用了 9 个月。种子轮由 TLV Partners 领投，A 轮有 Lightspeed Venture Partners 和 Ballistic Ventures 加入。

客户覆盖计算机科技、分析软件、全球商业地产与投资服务、在线金融服务等领域。团队 25 人时设在特拉维夫，同时在纽约开办公室。

## 流量从哪来

第一，**产品原点是一个能讲一辈子的故事**。2020 年 9 月，联合创始人兼 CTO **Gal Elbaz 发现了一种通过滥用开源库攻陷 Instagram 的方法**。他后来解释说，让他震惊的不是漏洞本身，而是**超出库权限的恶意行为居然完全不被察觉**。这个故事既是产品的由来，也是最好的传播素材——它具体、可验证、有戏剧性。

第二，**技术路线天然差异化**。当所有同行都在做「扫清单」的时候，Oligo 做「看行为」。这不是营销差异，是架构差异——漏洞库永远追不完，但一个库该干什么、不该干什么，是可以被画像的。

第三，**以色列网安圈的集体背书**。天使名单几乎是以色列网络安全的名人堂：Snyk 的 CTO Adi Sharabani、Check Point 联合创始人 Shlomo Kramer、Mellanox 创始人 Eyal Waldman、前 Google Cloud 总经理 Eyal Manor、Dome9 创始人 Zohar Alon、SafeBreach 联合创始人 Guy Bejerano、Ermetic 联合创始人 Shai Morag、Talon 联合创始人 Ofer Ben-Noon 与 Ohad Bobrov。**这些人既是钱，也是渠道和 credibility**。

第四，**踩中了 Log4Shell 之后的时间窗口**。2022 年那一串开源攻击让整个行业重新审视开源安全，预算和需求同时到位。

## 站长是谁

**Nadav Czerninski**，联合创始人兼 CEO。

**Gal Elbaz**，联合创始人兼 CTO，此前在 Check Point 工作。他是那个发现 Instagram 漏洞的人，也是 Oligo 技术路线的定义者。

**Avshalom Hilu**，联合创始人兼 CPO。

三个人有一个共同背景：**都曾是以色列国防军精锐网络部队的军官**。这个履历在以色列网安创业圈是硬通货——它意味着从十几岁起就在真实的攻防环境里训练。

公司从 Intel Ignite 项目的第六期毕业。

Czerninski 这样描述产品逻辑：**在 Gal 发现 Instagram 这样的主流应用都能被轻易攻破之后，我们意识到市场对开源安全的处理方式存在巨大缺口。我们最终聚焦在一种保护方法上——在运行时或预发布环境里检查每一个库，让我们能在出现偏离时精准识别攻击，并修复那些真正重要的漏洞。**

## 这个案例能学到什么

第一，**最好的产品原点是创始人亲手挖出的洞**。Gal Elbaz 不是在调研报告里读到开源安全有问题，是自己发现了 Instagram 的攻击路径。这种一手经验会直接变成产品判断力和融资故事，两者都极难复制。

第二，**别在噪音上加噪音**。传统 SCA 的核心痛点不是检测不到，是误报太多把团队淹没了。Oligo 的关键创新是「只在偏离时告警」，把响应工作量砍掉 85%。**减少客户的工作量，本身就是最锋利的产品价值**。

第三，**从「检测清单」转向「检测行为」**。漏洞数据库永远滞后，但行为画像是主动的——它不需要知道这个漏洞叫什么，只需要知道这个库不该这么干。这个转变让产品具备了对未知漏洞的抵抗力。

第四，**把性能开销做成产品前提，而不是优化项**。安全工具进不了生产环境，通常不是因为不准，是因为拖慢应用。Oligo 用 eBPF 在库级别工作，既精准又保持应用稳定——这是能落地的硬门槛。

第五，**早期把行业关键人物变成股东**。Snyk 的 CTO、Check Point 的创始人——这些名字出现在天使名单里，等于向整个行业宣告：我们自己人认可这个方向。这种背书比任何 PR 都有效。

## 来源与数据

- 站点：https://www.oligo.security
- 融资：2023 年 2 月出 stealth，累计 2800 万美金（种子轮 + A 轮），成立 9 个月内完成；种子轮由 TLV Partners 领投，A 轮由 Lightspeed Venture Partners、Ballistic Ventures 参与（Business Wire 官方通稿、Globes、FinSMEs、Calcalist）
- 投资人：Lightspeed Venture Partners、Ballistic Ventures、TLV Partners、Shlomo Kramer、Eyal Waldman、Adi Sharabani、Eyal Manor、Zohar Alon、Guy Bejerano、Shai Morag、Ofer Ben-Noon、Ohad Bobrov、Yair Amit；基金包括 Cyber Club London、Kmehin Ventures、OperAngels（Business Wire、Calcalist、TLV Partners 投资笔记）
- 技术与成效：基于自研 eBPF 引擎的动态库级分析与行为监控；为每个开源库建立合法行为画像，偏离权限策略时告警或阻断；客户响应安全警报的工作量减少约 85%（Business Wire、FinSMEs）
- 公司：2022 年成立于以色列特拉维夫，出 stealth 时 25 人并在纽约设办公室；创始团队毕业于 Intel Ignite 第六期（Calcalist、Business Wire）
- 创始人：Nadav Czerninski（CEO）、Gal Elbaz（CTO，前 Check Point，2020 年 9 月发现 Instagram 开源库攻击路径）、Avshalom Hilu（CPO），三人均为以色列国防军精锐网络部队前军官（Business Wire、Calcalist、Globes）
- 行业背景：现代软件 80% 至 90% 的代码来自开源；2022 年 Log4Shell 波及数亿台设备，其后 Text4Shell、Spring4Shell、OpenSSL、PyTorch、colors、faker 等攻击相继出现（Business Wire）

## 一句话总结

> 2020 年，一个前 Check Point 的工程师发现 Instagram 能被一个开源库滥用攻陷。真正让他不安的不是漏洞本身，而是「超出库权限的恶意行为居然完全不被察觉」。三个以色列前国防军网络军官据此创立 Oligo：不去追永远追不完的漏洞清单，而是用 eBPF 给每个运行中的开源库建立行为画像，一有偏离就告警。客户响应警报的工作量因此减少约 85%。九个月内，他们拿下了 2800 万美金，天使名单里躺着 Snyk 的 CTO 和 Check Point 的创始人。真正可迁移的是那次视角转换——当所有人都在数漏洞时，有人选择去盯行为。
