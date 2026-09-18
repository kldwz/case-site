#!/usr/bin/env python3
"""Stage 2 - LLM-enrich curated cases, writing long-form sections back to source md.

For every slug in pipeline/curated_slugs.txt:
- extract REAL fields from src/content/cases/<slug>.md (frontmatter + existing body)
- call SiliconFlow DeepSeek-V3 with a strict "only use the fact list, never fabricate"
  system prompt -> JSON of three sections:
      产品详解 (350-500字) / 盈利模式 (honest) / 你能学到什么 (300字)
- replace OR insert the body's 产品是什么 / 怎么赚的钱 / 这个案例能学到什么 sections
  with the expanded text. Headings are inserted in canonical order right after the
  intro, before the analytical sections (流量从哪来 / 站长是谁 / 来源与数据 / 一句话总结).
  Frontmatter and all other sections are preserved untouched.

Revenue honesty is enforced in the prompt: if 营收模式/月收入估算 say 未披露, the
盈利模式 section must say 未披露 and must NOT invent any number.

Usage:
  python3 enrich_cases.py            # enrich all curated (skip already-long)
  python3 enrich_cases.py --force    # re-enrich even if already long
  python3 enrich_cases.py --slug 1devtool --force   # one case
"""
import os, re, sys, json, time, urllib.request, urllib.error

CASE_SITE = "/Users/hxw/codebuddy/case-site"
PIPE = os.path.join(CASE_SITE, "pipeline")
CASES = os.path.join(CASE_SITE, "src/content/cases")
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "deepseek-ai/DeepSeek-V3"
SLUGS = [s.strip() for s in open(os.path.join(PIPE, "curated_slugs.txt"), encoding="utf-8") if s.strip()]

# Where the three detail sections should be placed (before any of these).
ANCHORS = ["流量从哪来", "用户从哪来", "谁做的", "来源与数据", "站长是谁", "一句话总结"]

SYSTEM = (
    "你是一名中文独立开发者/副业案例库的资深编辑。下面会给一份『事实清单』，"
    "你只能依据清单里给出的信息写作，严禁补充清单之外的任何具体数字、人物背景、"
    "社区规模、融资额、第三方流量估算、用户故事或未被提供的内容。清单里没有的营收/"
    "流量信息，用『未披露』或『未官方披露』带过，绝不编造。语气客观、专业、带一点分析，"
    "面向『想做类似小产品赚钱』的读者。全部用中文，避免英文术语堆砌。"
    "输出严格为 JSON，只有三个键：产品详解、盈利模式、你能学到什么。"
    "『产品详解』350–500字，讲清它是什么、给谁用、解决什么问题、核心功能/使用方式。"
    "『盈利模式』基于『营收模式』字段客观说明如何变现；若字段为未披露，明确写未披露，不编造金额。"
    "『你能学到什么』基于『可迁移点』扩写成可复用的方法论，300字左右。"
)

def fm_and_body(txt):
    m = re.match(r"^(---\n.*?\n---\n?)(.*)$", txt, re.S)
    if not m:
        return None, txt
    return m.group(1), m.group(2)

def get_field(txt, key):
    m = re.search(r"^" + re.escape(key) + r"\s*:\s*(.+)$", txt, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else ""

def section(body, title):
    m = re.search(r"##\s*" + re.escape(title) + r"\s*\n(.*?)(?=\n##\s|\Z)", body, re.S)
    return m.group(1).strip() if m else ""

def strip_detail(body):
    """Remove any existing 产品是什么 / 怎么赚的钱 / 这个案例能学到什么 blocks
    (canonical heading OR misplaced), so we can rebuild deterministically."""
    for t in ("产品是什么", "怎么赚的钱", "这个案例能学到什么"):
        body = re.sub(r"\n##\s*" + re.escape(t) + r"\s*\n.*?(?=\n##\s|\Z)",
                      "", body, flags=re.S)
    return body

def rebuild_body(body, data, name):
    """Deterministic rebuild: title + 3 fresh detail sections + analytical sections.
    Ignores any prior corruption; produces a clean, canonical structure."""
    body = strip_detail(body)
    anchor_re = re.compile(r"\n##\s*(" + "|".join(re.escape(a) for a in ANCHORS) + r")\s*\n")
    m = anchor_re.search(body)
    analytical = body[m.start():] if m else ""
    detail = ""
    for t, key in (("产品是什么", "产品详解"), ("怎么赚的钱", "盈利模式"),
                   ("这个案例能学到什么", "你能学到什么")):
        detail += f"\n\n## {t}\n\n{data.get(key, '').strip()}\n"
    return f"# {name}\n" + detail + (analytical if analytical else "\n")

def build_user(fm_raw, body):
    def g(k): return get_field(fm_raw, k)
    return f"""# 事实清单（只能基于这些信息写作，严禁编造任何数字/人物/融资/流量估算）
- 名称：{g('name')}
- 一句话：{g('一句话')}
- 类型：{g('类型')}
- 营收模式：{g('营收模式')}
- 月收入估算：{g('月收入估算')}
- 流量来源：{g('流量来源')}
- 可迁移点：{g('可迁移点')}
- 平台数据：{g('平台数据')}
- 创始人地区：{g('创始人地区')}
- 证据等级：{g('证据等级')}
- 原文链接：{g('原文链接')}
- 现有素材（仅作参考，可重写）：
  产品是什么：{section(body, '产品是什么')}
  怎么赚的钱：{section(body, '怎么赚的钱')}
  这个案例能学到什么：{section(body, '这个案例能学到什么')}

请只输出 JSON，三键：产品详解 / 盈利模式 / 你能学到什么。"""

def call_llm(user):
    payload = json.dumps({
        "model": MODEL, "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user},
        ],
        "max_tokens": 1500, "temperature": 0.3, "response_format": {"type": "json_object"},
    }).encode("utf-8")
    req = urllib.request.Request(API_URL, data=payload, headers={
        "Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read().decode("utf-8"))
            return d["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"  ! attempt {attempt+1} failed: {e}")
            time.sleep(2 + attempt * 2)
    return None

def parse_json(s):
    if not s:
        return None
    try:
        return json.loads(s)
    except Exception:
        m = re.search(r"\{.*\}", s, re.S)
        if m:
            try: return json.loads(m.group(0))
            except Exception: return None
    return None

def main():
    args = set(sys.argv[1:])
    force = "--force" in args
    only = None
    for a in args:
        if a.startswith("--slug"):
            only = a.split("=", 1)[1] if "=" in a else None
    if only is None and "--slug" in args:
        idx = sys.argv.index("--slug"); only = sys.argv[idx+1]
    slugs = [only] if only else SLUGS

    done = skip = fail = 0
    for slug in slugs:
        path = os.path.join(CASES, slug + ".md")
        if not os.path.exists(path):
            print(f"missing {slug}"); fail += 1; continue
        txt = open(path, encoding="utf-8").read()
        fm_raw, body = fm_and_body(txt)
        existing = section(body, "产品是什么")
        if not force and len(existing) > 200:
            print(f"skip (already enriched) {slug}")
            skip += 1; continue
        user = build_user(fm_raw, body)
        out = call_llm(user)
        data = parse_json(out)
        if not data or not data.get("产品详解"):
            print(f"FAIL parse {slug}"); fail += 1; continue
        # deterministic rebuild (immune to prior corruption)
        new_body = rebuild_body(body, data, get_field(fm_raw, "name"))
        open(path, "w", encoding="utf-8").write(fm_raw + new_body)
        print(f"ok {slug}  [详解{len(data['产品详解'])}字 / 盈利{len(data.get('盈利模式',''))}字 / 学到{len(data.get('你能学到什么',''))}字]")
        done += 1
        time.sleep(0.3)
    print(f"\nDONE={done} SKIP={skip} FAIL={fail}")

if __name__ == "__main__":
    main()
