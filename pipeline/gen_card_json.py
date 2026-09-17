import os, sys, json, time, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trustmrr_common import parse_md
import gen_trustmrr as g

API_URL = g.API_URL
API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = "deepseek-ai/DeepSeek-V3"
PROXY = getattr(g, "PROXY", "")

PUBLIC = "/Users/hxw/codebuddy/case-site/public/cases"
SITE = "https://kldwz.github.io/case-site"
OUT = "/Users/hxw/codebuddy/case-miniprogram/data/cases.json"
N = 10

SYSTEM = (
    "你是一位给「想搞副业/创业的普通人」写案例拆解的中文内容编辑，"
    "文风接地气、有画面感、像在讲故事，但不要浮夸。只输出严格的 JSON，不要任何解释。"
)


def call_json(prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 1400,
        "temperature": 0.6,
        "response_format": {"type": "json_object"},
    }
    last = None
    for via in (False, True):
        try:
            handlers = []
            if via and PROXY:
                from urllib.request import ProxyHandler
                handlers.append(ProxyHandler({"https": PROXY, "http": PROXY}))
            opener = urllib.request.build_opener(*handlers)
            req = urllib.request.Request(
                API_URL,
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json",
                         "Authorization": "Bearer " + API_KEY},
            )
            with opener.open(req, timeout=60) as r:
                resp = json.loads(r.read())
            return json.loads(resp["choices"][0]["message"]["content"])
        except Exception as e:  # noqa
            last = e
            continue
    raise last


def monthly(facts):
    for k in ("rev_30d", "mrr"):
        v = facts.get(k) or 0
        if v > 0:
            return float(v)
    a = facts.get("rev_all") or 0
    return a / 12.0 if a > 0 else 0.0


def fmt_money(usd):
    if usd <= 0:
        return "未披露"
    if usd >= 10000:
        return "$" + format(usd / 10000, ".1f") + "万/月"
    return "$" + format(usd, ",.0f") + "/月"


USER_TMPL = """下面是国外一个真实副业/独立产品的数据，请你基于这些事实，写一套适合放进「副业案例小程序」的优美中文内容。

【产品事实】
- 名称：{name}
- 一句话描述：{description}
- 官网：{website}
- 国家：{country}
- 成立时间：{founded}
- 创始人：{founder}
- 月收入（估算）：{mrev}
- 年营收/累计：{rev_all}
- 定价模式：{pricing}
- 受众：{audience}
- 解决的问题：{problem}
- 价值主张：{value_prop}
- 流量/SEO：DR={dr}，粉丝={x_followers}

【要求】
请用 JSON 输出以下字段（字段名严格如下，值用中文）：
- "headline": 一句话（不超过 22 字），让人一眼看懂「这是什么 + 赚多少」，例如「Notion 平替，月入 $4.2万」
- "type": 用 2-4 字判断形态，从{{网站/浏览器插件/App/小程序/独立站/SaaS/工具/课程/社群/模板}}里选最贴切的一个
- "category": 2-6 字分类，例如「AI 工具」「设计素材」「效率」「电商」「写作」
- "summary": 2 句话的吸引人摘要（60 字内），说清它帮谁解决了什么
- "highlights": 数组，3 条「关键打法/看点」，每条 15-25 字，像是给副业者的经验
- "story": 数组，3 个段落，每段 2-3 句，像在讲故事（背景→怎么做的→结果），生动但真实，不要编造事实
- "takeaway": 1 句话给想搞副业的人的启发（30 字内）
- "tags": 数组，3-5 个短标签（如「AI」「出海」「SEO」「独立开发」）

只输出 JSON。"""

# ---- 选 10 条：有真实封面 + 有月收入，按收入降序 ----
existing = {f[:-3] for f in os.listdir(g.CASES_DIR) if f.endswith(".md")}
cands = []
for slug in existing:
    cover = os.path.join(PUBLIC, slug, "site.webp")
    if not os.path.exists(cover):
        continue
    try:
        facts = parse_md(os.path.join(g.CACHE_DIR, slug + ".md"))
    except Exception:
        continue
    m = monthly(facts)
    if m <= 0:
        continue
    cands.append((m, slug, facts))
cands.sort(reverse=True)
picks = [(s, f) for _, s, f in cands[:N]]
print("selected", len(picks), "candidates, top revenue:",
      [round(monthly(f)) for _, f in picks], flush=True)

results = []
for slug, facts in picks:
    mrev = monthly(facts)
    prompt = USER_TMPL.format(
        name=facts.get("name", ""),
        description=facts.get("description", ""),
        website=facts.get("website", ""),
        country=facts.get("country", ""),
        founded=facts.get("founded", ""),
        founder=facts.get("founder", ""),
        mrev=fmt_money(mrev),
        rev_all=facts.get("rev_all", 0),
        pricing=facts.get("pricing", ""),
        audience=facts.get("audience", ""),
        problem=facts.get("problem", ""),
        value_prop=facts.get("value_prop", ""),
        dr=facts.get("dr", ""),
        x_followers=facts.get("x_followers", ""),
    )
    data = call_json(prompt)
    cover_url = SITE + "/cases/" + slug + "/site.webp"
    metrics = {
        "月收入": fmt_money(mrev),
        "年营收/累计": ("$" + format(facts.get("rev_all", 0), ",.0f")) if facts.get("rev_all") else "未披露",
        "DR": str(facts.get("dr", "")) or "未披露",
        "成立": str(facts.get("founded", "")) or "未披露",
        "定价": str(facts.get("pricing", "")) or "未披露",
        "X 粉丝": str(facts.get("x_followers", "")) or "未披露",
    }
    obj = {
        "id": slug,
        "name": facts.get("name", ""),
        "headline": data.get("headline", ""),
        "type": data.get("type", "独立产品"),
        "region": "国外",
        "category": data.get("category", ""),
        "platform": facts.get("payment_provider", "") or "",
        "monthlyRevenue": round(mrev),
        "monthlyRevenueText": fmt_money(mrev),
        "summary": data.get("summary", ""),
        "highlights": data.get("highlights", []),
        "metrics": metrics,
        "story": data.get("story", []),
        "takeaway": data.get("takeaway", ""),
        "cover": cover_url,
        "website": facts.get("website", ""),
        "tags": data.get("tags", []),
    }
    results.append(obj)
    print("ok", slug, "-", obj["headline"], flush=True)
    time.sleep(1.5)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("WROTE", len(results), "cases ->", OUT, flush=True)
