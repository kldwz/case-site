import os, sys, time
from playwright.sync_api import sync_playwright

PROXY = "http://127.0.0.1:58350"
OUT = "/Users/hxw/codebuddy/case-site/public/cases"

targets = [
    ("prime-intellect", "https://www.primeintellect.ai"),
    ("origami",        "https://www.origami.chat"),
    ("medvi",          "https://www.medvi.org"),
    ("bland",          "https://www.bland.ai"),
    ("tern",           "https://www.tern-group.com"),
    ("sitegpt",        "https://www.sitegpt.ai"),
    ("paper",          "https://paper.design"),
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
                # try to wait for hero/visible text
                try:
                    pg.wait_for_load_state("networkidle", timeout=8000)
                except Exception:
                    pass
                time.sleep(2)
                pg.screenshot(path=dest, full_page=False)
                b.close()
            print(f"OK  {slug} <- {url}")
            return True
        except Exception as e:
            last = e
            print(f"try {i+1} FAIL {slug}: {type(e).__name__} {str(e)[:120]}")
            time.sleep(2)
    print(f"GIVEUP {slug}: {last}")
    return False

if __name__ == "__main__":
    for slug, url in targets:
        shoot(slug, url)
    print("DONE")
