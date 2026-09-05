---
name: Agent Sandbox & Site
一句话: 开源AI Agent基础设施，盈利模式未提及
创始人地区: 未知
营收模式: 未官方披露。项目以MIT协议开源，目前没有展示任何付费功能或商业模式，可能通过后续企业服务或赞助获得收入，但候选信息中无公开说明。
月收入估算: 未官方披露
流量来源: 主要来自V2EX的“分享创造”板块，通过标题和内容吸引开发者关注，讨论AI Agent基础设施话题。由于项目是开源的，流量也可能通过GitHub等代码平台自然传播，但候选信息未提及具体渠道数据。
可迁移点: 关注AI Agent的信任问题，解决执行边界和交付证据痛点；用Kubernetes原生能力构建安全沙箱，默认安全配置；提供多种接口（HTTP/CLI/MCP）降低使用门槛；用可验证的部署结果替代简单的成功回执
原文链接: https://www.v2ex.com/t/1239711#reply0
数据口径: v2ex_create 收录
分类: 开发者工具 / 开源 / AI Agent
封面: /case-site/cases/ai-agent-gvisor/site.png
---

![Agent Sandbox & Site 官网](/case-site/cases/ai-agent-gvisor/site.png)

# Agent Sandbox & Site：开源AI Agent基础设施，盈利模式未提及

## 产品是什么

这是两个面向AI Agent的开源基础设施项目：Sandbox提供安全执行环境，每个Runtime都是Kubernetes上的gVisor Pod，默认非root、只读根文件系统、无ServiceAccount token、默认拒绝网络策略；Site则是可验证的网站部署工具，Agent通过HTTP/CLI/MCP提交部署，工作负载就绪后会请求真实地址，并将HTTP状态码和响应体SHA-256写入status。普通使用者可以在自己的Kubernetes集群中安装这两个项目，让Agent安全执行命令，并确认网站真的部署成功。

## 怎么赚的钱

未官方披露。项目以MIT协议开源，目前没有展示任何付费功能或商业模式，可能通过后续企业服务或赞助获得收入，但候选信息中无公开说明。

## 流量从哪来

主要来自V2EX的“分享创造”板块，通过标题和内容吸引开发者关注，讨论AI Agent基础设施话题。由于项目是开源的，流量也可能通过GitHub等代码平台自然传播，但候选信息未提及具体渠道数据。

## 这个案例能学到什么

关注AI Agent的信任问题，解决执行边界和交付证据痛点；用Kubernetes原生能力构建安全沙箱，默认安全配置；提供多种接口（HTTP/CLI/MCP）降低使用门槛；用可验证的部署结果替代简单的成功回执

## 来源与数据

- 站点：https://www.v2ex.com/t/1239711#reply0
- 来源：v2ex_create（2026-09-05）
- 收入：未官方披露

## 一句话总结

> 开源AI Agent基础设施，盈利模式未提及
