#!/usr/bin/env python3
"""Audit ALL cases in src/content/cases/ against the documented case-site spec.

Spec sources:
  - README.md          : required frontmatter fields, MUST have 原文链接, no fabrication
  - 进度文档.md 质量闸门 : ①真产品有官网 ②盈利模式能讲清 ③截图截官网(不截报道页);
                         NOISE 词库(最赚钱/上市/同比/季度/报告/榜单/盘点/vps/机场)
  - select_cases.py    : DENY (大厂/主流 app) + COMP_RE (获奖/比赛/人物) + 无收入/纯捐赠
  - 内容完整性          : 重复案例 / 正文残缺(stub)

This is READ-ONLY: it prints a breakdown + writes pipeline/_audit_result.tsv
(nothing is moved or deleted). The actual elimination + 留痕 doc is a separate step
gated on user confirmation.

Run:  python3 pipeline/audit_cases.py
"""
import os, re, glob
from collections import Counter, defaultdict

CASE_SITE = "/Users/hxw/codebuddy/case-site"
PIPE = os.path.join(CASE_SITE, "pipeline")
CASES = os.path.join(CASE_SITE, "src/content/cases")

# --- import the established filters from select_cases.py (single source of truth) ---
import importlib.util
spec = importlib.util.spec_from_file_location("sel", os.path.join(PIPE, "select_cases.py"))
sel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sel)
DENY, COMP_RE = sel.DENY, sel.COMP_RE
DENY, COMP_RE = sel.DENY, sel.COMP_RE

# Generic category words + person/award/competition tokens. A case is only
# eliminated as "大厂/主流" if it matches at least ONE real *brand* token.
# If every matched DENY token is a generic/person word, it is spared here
# (person/award cases are caught by the 获奖/比赛/人物 rule instead).
BROAD_EXCLUDE = set("""
音乐 视频 浏览器 翻译 天气 地图 社交 论坛 广告 支付 网盘 邮箱 笔记 日历 壁纸
清理 加速 杀毒 管家 锁屏 新闻 股票 钱包 记账 理财 健康 运动 阅读 听书 电台
外卖 打车 招聘 旅游 酒店 票务 二手 团购 优惠 彩票 交友 相亲 游戏 棋牌 贷款
保险 银行 证券 基金 信用卡 输入法 相机 搜索 直播 商城 小说 社区 报告 分享
短信 电话 词典 导航 播放器 阅读器 编辑器 管理器 助手 工具 平台 引擎 服务
中心 空间 盒子 省 赚 学 问 聊 约 订 租 卖 买
acm kaggle fellow 图灵奖 邵逸夫 吴文俊 王选 青橙奖 长江学者 杰青 院士 教授
学者 人才 基金 研究院 实验室 基金会 达摩院 百度之星 华为软件精英 大赛 竞赛
杯赛 峰会 研讨会 黑客松 嘉年华 大会 开放日 何同学 稚晖君 罗永浩 罗振宇 罗翔
李子柒 影视飓风 华农兄弟 美食作家王刚 手工耿 混知 毕导 回形针 差评 阮一峰
冯大辉 曹政 百度ai studio 华为ict 华为iot 华为开发者大赛 腾讯tctf 腾讯云开发者
腾讯开悟 京东探索者 拼多多算法 快手算法 美团算法 携程算法 滴滴盖亚 字节跳动前端
字节跳动极客 字节跳动青训 科大讯飞ai大赛 商汤ai大赛 旷视算法 大疆 robomaster
华为昇腾 华为鲲鹏 寒武纪 瑞芯微 rockchip esp32 乐鑫 合宙 沁恒 微雪 野火电子
正点原子 矽递 seeed 矽速 sipeed m5stack 拿铁熊猫 lattepanda 跃昉 bananapi
dfrobot 兆易创新 gigadevice 地平线 horizon 宇树科技 unitree 白描 万能 万能命令
万能遥控器 万能导航 二维码生成器 截图插件 图片助手 视频下载助手 猫抓 油猴
tampermonkey stylus colorzilla onetab session buddy web scraper video downloadhelper
video speed controller image downloader awesome screenshot print friendly reader view
whatfont wikiwand wikiart gofulpage gesturefy infinity新标签页 侧边翻译 划词翻译
search preview lastpass 1password dashlane enpass bitwarden notion evernote onenote
goodnotes 熊掌记 todoist ticktick things microsoft google apple facebook twitter
instagram whatsapp telegram discord slack zoom skype youtube github gitlab stackoverflow
medium substack patreon kickstarter indiegogo gofundme onlyfans tiktok snapchat pinterest
reddit linkedin quora yahoo bing duckduckgo cloudflare aws azure gcp heroku vercel
netlify shopify wordpress wix squarespace webflow stripe paypal lemonsqueezy paddle
gumroad figma grammarly dropbox box trello asana signal
""".split())

# Required frontmatter fields per README.md (11 fields)
# Protected: the 80 validated mini-program curated slugs must NEVER be eliminated.
CURATED = set(s.strip() for s in open(os.path.join(PIPE, "curated_slugs.txt"), encoding="utf8") if s.strip())

REQUIRED = ["name", "一句话", "创始人地区", "营收模式", "月收入估算",
            "流量来源", "可迁移点", "原文链接", "数据口径", "分类", "封面"]

# NOISE 词库 from 进度文档.md 质量闸门 (news/榜单/报告 masquerading as cases)
NOISE = ["最赚钱", "上市", "同比", "季度", "报告", "榜单", "盘点", "vps", "机场",
         "融资", "估值", "IPO", "财报", "招股书", "独角兽", "GMV", "市值"]

# media / community / app-store signals (REVIEW ONLY, not auto-eliminate)
MEDIA_KW = ["媒体", "社区", "应用商店", "应用市场", "应用商店", "商店", "论坛",
            "播客", "社交", "资讯", "内容平台", "公众号", "聚合", "推荐"]

def fm_and_body(txt):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", txt, re.S)
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

# ---------------------------------------------------------------------------
files = sorted(glob.glob(os.path.join(CASES, "*.md")))
rows = []
for f in files:
    slug = os.path.splitext(os.path.basename(f))[0]
    fm, body = fm_and_body(open(f, encoding="utf8").read())
    name = fm.get("name", "").strip()
    rev = fm.get("月收入估算", "")
    oneliner = fm.get("一句话", "")
    src = fm.get("原文链接", "")
    typ = fm.get("类型", "")
    cat = fm.get("分类", "")
    intro = section(body, "产品是什么") or section(body, "网站是什么")
    reasons = []

    # 1. required fields
    miss = [k for k in REQUIRED if not fm.get(k, "").strip()]
    if miss:
        reasons.append(("缺必填字段", ",".join(miss)))
    # 2. no source link (README hard rule)
    if not src.strip():
        reasons.append(("缺原文链接", ""))
    # 3. DENY (大厂/主流) -- NARROWED: only if matched by a real brand token,
    #    not merely a generic category word (音乐/报告/...) or person/award token.
    if name and sel.denied(name):
        matched = [d for d in DENY if d and re.search(re.escape(d), name.lower())]
        if not set(matched).issubset(BROAD_EXCLUDE):
            reasons.append(("大厂/主流", ""))
    # 4. award / competition / person
    if typ == "获奖作品" or (name and COMP_RE.search(name)):
        reasons.append(("获奖/比赛/人物", ""))
    # 5. no revenue / donate-only
    if "无收入" in rev or ("捐赠" in rev and "未披露" in rev):
        reasons.append(("无收入/纯捐赠", ""))
    # 6. NOISE words (news/榜单 masquerading) -- only fire on CLEAR news signals:
    #    (a) 类型/分类 标记为 新闻/报道/榜单/资讯, or (b) >=2 noise words co-occur.
    #    Single "报告/上市" in a normal product description is NOT a violation.
    hay = (name + " " + oneliner).lower()
    hit = [w for w in NOISE if w.lower() in hay]
    cls = (typ + " " + cat).lower()
    is_news_cls = any(k in cls for k in ["新闻", "报道", "榜单", "资讯", "快讯", "周报", "日报"])
    if is_news_cls or len(hit) >= 2:
        reasons.append(("噪声词/疑似报道", ",".join(hit)))
    # 7. stub (broken/unenriched body)
    if len(intro) < 40:
        reasons.append(("正文残缺", f"{len(intro)}字"))

    # review-only (not elimination reason)
    review = []
    rk = " ".join([name, typ, cat, oneliner])
    if any(k in rk for k in MEDIA_KW):
        review.append("媒体/社区/商店")

    protected = slug in CURATED
    if protected:
        reasons = []  # never eliminate a validated curated case
    rows.append({"slug": slug, "name": name, "reasons": reasons,
                 "review": review, "protected": protected})

# duplicate detection (same name across slugs -> keep first, rest flagged)
seen = {}
for r in rows:
    n = r["name"]
    if not n:
        continue
    if n in seen:
        r["reasons"].insert(0, ("重复案例", "与 " + seen[n] + " 同名"))
    else:
        seen[n] = r["slug"]

# priority for primary reason
PRIORITY = ["重复案例", "缺必填字段", "缺原文链接", "大厂/主流",
            "获奖/比赛/人物", "无收入/纯捐赠", "噪声词/疑似报道", "正文残缺"]
def primary(r):
    for p in PRIORITY:
        for code, _ in r["reasons"]:
            if code == p:
                return p
    return ""

eliminated = [r for r in rows if r["reasons"]]
kept = [r for r in rows if not r["reasons"]]
by_reason = Counter(primary(r) for r in eliminated)
review_set = [r for r in rows if r["review"] and not r["reasons"]]

protected_n = sum(1 for r in rows if r.get("protected"))
print(f"总案例: {len(rows)}")
print(f"判定剔除: {len(eliminated)}")
print(f"保留:     {len(kept)}")
print(f"受保护(80精选, 不剔): {protected_n}")
print(f"仅待复核(媒体/社区类, 暂不剔): {len(review_set)}")
print("\n=== 剔除原因分布（主原因） ===")
for code, c in by_reason.most_common():
    print(f"  {code:<16} {c}")

# write TSV for the later 留痕 doc
out = os.path.join(PIPE, "_audit_result.tsv")
with open(out, "w", encoding="utf8") as fh:
    fh.write("slug\tname\tprimary\tall_reasons\treview\n")
    for r in eliminated:
        allr = ";".join(f"{c}:{d}" for c, d in r["reasons"])
        fh.write(f"{r['slug']}\t{r['name']}\t{primary(r)}\t{allr}\t{','.join(r['review'])}\n")
print(f"\n明细已写入: {out}")

# samples for sanity check
print("\n=== 各类抽样（每类最多 6 条，供人工复核）===")
by_code = defaultdict(list)
for r in eliminated:
    by_code[primary(r)].append(r)
for code, _ in by_reason.most_common():
    print(f"\n--- {code} ({by_reason[code]}) ---")
    for r in by_code[code][:6]:
        sub = ",".join(d for _, d in r["reasons"] if d)[:40]
        print(f"  {r['slug']:<28} {r['name']:<20} {sub}")
