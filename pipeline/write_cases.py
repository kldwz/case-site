#!/usr/bin/env python3
"""
write_cases.py - 从 inbox/YYYY-MM-DD.json 候选批量生成中文案例文章

用法:
  python3 pipeline/write_cases.py                       # 处理今天的 inbox 所有候选
  python3 pipeline/write_cases.py --date 2026-09-05     # 处理指定日期
  python3 pipeline/write_cases.py --limit 5             # 最多处理 5 条
  python3 pipeline/write_cases.py --no-screenshot       # 跳过截图

流程:
  1. 读 inbox/<date>.json 候选
  2. 跳过已有案例（src/content/cases 已存在同名）
  3. 调 claude -p 生成结构化 JSON（name/overview/revenue/traffic/lesson/founder）
  4. 模板拼装成 src/content/cases/<slug>.md（frontmatter + 正文）
  5. screenshot.py 截官网图（失败生成占位 SVG）
  6. 追加一行到 cases.tsv（全部成功后才追加）

数字规矩: 有公开来源标来源，没有写「未官方披露 / 未知」，绝不编造精确数字
"""
import argparse, json, os, re, subprocess, sys, datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
CASES_DIR = ROOT / "src" / "content" / "cases"
TSV = ROOT / "cases.tsv"
PUBLIC_CASES = ROOT / "public" / "cases"
FAILURES_DIR = ROOT / "pipeline" / "failures"

# LLM 配置：优先读环境变量，否则用 token hub 默认（用户提供）
if not os.environ.get("ANTHROPIC_BASE_URL"):
    os.environ["ANTHROPIC_BASE_URL"] = "https://api.tokenshub.org"
if not os.environ.get("ANTHROPIC_AUTH_TOKEN"):
    os.environ["ANTHROPIC_AUTH_TOKEN"] = (
        "sk-6f090a6d0704634429ab308e6f62cd97637e4cc53143e966b575e3e42a8d5704"
    )
if not os.environ.get("CASE_LLM_MODEL"):
    os.environ["CASE_LLM_MODEL"] = "deepseek-v4-flash"

FIELDS = ["name", "一句话", "创始人地区", "营收模式", "月收入估算", "流量来源", "可迁移点", "原文链接", "数据口径", "分类", "封面"]

GEN_PROMPT_TMPL = """你是一个独立开发者收入案例库的编辑。根据下面的候选信息，生成一篇标准中文案例的结构化数据。

候选信息：
- 标题：{title}
- 链接：{link}
- 来源：{source}
- 摘要：{summary}
- 发布时间：{published}
- 地区：{category}

输出严格 JSON（不要 markdown 代码围栏，不要多余文字），字段：
- name: 案例名（简洁，如 "Covai Cars"）
- slogan: 一句话概括，讲清它靠什么赚钱（30字内）
- overview: 产品/网站是什么，120-180字，讲普通人怎么用
- revenue: 怎么赚的钱，100-150字，拆解商业模式。有公开收入就写，没有写「未官方披露」
- revenue_est: 月收入估算，纯文本（有来源写数字+来源，无来源写「未官方披露」）
- traffic: 流量从哪来，80-120字
- lesson: 普通人能学到的经验，3-4条，用分号分隔
- founder: 创始人/地区，简单（未知写「未知」）
- category_tags: 分类标签，斜杠分隔，如 "工具站 / 广告变现 / 英文"

规则：所有数字必须来自候选信息，没有就写「未官方披露 / 未知」，绝不编造精确数字。
"""


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", type=str, default=None, help="inbox 日期，默认今天")
    ap.add_argument("--limit", type=int, default=0, help="最多处理几条，0=全部")
    ap.add_argument("--claude-bin", type=str, default="claude", help="claude CLI 路径")
    ap.add_argument("--no-screenshot", action="store_true", help="跳过截图")
    ap.add_argument("--append", action="store_true", help="写入成功后追加汇总表")
    return ap.parse_args()


# 社区/资讯源域名——slug 该用标题，不用域名
COMMUNITY_DOMAINS = {
    "indiehackers.com", "producthunt.com", "v2ex.com", "36kr.com",
    "news.ycombinator.com", "hnrss.org", "ycombinator.com",
}


def get_domain_slug(candidate):
    """slug 生成：独立官网用域名，社区/资讯链接用标题。中文标题兜底用日期+序号。"""
    link = candidate.get("link", "")
    try:
        netloc = urlparse(link).netloc
        domain = netloc.lower().replace("www.", "").split(":")[0]
    except Exception:
        domain = ""
    # 社区链接：用标题 slug（避免 producthunt 这种通用域名）
    if domain in COMMUNITY_DOMAINS or domain.endswith("indiehackers.com") or domain.endswith("producthunt.com"):
        t = re.sub(r"[^\w\s-]", "", candidate.get("title", "")).lower()
        parts = [p for p in re.split(r"[^a-z0-9]+", t) if p]
        # 去掉 "show hn"/"[分享创造]" 前缀和语种词
        parts = [p for p in parts if p not in ("show", "hn")][:4]
        slug = "-".join(parts)
        if slug:
            return slug[:50].strip("-")
    # 独立官网：用域名第一段
    if domain:
        parts = [p for p in domain.split(".") if p]
        if parts:
            return parts[0]
    # 兜底：中文标题被全滤光 → 用链接里的路径最后一段或日期
    try:
        path_part = [p for p in re.split(r"/|\?|#", urlparse(link).path) if p][-1]
        if path_part and re.search(r"[a-z0-9]", path_part):
            return path_part[:50].strip("-")
    except Exception:
        pass
    return f"case-{datetime.date.today().isoformat()}"


def already_exists(candidate):
    link = (candidate.get("link") or "").strip()
    title = (candidate.get("title") or "").strip()
    for md in CASES_DIR.glob("*.md"):
        text = md.read_text()
        if link and link in text:
            return True
        if title and title in text:
            return True
    return False


def call_claude(prompt, claude_bin, timeout=90):
    """调用 LLM 生成结构化数据。优先 Anthropic SDK 直连（ANTHROPIC_AUTH_TOKEN），
    失败/未配置时退回 claude CLI。"""
    # 方式 1：Anthropic SDK 直连（模型 deepseek-v4-flash，经 token hub）
    env_token = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("ANTHROPIC_API_KEY")
    if env_token:
        try:
            from anthropic import Anthropic
            client = Anthropic()
            msg = client.messages.create(
                model=os.environ.get("CASE_LLM_MODEL", "deepseek-v4-flash"),
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            texts = [b.text for b in msg.content if hasattr(b, "text") and b.type == "text"]
            if texts:
                return texts[0].strip()
        except Exception as e:
            print(f"    ! SDK 直连失败，退回 CLI: {str(e)[:120]}", file=sys.stderr)
    # 方式 2：claude CLI
    try:
        r = subprocess.run(
            [claude_bin, "-p", prompt, "--output-format", "text", "--bare"],
            capture_output=True, text=True, timeout=timeout, check=False,
        )
        if r.returncode != 0:
            print(f"    ! claude 调用失败: {r.stderr[:150]}", file=sys.stderr)
            return None
        return r.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"    ! claude 超时（{timeout}s）", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(f"    ! 找不到 claude CLI: {claude_bin}", file=sys.stderr)
        return None


KEYS = ['"name"', '"slogan"', '"overview"', '"revenue"',
        '"revenue_est"', '"traffic"', '"lesson"', '"founder"', '"category_tags"']


def _segments(text):
    """枚举候选 JSON 片段起点。LLM 常先写思考草稿再给 JSON，且可能被截断。"""
    segs = []
    # 所有 { 位置（按出现顺序，靠前的 { 可能来自思考草稿）
    for m in re.finditer(r"\{", text):
        segs.append(m.start())
    # 所有 "name" 位置（裸字段场景）
    for m in re.finditer(r'"name"', text):
        segs.append(m.start())
    return sorted(set(segs))


def extract_json(text):
    """从 LLM 输出提取 JSON。处理包裹/围栏/前置思考草稿/截断。"""
    if not text:
        return None
    text = re.sub(r"```(?:json)?\s*", "", text).strip()

    def try_parse(seg):
        try:
            d = json.loads(seg)
            return d if isinstance(d, dict) else None
        except json.JSONDecodeError:
            return None

    def try_segment(seg):
        """对单个片段尝试：完整 → 补} → 逐步截断+补}。返回 dict 或 None。"""
        # 完整
        d = try_parse(seg)
        if d:
            return d
        # 补 }（缺尾括号）
        d = try_parse(seg + "}")
        if d:
            return d
        # 缺 {（裸字段）
        d = try_parse("{" + seg)
        if d:
            return d
        d = try_parse("{" + seg + "}")
        if d:
            return d
        # 逐步截断 + 补 }（截断在值内部）
        last_key = max((seg.rfind(k) for k in KEYS if k in seg), default=-1)
        if last_key >= 0:
            head = seg[:last_key]
            tail = seg[last_key:]
            for i in range(len(tail), 0, -1):
                d = try_parse("{" + head + tail[:i] + "}")
                if d:
                    return d
        return None

    # 按起点枚举，优先靠后的（越靠后越接近真正的 JSON 正文）
    for st in reversed(_segments(text)):
        # 排除思考草稿里的裸 { 片段（不含任何 key）
        seg = text[st:]
        if not any(k in seg for k in KEYS):
            continue
        d = try_segment(seg)
        if d:
            return d
    # 最后手段：从任意 { 到最后一个 }（贪心）
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        d = try_parse(m.group(0))
        if d:
            return d
    print(f"    ! JSON 解析失败（前200字: {text[:200]!r}）", file=sys.stderr)
    return None


def build_md(candidate, data, slug):
    """用模板拼装完整 md"""
    link = candidate.get("link", "")
    source = candidate.get("source", "")
    raw_tags = data.get("category_tags", "独立开发 / 英文")
    if isinstance(raw_tags, list):
        tags = " / ".join(str(t).strip() for t in raw_tags if str(t).strip()) or "独立开发 / 英文"
    elif not isinstance(raw_tags, str) or not raw_tags.strip():
        tags = "独立开发 / 英文"
    else:
        tags = raw_tags
    cover = f"/case-site/cases/{slug}/site.png"

    def s(key, default="未官方披露"):
        v = data.get(key)
        if not isinstance(v, str) or not v.strip():
            return default
        return v.strip()

    fm = f"""---
name: {s('name', candidate.get('title', ''))}
一句话: {s('slogan')}
创始人地区: {s('founder', '未知')}
营收模式: {s('revenue').split(chr(10))[0][:80]}
月收入估算: {s('revenue_est')}
流量来源: {s('traffic').replace(chr(10), ' ')[:100]}
可迁移点: {s('lesson').replace(chr(10), ' ')[:150]}
原文链接: {link}
数据口径: {source} 收录
分类: {tags}
封面: {cover}
---

![{data.get('name', candidate.get('title', ''))} 官网](/case-site/cases/{slug}/site.png)

# {data.get('name', candidate.get('title', ''))}：{data.get('slogan', '')}

## 产品是什么

{data.get('overview', '')}

## 怎么赚的钱

{data.get('revenue', '')}

## 流量从哪来

{data.get('traffic', '')}

## 这个案例能学到什么

{data.get('lesson', '')}

## 来源与数据

- 站点：{link}
- 来源：{source}（{candidate.get('published', '')[:10]}）
- 收入：{data.get('revenue_est', '未官方披露')}

## 一句话总结

> {data.get('slogan', '')}
"""

    # 提取营收模式行的纯文本
    return fm


def placeholder_svg(slug, name):
    """生成占位 SVG（截图失败时用）"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720">
  <rect width="100%" height="100%" fill="#f0f0ee"/>
  <text x="50%" y="45%" font-size="40" font-family="sans-serif" fill="#6b6b6b" text-anchor="middle">{name}</text>
  <text x="50%" y="55%" font-size="20" font-family="sans-serif" fill="#999" text-anchor="middle">官网截图暂缺</text>
</svg>"""
    return svg


def screenshot(candidate, slug):
    """截官网首页图，失败生成占位 SVG"""
    link = candidate.get("link", "")
    pub_dir = PUBLIC_CASES / slug
    pub_dir.mkdir(parents=True, exist_ok=True)
    png = pub_dir / "site.png"
    if png.exists():
        return True
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                args=["--no-sandbox"],
            )
            pg = b.new_page(viewport={"width": 1280, "height": 900})
            pg.goto(link, timeout=40000, wait_until="domcontentloaded")
            pg.wait_for_timeout(5000)
            pg.screenshot(path=str(png), full_page=False)
            b.close()
        return True
    except Exception as e:
        print(f"    ! 截图失败: {e}", file=sys.stderr)
        (pub_dir / "site.png").write_text(placeholder_svg(slug, candidate.get("title", "")), encoding="utf-8")
        return False


def append_tsv(candidate, data):
    """追加汇总表行"""
    name = data.get("name", candidate.get("title", "")).strip().replace("\t", " ")
    date = datetime.date.today().isoformat()
    source = candidate.get("source", "").replace("\t", " ")
    note = data.get("slogan", "")[:50].replace("\t", " ").replace("\n", " ")
    row = f"{name}\t{date}\t{source}\t{note}\t✅\t❌\t❌\n"
    with open(TSV, "a", encoding="utf-8") as f:
        f.write(row)
    print(f"  ✓ 已追加汇总表: {name}")


def record_failure(candidate, date):
    """重试多次仍失败的候选，记录到失败文档（用户会人工补写）"""
    FAILURES_DIR.mkdir(parents=True, exist_ok=True)
    f = FAILURES_DIR / f"{date}.md"
    link = candidate.get("link", "")
    title = candidate.get("title", "")
    source = candidate.get("source", "")
    summary = (candidate.get("summary") or "")[:300]
    block = (
        f"## {title}\n\n"
        f"- 链接：{link}\n"
        f"- 来源：{source}\n"
        f"- 摘要：{summary}\n\n"
    )
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(block)
    print(f"  ! 已记录失败: {title} -> {f.name}")


def warmup(claude_bin):
    """预热 claude -p（--bare 冷启动慢，先跑个短 prompt 唤起）"""
    try:
        subprocess.run(
            [claude_bin, "-p", "回一字：好", "--output-format", "text", "--bare"],
            capture_output=True, text=True, timeout=60, check=False,
        )
    except Exception:
        pass


def main():
    args = parse_args()
    date = args.date or datetime.date.today().isoformat()
    inbox_file = INBOX / f"{date}.json"
    if not inbox_file.exists():
        print(f"没有 inbox/{date}.json", file=sys.stderr)
        sys.exit(1)

    with open(inbox_file) as f:
        candidates = json.load(f)
    if args.limit:
        candidates = candidates[: args.limit]

    print("预热 claude（--bare 冷启动）...", file=sys.stderr)
    warmup(args.claude_bin)

    ok = 0
    for i, c in enumerate(candidates, 1):
        title = c.get("title", "")
        print(f"[{i}/{len(candidates)}] {title} ({c.get('source','')})")

        if already_exists(c):
            print("  - 跳过：已存在")
            continue

        slug = get_domain_slug(c)
        if not slug:
            print("  ! 无法生成 slug，跳过")
            continue

        # 生成文章（重试兜底：最多 5 次，第二次起超时拉长 20s）
        prompt = GEN_PROMPT_TMPL.format(
            title=c.get("title", ""), link=c.get("link", ""),
            source=c.get("source", ""), summary=c.get("summary", "")[:600],
            published=c.get("published", ""), category=c.get("category", ""),
        )
        out = None
        timeout = 90
        for attempt in range(1, 6):
            out = call_claude(prompt, args.claude_bin, timeout=timeout)
            if out:
                data = extract_json(out)
                if data:
                    break
                out = None
                print(f"    ! 第{attempt}次输出非 JSON，重试...")
            else:
                print(f"    ! 第{attempt}次调用失败，重试...")
            timeout += 20  # 重试拉长超时
        if not out:
            record_failure(c, date)
            print("  ! 重试 5 次仍失败，已记入失败文档")
            continue
        data = extract_json(out)
        if not data:
            record_failure(c, date)
            print("  ! 输出非 JSON，已记入失败文档")
            continue

        md = build_md(c, data, slug)
        md_path = CASES_DIR / f"{slug}.md"
        md_path.write_text(md, encoding="utf-8")
        print(f"  ✓ 写入 {md_path.name}")

        # 截图
        if not args.no_screenshot:
            ok_img = screenshot(c, slug)
            print(f"  {'✓ 截图成功' if ok_img else '! 截图失败(已占位)'}")

        if args.append:
            append_tsv(c, data)
        ok += 1

    print(f"\n完成：生成 {ok} 篇")


if __name__ == "__main__":
    main()