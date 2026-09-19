#!/usr/bin/env python3
"""Bundle the curated covers INTO the mini-program package as shrunk JPEGs.

Why: the mini-program previously hot-linked covers from GitHub Pages
(kldwz.github.io/case-site/...). If that repo vanishes, images go blank, and
production needs the domain whitelisted. Bundling locally removes both risks.

The main package caps at 2 MB. Code+data+assets+configs are ~0.6 MB, leaving
~1.3 MB for covers -> at ~14 KB each that is room for ~80 covers with headroom.
We resize to 260px wide + re-encode JPEG q7.

Run after curated_slugs.txt / source covers change.
"""
import os, subprocess, shutil, shutil

CASE_SITE = "/Users/hxw/codebuddy/case-site"
MINI = "/Users/hxw/codebuddy/case-miniprogram"
OUT = os.path.join(MINI, "covers")
os.makedirs(OUT, exist_ok=True)
WEB = os.path.join(CASE_SITE, "public", "mini", "covers")
os.makedirs(WEB, exist_ok=True)
WEB = os.path.join(CASE_SITE, "public", "mini", "covers")
os.makedirs(WEB, exist_ok=True)

slugs = [s.strip() for s in open(os.path.join(CASE_SITE, "pipeline/curated_slugs.txt"), encoding="utf-8") if s.strip()]
made = miss = 0
total = 0
missing = []
for slug in slugs:
    src = None
    for ext in ("site.webp", "site.png"):
        p = os.path.join(CASE_SITE, "public", "cases", slug, ext)
        if os.path.exists(p):
            src = p
            break
    if not src:
        miss += 1
        missing.append(slug)
        continue
    dest = os.path.join(OUT, slug + ".jpg")
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", src, "-vf", "scale=260:-1", "-q:v", "7", dest],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if r.returncode == 0 and os.path.exists(dest):
        total += os.path.getsize(dest)
        made += 1
        try:
            shutil.copy(dest, os.path.join(WEB, slug + ".jpg"))
        except Exception as e:
            print("COPY FAIL", slug, e)
    else:
        print("FAIL", slug)

print(f"covers made={made} missing={miss} {missing}")
print(f"covers total: {total/1024/1024:.2f} MB  -> avg { (total/made/1024) if made else 0:.0f} KB each")
