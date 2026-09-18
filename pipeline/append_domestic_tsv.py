#!/usr/bin/env python3
"""Idempotently append 国内实践 (domestic) cases to cases.tsv.

Mirrors append_trustmrr_tsv.py but for slugs listed in
domestic_candidates.json. Only appends rows whose case file exists and whose
标题 is not already present, so reruns are safe.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAND = os.path.join(ROOT, "pipeline", "domestic_candidates.json")
CASES_DIR = os.path.join(ROOT, "src", "content", "cases")
TSV = os.path.join(ROOT, "cases.tsv")
TODAY = "2026-09-17"


def frontmatter(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def main():
    slugs = set(c["slug"] for c in json.load(open(CAND, encoding="utf-8")))
    existing = set()
    rows = []
    if os.path.exists(TSV):
        with open(TSV, encoding="utf-8") as f:
            for line in f:
                rows.append(line.rstrip("\n"))
                first = line.split("\t")[0].strip()
                if first:
                    existing.add(first)

    added = 0
    for fn in sorted(os.listdir(CASES_DIR)):
        if not fn.endswith(".md"):
            continue
        slug = fn[:-3]
        if slug not in slugs:
            continue
        fm = frontmatter(os.path.join(CASES_DIR, fn))
        name = fm.get("name", "")
        if not name or name in existing:
            continue
        note = fm.get("平台数据", "")
        row = "\t".join([name, TODAY, "国内案例收录", note[:60],
                         "✅", "❌", "❌", "❌"])
        rows.append(row)
        existing.add(name)
        added += 1

    with open(TSV, "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")
    print(f"appended {added} domestic rows; tsv now {len(rows)} lines")


if __name__ == "__main__":
    main()
