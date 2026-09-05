#!/usr/bin/env python3
"""
fetch.py - 从 config/sources.yaml 拉取案例候选，过滤+去重后输出 inbox/YYYY-MM-DD.json

用法:
  python3 fetch.py                 # 拉今天
  python3 fetch.py --days 3        # 拉最近 3 天
  python3 fetch.py --since 2026-09-01
  python3 fetch.py --fresh         # 清空历史去重记录再拉（排查用，会重新产生历史候选）

支持抓取方式（sources.yaml 的 method 字段）:
  rss          - 标准 RSS/Atom，feedparser 解析
  html         - 静态 HTML 列表页
  js           - JS 站点（Playwright + Chrome），等待 domcontentloaded
  chrome_store - Chrome 应用商店（受 Shadow DOM / 地区重定向限制，当前不可用）
  supabase     - Supabase 公开 REST API（如 trustmrr 的 startup 表，含 MRR 结构化数据）
"""
import argparse, json, os, re, sys, datetime, ssl, time, urllib.request, urllib.error
from pathlib import Path
from urllib.parse import urlparse

try:
    import yaml
except ImportError:
    print("需要 pyyaml: pip3 install pyyaml"); sys.exit(1)
try:
    import feedparser
except ImportError:
    print("需要 feedparser: pip3 install feedparser"); sys.exit(1)
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "pipeline" / "config" / "sources.yaml"
INBOX = ROOT / "inbox"
SEEN = ROOT / "pipeline" / "seen.json"

# 只有命中这些关键词的条目才可能是「挣钱案例」
CASE_KEYWORDS = [
    "revenue", "mrr", "monthly recurring", "earn", "earning", "income", "profit",
    "saas", "subscription", "订阅", "付费", "营收", "收入", "盈利", "赚钱", "变现",
    "side project", "indie", "bootstrapped", "solo", "创始人", "独立开发", "创业",
    "chrome extension", "插件", "extension", "template", "模板", "newsletter", "课程",
    "affiliate", "联盟", "ad", "广告", "marketplace", "shop", "store", "产品",
]

# 这些词说明不是案例（纯资讯/新闻/招聘/灌水）
NOISE = [
    "招聘", "hiring", "job", "career", "融资速递", "早报", "日报", "周报",
    "新闻", "news", "breaking", "财报", "政策", "分析", "评论", "评测",
    "vps", "机场", "加速器", "翻墙", "梯子",  # v2ex 常见灌水话题
]

# 导航/站内功能链接文本，parse_html_list 里直接丢弃
NAV_WORDS = {
    "home", "sign in", "log in", "login", "sign out", "logout", "register",
    "sign up", "subscribe", "pricing", "about", "contact", "faq", "help",
    "terms", "privacy", "careers", "jobs", "submit", "submit a post",
    "advertise", "advertising", "new post", "write", "start posting",
    "settings", "account", "profile", "notifications", "search", "explore",
    "language", "中文", "chrome 应用商店", "我的扩展程序和主题", "开发者信息中心",
    "登录", "详细了解结果和评价", "更多", "查看全部",
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

UA = "Mozilla/5.0 (CaseLibBot/1.0)"


def debug(*a):
    if os.environ.get("FETCH_DEBUG"):
        print("[debug]", *a, file=sys.stderr)


def _http(url, timeout=20):
    """单次 HTTP GET，返回解码后的文本"""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.read().decode("utf-8", "ignore")


def with_retry(fn, retries=2, delay=3):
    """网络操作重试：很多反爬/RSS 站点会随机断连"""
    last = None
    for i in range(retries + 1):
        try:
            return fn()
        except Exception as e:
            last = e
            if i < retries:
                debug(f"retry {i + 1} after {e}")
                time.sleep(delay * (i + 1))
    raise last


def fetch_text(url, timeout=25, browser=False, wait_ms=6000):
    """抓网页文本。browser=True 时用 Playwright + Chrome。
    等待策略用 domcontentloaded + 固定等待，而不是 networkidle：
    networkidle 在广告/长连接站点上会永远不触发（trustmrr 曾因此超时）。"""
    if browser:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                args=["--no-sandbox"],
            )
            pg = b.new_page()
            pg.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
            pg.wait_for_timeout(wait_ms)
            html = pg.content()
            b.close()
            return html
    return _http(url, timeout=timeout)


def parse_rss(url, browser=False):
    raw = with_retry(lambda: fetch_text(url, browser=browser))
    fp = feedparser.parse(raw)
    items = []
    for e in fp.entries:
        items.append({
            "title": e.get("title", "").strip(),
            "link": e.get("link", "").strip(),
            "summary": re.sub(r"<[^>]+>", "", e.get("summary", "")).strip()[:400],
            "published": e.get("published", e.get("updated", "")),
        })
    return items


def _nav_like(title, href, link_allow=None):
    """判断 (title, href) 是不是导航/功能链接"""
    t = title.strip().lower()
    # 文本层面的噪音：太短 / 导航词 / 纯计数（"6 comments"），先于链接白名单判断
    if len(t) < 4 or t in NAV_WORDS:
        return True
    if re.fullmatch(r"\d+\s*(comments?|replies?|likes?|votes?)?", t):
        return True
    if link_allow:
        # 给了链接白名单：只收匹配的，其余全丢（最可靠的防导航手段）
        return not any(re.search(pat, href) for pat in link_allow)
    # 常见外链文本以 "visit site / read more" 等结尾的导航块
    for w in ("visit site", "read more", "learn more", "view all", "see all"):
        if t == w:
            return True
    # 纯用户名/账号主页：路径只有一段、无连字符（文章 slug 靠连字符区分），不像功能页
    _KNOWN_SINGLE = {"post", "product", "stories", "products", "ideas", "plus",
                     "starting-up", "about", "sign-in", "startups", "leaderboard",
                     "olympics", "blog", "new-post", "interviews", "dashboard"}
    try:
        path = urlparse(href).path.strip("/")
        if path and "/" not in path and "-" not in path:
            seg = path.lower()
            if seg not in _KNOWN_SINGLE:
                return True
    except Exception:
        pass
    return False


def parse_html_list(url, browser=False, link_allow=None):
    """从 HTML 列表页提取 (title, link) 对：跳过导航/用户主页，可选链接白名单"""
    raw = with_retry(lambda: fetch_text(url, browser=browser))
    if not BeautifulSoup:
        return []
    soup = BeautifulSoup(raw, "html.parser")
    items, seen = [], set()
    base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    for a in soup.find_all("a", href=True):
        txt = a.get_text(" ", strip=True)
        href = a["href"]
        if not txt or len(txt) < 4 or len(txt) > 200:
            continue
        if href.startswith("/"):
            href = base + href
        if href in seen:
            continue
        seen.add(href)
        if _nav_like(txt, href, link_allow=link_allow):
            continue
        items.append({"title": txt, "link": href, "summary": "", "published": ""})
    return items[:80]


def parse_chrome_store(url, limit=15):
    """Chrome 应用商店（受限：内容在 Shadow DOM + 按地区重定向，目前基本抓不到）。
    扩展类案例请依赖其他源的关键词命中 + 人工补充。"""
    raw = with_retry(lambda: fetch_text(url, browser=True, timeout=45))
    items = []
    for m in re.finditer(r'href="(/webstore/detail/[^"?]+)"', raw):
        href = "https://chromewebstore.google.com" + m.group(1)
        name = href.rstrip("/").split("/")[-1].replace("-", " ").title()
        items.append({"title": name, "link": href, "summary": "Chrome 扩展", "published": ""})
    if not items:
        for m in re.finditer(r'href="(https://chromewebstore[^"]*?/detail/[^"?]+)"', raw):
            href = m.group(1)
            name = href.rstrip("/").split("/")[-1].replace("-", " ").title()
            items.append({"title": name, "link": href, "summary": "Chrome 扩展", "published": ""})
    return items[:limit]


def parse_supabase(src, max_age_days=30):
    """从 Supabase 公开 REST API 拉结构化案例（如 trustmrr 的 startups 表）。
    返回候选列表；只收最近 max_age_days 天内有更新的记录，避免首次运行把整个
    存量库灌进 inbox。summary 里拼上 MRR/总收入/verified 等字段，供后续写文章用。"""
    api = src["supabase_url"]
    table = src.get("table", "startups")
    headers = {"apikey": src["apikey"], "Authorization": "Bearer " + src["apikey"]}

    def _get():
        url = f"{api}/rest/v1/{table}?select=*&order=updated_at.desc&limit=5000"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            return json.loads(r.read().decode("utf-8", "ignore"))

    rows = with_retry(_get)
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=max_age_days)
    items = []
    for r in rows:
        try:
            upd = datetime.datetime.fromisoformat(r.get("updated_at", "").replace("Z", "+00:00"))
        except Exception:
            upd = None
        if upd is not None and upd < cutoff:
            continue
        name = (r.get("name") or "").strip()
        website = (r.get("website") or "").strip()
        if not name or not website:
            continue
        mr = r.get("monthly_revenue")
        tr = r.get("total_revenue")
        desc = (r.get("description") or "").strip()
        summ = f"{desc} | " if desc else ""
        summ += (f"MRR ${mr:,.0f}/mo" if isinstance(mr, (int, float)) else "MRR 未知")
        if isinstance(tr, (int, float)):
            summ += f" | 累计 ${tr:,.0f}"
        summ += f" | verified={bool(r.get('verified'))}"
        if r.get("category"):
            summ += f" | 分类:{r['category']}"
        if r.get("country"):
            summ += f" | {r['country']}"
        if r.get("revenue_provider"):
            summ += f" | 数据源:{r['revenue_provider']}"
        if upd:
            summ += f" | 更新:{upd.date()}"
        items.append({"title": name, "link": website, "summary": summ, "published": upd.isoformat() if upd else ""})
    return items


def is_case(title, summary):
    text = (title + " " + summary).lower()
    if any(k in text for k in NOISE):
        return False
    return any(k in text for k in CASE_KEYWORDS)


def load_seen():
    if SEEN.exists():
        try:
            return json.loads(SEEN.read_text())
        except Exception:
            return {}
    return {}


def save_seen(seen):
    SEEN.write_text(json.dumps(seen, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=1)
    ap.add_argument("--since", type=str, default=None)
    ap.add_argument("--limit", type=int, default=25, help="每个源最多取多少条")
    ap.add_argument("--fresh", action="store_true", help="清空去重记录重拉（排查用）")
    args = ap.parse_args()

    cfg = yaml.safe_load(CONFIG.read_text())
    sources = [s for s in cfg["sources"] if s.get("enabled")]

    seen = {} if args.fresh else load_seen()
    today = datetime.date.today().isoformat()
    out_path = INBOX / f"{today}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    candidates = []
    for src in sources:
        name, url, method = src["name"], src["url"], src.get("method", "rss")
        link_allow = src.get("link_allow")  # 正则白名单列表，如 ^https://www.indiehackers.com/(post|product)/
        if not url:
            continue
        debug(f"pulling {name} ({method})")
        try:
            if method == "rss":
                items = parse_rss(url)
            elif method == "html":
                items = parse_html_list(url, link_allow=link_allow)
            elif method == "chrome_store":
                items = parse_chrome_store(url)
            elif method == "js":
                items = parse_html_list(url, browser=True, link_allow=link_allow)
            elif method == "supabase":
                items = parse_supabase(src)
            else:
                items = []
        except Exception as e:
            print(f"  ! {name} 抓取失败: {e}", file=sys.stderr)
            continue

        kept = 0
        title_allow = src.get("title_allow")  # 标题必须命中其一（如 v2ex 只收「分享创造/创业」节点）
        for it in items[: args.limit * 3]:
            link = it.get("link", "")
            if not link or link in seen:
                continue
            if title_allow and not any(k in it.get("title", "") for k in title_allow):
                continue
            # 专门案例源直接收（只过滤噪音），综合源才用关键词筛
            if not src.get("accept_all") and not is_case(it.get("title", ""), it.get("summary", "")):
                continue
            if any(k in (it.get("title", "") + it.get("summary", "")).lower() for k in NOISE):
                continue
            it["source"] = name
            it["category"] = src.get("category", "")
            candidates.append(it)
            seen[link] = today
            kept += 1
            if kept >= args.limit:
                break
        print(f"  ✓ {name}: 命中 {kept} 条")

    save_seen(seen)
    out_path.write_text(json.dumps(candidates, ensure_ascii=False, indent=2))
    print(f"\n共 {len(candidates)} 条候选 → {out_path}")
    return out_path


if __name__ == "__main__":
    main()
