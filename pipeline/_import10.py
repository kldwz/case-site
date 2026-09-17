import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_trustmrr as g

TOP10 = [
    "brand-on-demand-inc",
    "bustem-inc",
    "corsidia",
    "aeo-engine",
    "cartboss",
    "backpedal-ltd",
    "based-labs-ai",
    "calendesk",
    "avenue-ticketing-inc",
    "advise-so",
]

g.make_placeholder()
for slug in TOP10:
    if os.path.exists(os.path.join(g.CASES_DIR, f"{slug}.md")):
        print(f"SKIP(exists) {slug}")
        continue
    t0 = time.time()
    res = g.build_case(slug)
    print(f"{res[0]:12s} {slug:24s} {time.time()-t0:.1f}s")
