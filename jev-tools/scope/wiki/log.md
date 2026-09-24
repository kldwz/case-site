---
janitor:
  bucket: log_entry
  persist: 1.5
  confidence: 1.0
  bucket_margin: 1.0
  contains_secret: 0.1
  safe_to_leave_in_git: 0.33
  action: frontmatter
  reason: normal vote
  model: jev-1.13.0
  taxonomy: be00a24c7a68
  at: '2026-09-23T04:56:34Z'
---
# 变更日志

## [2026-08-09] restructure | 知识库三层架构重组
来源: karpathy-llm-wiki skill 方法论
影响页面: 全部（55 个文件 -> 22 个 wiki 页 + 4 个 sources 目录 + 3 个 drafts）
---
操作摘要:
- 创建三层分离架构：sources/ (只读) + wiki/ (编译知识) + SCHEMA.md (规则)
- 去重合并 5 组跨日期重复文件（语音ramble、每日市场信号、PDF转Markdown、levelsio视频编辑器、营销Agent）
- 拆分 1 组文件名碰撞（"普通人用LLM理财" 08-08 是 MIT 理财研究，08-09 实为 FutureTools 死站筛选）
- 创建 6 个实体页（gregisenberg, levelsio, karpathy, simonw, emollick, mreflow）
- 创建 7 个概念页（marketing-agent-loop, voice-ramble-method, daily-market-signal-md, pdf-to-markdown, agent-as-daily-sms, copilot-to-loop-framework, install-md-skills, codex-control-bluetooth）
- 创建 7 个主题页（26-startup-directions, 5-solo-opportunities, levelsio-ai-video-editor, futuretools-dead-filtering, llm-financial-advice, hardware-startup-golden-age, creator-ai-boundary, software-not-dead-debate）
- 创建 index.md（总目录索引）和 log.md（本文件）
- 迁移原始采集到 sources/raw-collect/，KEEP 候选到 sources/keep-candidates/，公众号文章到 sources/mpwechat/
- 迁移日报到 wiki/daily/，周报到 wiki/weekly/，战略文档到 wiki/strategy/，草稿到 drafts/
- 清理空文件（2026-02-06.md）和重复的 excalidraw 文件
- 旧 `AI机会侦察/` 目录（24 个文件）已移入 `.trash/`，所有内容均已合并到 wiki/ 中
- 修正 index.md 页面计数（22 -> 28，概念 7->8，主题 7->8）
- 备份到 obsidian_workspace_backup_20260809
---

## [2026-08-09] ingest | 08-09 采集
来源: X 6 个账号（@ruben_hassid 限流失败; Reddit 全社区 403）
Pages affected: 日报-08-09 (new), KEEP候选-08-09 (new), 周报-2026-08-09 (new), 10 条 KEEP 落库
---

## [2026-08-08] ingest | 08-08 采集
来源: X 6 个账号（@ruben_hassid 限流; Reddit 403）
Pages affected: 日报-08-08 (new), KEEP候选-08-08 (new), 12 条 KEEP 落库, 副业作战地图 (new), 生产流水线搭建计划 (new), 行动卡-本周练手 (new)
---

---

## [2026-08-31] maintenance | 收敛整理（治"乱"）
来源: 用户反馈知识库混乱，参照 LLM wiki 三层架构做校准。
Pages affected:
- 重命名 4 个实体页以统一 kebab-case：0xROAS→0x-roas、EXM7777→exm-7777、AmirMushich→amir-mushich、ai_explorer25→ai-explorer25（双链引用已全局替换，零残留）
- 重新生成 wiki/index.md：由失真的 28 页（停于 2026-08-09）校准为真实 45 个 wiki 页 + 15 份 sources 原始资料
- 修订 SCHEMA.md：消除"kebab-case vs 中文日报名"自相矛盾；补充三层边界、三套记忆职责表、index 维护纪律
待人工确认:
- drafts/、Mem0记忆/、Excalidraw/ 三个游离目录是否长期保留为"体系外"（当前已明确不计入 index）
- strategy/ 下中文页（副业作战地图等）是否未来也 kebab 化

---

## [2026-08-31] ingest | 苍何《自生长知识库》文章入库
来源: 用户提供的微信公众号文章 https://mp.weixin.qq.com/s/6pkU-Ggx1KkM_7Blgpbdhw
Pages affected:
- sources/mpwechat/用WorkBuddy_Codex加Obsidian搭建自生长个人知识库.md (new, Raw 层原始资料)
- wiki/sources/obsidian-llm-wiki-zi-growth.md (new, 来源摘要页)
- wiki/concepts/llm-wiki.md (new, 核心概念：LLM wiki 自生长)
- wiki/topics/self-growing-kb.md (new, 主题综述)
- wiki/entities/karpathy.md (updated, 补充 LLM wiki 方法关联)
双链: llm-wiki ↔ karpathy ↔ self-growing-kb ↔ sources 摘要，全部连通
待人工确认:
- 是否要把 "wiki/sources/" 正式纳入 SCHEMA 目录结构说明（之前 SCHEMA 未列此目录，本次按规则补建）

---

## [2026-08-31] ingest | X 值得关注博主清单（13 个账号）
来源: 用户提供的 X/Twitter 博主清单及领域标注
Pages affected:
- wiki/entities/ 新建 8 个实体页: tibo-maker, athcanft, wickedguro, robj3d3, illyism, dannypostma, alexfinn, romanbuildsaas
- wiki/entities/ 补充 5 个已有页的"用户标注领域": levelsio(山羊/待确认), marclou(SaaS), jackfriks(微应用), ai-explorer25(人工智能与科技), gregisenberg(创业理念)
- wiki/entities/x-ai-accounts.md 追加 #16-28 批次（现共 28 个 X 账号）
待人工确认:
- levelsio 的"山羊"含义（GOAT 谐音梗 or 具体方向？）

---

## [2026-09-13] ingest | 核心 10 人清单（中文圈为主）
来源: 用户提供的"AI 值得关注的 10 个人"清单（筛选逻辑：实用 + 深度 + 一手；覆盖工具、测评、原理、落地、变现）
Pages affected:
- wiki/entities/ 新建 8 个实体页: dotey, op7418, khazix0918, vista8, lijigang, jason23818126, ai-jasonyu, smartpigai
- wiki/entities/karpathy.md (updated): 补"全球 AI 教育天花板"标签 + 列入核心清单记录
- wiki/entities/simonw.md (updated): 补关注动机"用 LLM 做实事" + 标签 + 列入核心清单记录
- wiki/entities/x-ai-accounts.md (updated): 追加 #36-45 批次（现共 45 个 X 账号）
- wiki/index.md (updated): 实体计数 35 → 43，总页数 62 → 70，x-ai-accounts 更新日期改 09-13
命名说明:
- handle `AI_Jasonyu` 含大写+下划线，按 kebab-case 规则转 `ai-jasonyu`（参照 kloss-xyz / alex-prompter 先例）
内容原则:
- 新页仅落用户提供的一句定位描述，观点区一律标"待补充"——不编造博主原话，待后续采集回填
待人工确认:
- 本批 8 个新账号是否需要纳入日常 X 采集源清单（当前采集脚本仅覆盖 6 个账号）

---

## [2026-09-14] ingest | 《程序员转AI副业指南》知识产品入库
来源: 旺旺自产的 19.9 元知识产品，8 个开源项目整理后原创写作
Pages affected:
- wiki/topics/ai-side-hustle-guide-product.md (new, 知识产品元索引卡)
- wiki/index.md (updated): topics 9 → 10，总页数 70 → 71

内容说明:
- 成品指南 30KB/1076 行，放在工作区 `/Users/hxw/AI-副业指南/`（不进 wiki 编译层，太重）
- wiki 里只留 topic 卡做"元索引"，指向工作区路径 + 核心判断
- 8 个开源项目：XiaomingX/ai-money-maker-handbook（主力，444章）+ easychen/lean-side-bussiness（方法论）+ garylab/MakeMoneyWithAI（工具清单）+ 5个二次索引
- 15 个方案分三梯队，MVP 推荐组合：方案1（小红书图文工具）+方案5（知识付费课程）+方案6（付费社群）
- 与 [[strategy/副业作战地图]] 的关系：作战地图讲执行路径，本指南讲方案拆解，互补不冲突

后续动作（工作区内）:
- [ ] 排版 PDF
- [ ] 公众号主售 + 小红书/闲鱼引流
- [ ] 内容加厚到 ¥49.9 版本

---

## [2026-09-21] bookmark | 手绘风 skill 仓库登记
来源: 用户提供的 GitHub 地址 https://github.com/yang0/handraw-style
Pages affected:
- wiki/bookmarks/bookmarks-2026-08-09.md (updated): 「AI/LLM 学习」节追加 1 条，归到既有 Claude Skills 仓库群（awesome-claude-skills / baoyu-skills / yunshu_skillshub / huashu-design 之后）
- wiki/index.md (updated): bookmarks 行更新日期 08-31 → 09-21

内容说明:
- 仅登记地址 + 结构概览，按用户要求不深挖内容、不装成 Hermes skill
- 仓库实测结构（tarball 34MB / 644 文件）：主 SKILL.md、STYLES.md 风格库、LAYOUTS.md 布局库、MANIFEST.md、.agents/skills/ 下 3 个子 skill（style-library-importer / layout-library-importer / tweet-style-importer）、images/ 约 300 张 webp 手绘参考图
- 分支是 master（不是 main）；GitHub API 与 api.github.com 当时限流，内容经 codeload tarball 获取
- 后续动作（未做，待用户明确）: 若确需调用，再考虑装进 ~/.hermes/skills/ —— 建议只装 md 文档（几 KB），300 张参考图留在仓库引用，避免撑爆 skill 目录

---

## [2026-09-21] bookmark | fmhy.net/ai AI 资源站登记
来源: 用户提供的网址 https://fmhy.net/ai（"很多 AI 相关的资源都可以从这里面获取到；以后问 AI 资源去哪找时调出这个网址"）
Pages affected:
- wiki/bookmarks/bookmarks-2026-08-09.md (updated): 「AI/LLM 学习」节追加 1 条，紧接 handraw-style
- wiki/index.md (updated): bookmarks 行更新日期同为 09-21（与上一条共用同一次日期改动）

内容说明:
- 站点识别: freemediaheckyeah (fmhy) 的 AI 版块，VitePress 静态站，页面标题 "Artificial Intelligence"，meta 描述 "Chatbots, Text Generators, Image Generators, Chatbot Tools"
- 规模实测: 285 个 li 条目 / 257 个独立外部域名 / 37 条标注 "No Sign-Up"（免注册）
- 9 大分类: AI Chatbots、AI Coding Tools（跳转 /developer-tools/#ai-tools）、Image Generation、Video Generation、Audio Generation、AI Agents、AI Tools、AI Indexes、AI Benchmarks
- 26 个子分类: text-to-speech、voice-change-clone、voice-removal-separation、image-restoration、local-frontends、local-ai-frontends、self-hosting-tools、multiple-model-sites、official-model-sites、roleplaying-chatbots、specialized-chatbots、ai-prompts、guides-tools、grammar-check、ai-agents、ai-tools、ai-indexes、ai-benchmarks、specialized-benchmarks、coding-benchmarks 等
- 域名构成: github.com 146、discord.com 66、discord.gg 59、reddit.com 24、x.com 18、huggingface.co 14、google colab 12 —— 开源项目为主
- 特色: 条目带 GitHub/Discord/Reddit/X/Colab 直达图标；标注 Windows/macOS/Linux/Web 平台；内嵌 HuggingFace ZeroGPU 限流警告说明（未登录 120 秒/天，注册后 300 秒/天）
- 站点自带隐私章节 /privacy，含 proxy 与 VPN 说明
- 获取方式: web_extract 被拦（判内网），改用 curl + 直接拉 VitePress 的 ai.md.<hash>.lean.js 打包源文件解析

---

## [2026-09-23] bookmark | LearnPrompt/awesome-seedance 视频提示词 skill 库登记
来源: 用户转发的公众号文章《我把463个AI视频做成了Skill和提示语模版，全都开源！》里提到的仓库；用户说"先不装，帮我记一下，等说做视频时能用"
Pages affected:
- wiki/bookmarks/bookmarks-2026-08-09.md (updated): 「AI/LLM 学习」节 skills 仓库群（awesome-claude-skills → baoyu-skills → yunshu_skillshub → huashu-design 之后）追加 1 条
- wiki/index.md (updated): bookmarks 行更新日期 09-21 → 09-23

内容说明:
- 仓库: https://github.com/LearnPrompt/awesome-seedance —— 本地已 clone 在 /Users/hxw/seedance-lib（v0.3.0），未装成 Hermes skill（用户要求先不装）
- 性质: Seedance 2.5/2.0 **提示词编写** skill 库，只写提示词、不生成视频；真出片走 即梦/Dreamina(免费) 或 火山方舟 Volcengine Ark API(付费)
- 结构: 主 skill `seedance-prompt-library` + 12 个分题材 skill（meme喜剧 / 复古DV家庭录像 / 旅行CityWalk / 宠物 / 时尚Lookbook / 3D卡通 / 车 / 史诗奇幻科幻 / 恐怖悬疑 / 运动极限 / 分镜网格转视频 / 表情包喜剧）；每个含 SKILL.md + references/cases.md（案例锚点 goodcase.ai）
- 触发用法: 用户说"做视频"时从知识库调出此条，进 /Users/hxw/seedance-lib 按题材取对应 SKILL.md 写提示词
- 后续动作（未做，待用户明确）: 是否装成 ~/.hermes/skills/ 待定；当前仅在本地 clone 备查

---

## [2026-09-23] bookmark | LearnPrompt/awesome-seedance 视频提示词 skill 库登记
来源: 用户转发的公众号文章《我把463个AI视频做成了Skill和提示语模版，全都开源！》里提到的仓库；用户说"先不装，帮我记一下，等说做视频时能用"
Pages affected:
- wiki/bookmarks/bookmarks-2026-08-09.md (updated): 「AI/LLM 学习」节 skills 仓库群（awesome-claude-skills → baoyu-skills → yunshu_skillshub → huashu-design 之后）追加 1 条
- wiki/index.md (updated): bookmarks 行更新日期 09-21 → 09-23

内容说明:
- 仓库: https://github.com/LearnPrompt/awesome-seedance —— 本地已 clone 在 /Users/hxw/seedance-lib（v0.3.0），未装成 Hermes skill（用户要求先不装）
- 性质: Seedance 2.5/2.0 **提示词编写** skill 库，只写提示词、不生成视频；真出片走 即梦/Dreamina(免费) 或 火山方舟 Volcengine Ark API(付费)
- 结构: 主 skill `seedance-prompt-library` + 12 个分题材 skill（meme喜剧 / 复古DV家庭录像 / 旅行CityWalk / 宠物 / 时尚Lookbook / 3D卡通 / 车 / 史诗奇幻科幻 / 恐怖悬疑 / 运动极限 / 分镜网格转视频 / 表情包喜剧）；每个含 SKILL.md + references/cases.md（案例锚点 goodcase.ai）
- 触发用法: 用户说"做视频"时从知识库调出此条，进 /Users/hxw/seedance-lib 按题材取对应 SKILL.md 写提示词
- 后续动作（未做，待用户明确）: 是否装成 ~/.hermes/skills/ 待定；当前仅在本地 clone 备查

---

## [2026-09-23] bookmark | gnipbao/story-to-handdrawn-video 手绘视频 Agent Skill 登记
来源: 用户提供的仓库 https://github.com/gnipbao/story-to-handdrawn-video ；用户说"记到知识库，后续做视频手绘画风格可以用上"
Pages affected:
- wiki/bookmarks/bookmarks-2026-08-09.md (updated): 「AI/LLM 学习」节 skills 仓库群（awesome-seedance 之后）追加 1 条
- wiki/index.md: 该书签页更新日期已是 09-23（本次连带改动，无需再改）

内容说明:
- 仓库: https://github.com/gnipbao/story-to-handdrawn-video —— 把中文故事/有序图片做成 3:4 竖屏、可后期配音的手绘动画
- 性质: 自然语言驱动的 **Agent Skill**（给 Codex / Claude Code / Kimi Code 用）+ Remotion 渲染器；不是只写提示词，是真出片管线（分镜→插画生成→素材处理→Remotion 导出）
- 关键能力: 默认由 Agent 生图工具同时绘插画 + 准确手写中文字，做「文字→黑白稿→彩色插画」逐层动画；或整页 + 右下角卷页翻书；327 项风格资产（75 风格 / 11 类画材 / 30 精选），含在线风格库
- 依赖: Node 20+ / Python 3.10+ / FFmpeg(含 ffprobe) / npm / Chrome；生成图片需 Agent 可调用的生图工具（即梦/Dreamina 或类似）
- 与 awesome-seedance 的关系: seedance 只写视频提示词（不动手绘），此仓是真·手绘风出片流水线；做"手绘风格视频"优先调此条
- 触发用法: 用户说"做手绘风格视频 / 手绘动画"时从知识库调出此条
- 后续动作（未做，待用户明确）: 是否 clone 到本地 / 装成 Hermes skill 待定；当前仅登记地址备查

---

## [2026-09-23] bookmark | gnipbao/story-to-handdrawn-video 手绘视频 Agent Skill 登记
来源: 用户提供的仓库 https://github.com/gnipbao/story-to-handdrawn-video ；用户说"记到知识库，后续做视频手绘画风格可以用上"
Pages affected:
- wiki/bookmarks/bookmarks-2026-08-09.md (updated): 「AI/LLM 学习」节 skills 仓库群（awesome-seedance 之后）追加 1 条
- wiki/index.md: 该书签页更新日期已是 09-23（本次连带改动，无需再改）

内容说明:
- 仓库: https://github.com/gnipbao/story-to-handdrawn-video —— 把中文故事/有序图片做成 3:4 竖屏、可后期配音的手绘动画
- 性质: 自然语言驱动的 **Agent Skill**（给 Codex / Claude Code / Kimi Code 用）+ Remotion 渲染器；不是只写提示词，是真出片管线（分镜→插画生成→素材处理→Remotion 导出）
- 关键能力: 默认由 Agent 生图工具同时绘插画 + 准确手写中文字，做「文字→黑白稿→彩色插画」逐层动画；或整页 + 右下角卷页翻书；327 项风格资产（75 风格 / 11 类画材 / 30 精选），含在线风格库
- 依赖: Node 20+ / Python 3.10+ / FFmpeg(含 ffprobe) / npm / Chrome；生成图片需 Agent 可调用的生图工具（即梦/Dreamina 或类似）
- 与 awesome-seedance 的关系: seedance 只写视频提示词（不动手绘），此仓是真·手绘风出片流水线；做"手绘风格视频"优先调此条
- 触发用法: 用户说"做手绘风格视频 / 手绘动画"时从知识库调出此条
- 后续动作（未做，待用户明确）: 是否 clone 到本地 / 装成 Hermes skill 待定；当前仅登记地址备查
