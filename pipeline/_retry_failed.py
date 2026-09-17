import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_trustmrr as g

# Failed slugs captured from logs/bulk_100.log
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs", "bulk_100.log")
failed = set()
with open(LOG) as f:
    for line in f:
        line = line.strip()
        if line.startswith("llm-fail"):
            parts = line.split()
            if len(parts) >= 2:
                failed.add(parts[1].split("|")[0])

CASES = g.CASES_DIR
# Only retry slugs that are NOT already imported
todo = [s for s in sorted(failed) if not os.path.exists(os.path.join(CASES, f"{s}.md"))]
print(f"failed-in-log={len(failed)} todo-retry={len(todo)}", flush=True)

g.make_placeholder()
done = 0
MAX_RETRY = 6
for slug in todo:
    if os.path.exists(os.path.join(CASES, f"{slug}.md")):
        print(f"SKIP(exists) {slug}", flush=True)
        done += 1
        continue
    res = ("llm-fail", slug)
    for attempt in range(MAX_RETRY):
        res = g.build_case(slug)
        if res[0] != "llm-fail":
            break
        # exponential-ish backoff
        time.sleep(5 + attempt * 5)
    print(f"{res[0]:12s} {slug:40s}", flush=True)
    done += 1
    if done % 20 == 0:
        print(f"[progress] {done}/{len(todo)}", flush=True)
    time.sleep(2)
print("DONE", flush=True)
