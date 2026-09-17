import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_trustmrr as g
from trustmrr_common import parse_md, passes_filter

CACHE = g.CACHE_DIR
CASES = g.CASES_DIR
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
MAX_RETRY = 4

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
    except Exception:
        continue
    ok, _ = passes_filter(facts)
    if not ok:
        continue
    cands.append((facts.get("rev_all", 0), slug))
cands.sort(reverse=True)
picks = [s for _, s in cands[:N]]
print(f"total candidates={len(cands)} importing={len(picks)}", flush=True)

g.make_placeholder()
done = 0
for slug in picks:
    if os.path.exists(os.path.join(CASES, f"{slug}.md")):
        print(f"SKIP(exists) {slug}", flush=True)
        done += 1
        continue
    res = ("llm-fail", slug)
    for attempt in range(MAX_RETRY):
        res = g.build_case(slug)
        if res[0] != "llm-fail":
            break
        time.sleep(3)
    print(f"{res[0]:12s} {slug:28s}", flush=True)
    done += 1
    if done % 25 == 0:
        print(f"[progress] {done}/{len(picks)}", flush=True)
    time.sleep(1)  # gentle pace to avoid rate limits
print("DONE", flush=True)
