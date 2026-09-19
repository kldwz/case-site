#!/usr/bin/env python3
"""Stage 3 - generate case-miniprogram data/cases.js from curated, enriched cases.

Reads pipeline/curated_slugs.txt (one slug per line) and the ENRICHED source md in
src/content/cases/<slug>.md, then emits a faceted schema:

  id, name, headline, region, form, monetizationMode, track, revenueTier,
  monthlyRevenueRMB, monthlyRevenueText, cumulativeRMB, cumulativeText,
  launchDate, launchDateText, cover, website,
  productIntro (long), monetization (long), learned (long),
  highlights [..], metrics {..}, story

Revenue is shown in RMB: overseas $ values are converted at RATE=6.7. Domestic ¥
values are kept as-is. Undisclosed stays 未披露 (never fabricated). Output is written
to case-miniprogram/data/cases.js (+.json). No truncation of long text.
"""
import os, re, glob, json
from collections import Counter

CASE_SITE = "/Users/hxw/codebuddy/case-site"
MINI = "/Users/hxw/codebuddy/case-miniprogram"
SITE_BASE = "https://kldwz.github.io/case-site"
PLACEHOLDER = "/case-site/cases/_placeholder/site.png"
RATE = 6.7  # 1 USD ≈ ¥6.7 (actual rate requested by user)

# canonical facet option order (UI uses these for stable display)
FORMS = ["App", "网站·Web工具", "浏览器插件", "小程序", "开源项目", "数字内容·游戏"]
MODES = ["订阅制SaaS", "一次性买断", "付费下载·内购", "免费+广告",
         "捐赠·开源赞助", "开源+商业版", "电商·带货", "知识付费", "未披露"]
TRACKS = ["AI工具", "开发者工具", "设计创意", "效率办公", "内容媒体",
          "电商带货", "教育培训", "游戏娱乐", "健康生活", "金融投资", "其他"]
TIERS = ["高", "中", "低", "未披露"]

def fm_and_body(txt):
    m = re.match(r"^(---\n.*?\n---\n?)(.*)$", txt, re.S)
    if not m:
        return {}, txt
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body

def section(body, title):
    m = re.search(r"##\s*" + re.escape(title) + r"\s*\n(.*?)(?=\n##\s|\Z)", body, re.S)
    return m.group(1).strip() if m else ""

def paras(text):
    out = []
    for blk in re.split(r"\n\s*\n", text):
        blk = blk.strip()
        if blk:
            out.append(re.sub(r"\s+", " ", blk))
    return out

def clean(s):
    return re.sub(r"\s+", " ", (s or "")).strip()

def to_paragraphs(text, group=2):
    """Split a Chinese prose blob into readable paragraphs (group N sentences)."""
    text = clean(text)
    if not text:
        return []
    raw = re.split(r"(?<=[。！？])", text)
    sents = [x.strip() for x in raw if x and x.strip()]
    out, buf = [], []
    for i, x in enumerate(sents):
        buf.append(x)
        if len(buf) >= group or i == len(sents) - 1:
            out.append("".join(buf))
            buf = []
    return out

def parse_highlights(text):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^[①②③④⑤⑥⑦⑧⑨⑩\s\-–—·.]*", "", line)
        line = re.sub(r"^\d+[.、]\s*", "", line)
        line = clean(line)
        if not line:
            continue
        # split combos like "a ② b ③ c" into separate bullets
        for part in re.split(r"\s*[②③④⑤⑥⑦⑧⑨⑩]\s*", line):
            part = clean(part)
            if part:
                out.append(part)
    return out

DATE_RE = re.compile(r"(20\d{2})[-/年.](\d{1,2})(?:[-/月.](\d{1,2}))?")
def launch_date(fm):
    for field in ("平台数据", "创始人地区"):
        m = re.search(r"(?:创立|成立|上架|上线|发布)[^0-9]*" + DATE_RE.pattern,
                      " " + fm.get(field, ""))
        if m:
            y, mo, d = m.group(1), int(m.group(2)), int(m.group(3) or 1)
            return int(f"{y}{mo:02d}{d:02d}"), f"{y}-{mo:02d}"
    return 0, ""

def parse_usd(s):
    m = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", s)
    return float(m.group(1).replace(",", "")) if m else None

def parse_rmb(s):
    # handles ¥12,345 / ¥5万 / ¥3.2万
    m = re.search(r"¥\s*([\d,]+(?:\.\d+)?)\s*万?", s)
    if not m:
        return None
    v = float(m.group(1).replace(",", ""))
    if "万" in m.group(0):
        v *= 10000
    return v

def monthly(s):
    """Return (rmb_number, tier)."""
    if not s:
        return 0, "未披露"
    if s.startswith("$"):
        usd = parse_usd(s)
        if usd is None:
            return 0, "未披露"
        rmb = usd * RATE
        if rmb >= 67000:
            tier = "高"
        elif rmb >= 6700:
            tier = "中"
        else:
            tier = "低"
        return round(rmb), tier
    if "¥" in s:
        rmb = parse_rmb(s)
        if rmb is None:
            return 0, "未披露"
        if rmb >= 67000:
            tier = "高"
        elif rmb >= 6700:
            tier = "中"
        else:
            tier = "低"
        return round(rmb), tier
    if any(k in s for k in ("未披露", "未官方披露", "未公开", "无收入")):
        return 0, "未披露"
    return 0, "未披露"

def cumulative(fm):
    blob = fm.get("平台数据", "")
    m = re.search(r"累计营收\s*\$?\s*([\d,]+(?:\.\d+)?)", blob)
    if m:
        return round(float(m.group(1).replace(",", "")) * RATE)
    m = re.search(r"累计营收[^\d¥]*¥\s*([\d,]+(?:\.\d+)?)\s*万?", blob)
    if m:
        v = float(m.group(1).replace(",", "")) * (10000 if "万" in m.group(0) else 1)
        return round(v)
    return 0

def subscribers(fm):
    blob = fm.get("平台数据", "")
    for label in ("活跃订阅", "付费订阅", "付费用户", "活跃用户", "订阅用户", "MAU", "月活", "注册用户"):
        m = re.search(label + r"\s*[:：]?\s*([\d,]+(?:\.\d+)?)\s*(万|千|k|K)?", blob)
        if m:
            v = float(m.group(1).replace(",", ""))
            unit = m.group(2)
            if unit == "万":
                v *= 10000
            elif unit in ("千", "k", "K"):
                v *= 1000
            return round(v), label
    return 0, ""

def classify_form(fm):
    cats = fm.get("分类", "")
    typ = fm.get("类型", "")
    low = cats.lower()
    if typ == "开源变现" or "开源" in cats:
        return "开源项目"
    if "插件" in cats or "扩展" in cats or "extension" in low or "chrome" in low:
        return "浏览器插件"
    if "小程序" in cats:
        return "小程序"
    if "游戏" in cats or "数字内容" in cats or "素材" in cats or "模板" in cats:
        return "数字内容·游戏"
    if any(k in cats for k in ("网站", "网页", "web", "saas")):
        return "网站·Web工具"
    return "App"

def classify_mode(fm):
    rev = fm.get("营收模式", "")
    cats = fm.get("分类", "")
    low = (rev + " " + cats).lower()
    if "捐赠" in rev or "赞助" in rev or "开源赞助" in rev:
        return "捐赠·开源赞助"
    if "买断" in rev or "one-time" in low or "一次性" in rev:
        return "一次性买断"
    if "内购" in low or "in-app" in low or "应用内" in rev:
        return "付费下载·内购"
    if "订阅" in rev or "subscription" in low or "月费" in rev or "会员" in rev or "saas" in low:
        return "订阅制SaaS"
    if "广告" in rev or "ad " in low or "ads" in low:
        return "免费+广告"
    if "电商" in cats or "带货" in cats or "shop" in low or "store" in low:
        return "电商·带货"
    if "知识付费" in cats or "课程" in cats or "教育" in cats:
        return "知识付费"
    if "付费下载" in cats or "付费下载" in rev:
        return "付费下载·内购"
    if "未披露" in rev or "未官方披露" in rev:
        # try infer from category even if revenue undisclosed
        if "免费+内购" in cats:
            return "付费下载·内购"
        if "付费下载" in cats:
            return "付费下载·内购"
        return "未披露"
    return "未披露"

TRACK_KW = [
    ("AI工具", ["ai", "llm", "人工智能", "机器学习", "gpt"]),
    ("开发者工具", ["dev tools", "开发", "开发者", "编程", "api", "代码", "saas"]),
    ("设计创意", ["设计", "design", "创意", "素材", "模板", "图片", "摄影", "视频编辑", "插画"]),
    ("效率办公", ["效率", "productivity", "办公", "笔记", "任务", "日历", "写作", "自动化"]),
    ("内容媒体", ["内容", "媒体", "博客", "新闻", "视频", "播客", "社区", "资讯"]),
    ("电商带货", ["电商", "带货", "shop", "store", "零售", "二手", "购物"]),
    ("教育培训", ["教育", "学习", "课程", "语言", "考试", "培训", "背单词"]),
    ("游戏娱乐", ["游戏", "game", "娱乐", "漫画"]),
    ("健康生活", ["健康", "医疗", "健身", "运动", "生活", "饮食", "睡眠", "心理"]),
    ("金融投资", ["金融", "投资", "理财", "股票", "基金", "保险", "加密", "钱包"]),
]
def classify_track(fm):
    cats = fm.get("分类", "").lower()
    name = fm.get("name", "").lower()
    blob = cats + " " + name
    for track, kws in TRACK_KW:
        if any(k in blob for k in kws):
            return track
    return "其他"

def fmt_rmb(n):
    return "¥" + format(n, ",d")

def main():
    slugs = [s.strip() for s in open(os.path.join(CASE_SITE, "pipeline/curated_slugs.txt"), encoding="utf-8") if s.strip()]
    rows = []
    for slug in slugs:
        f = os.path.join(CASE_SITE, "src/content/cases", slug + ".md")
        if not os.path.exists(f):
            print("MISSING", slug); continue
        fm, body = fm_and_body(open(f, encoding="utf-8").read())
        name = fm.get("name", "")
        if not name:
            continue
        region = "国内" if (fm.get("类型", "") == "国内实践" or "国内" in fm.get("分类", "")) else "国外"
        rev = fm.get("月收入估算", "")
        rmb, tier = monthly(rev)
        cum = cumulative(fm)
        u, ulabel = subscribers(fm)
        ld, ldtext = launch_date(fm)
        headline = clean(fm.get("一句话", "")) or (paras(section(body, "产品是什么"))[0][:40] if paras(section(body, "产品是什么")) else name)

        cover_field = fm.get("封面", "")
        cover = ""
        if cover_field and cover_field != PLACEHOLDER and "/case-site/cases/" in cover_field:
            sdir = cover_field.split("/case-site/cases/")[1].split("/")[0]
            d = os.path.join(CASE_SITE, "public", "cases", sdir)
            if os.path.exists(os.path.join(d, "site.png")):
                cover = f"{SITE_BASE}/cases/{sdir}/site.png"
            elif os.path.exists(os.path.join(d, "site.webp")):
                cover = f"{SITE_BASE}/cases/{sdir}/site.webp"

        metrics = {}
        for k in ("营收模式", "流量来源", "平台数据", "证据等级"):
            if fm.get(k):
                metrics[k] = clean(fm[k])

        intro_paras = []
        for _sec in ("产品是什么", "站长是谁", "怎么赚的钱"):
            intro_paras.extend(to_paragraphs(section(body, _sec), 2))
        lesson_paras = to_paragraphs(section(body, "这个案例能学到什么"), 2)
        facts = [{"k": k, "v": metrics[k]} for k in ("流量来源", "证据等级") if metrics.get(k)]

        rows.append({
            "id": slug,
            "name": name,
            "headline": headline[:42],
            "region": region,
            "form": classify_form(fm),
            "monetizationMode": classify_mode(fm),
            "track": classify_track(fm),
            "revenueTier": tier,
            "monthlyRevenueRMB": rmb,
            "monthlyRevenueText": fmt_rmb(rmb) + "/月" if rmb else "未披露",
            "cumulativeRMB": cum,
            "cumulativeText": ("累计 " + fmt_rmb(cum)) if cum else "",
            "cumulativeShort": fmt_rmb(cum) if cum else "",
            "users": u,
            "usersText": format(u, ",d") if u else "",
            "usersLabel": ulabel if u else "",
            "launchDate": ld,
            "launchDateText": ldtext,
            "cover": cover,
            "website": clean(fm.get("原文链接", "")),
            "intro": intro_paras,
            "tactics": parse_highlights(fm.get("可迁移点", "")),
            "lessons": lesson_paras,
            "facts": facts,
        })

    js_path = os.path.join(MINI, "data/cases.js")
    json_path = os.path.join(MINI, "data/cases.json")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("module.exports = ")
        json.dump(rows, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)

    size = os.path.getsize(js_path)
    print(f"wrote {len(rows)} cases -> {js_path}")
    print(f"size: {size/1024/1024:.2f} MB (limit 2.00 MB)")
    print("region:", dict(Counter(r["region"] for r in rows)))
    print("form:", dict(Counter(r["form"] for r in rows)))
    print("mode:", dict(Counter(r["monetizationMode"] for r in rows)))
    print("track:", dict(Counter(r["track"] for r in rows)))
    print("tier:", dict(Counter(r["revenueTier"] for r in rows)))
    # integrity checks
    short_intro = [r["id"] for r in rows if sum(len(p) for p in r["intro"]) < 200]
    print("intro total <200:", short_intro)
    nopara = [r["id"] for r in rows if len(r["intro"]) < 2]
    print("intro <2 paragraphs:", nopara)
    nofacts = [r["id"] for r in rows if not r["facts"]]
    print("no facts:", nofacts)
    print("launchDate==0:", [r["id"] for r in rows if r["launchDate"] == 0])

if __name__ == "__main__":
    main()
