---
name: Hightouch
一句话: 三个 Segment 老兵反着做 CDP——不把数据搬到新平台，而是直接从数据仓库同步；7 年做到 27.5 亿美金估值、年经常性收入破 1 亿美金
创始人地区: Tejas Manohar（联合创始人兼联席 CEO）、Kashish Gupta（联合创始人兼联席 CEO）、Josh Curl（联合创始人兼 CTO），总部美国旧金山
营收模式: 企业级 Composable CDP 与 Agentic Marketing 平台订阅，按同步的数据量与激活目的地收费，客户以零售、金融、媒体与 B2B SaaS 的中大型企业为主
月收入估算: 2025 年 ARR 突破 1 亿美金，连续两年增速超 100%；2026 年 4 月 D 轮后估值 27.5 亿美金，累计融资超 3.22 亿美金，约 400 名员工
流量来源: YC S19 起步并开创「反向 ETL」这一品类心智 + 2026 年首次参评即入选 Gartner CDP 魔力象限领导者且执行力维度最高 + 标杆客户背书（Spotify、DoorDash、Domino's、PetSmart、Grammarly、Chime、WHOOP）+ Snowflake 精英级合作伙伴身份带来的渠道分发
可迁移点: ① 反共识要反在架构上，而不是话术上——传统 CDP 让企业把数据复制一份出来，Hightouch 坚持不复制、直接在仓库上跑，这个架构差异后来长成了合规、成本和实时性三重护城河 ② 先在一个品类里做到定义者，再扩张品类——他们先用反向 ETL 立住，再切 CDP，最后才讲 Agentic Marketing，每一步都有前一步的信任做垫脚 ③ 让 AI 吃进「品牌上下文」而不是只调通用模型——他们的 AI 决策直接连客户的品牌规范、素材库与受众数据，模型再强也不会有品牌上下文，这是 Tejas 反复强调的 ④ 创始团队的旧履历就是最好的差异化证据——三个人都做过 Segment 的 Personas 与 Warehouses，他们比任何人都清楚上一代 CDP 为什么慢 ⑤ 增长数字要挑能被第三方验证的讲——ARR、同比增速、Gartner 定位、客户名单，这些都能被查，比自说自话的行业领导地位有效得多
原文链接: https://hightouch.com
数据口径: 融资——2025 年 2 月 8000 万美金 C 轮由 Sapphire Ventures 领投，估值 12 亿美金；2026 年 4 月 29 日 1.5 亿美金 D 轮由 Goldman Sachs Alternatives 与 Bain Capital Ventures 共同领投，估值 27.5 亿美金，14 个月翻倍，累计融资超 3.22 亿美金（Hightouch 官方公告与博客）；营收——2025 年 ARR 突破 1 亿美金，连续两年增速超 100%，欧洲市场贡献约 25%（Hightouch 官方、Silicon Valley Investclub 公司档案）；客户与规模——同步超 7.3 万亿条记录、覆盖 200 多个目的地，驱动超 100 亿次 AI 决策事件，客户包括 Spotify、DoorDash、Domino's、PetSmart、Warner Music Group、Grammarly、Chime、WHOOP，约 400 名员工（Hightouch 官方、Gartner 2026 CDP 魔力象限）
分类: 企业数据基础设施 / 营销自动化 / 英文 / 美国
封面: /case-site/cases/hightouch/site.png
---

![Hightouch 官网](/cases/hightouch/site.png)

# Hightouch：不搬数据的 CDP，7 年做到 27.5 亿美金

## 产品是什么

Hightouch 做的是**可组合式客户数据平台（Composable CDP）**。

理解它的关键在「不搬数据」这四个字。传统 CDP 的玩法是：企业把散落各处的数据复制一份到 CDP 里，再在里面做分群和投放。这套做法有三个老问题——数据搬出去就有了合规风险，复制延迟让投放不实时，而且每次改需求都要重新导一遍。

Hightouch 反过来：**数据就留在 Snowflake、Databricks、BigQuery 这些客户已经建好的数据仓库里，Hightouch 只负责把数据「同步」到营销、销售、客服要用的 200 多个工具里**。它把这条路径开创成了一个品类，叫反向 ETL（Reverse ETL）。

到 2025 年之后，它在反向 ETL 之上又叠了一层 **Agentic Marketing Platform**：AI agent 能自己研究受众、生成符合品牌调性的广告素材，并在广告、邮件、短信、网页这些渠道里执行跨渠道投放。

## 怎么赚的钱

**企业级平台订阅**，按同步的数据量与激活目的地收费。客户是零售、金融、媒体和 B2B SaaS 里那些「数据量大、营销触点多」的公司。

增长曲线很陡：

- **2025 年 ARR 突破 1 亿美金**，连续两年增速超过 100%
- **2025 年 2 月**：8000 万美金 C 轮，Sapphire Ventures 领投，估值 **12 亿美金**
- **2026 年 4 月 29 日**：1.5 亿美金 D 轮，Goldman Sachs Alternatives 与 Bain Capital Ventures 共同领投，估值 **27.5 亿美金**

14 个月，估值翻了一倍多。累计融资超 3.22 亿美金，团队约 400 人，分布在旧金山、纽约、奥斯汀、伦敦和东南亚，还在巴黎扩办公室。

值得注意的是 **25% 的收入来自欧洲市场**——对一家 2019 年才从 YC 起步的公司来说，这个海外占比说明产品不是靠美国本土关系卖出来的。

## 流量从哪来

第一，**开创了一个能占住心智的品类词**。他们 coined 了「Composable CDP」和「反向 ETL」。当一个问题还没有名字的时候，给它命名的人会天然成为默认选项。

第二，**Gartner 的第三方背书**。2026 年他们第一次参评 CDP 魔力象限就直接进了领导者象限，而且在执行力维度上排到最高。对企业采购来说，这个位置的说服力远大于自吹自擂。

第三，**客户名单本身就是广告**。Spotify、DoorDash、Domino's、PetSmart、Warner Music Group、Grammarly、Chime、WHOOP——这份名单覆盖了零售、餐饮、媒体、金融、消费电子，等于告诉所有潜在客户「你这个行业的一线公司已经在用了」。

第四，**数据规模构成了可信度**。同步超 7.3 万亿条记录、驱动超 100 亿次 AI 决策事件。这种量级不是 PPT 能编的，它直接回答了采购最关心的问题：你扛得住我们的规模吗。

## 站长是谁

**Tejas Manohar** 和 **Kashish Gupta** 是联席 CEO，**Josh Curl** 是 CTO。三个人都出自 **Segment**——那家被 Twilio 以 32 亿美金收购的 CDP 公司。

他们不是普通员工。Manohar 是 Segment 仓库产品的早期工程师，Gupta 做过 Personas 里的机器学习部分，Curl 则开发了 Personas 的激活功能。换句话说，**上一代 CDP 的核心模块就是他们写的**。

正因为如此，他们对 CDP 的痛点不是调研出来的，是自己踩出来的：CDP 承诺让营销人员激活数据，实际交付的是一套僵化的数据要求、昂贵的价格标签和脱离企业真实数据源的孤岛。

2019 年，三人通过 Y Combinator 创立 Hightouch，最初只做反向 ETL 这一件事。后来发现数据团队之外，营销和增长团队的需求更大，于是做了 Customer Studio 让不懂 SQL 的人也能直接从仓库取数、建人群、做多渠道投放——这才是真正对标 CDP 的产品。

Tejas 有一句话点出了 AI 时代他们的位置：**模型会越来越强，但它们永远不会拥有一家品牌的全部上下文**。

## 这个案例能学到什么

第一，**反共识要反在架构层**。Hightouch 的差异化不是「我们更便宜」或者「我们功能更多」，而是「我们不复制你的数据」。这个架构选择带来了连锁收益：合规更简单、延迟更低、成本更省。竞争者也很难跟进，因为那等于重做产品。

第二，**一个阶段只定义一个品类**。反向 ETL → Composable CDP → Agentic Marketing，三次定位升级，每一次都建立在上一次已经兑现的信任之上。如果 2019 年就喊 Agentic Marketing，大概率没人信。

第三，**把品牌的上下文变成 AI 的护城河**。通用模型谁都能调，Hightouch 的 AI 直接吃客户的品牌规范、Figma 素材和历史受众数据，输出天然「像这个品牌」。模型再进步也补不上这块。

第四，**创始人的旧履历是最有说服力的差异化**。三个人做过 Segment 的仓库和 Personas，这个事实本身就解释了「为什么是他们」——投资人、客户、媒体都吃这一套，因为它可验证。

第五，**只讲能被第三方验证的数字**。ARR、同比增速、Gartner 定位、客户名单、同步记录数——每一项都能查。相比之下，「我们是行业领导者」这种话没有任何信息量。

## 来源与数据

- 站点：https://hightouch.com
- 融资：2025 年 2 月 8000 万美金 C 轮由 Sapphire Ventures 领投，估值 12 亿美金；2026 年 4 月 29 日 1.5 亿美金 D 轮由 Goldman Sachs Alternatives 与 Bain Capital Ventures 共同领投，估值 27.5 亿美金；D 轮跟投方包括 Sapphire Ventures、ICONIQ Capital、Amplify Partners、TD7；累计融资超 3.22 亿美金（Hightouch 官方博客、Silicon Valley Investclub 公司档案）
- 营收：2025 年 ARR 突破 1 亿美金，连续两年增速超 100%，欧洲市场占收入约 25%（Hightouch 官方、Silicon Valley Investclub）
- 客户与规模：同步超 7.3 万亿条记录、覆盖 200 多个目的地，驱动超 100 亿次 AI 决策事件；客户包括 Spotify、DoorDash、Domino's、PetSmart、Warner Music Group、Grammarly、Chime、WHOOP；约 400 名员工，办公地含旧金山、纽约、奥斯汀、伦敦与东南亚（Hightouch 官方、Gartner 2026 CDP 魔力象限）
- 产品里程碑：2019 年 YC S19 起步做反向 ETL；2024 年 8 月推出 AI Decisioning；2026 年 2 月发布 Agentic Marketing Platform 并推出 Ad Studio；2023 年底收购 HeadsUp（Hightouch 官方博客）
- 创始人：Tejas Manohar（联席 CEO，Segment 仓库产品早期工程师）、Kashish Gupta（联席 CEO，宾大机器学习背景）、Josh Curl（CTO，Segment Personas 开发者）（Hightouch 官网、Silicon Valley Investclub）

## 一句话总结

> 三个亲手做过上一代 CDP 的人，选择了一条最笨的路——不把客户的数据搬出来，而是在客户已有的数据仓库上直接干活。这个「不复制」的架构决定，后来成了合规、实时性和成本上的三重护城河。七年后，他们年经常性收入破 1 亿美金、估值 27.5 亿美金，客户名单里躺着 Spotify 和 Domino's。真正可复制的不是「做 CDP」，而是他们给一个没人命名的问题起了名字，然后一步步把这个名字变成行业标准。
