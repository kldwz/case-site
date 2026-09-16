#!/usr/bin/env python3
"""Generate case-site Markdown cases from cached TrustMRR profiles.

Pipeline:
  parse_md -> passes_filter -> download cover -> LLM writes Chinese prose
  -> assemble src/content/cases/<slug>.md

Usage:
  python3 gen_trustmrr.py --slug chatbase
  python3 gen_trustmrr.py --all [--limit N] [--offset N] [--workers N]
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import concurrent.futures as cf
import zlib
import struct

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(ROOT, "pipeline", "trustmrr_cache")
CASES_DIR = os.path.join(ROOT, "src", "content", "cases")
PUBLIC_CASES = os.path.join(ROOT, "public", "cases")
PLACEHOLDER = os.path.join(PUBLIC_CASES, "_placeholder", "site.png")

from trustmrr_common import parse_md, passes_filter, fmt_money  # noqa

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "deepseek-ai/DeepSeek-V3"
PROXY = "http://127.0.0.1:1082"

SYSTEM = (
    "你是一名中文独立开发者案例库的编辑。只根据下面『事实清单』里给出的信息写作，"
    "严禁补充任何事实清单之外的具体数字、人物背景、社区规模、融资额、第三方流量估算、"
    "用户故事或任何未被提供的内容。事实清单里没有的信息，用『未披露』或『未官方披露』带过，"
    "不要编造。用简洁、客观、带一点分析口吻的中文写作。输出严格为 JSON，键为："
    "一句话, 可迁移点, 产品是什么, 怎么赚的钱, 流量从哪来, 站长是谁, "
    "这个案例能学到什么, 一句话总结。"
    "『可迁移点』用 ①②③… 编号的多行字符串。所有金额直接引用事实清单里的数字，不要换算。"
)

USER_TMPL = """# 事实清单（只能使用这些信息）
- 名称：{name}
- 一句话描述：{description}
- 网站：{website}
- 国家/地区：{country}
- 创立时间：{founded}
- 创始人：{founder}
- X 粉丝数：{x_followers}
- 支付验证来源：{payment_provider}（营收由该支付服务商 API 验证，非自报）
- 凭证是否过期：{cred}
- 当前 MRR：{mrr}
- 近30天营收：{r30}
- 近12个月营收：{r12}
- 累计营收：{rall}
- 活跃订阅数：{subs}
- 定价模式：{pricing}
- 受众类型：{audience}
- 预估用户数：{est_users}
- 价值主张：{value_prop}
- 解决的问题：{problem}
- 补充说明：{extra}
- 赛道/标签：{markets}
- 域名评分(DR)：{dr}
- 是否挂牌出售：{for_sale}
- 营收最后同步时间：{synced}

请输出 JSON。"""


def make_placeholder():
    os.makedirs(os.path.dirname(PLACEHOLDER), exist_ok=True)
    if os.path.exists(PLACEHOLDER):
        return
    w, h = 1280, 640
    color = (15, 23, 42)
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w):
            raw += bytes(color)
    comp = zlib.compress(bytes(raw), 9)
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        crc = zlib.crc32(typ + data) & 0xffffffff
        return c + struct.pack(">I", crc)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(PLACEHOLDER, "wb") as f:
        f.write(png)


def download_cover(facts):
    slug = facts["slug"]
    dest_dir = os.path.join(PUBLIC_CASES, slug)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "site.webp")
    url = facts.get("screenshot")
    if not url:
        return "/case-site/cases/_placeholder/site.png"
    if os.path.exists(dest):
        return f"/case-site/cases/{slug}/site.webp"
    last_err = None
    for via in (True, False):
        try:
            handlers = []
            if via:
                from urllib.request import ProxyHandler
                handlers.append(ProxyHandler({"https": PROXY, "http": PROXY}))
            opener = urllib.request.build_opener(*handlers)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with opener.open(req, timeout=30) as r:
                data = r.read()
            if len(data) < 500:
                raise ValueError("too small")
            with open(dest, "wb") as f:
                f.write(data)
            return f"/case-site/cases/{slug}/site.webp"
        except Exception as e:  # noqa
            last_err = e
            continue
    return "/case-site/cases/_placeholder/site.png"


def call_llm(facts):
    prompt = USER_TMPL.format(
        name=facts.get("name", ""),
        description=facts.get("description", ""),
        website=facts.get("website", ""),
        country=facts.get("country", ""),
        founded=facts.get("founded", ""),
        founder=facts.get("founder", "") or "未披露",
        x_followers=facts.get("x_followers", ""),
        payment_provider=facts.get("payment_provider", ""),
        cred="已过期（营收数据停留在最后同步日）" if facts.get("credential_expired") else "有效",
        mrr=fmt_money(facts.get("mrr", 0)),
        r30=fmt_money(facts.get("rev_30d", 0)),
        r12=fmt_money(facts.get("rev_12m", 0)),
        rall=fmt_money(facts.get("rev_all", 0)),
        subs=facts.get("subs", 0),
        pricing=facts.get("pricing", "") or "未披露",
        audience=facts.get("audience", "") or "未披露",
        est_users=facts.get("est_users", "") or "未披露",
        value_prop=facts.get("value_prop", ""),
        problem=facts.get("problem", ""),
        extra=facts.get("extra", ""),
        markets="、".join(m[0] for m in facts.get("markets", [])) or "未披露",
        dr=facts.get("dr", "") or "未披露",
        for_sale="是" if facts.get("for_sale") else "否",
        synced=facts.get("rev_synced", "") or "未披露",
    )
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 1500,
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
    }
    last_err = None
    for via in (True, False):
        try:
            handlers = []
            if via:
                from urllib.request import ProxyHandler
                handlers.append(ProxyHandler({"https": PROXY, "http": PROXY}))
            opener = urllib.request.build_opener(*handlers)
            req = urllib.request.Request(
                API_URL,
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json",
                         "Authorization": f"Bearer {API_KEY}"},
            )
            with opener.open(req, timeout=60) as r:
                resp = json.loads(r.read())
            content = resp["choices"][0]["message"]["content"]
            return json.loads(content)
        except Exception as e:  # noqa
            last_err = e
            continue
    raise last_err or RuntimeError("llm failed")


def build_case(slug):
    cache = os.path.join(CACHE_DIR, f"{slug}.md")
    if not os.path.exists(cache):
        return ("no-cache", slug)
    case_path = os.path.join(CASES_DIR, f"{slug}.md")
    if os.path.exists(case_path):
        return ("exists", slug)
    facts = parse_md(cache)
    ok, reason = passes_filter(facts)
    if not ok:
        return ("skip-" + reason, slug)
    try:
        prose = call_llm(facts)
    except Exception as e:  # noqa
        return ("llm-fail", f"{slug}|{e}")
    # flatten any newlines/tabs the model may emit so YAML frontmatter stays valid
    for k in list(prose):
        v = prose[k]
        if isinstance(v, str):
            prose[k] = " ".join(v.split())
    cover = download_cover(facts)

    # deterministic frontmatter
    name = facts["name"]
    website = facts["website"]
    mrr = facts["mrr"]
    r30 = facts["rev_30d"]
    monthly = fmt_money(mrr) if mrr > 0 else fmt_money(r30)
    founder_line = f"由 {facts['founder']} 创立" if facts.get("founder") else "创始人未披露"
    region = f"{founder_line}，{facts.get('country','') or '地区未披露'}，{facts.get('founded','')[:4] or '?'} 年成立" \
        if facts.get("founded") else founder_line
    pricing = facts.get("pricing") or "订阅制（具体档位未披露）"
    audience = facts.get("audience") or "未披露"
    dr = facts.get("dr") or "未披露"
    dr_disp = dr[:-2] if dr.endswith(".0") else dr
    markets = "、".join(m[0] for m in facts.get("markets", [])) or "未披露"
    cat = f"{markets} / {audience} / 海外"
    synced = facts.get("rev_synced") or "未披露"
    prov = facts.get("payment_provider") or "支付服务商"
    cred_note = "（凭证已过期，数据停留在最后同步日）" if facts.get("credential_expired") else ""
    data_calibre = (
        f"营收数据来自 TrustMRR 对接的支付服务商 API（{prov}）验证{cred_note}，"
        f"最后同步于 {synced}；域名评分 DR{dr_disp}；原始页 https://trustmrr.com/startup/{slug}。"
    )
    platform = (f"支付验证：{prov} · 当前 MRR {fmt_money(mrr)} · "
                f"活跃订阅 {facts.get('subs',0):,} · 近12个月营收 {fmt_money(facts.get('rev_12m',0))} · "
                f"累计营收 {fmt_money(facts.get('rev_all',0))} · 域名 DR{dr_disp} · "
                f"国家 {facts.get('country','') or '未披露'} · 创立 {facts.get('founded','') or '未披露'}")

    # body
    img = f"![{name} 官网](/cases/{slug}/site.webp)\n\n" if cover.endswith("site.webp") else ""
    hook = prose.get('一句话', '')
    hook = re.sub(rf'^【?{re.escape(name)}[：: ]?', '', hook).strip()
    body = (
        f"{img}# {name}：{hook}\n\n"
        f"## 产品是什么\n\n{prose.get('产品是什么','')}\n\n"
        f"## 怎么赚的钱\n\n{prose.get('怎么赚的钱','')}\n\n"
        f"## 流量从哪来\n\n{prose.get('流量从哪来','')}\n\n"
        f"## 站长是谁\n\n{prose.get('站长是谁','')}\n\n"
        f"## 这个案例能学到什么\n\n{prose.get('这个案例能学到什么','')}\n\n"
        f"## 来源与数据\n\n"
        f"- TrustMRR 原始页：`https://trustmrr.com/startup/{slug}`\n"
        f"- 营收由 {prov} API 验证，非自报{cred_note}；最后同步 {synced}。\n"
        f"- 官网：`{website}`\n\n"
        f"## 一句话总结\n\n> {prose.get('一句话总结','')}\n"
    )
    def yq(v):
        s = "" if v is None else str(v)
        s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").replace("\r", " ")
        return '"' + s + '"'

    fm = (
        "---\n"
        f"name: {yq(name)}\n"
        f"一句话: {yq(prose.get('一句话',''))}\n"
        f"创始人地区: {yq(region)}\n"
        f"营收模式: {yq(pricing)}\n"
        f"月收入估算: {yq(f'{monthly}/月（{prov} 验证）')}\n"
        f"流量来源: {yq((('SEO 自然流量为主' if dr not in ('未披露',) else '流量来源未披露') + f'（域名评分 DR{dr_disp}），{audience} 受众；官网 {website}')}\n"
        f"可迁移点: {yq(prose.get('可迁移点',''))}\n"
        f"原文链接: {yq(website)}\n"
        f"数据口径: {yq(data_calibre)}\n"
        f"分类: {yq(cat)}\n"
        f"类型: 收入案例\n"
        f"证据等级: 官方披露\n"
        f"平台数据: {yq(platform)}\n"
        f"封面: {yq(cover)}\n"
        "---\n\n"
    )
    with open(case_path, "w", encoding="utf-8") as f:
        f.write(fm + body)
    return ("ok", slug)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", help="single slug")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    make_placeholder()
    os.makedirs(CASES_DIR, exist_ok=True)

    if args.slug:
        res = build_case(args.slug)
        print(res)
        return

    # batch over cached files
    slugs = [f[:-3] for f in os.listdir(CACHE_DIR) if f.endswith(".md")]
    slugs.sort()
    slugs = slugs[args.offset:]
    if args.limit:
        slugs = slugs[: args.limit]

    stats = {}
    t0 = time.time()
    done = 0
    total = len(slugs)

    def record(r):
        nonlocal done
        kind, slug = r
        stats[kind] = stats.get(kind, 0) + 1
        done += 1
        if done % 100 == 0 or done == total:
            print(f"[{done}/{total}] {time.time()-t0:.0f}s {stats}", flush=True)

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(build_case, s) for s in slugs]
        for fut in cf.as_completed(futs):
            record(fut.result())
    print("DONE", stats, flush=True)


if __name__ == "__main__":
    main()
