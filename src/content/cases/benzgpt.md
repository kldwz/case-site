---
name: BenzGPT
一句话: Honorable Mention（Google Chrome 内置 AI 挑战赛）：让 AI 的输出从文字变成动作——浏览器 + 蓝牙，就能控制现实世界的设备。
创始人地区: 独立开发者/小团队参赛作品，提交于 Google Chrome Built-in AI Challenge
场景: 用自然语言控制一台小车：在网页里说话，小车照做（Web Bluetooth + 语音识别）
营收模式: 尚未商业化（黑客松参赛作品，无营收数据）
月收入估算: 无收入（黑客松获奖作品）
流量来源: 赛事作品页 + 端侧/浏览器 AI 话题传播
原文链接: https://devpost.com/software/wheely-wonka
数据口径: Devpost 官方作品页（https://devpost.com/software/wheely-wonka），2026-09-13 抓取：赛事 Google Chrome Built-in AI Challenge（https://googlechromeai.devpost.com/）、奖项 Honorable Mention、23 likes、技术栈 promptapi / speechrecognitionapi / webbluetooth / webspeechapi、源码 https://github.com/nico-martin/benz-gpt。无营收数据
分类: AI 应用 / 浏览器内置 AI / 英文
类型: 获奖作品
证据等级: 平台数据可查
平台数据: Devpost 官方作品页：Honorable Mention · 23 likes（2026-09-13）
赛事: Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）
奖项: Honorable Mention
封面: /case-site/cases/benzgpt/site.png
---

![BenzGPT 作品页](/cases/benzgpt/site.png)

> **赛事**：Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）
> **场景**：用自然语言控制一台小车：在网页里说话，小车照做（Web Bluetooth + 语音识别）
> **奖项**：Honorable Mention
> **出处**：[作品页](https://devpost.com/software/wheely-wonka) ｜ [赛事页](https://googlechromeai.devpost.com/) ｜ [源码](https://github.com/nico-martin/benz-gpt)

# BenzGPT：让 AI 的输出从文字变成动作——浏览器 + 蓝牙，就能控制现实世界的设备。

## 它做了什么

一个把大模型接到真实硬件上的项目：你在网页里用自然语言说"往前开、左转、停"，小车通过蓝牙收到指令照做。

## 这个解法妙在哪

1. **它把 AI 从屏幕里搬到了现实世界**。大部分 AI 产品的输出是文字，它的输出是**动作**——这个差别让它在一堆网页工具里非常扎眼。
2. **全部用浏览器 API 完成**：语音识别（WebSpeech）、蓝牙（Web Bluetooth）、Prompt API 做意图解析——不需要写原生 App，一个网页就能控制硬件。
3. **它演示的是一种可能性**：浏览器正在变成一个能接触物理世界的控制界面。

## 技术怎么实现的

Prompt API 解析自然语言意图，WebSpeech API / SpeechRecognition API 做语音输入，Web Bluetooth 把指令发给小车。全程在浏览器里完成，没有原生 App。

## 团队与赛事

Google Chrome Built-in AI Challenge（谷歌官方，Devpost 承办）（赛事页 https://googlechromeai.devpost.com/）。作品页获 **Honorable Mention** 徽章，23 个赞；源码公开在 GitHub。

## 这个案例能学到什么

1. **AI 的输出不一定非要是文字**。动作、控制、指令——都是被忽视的方向。
2. **Web Bluetooth 让网页能直接控制硬件**。这个能力远未被充分使用。
3. **"用嘴控制"是最自然的交互**。语音 + 硬件的组合在产品演示里极具冲击力。
4. **比赛里，能"动起来"的作品天然有优势**。评委记得住。
5. **不需要原生 App 就能做硬件控制**，这个门槛低得超出大多数人想象。

## 来源与数据

- Devpost 官方作品页：`https://devpost.com/software/wheely-wonka`（2026-09-13 抓取：奖项 Honorable Mention、23 likes、技术栈 promptapi / speechrecognitionapi / webbluetooth / webspeechapi）
- 赛事页：`https://googlechromeai.devpost.com/`
 - 源码：`https://github.com/nico-martin/benz-gpt`
- 赛事作品，无营收数据，本站不做估算

## 一句话总结

> 让 AI 的输出从文字变成动作——浏览器 + 蓝牙，就能控制现实世界的设备。