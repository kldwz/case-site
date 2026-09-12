"""给 TrustMRR 来源的 6 篇案例截官网封面。

沿用 scripts/capture_covers.py 的标准：
  - 输出 public/cases/<slug>/site.png
  - 视口 1280x860，非全页截图
  - 每个站最多重试 5 次（这些站大多在墙外，代理偶发 503）
"""
import os, time
from playwright.sync_api import sync_playwright

PROXY = "http://127.0.0.1:1082"
OUT = "/Users/hxw/codebuddy/case-site/public/cases"

targets = [
    ("research-match", "https://www.researchmatch.site"),
    ("upvoty",         "https://upvoty.com"),
    ("campfirecrm",    "https://campfirecrm.com"),
    ("rankradar",      "https://rankradar.io"),
    ("dappsentry",     "https://dappsentry.com"),
    ("covai-cars",     "https://covai.es/"),
]

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def shoot(slug, url):
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    dest = os.path.join(d, "site.png")
    last = None
    for i in range(5):
        try:
            with sync_playwright() as p:
                b = p.chromium.launch(
                    args=["--no-sandbox", "--disable-dev-shm-usage"],
                    proxy={"server": PROXY},
                )
                ctx = b.new_context(user_agent=UA, viewport={"width": 1280, "height": 860})
                pg = ctx.new_page()
                pg.goto(url, wait_until="domcontentloaded", timeout=45000)
                time.sleep(3)
                try:
                    pg.wait_for_load_state("networkidle", timeout=8000)
                except Exception:
                    pass
                time.sleep(2)
                pg.screenshot(path=dest, full_page=False)
                b.close()
            print(f"OK  {slug} <- {url} ({os.path.getsize(dest)} 字节)", flush=True)
            return True
        except Exception as e:
            last = e
            print(f"try {i+1} FAIL {slug}: {type(e).__name__} {str(e)[:120]}", flush=True)
            time.sleep(2)
    print(f"GIVEUP {slug}: {last}", flush=True)
    return False


if __name__ == "__main__":
    for slug, url in targets:
        shoot(slug, url)
    print("DONE")
