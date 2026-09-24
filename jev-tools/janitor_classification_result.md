# jev-the-janitor 实测分类结果（108 篇自有笔记）

数据来源：同一批 108 篇笔记，离线玩具规则（offline） vs 真 Jev（live，TYPESAFE key）各跑一遍。原库未改动。

## 一、真 Jev 全部分桶分布（108 篇）

- durable_memory：60 篇
- log_entry：20 篇
- needs_review：7 篇
- project_decision：6 篇
- code_note：6 篇
- ephemeral：5 篇
- reference：4 篇

共 108 篇，其中 **62 篇被真 Jev 重新分类**（离线规则判错/过粗）。

## 二、被重新分类的 62 篇（离线桶 → 真 Jev 桶）

| # | 笔记（相对 scope/ 路径） | 离线判定 | 真 Jev 判定 | 置信度 |
|---|---|---|---|---|
| 1 | mpwechat/[202608091531]用WorkBuddyCodexObsidian搭建自生长的个人知识库实战.md | reference | code_note | 0.43 |
| 2 | mpwechat/偶像的书《MAKE：初创者手册》被我用插件一分钟翻译成中英双语的电子书，真香.md | reference | code_note | 0.21 |
| 3 | mpwechat/temp_article.md | reference | durable_memory | 0.50 |
| 4 | mpwechat/挖到宝藏开源工具！一键下载优质博主的公众号文章，格式100%还原.md | reference | durable_memory | 0.55 |
| 5 | wiki/concepts/agent-as-daily-sms.md | reference | durable_memory | 0.89 |
| 6 | wiki/concepts/codex-control-bluetooth.md | reference | durable_memory | 0.59 |
| 7 | wiki/concepts/copilot-to-loop-framework.md | reference | durable_memory | 0.86 |
| 8 | wiki/concepts/daily-market-signal-md.md | reference | durable_memory | 0.91 |
| 9 | wiki/concepts/install-md-skills.md | reference | durable_memory | 0.72 |
| 10 | wiki/concepts/llm-wiki.md | reference | durable_memory | 0.87 |
| 11 | wiki/concepts/marketing-agent-loop.md | reference | durable_memory | 0.94 |
| 12 | wiki/concepts/pdf-to-markdown.md | reference | durable_memory | 0.70 |
| 13 | wiki/concepts/production-vs-tutorial-context.md | code_note | durable_memory | 0.97 |
| 14 | wiki/concepts/production-vs-tutorial-memory.md | code_note | durable_memory | 0.99 |
| 15 | wiki/concepts/voice-ramble-method.md | reference | durable_memory | 0.93 |
| 16 | wiki/topics/26-startup-directions.md | reference | durable_memory | 0.81 |
| 17 | wiki/topics/creator-ai-boundary.md | reference | durable_memory | 0.83 |
| 18 | wiki/topics/futuretools-dead-filtering.md | reference | durable_memory | 0.71 |
| 19 | wiki/topics/hardware-startup-golden-age.md | reference | durable_memory | 0.72 |
| 20 | wiki/topics/levelsio-ai-video-editor.md | reference | durable_memory | 0.76 |
| 21 | wiki/topics/llm-financial-advice.md | reference | durable_memory | 0.36 |
| 22 | wiki/topics/self-growing-kb.md | reference | durable_memory | 0.70 |
| 23 | drafts/今日内容选题.md | durable_memory | ephemeral | 0.52 |
| 24 | mpwechat/article_ai_era.md | durable_memory | ephemeral | 0.39 |
| 25 | mpwechat/花大价钱入手Screen Studio，香是真的香，惨也是真的惨.md | durable_memory | ephemeral | 0.27 |
| 26 | wiki/strategy/行动卡-本周练手.md | durable_memory | ephemeral | 0.43 |
| 27 | wiki/topics/software-not-dead-debate.md | reference | ephemeral | 0.22 |
| 28 | keep-candidates/KEEP候选-08-08.md | reference | log_entry | 0.26 |
| 29 | keep-candidates/KEEP候选-08-09.md | code_note | log_entry | 1.00 |
| 30 | keep-candidates/KEEP候选-2026-09-03.md | code_note | log_entry | 0.92 |
| 31 | keep-candidates/x-follow-feed/KEEP候选-2026-09-03.md | needs_review | log_entry | 0.92 |
| 32 | mpwechat/_INDEX.md | reference | log_entry | 0.77 |
| 33 | mpwechat/从0到1，我在Coze上打造财富测评Skill的真实历程（精简版）.md | durable_memory | log_entry | 0.34 |
| 34 | raw-collect/x-follow-feed/原始采集-2026-09-03.md | code_note | log_entry | 0.97 |
| 35 | raw-collect/原始采集-08-08.md | code_note | log_entry | 0.99 |
| 36 | raw-collect/原始采集-08-09.md | code_note | log_entry | 0.99 |
| 37 | wiki/daily/2026-09-03-AI摘要.md | durable_memory | log_entry | 1.00 |
| 38 | wiki/daily/2026-09-03-完整.md | code_note | log_entry | 1.00 |
| 39 | wiki/daily/2026-09-03.md | reference | log_entry | 1.00 |
| 40 | wiki/daily/日报-08-08.md | durable_memory | log_entry | 1.00 |
| 41 | wiki/daily/日报-08-09.md | durable_memory | log_entry | 1.00 |
| 42 | wiki/entities/emollick.md | code_note | log_entry | 0.55 |
| 43 | wiki/index.md | durable_memory | log_entry | 0.75 |
| 44 | wiki/log.md | code_note | log_entry | 1.00 |
| 45 | wiki/topics/5-solo-opportunities.md | durable_memory | log_entry | 0.55 |
| 46 | wiki/weekly/周报-2026-08-09.md | durable_memory | log_entry | 1.00 |
| 47 | wiki/整理总结.md | code_note | log_entry | 0.93 |
| 48 | wiki/entities/alex-prompter.md | durable_memory | needs_review | 0.33 |
| 49 | wiki/entities/andrewyng.md | durable_memory | needs_review | 0.25 |
| 50 | wiki/entities/claudeskills101.md | durable_memory | needs_review | 0.38 |
| 51 | wiki/entities/corbin-braun.md | durable_memory | needs_review | 0.30 |
| 52 | wiki/entities/hesamation.md | durable_memory | needs_review | 0.50 |
| 53 | wiki/entities/kloss-xyz.md | durable_memory | needs_review | 0.36 |
| 54 | wiki/entities/mardehaym.md | durable_memory | needs_review | 0.39 |
| 55 | Mem0记忆/记忆架构与多Agent共用方案.md | code_note | project_decision | 0.73 |
| 56 | strategy/多Agent共用记忆落地计划.md | durable_memory | project_decision | 0.51 |
| 57 | wiki/strategy/副业作战地图.md | durable_memory | project_decision | 0.90 |
| 58 | wiki/strategy/生产流水线搭建计划.md | code_note | project_decision | 0.96 |
| 59 | wiki/topics/10-indie-first-bucket-criteria.md | reference | project_decision | 0.62 |
| 60 | wiki/topics/ai-side-hustle-guide-product.md | durable_memory | project_decision | 0.59 |
| 61 | mpwechat/用WorkBuddy_Codex加Obsidian搭建自生长个人知识库.md | code_note | reference | 0.56 |
| 62 | wiki/bookmarks/bookmarks-2026-08-09.md | needs_review | reference | 0.48 |

## 三、全 108 篇落桶明细（真 Jev）

| # | 笔记（相对 scope/ 路径） | 真 Jev 桶 | 置信度 | 疑似泄密分 |
|---|---|---|---|---|
| 1 | Mem0记忆/wangwang-memory-mirror.md | durable_memory | 0.45 | 0.39 |
| 2 | Mem0记忆/记忆架构与多Agent共用方案.md | project_decision | 0.73 | 0.23 |
| 3 | drafts/今日内容选题.md | ephemeral | 0.52 | 0.02 |
| 4 | drafts/多Agent共用记忆-从选型到落地.md | code_note | 0.88 | 0.28 |
| 5 | keep-candidates/KEEP候选-08-08.md | log_entry | 0.26 | 0.05 |
| 6 | keep-candidates/KEEP候选-08-09.md | log_entry | 1.00 | 0.04 |
| 7 | keep-candidates/KEEP候选-2026-09-03.md | log_entry | 0.92 | 0.06 |
| 8 | keep-candidates/x-follow-feed/KEEP候选-2026-09-03.md | log_entry | 0.92 | 0.08 |
| 9 | mpwechat/# 录屏踩坑后，我最终锁定了这款Mac神器.md | durable_memory | 0.54 | 0.02 |
| 10 | mpwechat/[202608091531]用WorkBuddyCodexObsidian搭建自生长的个人知识库实战.md | code_note | 0.43 | 0.04 |
| 11 | mpwechat/[20260905230250]为什么还没有拿到第一桶金看看这10条准则.md | durable_memory | 0.60 | 0.06 |
| 12 | mpwechat/_INDEX.md | log_entry | 0.77 | 0.04 |
| 13 | mpwechat/article_ai_era.md | ephemeral | 0.39 | 0.02 |
| 14 | mpwechat/temp_article.md | durable_memory | 0.50 | 0.24 |
| 15 | mpwechat/为什么还没有拿到第一桶金-看看这10条准则.md | reference | 0.85 | 0.03 |
| 16 | mpwechat/从0到1，我在Coze上打造财富测评Skill的真实历程（精简版）.md | log_entry | 0.34 | 0.03 |
| 17 | mpwechat/偶像的书《MAKE：初创者手册》被我用插件一分钟翻译成中英双语的电子书，真香.md | code_note | 0.21 | 0.03 |
| 18 | mpwechat/发现一个超牛的chrome插件，截图+录制一键搞定.md | durable_memory | 0.75 | 0.02 |
| 19 | mpwechat/实测腾讯CodeBuddy Code：Claude Code平替，低成本解决AI封号痛点.md | code_note | 0.52 | 0.04 |
| 20 | mpwechat/我花10块钱，给自己的黄金交易配了个“顶级研究员”.md | code_note | 0.94 | 0.11 |
| 21 | mpwechat/挖到宝藏开源工具！一键下载优质博主的公众号文章，格式100%还原.md | durable_memory | 0.55 | 0.24 |
| 22 | mpwechat/用WorkBuddy_Codex加Obsidian搭建自生长个人知识库.md | reference | 0.56 | 0.03 |
| 23 | mpwechat/用了7年为知笔记，几千篇笔记导出难住我，最终靠开源工具破局.md | code_note | 0.88 | 0.11 |
| 24 | mpwechat/花大价钱入手Screen Studio，香是真的香，惨也是真的惨.md | ephemeral | 0.27 | 0.04 |
| 25 | raw-collect/x-follow-feed/原始采集-2026-09-03.md | log_entry | 0.97 | 0.06 |
| 26 | raw-collect/原始采集-08-08.md | log_entry | 0.99 | 0.07 |
| 27 | raw-collect/原始采集-08-09.md | log_entry | 0.99 | 0.08 |
| 28 | strategy/多Agent共用记忆落地计划.md | project_decision | 0.51 | 0.31 |
| 29 | wiki/bookmarks/bookmarks-2026-08-09.md | reference | 0.48 | 0.63 |
| 30 | wiki/concepts/agent-as-daily-sms.md | durable_memory | 0.89 | 0.03 |
| 31 | wiki/concepts/codex-control-bluetooth.md | durable_memory | 0.59 | 0.03 |
| 32 | wiki/concepts/copilot-to-loop-framework.md | durable_memory | 0.86 | 0.04 |
| 33 | wiki/concepts/daily-market-signal-md.md | durable_memory | 0.91 | 0.05 |
| 34 | wiki/concepts/install-md-skills.md | durable_memory | 0.72 | 0.02 |
| 35 | wiki/concepts/llm-wiki.md | durable_memory | 0.87 | 0.03 |
| 36 | wiki/concepts/marketing-agent-loop.md | durable_memory | 0.94 | 0.04 |
| 37 | wiki/concepts/pdf-to-markdown.md | durable_memory | 0.70 | 0.03 |
| 38 | wiki/concepts/production-vs-tutorial-context.md | durable_memory | 0.97 | 0.02 |
| 39 | wiki/concepts/production-vs-tutorial-memory.md | durable_memory | 0.99 | 0.02 |
| 40 | wiki/concepts/voice-ramble-method.md | durable_memory | 0.93 | 0.03 |
| 41 | wiki/daily/2026-09-03-AI摘要.md | log_entry | 1.00 | 0.03 |
| 42 | wiki/daily/2026-09-03-完整.md | log_entry | 1.00 | 0.03 |
| 43 | wiki/daily/2026-09-03.md | log_entry | 1.00 | 0.03 |
| 44 | wiki/daily/日报-08-08.md | log_entry | 1.00 | 0.06 |
| 45 | wiki/daily/日报-08-09.md | log_entry | 1.00 | 0.07 |
| 46 | wiki/entities/0x-roas.md | durable_memory | 0.69 | 0.05 |
| 47 | wiki/entities/ai-bloggers.md | durable_memory | 0.76 | 0.05 |
| 48 | wiki/entities/ai-explorer25.md | durable_memory | 0.57 | 0.05 |
| 49 | wiki/entities/ai-jasonyu.md | durable_memory | 0.85 | 0.06 |
| 50 | wiki/entities/alex-prompter.md | needs_review | 0.33 | 0.06 |
| 51 | wiki/entities/alexfinn.md | durable_memory | 0.48 | 0.05 |
| 52 | wiki/entities/amir-mushich.md | durable_memory | 0.75 | 0.04 |
| 53 | wiki/entities/andrewyng.md | needs_review | 0.25 | 0.05 |
| 54 | wiki/entities/athcanft.md | durable_memory | 0.55 | 0.05 |
| 55 | wiki/entities/claudeskills101.md | needs_review | 0.38 | 0.05 |
| 56 | wiki/entities/corbin-braun.md | needs_review | 0.30 | 0.05 |
| 57 | wiki/entities/dannypostma.md | durable_memory | 0.53 | 0.05 |
| 58 | wiki/entities/dotey.md | durable_memory | 0.88 | 0.05 |
| 59 | wiki/entities/egeberkina.md | durable_memory | 0.61 | 0.04 |
| 60 | wiki/entities/emollick.md | log_entry | 0.55 | 0.06 |
| 61 | wiki/entities/eptwts.md | durable_memory | 0.74 | 0.05 |
| 62 | wiki/entities/exm-7777.md | durable_memory | 0.70 | 0.05 |
| 63 | wiki/entities/godofprompt.md | durable_memory | 0.49 | 0.04 |
| 64 | wiki/entities/gregisenberg.md | durable_memory | 0.43 | 0.06 |
| 65 | wiki/entities/hesamation.md | needs_review | 0.50 | 0.06 |
| 66 | wiki/entities/illyism.md | durable_memory | 0.61 | 0.06 |
| 67 | wiki/entities/jackfriks.md | durable_memory | 0.73 | 0.04 |
| 68 | wiki/entities/jason23818126.md | durable_memory | 0.79 | 0.14 |
| 69 | wiki/entities/karpathy.md | durable_memory | 0.81 | 0.06 |
| 70 | wiki/entities/khazix0918.md | durable_memory | 0.85 | 0.08 |
| 71 | wiki/entities/kloss-xyz.md | needs_review | 0.36 | 0.06 |
| 72 | wiki/entities/levelsio.md | durable_memory | 0.41 | 0.05 |
| 73 | wiki/entities/lijigang.md | durable_memory | 0.77 | 0.05 |
| 74 | wiki/entities/marclou.md | durable_memory | 0.68 | 0.04 |
| 75 | wiki/entities/mardehaym.md | needs_review | 0.39 | 0.06 |
| 76 | wiki/entities/mreflow.md | durable_memory | 0.67 | 0.04 |
| 77 | wiki/entities/op7418.md | durable_memory | 0.82 | 0.06 |
| 78 | wiki/entities/rileybrown.md | durable_memory | 0.56 | 0.04 |
| 79 | wiki/entities/robj3d3.md | durable_memory | 0.55 | 0.05 |
| 80 | wiki/entities/romanbuildsaas.md | durable_memory | 0.50 | 0.04 |
| 81 | wiki/entities/simonw.md | durable_memory | 0.51 | 0.05 |
| 82 | wiki/entities/smartpigai.md | durable_memory | 0.85 | 0.07 |
| 83 | wiki/entities/steipete.md | durable_memory | 0.83 | 0.04 |
| 84 | wiki/entities/tibo-maker.md | durable_memory | 0.55 | 0.04 |
| 85 | wiki/entities/vasuman.md | durable_memory | 0.68 | 0.04 |
| 86 | wiki/entities/vista8.md | durable_memory | 0.87 | 0.04 |
| 87 | wiki/entities/wickedguro.md | durable_memory | 0.54 | 0.05 |
| 88 | wiki/entities/x-ai-accounts.md | durable_memory | 0.70 | 0.03 |
| 89 | wiki/entities/关注的AI创业公众号.md | durable_memory | 0.33 | 0.49 |
| 90 | wiki/index.md | log_entry | 0.75 | 0.07 |
| 91 | wiki/log.md | log_entry | 1.00 | 0.11 |
| 92 | wiki/sources/obsidian-llm-wiki-zi-growth.md | reference | 0.55 | 0.03 |
| 93 | wiki/strategy/副业作战地图.md | project_decision | 0.90 | 0.03 |
| 94 | wiki/strategy/生产流水线搭建计划.md | project_decision | 0.96 | 0.05 |
| 95 | wiki/strategy/行动卡-本周练手.md | ephemeral | 0.43 | 0.02 |
| 96 | wiki/topics/10-indie-first-bucket-criteria.md | project_decision | 0.62 | 0.02 |
| 97 | wiki/topics/26-startup-directions.md | durable_memory | 0.81 | 0.04 |
| 98 | wiki/topics/5-solo-opportunities.md | log_entry | 0.55 | 0.02 |
| 99 | wiki/topics/ai-side-hustle-guide-product.md | project_decision | 0.59 | 0.17 |
| 100 | wiki/topics/creator-ai-boundary.md | durable_memory | 0.83 | 0.04 |
| 101 | wiki/topics/futuretools-dead-filtering.md | durable_memory | 0.71 | 0.04 |
| 102 | wiki/topics/hardware-startup-golden-age.md | durable_memory | 0.72 | 0.04 |
| 103 | wiki/topics/levelsio-ai-video-editor.md | durable_memory | 0.76 | 0.07 |
| 104 | wiki/topics/llm-financial-advice.md | durable_memory | 0.36 | 0.05 |
| 105 | wiki/topics/self-growing-kb.md | durable_memory | 0.70 | 0.03 |
| 106 | wiki/topics/software-not-dead-debate.md | ephemeral | 0.22 | 0.05 |
| 107 | wiki/weekly/周报-2026-08-09.md | log_entry | 1.00 | 0.04 |
| 108 | wiki/整理总结.md | log_entry | 0.93 | 0.15 |