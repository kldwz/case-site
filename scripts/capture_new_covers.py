#!/usr/bin/env python3
# 抓取 4 个新案例的官网首页截图到 public/cases/<slug>/site.png
import os, sys
from playwright.sync_api import sync_playwright

PROXY = "http://127.0.0.1:58350"
OUT = "/Users/hxw/codebuddy/case-site/public/cases"

targets = [
    ("higgsfield", "https://higgsfield.ai"),
    ("chatbase", "https://chatbase.co"),
    ("crowdreply", "https://crowdreply.io"),
    ("trendtrack", "https://www.trendtrack.io"),
]

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

def shoot(slug, url):
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    out = os.path.join(d, "site.png")
    last = None
    for attempt in range(5):
        try:
            with sync_playwright() as p:
                b = p.chromium.launch(args=["--no-sandbox"])
                pg = b.new_page(viewport={"width": 1280, "height": 900},
                                 user_agent=UA)
                pg.goto(url, wait_until="domcontentloaded", timeout=45000)
                pg.wait_for_timeout(4000)
                pg.screenshot(path=out, full_page=False)
                b.close()
            print(f"OK  {slug} <- {url}  ({os.path.getsize(out)} bytes)")
            return True
        except Exception as e:
            last = e
            print(f"retry {slug} ({attempt+1}/5): {e}")
    print(f"FAIL {slug}: {last}")
    return False

ok = 0
for slug, url in targets:
    if shoot(slug, url):
        ok += 1
print(f"\n=== captured {ok}/{len(targets)} ===")
sys.exit(0 if ok == len(targets) else 1)
