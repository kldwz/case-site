import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trustmrr_common import parse_md, passes_filter, fmt_money

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trustmrr_cache")
CASES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "content", "cases")

existing = {f[:-3] for f in os.listdir(CASES) if f.endswith(".md")}
cands = []
for fn in os.listdir(CACHE):
    if not fn.endswith(".md"):
        continue
    slug = fn[:-3]
    if slug in existing:
        continue
    try:
        facts = parse_md(os.path.join(CACHE, fn))
    except Exception as e:
        continue
    ok, reason = passes_filter(facts)
    if not ok:
        continue
    cands.append((facts.get("rev_all", 0), facts.get("mrr", 0), facts.get("rev_30d", 0), slug, facts.get("name",""), reason))

cands.sort(reverse=True)
print(f"passing candidates (not yet imported): {len(cands)}")
for rev_all, mrr, r30, slug, name, reason in cands[:20]:
    print(f"{slug:30s} | {name[:24]:24s} | all={fmt_money(rev_all)} mrr={fmt_money(mrr)} r30={fmt_money(r30)}")
