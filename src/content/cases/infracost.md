---
name: Infracost
一句话: 三兄弟（含一位云成本建模博士）把「等账单出来再优化」改成「写代码时就看见成本」，做了一个开源云成本估算工具，YC W21 起步，五年做到 3500+ 企业用户、1500 万美金 A 轮
创始人地区: Hassan Khajeh-Hosseini（CEO）、Ali Khajeh-Hosseini（CPO，云成本建模博士）、Alistair Scott（CTO），美国圣地亚哥；FinOps 老兵，2012 年做过最早的云成本管理产品（后被 RightScale/Flexera 收购）
营收模式: 开源核心 + 企业版 SaaS；CI/CD 免费层面向个人工程师，托管 Cloud Pricing API 按用量计费（250 美金/月每 1 万次运行），企业版支持定制价目表（EDP/EA）
月收入估算: 未公开 ARR；2025-11 完成 1500 万美金 A 轮（Pruven Capital 领投，YC、Sequoia、Mango、Alumni Ventures、TIAA Ventures 等参投），累计约 1800 万美金；3500+ 企业用户，含 10% 财富 500 强
流量来源: 开源社区（1.2 万 GitHub stars）自然获客；嵌入 GitHub/GitLab/Azure DevOps PR 评论，开发者即用即见；FinOps Foundation 官方成员身份与行业背书；财富 500 强标杆案例
可迁移点: ① 把分析的起点从「账单」前移到「代码」——Shift FinOps Left ② 开源做获客引擎，企业版做变现，开发者工具经典双轨 ③ 创始人本身就是品类老兵，认知即护城河 ④ 嵌入工作流（PR 评论）比单独 dashboard 留存高 ⑤ 用合规/企业特性（SOC2、定制价目表）切大客户
原文链接: https://www.infracost.io
数据口径: 融资——YC W21；种子轮 2021-09 约 300 万美金（Sequoia、YC、SV Angel、Mango、Brighter、Conductive、Goodwater 等）；A 轮 2025-11 约 1500 万美金（Pruven Capital 领投，YC、Sequoia、Mango、Alumni Ventures、TIAA Ventures 参投，Supabase 联创 Paul Copplestone、Essence VC Timothy Chen 等天使），累计约 1800 万美金（startupintros、infracost.io/blog）；规模——3500+ 企业用户、10% 财富 500 强、1.2 万 GitHub stars、追踪 400 万+ 云价格（infracost.io、startupintros）；产品——开源云成本估算，嵌入 GitHub/GitLab/Azure DevOps PR 评论，预算检查、FinOps 策略、标签合规、SOC 2 Type 2（infracost.io、extruct.ai）；创始人——Hassan Khajeh-Hosseini（CEO）、Ali Khajeh-Hosseini（CPO，云成本建模博士）、Alistair Scott（CTO），2012 年做过最早云成本管理产品（被 RightScale/Flexera 收购），FinOps Foundation 董事会成员（infracost.io/about）
分类: AI 基础设施 / 开发者工具·FinOps / 英文 / 美国
封面: /case-site/cases/infracost/site.png
---

![Infracost 官网](/cases/infracost/site.png)

# Infracost：在你写代码时就告诉你「这改一下要花多少钱」

## 产品是什么

Infracost 是一个**开源的云成本估算工具**，核心理念叫 **Shift FinOps Left**——把成本分析从「账单出来之后」前移到「代码写的时候就看见」。

传统云成本管理是事后算账：资源先部署、产生费用、月底看账单、再回头优化。但等账单出来，写代码的工程师早就去赶下个 sprint 了。

Infracost 的做法是直接坐进工程师的工作流：

- 你提一个 Infrastructure-as-Code 的改动（PR），它就在 **GitHub/GitLab/Azure DevOps 的 PR 评论里**，直接给出这次改动会增加多少月度成本、有没有更优选项（比如 GP2 卷换成 GP3）。
- **预算检查**：改动超预算就触发审批流。
- **FinOps 策略**：自动检查标签合规、最佳实践。
- 支持 AWS、Azure、GCP，追踪 **400 万+ 云价格**。

一句话：**给云资源加一个「结账前的价签」**。

## 怎么赚的钱

**开源核心 + 企业版 SaaS** 的双轨模式。

- **CI/CD 免费层**：个人工程师免费，集成 GitHub/GitLab/Azure，社区支持。
- **托管 Cloud Pricing API**：按用量计费，250 美金/月每 1 万次运行。
- **企业版**：支持定制价目表（EDP/EA 等），对接大客户采购流程；SOC 2 Type 2 认证。

融资节奏：

- 种子轮 2021-09 约 **300 万美金**（Sequoia、YC、SV Angel、Mango 等）
- A 轮 2025-11 约 **1500 万美金**（Pruven Capital 领投，YC、Sequoia、Mango、Alumni Ventures、TIAA Ventures 参投），累计约 **1800 万美金**

## 流量从哪来

第一，**开源社区自然获客**。1.2 万 GitHub stars，工程师用了觉得好就带进公司。

第二，**嵌入工作流**。PR 评论这种「即用即见」的形态，比单独开个 dashboard 留存高得多——它长在工程师每天待的地方。

第三，**FinOps Foundation 官方成员**。创始人是这个领域的老兵，还是基金会董事会成员，行业背书强。

第四，**财富 500 强标杆**。10% 的财富 500 强在用，这种案例本身就是销售弹药。

## 站长是谁

**Hassan Khajeh-Hosseini**（CEO）、**Ali Khajeh-Hosseini**（CPO，云成本建模博士）、**Alistair Scott**（CTO）。

这三位是 FinOps 赛道的老兵，2012 年就做过市场上最早的云成本管理产品（后来被 RightScale 收购，成为 Flexera FinOps 方案的基础）。Ali 的云成本建模博士背景，是 Infracost 能精确建模 400 万+ 价格的一块基石。

团队来自 AWS、HashiCorp、Pulumi、Snyk，2021 年成立，总部圣地亚哥。

## 这个案例能学到什么

第一，**把分析的起点从「账单」前移到「代码」**。这是 Infracost 整个产品的灵魂——等账单出来再优化，工程师早走了；写代码时看见成本，他当场就改。

第二，**开源做获客引擎，企业版做变现**。开发者工具最稳的双轨：先用免费开源把人圈进来，再向大客户收企业特性的钱。

第三，**创始人本身就是品类老兵，认知即护城河**。他们在 2012 年就被收购过一次，对云成本的理解比任何新团队都深。

第四，**嵌入工作流比单独 dashboard 留存高**。长在 PR 评论里，工程师每天都能见到，自然形成习惯。

第五，**用合规和企业特性切大客户**。SOC 2、定制价目表这些「无聊」的东西，恰恰是打开财富 500 强门的钥匙。

## 来源与数据

- 站点：https://www.infracost.io
- 融资：YC W21；种子轮 2021-09 约 300 万（Sequoia、YC、SV Angel、Mango 等）；A 轮 2025-11 约 1500 万（Pruven Capital 领投，YC、Sequoia、Mango、Alumni Ventures、TIAA Ventures 参投），累计约 1800 万（startupintros、infracost.io/blog）
- 规模：3500+ 企业用户、10% 财富 500 强、1.2 万 GitHub stars、追踪 400 万+ 云价格（infracost.io、startupintros）
- 产品：开源云成本估算，嵌入 GitHub/GitLab/Azure DevOps PR 评论，预算检查、FinOps 策略、标签合规、SOC 2 Type 2（infracost.io、extruct.ai）
- 创始人：Hassan Khajeh-Hosseini（CEO）、Ali Khajeh-Hosseini（CPO，云成本建模博士）、Alistair Scott（CTO），2012 年做过最早云成本管理产品（被 RightScale/Flexera 收购），FinOps Foundation 董事会成员（infracost.io/about）

## 一句话总结

> 三兄弟（含一位云成本建模博士）把「等账单出来再优化」改成「写代码时就看见成本」，做了开源云成本估算工具 Infracost，提出 Shift FinOps Left 理念。它直接坐进 GitHub PR 评论，告诉你这次改动会多花多少钱、有没有更优选项，追踪 400 万+ 云价格。YC W21 起步，开源获客、企业版变现，五年做到 3500+ 企业用户、10% 财富 500 强在用，2025 年完成 1500 万美金 A 轮。真正可迁移的那句话是：**把分析的起点前移到用户每天待的地方（代码），比做一个独立 dashboard 留存高得多**——而且创始人本身就是品类老兵，认知就是护城河。
