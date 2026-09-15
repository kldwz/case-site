#!/usr/bin/env python3
# gen_oss_case.py - 用 SiliconFlow deepseek-v3 生成「开源变现」案例 .md
# 输入: pipeline/oss_facts.json  (已核实/标注 provenance 的事实)
# 输出: src/content/cases/<slug>.md
# 约束: 只使用提供的事实，绝不编造数字；未知标 未官方披露/第三方估算。
import json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS = os.path.join(ROOT, "pipeline", "oss_facts.json")
OUT = os.path.join(ROOT, "src", "content", "cases")
os.makedirs(OUT, exist_ok=True)

SF_URL = os.environ.get("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1")
SF_KEY = os.environ.get("OPENAI_API_KEY")
SF_MODEL = "deepseek-ai/DeepSeek-V3"

SYSTEM = """你是一个中文「独立开发者/开源项目收入案例库」的资深编辑。你只负责把已核实的事实，组织成结构严谨、可读性强的中文案例文章。

铁律（违反任何一条都会毁掉案例可信度，必须严格遵守）：
- 只能使用用户提供的「事实清单」里的信息。事实清单之外，严禁补充任何具体数字、人物背景细节、社区规模（如 Discord/论坛人数）、第三方流量/访问量估算、客户或集成方名称、百分比。
- 事实清单里没有的数字，必须写成「未官方披露」或「第三方估算」（并注明来源性质），严禁给出精确假数字。
- 想写「社区活跃」「文档完善」「被开发者广泛使用」这类概括可以，但绝不能给未提供的精确数字（如「3.5万成员」「年访问百万」「98%用户」）。
- 人物背景只写事实清单里给的 founder/region/founded，不要编造履历（如「曾为政府构建数据库」「多年优化经验」）。
- 行文给中国普通开发者/创业者看，具体、有产品细节、有判断，但所有具体claims必须来自事实清单。
- frontmatter 的每个值都不要以英文双引号开头（避免 YAML 解析出错）。
- 严格按给定结构输出，包含 YAML frontmatter（用 --- 包裹）和正文。"""

def build_user(f):
    slug = f["slug"]
    facts_block = "\n".join(f"- {k}: {v}" for k, v in f.items() if k != "lessons" and k != "sources")
    lessons = "\n".join(f"  - {l}" for l in f["lessons"])
    sources = "\n".join(f"  - {s}" for s in f["sources"])
    return f"""请为下面的开源变现案例生成完整文章（frontmatter + 正文）。

## 事实清单（全部来自公开可查证来源，未标注的不要瞎写）
{facts_block}
- lessons(可迁移点要点):
{lessons}
- sources(来源链接):
{sources}

## 必输结构

YAML frontmatter（字段顺序如下，值不要以双引号开头）：
---
name: {f['name']}
一句话: <30字内，讲清靠什么赚钱>
创始人地区: <创始人 + 地区 + 创办年份>
营收模式: <怎么赚钱，拆解商业模式，2-3句>
月收入估算: <ARR/月收入；有来源写来源，无写 未官方披露>
流量来源: <80-120字，开源仓库如何当漏斗、社区/文档/内容怎么供应用户>
可迁移点: <把 lessons 写成 ①…②…③…④… 一行内联，每条简短>
原文链接: {f['site']}
数据口径: <说明数据来自哪里：官方博客/pricing/融资公告/GitHub；含抓取日期 2026-09-15>
分类: <赛道 / 开源+订阅 / 英文 或 中文>
类型: 开源变现
证据等级: <官方披露 / 平台数据可查 / 第三方估算 / 作者自述 之一，按事实可信度选>
平台数据: <{f['github_note']}。若含 __GH__ 占位符则原样保留 __GH__>
封面: /case-site/cases/{slug}/site.png
---

正文（带 h2 小标题，和示例同风格）：
![<name> 官网](/cases/{slug}/site.png)

# <name>：<一句抓人的副标题，讲清它靠什么赚钱/做到了什么>

## 产品是什么
（120-180字，讲普通人怎么用，点出对标谁、核心能力，可引用平台数据里的 star 数）

## 怎么赚的钱
（拆解商业模式：免费自托管/开源版 vs 云托管/订阅/企业版/白标，分别怎么收钱；融资轮次与金额来自事实清单，不确定标 未官方披露）

## 流量从哪来
（开源仓库即漏斗 + 文档/社区/模板/Discord/内容 等真实获客方式）

## 站长是谁
（创始人背景、为什么是他做成；用事实清单里的 founder/region/founded）

## 这个案例能学到什么
（把 lessons 展开成 ① ② ③ ④ 每条 1-2 句带判断的要点）

## 来源与数据
（列出 sources 里的链接，注明数据口径与抓取日期 2026-09-15）

## 一句话总结
> <一句有态度的总结，引用块>

重要：再次强调，正文中任何具体数字、社区规模、人物履历、第三方数据，若不在事实清单里，一律不写，用概括措辞代替或标 未官方披露。绝不给未提供的精确数字。

只输出文章本身，不要任何额外说明，不要 markdown 代码围栏。"""

def call_llm(user):
    body = json.dumps({
        "model": SF_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user}
        ],
        "max_tokens": 4000,
        "temperature": 0.7,
        "stream": False
    }).encode("utf-8")
    req = urllib.request.Request(SF_URL + "/chat/completions",
        data=body, headers={
            "Authorization": "Bearer " + SF_KEY,
            "Content-Type": "application/json"
        })
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]

def strip_fence(s):
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\n?", "", s)
        s = re.sub(r"\n?```$", "", s)
    return s.strip()

def main():
    only = sys.argv[1:] or None
    facts = json.load(open(FACTS, encoding="utf-8"))
    for f in facts:
        if only and f["slug"] not in only:
            continue
        print(f"== generating {f['slug']} ==")
        user = build_user(f)
        try:
            txt = strip_fence(call_llm(user))
        except Exception as e:
            print(f"  !! LLM 失败: {e}")
            continue
        if not txt.startswith("---"):
            print(f"  !! 输出缺少 frontmatter，跳过。前80字: {txt[:80]}")
            # 存草稿以便检查
            open(os.path.join(OUT, f["slug"] + ".draft.md"), "w").write(txt)
            continue
        path = os.path.join(OUT, f["slug"] + ".md")
        open(path, "w", encoding="utf-8").write(txt + "\n")
        print(f"  -> wrote {path} ({len(txt)} chars)")

if __name__ == "__main__":
    main()
