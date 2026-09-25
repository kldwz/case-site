#!/usr/bin/env python3
"""Generate 国内实践 (domestic) case-site Markdown cases.

Source: pipeline/domestic_candidates.json  (108 curated real projects)
  - kind "app":        App Store CN; verify via Apple iTunes official search API,
                       download a real screenshot as cover.
  - kind "ext"|"competition"|"hardware"|"maker":
                       grounded only in the curated `note` + `source_url`.

All prose is written by DeepSeek-V3 (SiliconFlow) strictly from a 事实清单
that contains ONLY verified facts. Revenue is ALWAYS 未官方披露 — never invented.

Output schema mirrors src/content/cases/xiaorichang.md (type: 国内实践).

Usage:
  python3 gen_domestic.py --slug fanqie-todo
  python3 gen_domestic.py --all [--limit N] [--offset N] [--workers N]
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import concurrent.futures as cf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAND = os.path.join(ROOT, "pipeline", "domestic_candidates.json")
CASES_DIR = os.path.join(ROOT, "src", "content", "cases")
PUBLIC_CASES = os.path.join(ROOT, "public", "cases")
PLACEHOLDER = "/case-site/cases/_placeholder/site.png"

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "deepseek-ai/DeepSeek-V3"
PROXY = "http://127.0.0.1:1082"
TODAY = "2026-09-25"

KIND_CN = {
    "app": "App",
    "ext": "Chrome 扩展",
    "competition": "比赛获奖项目",
    "hardware": "开源硬件",
    "maker": "创作者/独立开发",
}
KIND_REGION = {
    "app": "App Store 中国区 · 平台数据可查",
    "ext": "Chrome 扩展 · 公开资料可查",
    "competition": "比赛获奖项目 · 公开资料可查",
    "hardware": "开源硬件 · 公开资料可查",
    "maker": "创作者/独立开发 · 公开资料可查",
}

SYSTEM = (
    "你是一名中文独立开发者/副业案例库编辑。只根据下面『事实清单』中的信息写作，"
    "严禁补充任何事实清单之外的具体数字、融资额、用户规模估算、第三方流量数据、"
    "人物背景故事或未经验证的说法。事实清单里没有的内容，用『未披露』或『未官方披露』带过，"
    "绝不编造。语气客观、简洁、带一点分析。输出严格为 JSON，键为："
    "一句话, 可迁移点, 产品是什么, 怎么赚的钱, 流量从哪来, 站长是谁, "
    "这个案例能学到什么, 一句话总结。"
    "『可迁移点』为用 ①②③… 编号的多行字符串。金额若事实清单未给出，统一写『未披露』。"
)

USER_APP = """# 事实清单（只能使用这些信息）
- 名称：{name}
- App Store 名称：{trackName}
- 开发者：{artist}
- 分类：{genre}
- 评分：{rating}（{count} 个评分）
- 价格：{price_text}
- 上架日期：{release}
- 官方链接：{trackViewUrl}
- 附注：{note}
- 收入：未官方披露（App Store 不公开收入与下载量）

请输出 JSON。"""

USER_OTHER = """# 事实清单（只能使用这些信息）
- 名称：{name}
- 类型：{kind_cn}
- 来源链接：{source_url}
- 附注：{note}
- 收入：未官方披露

请输出 JSON。"""


# --------------------------------------------------------------------------
# iTunes verification (direct, no proxy needed for Apple's public API)
# --------------------------------------------------------------------------
def itunes_search(q):
    url = ("https://itunes.apple.com/search?term=" + urllib.parse.quote(q)
           + "&country=cn&entity=software&limit=25")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read()).get("results", [])


def _norm(s):
    return re.sub(r"[\s\-_—:：.,。·()（）]", "", (s or "").lower())


def best_match(results, name):
    if not results:
        return None, False
    nn = _norm(name)
    cands = []
    for r in results:
        tn = _norm(r.get("trackName", ""))
        if tn and (tn == nn or nn in tn or tn in nn):
            cands.append(r)
    if not cands:
        for r in results:
            an = _norm(r.get("artistName", ""))
            if an and (nn in an or an in nn):
                cands.append(r)
    if cands:
        return max(cands, key=lambda r: r.get("userRatingCount", 0) or 0), True
    return results[0], False


def download_app_cover(slug, r):
    dest_dir = os.path.join(PUBLIC_CASES, slug)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "site.png")
    if os.path.exists(dest):
        return f"/case-site/cases/{slug}/site.png"
    urls = list(r.get("screenshotUrls", []) or []) + list(r.get("ipadScreenshotUrls", []) or [])
    if not urls and r.get("artworkUrl512"):
        urls = [r["artworkUrl512"]]
    if not urls:
        return PLACEHOLDER
    base = urls[0]
    # try a higher-resolution variant, then fall back to original
    bigger = base.replace("320x480bb", "1290x2796bb").replace("750x1334bb", "1290x2796bb")
    tried = []
    if bigger != base:
        tried.append(bigger)
    tried.append(base)
    last_err = None
    for u in tried:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            if len(data) < 500:
                raise ValueError("too small")
            # normalize to PNG via PIL if available, else save raw bytes
            try:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(data)).convert("RGB")
                img.save(dest, "PNG")
            except Exception:
                with open(dest, "wb") as f:
                    f.write(data)
            return f"/case-site/cases/{slug}/site.png"
        except Exception as e:  # noqa
            last_err = e
            continue
    return PLACEHOLDER


# --------------------------------------------------------------------------
# LLM
# --------------------------------------------------------------------------
def call_llm(prompt):
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
            with opener.open(req, timeout=90) as r:
                resp = json.loads(r.read())
            return json.loads(resp["choices"][0]["message"]["content"])
        except Exception as e:  # noqa
            last_err = e
            continue
    raise last_err or RuntimeError("llm failed")


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def yq(v):
    s = "" if v is None else str(v)
    s = (s.replace("\\", "\\\\").replace('"', '\\"')
         .replace("\n", " ").replace("\r", " "))
    return '"' + s + '"'


def flatten(prose):
    for k in list(prose):
        v = prose[k]
        if isinstance(v, str):
            prose[k] = " ".join(v.split())
    return prose


def fm_block(fm_dict):
    lines = ["---"]
    for k, v in fm_dict.items():
        lines.append(f"{k}: {yq(v)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


# --------------------------------------------------------------------------
# per-candidate build
# --------------------------------------------------------------------------
def build(cand):
    slug = cand["slug"]
    case_path = os.path.join(CASES_DIR, f"{slug}.md")
    if os.path.exists(case_path):
        return ("exists", slug)
    kind = cand["kind"]
    name = cand["name"]

    # ---- gather verified facts ----
    if kind == "app":
        try:
            results = itunes_search(cand.get("itunes_q", name))
            rec, matched = best_match(results, name)
        except Exception as e:  # noqa
            rec, matched = None, False
        if not rec:
            return ("itunes-empty", slug)
        rating = rec.get("averageUserRating") or 0
        count = rec.get("userRatingCount") or 0
        artist = rec.get("artistName") or "未披露"
        price = rec.get("price")
        fprice = rec.get("formattedPrice") or ("免费" if price in (0, 0.0, None) else f"¥{price}")
        release = (rec.get("releaseDate") or "")[:10]
        genre = rec.get("primaryGenreName") or "未披露"
        track_view = rec.get("trackViewUrl") or cand.get("source_url", "")
        track_name = rec.get("trackName") or name
        monet = "免费+内购" if price in (0, 0.0, None) else "付费下载"
        rev_mode = ("免费下载 + 内购（具体档位未披露）"
                    if price in (0, 0.0, None) else f"付费下载（{fprice}）")
        rating_disp = round(rating, 2)
        cover = download_app_cover(slug, rec)
        prompt = USER_APP.format(
            name=name, trackName=track_name, artist=artist, genre=genre,
            rating=rating, count=f"{count:,}", price_text=fprice,
            release=release, trackViewUrl=track_view, note=cand.get("note", ""),
        )
        try:
            prose = call_llm(prompt)
        except Exception as e:  # noqa
            return ("llm-fail", f"{slug}|{e}")
        prose = flatten(prose)
        data_calibre = (
            f"Apple iTunes 官方搜索 API（itunes.apple.com/search?country=cn），{TODAY} 抓取："
            f"开发者 {artist}、价格 {fprice}、评分 {rating_disp}、评分人数 {count:,}、"
            f"上架日期 {release}。收入未官方披露。"
        )
        platform = (f"App Store 中国区 ★{rating_disp}（{count:,} 个评分）· {fprice} · "
                    f"上架 {release}（iTunes 官方 API）")
        fm = {
            "name": name,
            "一句话": prose.get("一句话", ""),
            "创始人地区": f"{artist}，{release} 上架 App Store 中国区",
            "营收模式": rev_mode,
            "月收入估算": "未官方披露（App Store 不公开下载量与收入，本站不做估算）",
            "流量来源": (f"App Store 中国区搜索与榜单（评分 {rating_disp}，{count:,} 个评分）；"
                         f"{genre} 类目长尾流量"),
            "可迁移点": prose.get("可迁移点", ""),
            "原文链接": track_view,
            "数据口径": data_calibre,
            "分类": f"{genre} / {monet} / 中文 / {cand.get('cat','')}",
            "类型": "国内实践",
            "证据等级": "平台数据可查" if matched else "公开资料",
            "平台数据": platform,
            "封面": cover,
        }
        img = f"![{name} App Store 页](/cases/{slug}/site.png)\n\n" if cover != PLACEHOLDER else ""
        body = (
            f"{img}# {name}：{prose.get('一句话','')}\n\n"
            f"## 产品是什么\n\n{prose.get('产品是什么','')}\n\n"
            f"## 怎么赚的钱\n\n{prose.get('怎么赚的钱','')}\n\n"
            f"## 流量从哪来\n\n{prose.get('流量从哪来','')}\n\n"
            f"## 站长是谁\n\n{prose.get('站长是谁','')}\n\n"
            f"## 这个案例能学到什么\n\n{prose.get('这个案例能学到什么','')}\n\n"
            f"## 来源与数据\n\n"
            f"- Apple iTunes 官方搜索 API：`https://itunes.apple.com/search?term={urllib.parse.quote(cand.get('itunes_q', name))}&country=cn&entity=software`"
            f"（{TODAY} 抓取：评分 {rating_disp}、评分人数 {count:,}、价格 {fprice}、上架 {release}、开发者 {artist}）\n"
            f"- App Store 页面：`{track_view}`\n"
            f"- 收入：未官方披露，本站不做估算\n\n"
            f"## 一句话总结\n\n> {prose.get('一句话总结','')}\n"
        )
    else:
        source_url = cand.get("source_url", "")
        prompt = USER_OTHER.format(
            name=name, kind_cn=KIND_CN.get(kind, kind),
            source_url=source_url, note=cand.get("note", ""),
        )
        try:
            prose = call_llm(prompt)
        except Exception as e:  # noqa
            return ("llm-fail", f"{slug}|{e}")
        prose = flatten(prose)
        data_calibre = f"公开资料整理（来源：{source_url}），{TODAY} 抓取。收入未官方披露。"
        fm = {
            "name": name,
            "一句话": prose.get("一句话", ""),
            "创始人地区": KIND_REGION.get(kind, "国内 · 公开资料可查"),
            "营收模式": "未官方披露",
            "月收入估算": "未官方披露",
            "流量来源": "公开资料可查，具体流量数据未官方披露",
            "可迁移点": prose.get("可迁移点", ""),
            "原文链接": source_url,
            "数据口径": data_calibre,
            "分类": f"{cand.get('cat','')} / 中文 / 国内",
            "类型": "国内实践",
            "证据等级": "公开资料",
            "平台数据": f"公开资料（{source_url}）",
            "封面": PLACEHOLDER,
        }
        body = (
            f"# {name}：{prose.get('一句话','')}\n\n"
            f"## 产品是什么\n\n{prose.get('产品是什么','')}\n\n"
            f"## 怎么赚的钱\n\n{prose.get('怎么赚的钱','')}\n\n"
            f"## 流量从哪来\n\n{prose.get('流量从哪来','')}\n\n"
            f"## 站长是谁\n\n{prose.get('站长是谁','')}\n\n"
            f"## 这个案例能学到什么\n\n{prose.get('这个案例能学到什么','')}\n\n"
            f"## 来源与数据\n\n"
            f"- 来源链接：`{source_url}`\n"
            f"- 收入：未官方披露，本站不做估算\n\n"
            f"## 一句话总结\n\n> {prose.get('一句话总结','')}\n"
        )

    with open(case_path, "w", encoding="utf-8") as f:
        f.write(fm_block(fm) + body)
    return ("ok", slug)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    os.makedirs(CASES_DIR, exist_ok=True)
    cands = json.load(open(CAND, encoding="utf-8"))
    if args.slug:
        c = next((c for c in cands if c["slug"] == args.slug), None)
        if not c:
            print("slug not found", args.slug)
            return
        print(build(c))
        return

    cands = cands[args.offset:]
    if args.limit:
        cands = cands[: args.limit]
    total = len(cands)
    stats = {}
    done = 0
    t0 = time.time()

    def record(r):
        nonlocal done
        kind, slug = r
        stats[kind] = stats.get(kind, 0) + 1
        done += 1
        if done % 20 == 0 or done == total:
            print(f"[{done}/{total}] {time.time()-t0:.0f}s {stats}", flush=True)

    def wrap(c):
        try:
            return build(c)
        except Exception as e:  # noqa
            return ("crash", f"{c['slug']}|{e}")

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(wrap, c) for c in cands]
        for fut in cf.as_completed(futs):
            record(fut.result())
    print("DONE", stats, flush=True)


if __name__ == "__main__":
    main()
