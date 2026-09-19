#!/usr/bin/env python3
"""Archive non-conforming cases out of src/content/cases/ into _excluded/.

READS pipeline/_to_archive.txt (one slug per line, produced by audit_cases.py).
For each slug: move src/content/cases/<slug>.md  ->  _excluded/cases/<slug>.md
              move public/cases/<slug>/*           ->  _excluded/public/<slug>  (if present)
Nothing is deleted; everything is reversible. Run audit_cases.py first.

This script is idempotent: slugs already in _excluded/ are skipped.
"""
import os, shutil, datetime

CASE_SITE = "/Users/hxw/codebuddy/case-site"
SRC = os.path.join(CASE_SITE, "src/content/cases")
PUB = os.path.join(CASE_SITE, "public/cases")
EXC = os.path.join(CASE_SITE, "_excluded")
EXC_CASES = os.path.join(EXC, "cases")
EXC_PUB = os.path.join(EXC, "public")
LIST = os.path.join(CASE_SITE, "pipeline/_to_archive.txt")
LOG = os.path.join(CASE_SITE, "pipeline/_archive_log.txt")

os.makedirs(EXC_CASES, exist_ok=True)
os.makedirs(EXC_PUB, exist_ok=True)

slugs = [s.strip() for s in open(LIST, encoding="utf8") if s.strip()]
moved_md, moved_pub, skipped = 0, 0, 0
log = [f"# archive run {datetime.date.today().isoformat()}  (total {len(slugs)} slugs)"]
for slug in slugs:
    src_md = os.path.join(SRC, slug + ".md")
    dst_md = os.path.join(EXC_CASES, slug + ".md")
    if not os.path.exists(src_md):
        skipped += 1
        log.append(f"SKIP  {slug}  (src missing)")
        continue
    if os.path.exists(dst_md):
        skipped += 1
        log.append(f"SKIP  {slug}  (already archived)")
        continue
    shutil.move(src_md, dst_md)
    moved_md += 1
    log.append(f"MOVE  {slug}.md  -> _excluded/cases/")
    # images
    src_pub = os.path.join(PUB, slug)
    if os.path.isdir(src_pub):
        dst_pub = os.path.join(EXC_PUB, slug)
        shutil.move(src_pub, dst_pub)
        moved_pub += 1
        log.append(f"      public/cases/{slug}/ -> _excluded/public/")

open(LOG, "a", encoding="utf8").write("\n".join(log) + "\n")
print(f"moved md: {moved_md}, moved image dirs: {moved_pub}, skipped: {skipped}")
print(f"remaining cases in src/content/cases: {len([f for f in os.listdir(SRC) if f.endswith('.md')])}")
