#!/usr/bin/env python3
"""Concurrent, resumable fetcher for TrustMRR per-startup Markdown profiles.

Each startup at https://trustmrr.com/startup/<slug> also exposes a Markdown
"Public AI-agent Markdown profile" at https://trustmrr.com/startup/<slug>.md
with Stripe-verified revenue. This script downloads all of them into
pipeline/trustmrr_cache/<slug>.md, resuming from whatever is already cached.

Usage:
  python3 fetch_trustmrr.py [--limit N] [--workers N] [--offset N]
"""
import argparse
import os
import sys
import time
import urllib.request
import urllib.error
import concurrent.futures as cf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG_FILE = os.path.join(ROOT, "pipeline", "trustmrr_slugs.txt")
CACHE_DIR = os.path.join(ROOT, "pipeline", "trustmrr_cache")
FAIL_FILE = os.path.join(ROOT, "pipeline", "trustmrr_failed.txt")

PROXY = "http://127.0.0.1:1082"
# If the proxy is down we fall back to direct; try both per request.
USE_PROXY_FIRST = True

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; case-site-importer/1.0)",
    "Accept": "text/markdown,text/plain,*/*",
}


import threading
import time

_lk = threading.Lock()
_last_req = [0.0]
_cooldown = [0.0]
_MIN_GAP = 0.5          # min seconds between request starts
_COOLDOWN = 45.0        # seconds to wait after a 429

def _acquire():
    while True:
        with _lk:
            now = time.time()
            if now < _cooldown[0]:
                wait = _cooldown[0] - now
            elif now - _last_req[0] < _MIN_GAP:
                wait = _MIN_GAP - (now - _last_req[0])
            else:
                _last_req[0] = now
                return
        time.sleep(max(0.05, min(wait, 5)))

def _throttle():
    with _lk:
        _cooldown[0] = max(_cooldown[0], time.time() + _COOLDOWN)

def _fetch_url(url, timeout=40):
    """Try direct then proxy; raise on non-200; honor 429 with cooldown."""
    last_err = None
    for via_proxy in ([False, True] if not USE_PROXY_FIRST else [True, False]):
        try:
            handlers = []
            if via_proxy:
                from urllib.request import ProxyHandler
                handlers.append(ProxyHandler({"https": PROXY, "http": PROXY}))
            opener = urllib.request.build_opener(*handlers)
            req = urllib.request.Request(url, headers=HEADERS)
            with opener.open(req, timeout=timeout) as r:
                return r.read(), getattr(r, "status", 200)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                _throttle()
                last_err = e
                continue
            last_err = e
            continue
        except Exception as e:  # noqa
            last_err = e
            continue
    raise last_err or RuntimeError("fetch failed")

import threading
import time
import random

_lk = threading.Lock()
_last_req = [0.0]
_cooldown = [0.0]
_MIN_GAP = 1.0
_COOLDOWN = 30.0

def _acquire():
    while True:
        with _lk:
            now = time.time()
            if now < _cooldown[0]:
                wait = _cooldown[0] - now
            elif now - _last_req[0] < _MIN_GAP:
                wait = _MIN_GAP - (now - _last_req[0])
            else:
                _last_req[0] = now
                return
        time.sleep(max(0.05, min(wait, 3)))

def _throttle():
    with _lk:
        _cooldown[0] = max(_cooldown[0], time.time() + _COOLDOWN)

def _fetch_url(url, timeout=45, max_tries=5):
    """Try direct then proxy; on 429 wait out cooldown and retry; on
    transient connection errors retry with short backoff. Returns bytes."""
    last_err = None
    for attempt in range(max_tries):
        for via_proxy in ([False, True] if not USE_PROXY_FIRST else [True, False]):
            try:
                handlers = []
                if via_proxy:
                    from urllib.request import ProxyHandler
                    handlers.append(ProxyHandler({"https": PROXY, "http": PROXY}))
                opener = urllib.request.build_opener(*handlers)
                req = urllib.request.Request(url, headers=HEADERS)
                with opener.open(req, timeout=timeout) as r:
                    return r.read()
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    _throttle()
                    # sleep until past cooldown (+jitter) then retry whole loop
                    sleep_for = max(0.0, _cooldown[0] - time.time()) + random.uniform(1, 4)
                    time.sleep(sleep_for)
                    last_err = ("429", str(e))
                    break  # retry outer loop (re-acquire paths)
                last_err = ("http%d" % e.code, str(e))
                continue
            except Exception as e:  # noqa  connection reset / timeout / proxy 000
                last_err = ("conn", str(e)[:80])
                time.sleep(2 + attempt)
                break
    raise RuntimeError("fetch failed: %s" % (last_err,))

def fetch_one(slug):
    url = f"https://trustmrr.com/startup/{slug}.md"
    out = os.path.join(CACHE_DIR, f"{slug}.md")
    if os.path.exists(out) and os.path.getsize(out) > 200:
        return ("cached", slug)
    _acquire()
    try:
        data = _fetch_url(url)
    except Exception as e:  # noqa
        kind = "fail-429" if "429" in str(e) else "fail-conn" if "conn" in str(e) else "fail"
        return (kind, f"{slug}|{e}")
    text = data.decode("utf-8", "replace")
    if "Public AI-agent Markdown profile" not in text and not text.startswith("# "):
        return ("skip-nonprofile", slug)
    if len(text) < 200:
        return ("skip-tooshort", slug)
    with open(out, "wb") as f:
        f.write(data)
    return ("ok", slug)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="max slugs to process")
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()

    with open(SLUG_FILE) as f:
        slugs = [s.strip() for s in f if s.strip()]
    slugs = slugs[args.offset:]
    if args.limit:
        slugs = slugs[: args.limit]

    os.makedirs(CACHE_DIR, exist_ok=True)

    stats = {}
    t0 = time.time()
    done = 0
    total = len(slugs)

    def record(res):
        nonlocal done
        kind, slug = res
        stats[kind] = stats.get(kind, 0) + 1
        done += 1
        if done % 200 == 0 or done == total:
            el = time.time() - t0
            print(f"[{done}/{total}] {el:.0f}s  {stats}", flush=True)

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(fetch_one, s) for s in slugs]
        for fut in cf.as_completed(futs):
            record(fut.result())

    # Persist failures for retry
    if "fail" in stats or "skip-nonprofile" in stats or "skip-tooshort" in stats:
        print("Some entries did not download cleanly; rerun to retry cached ones.",
              file=sys.stderr)

    print("DONE", stats, flush=True)


if __name__ == "__main__":
    main()
