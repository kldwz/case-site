#!/usr/bin/env python3
"""Idempotently append TrustMRR-imported cases to cases.tsv.

cases.tsv columns: 标题 创建时间 来源 备注 推送网站 推送公众号 推送头条号 同步飞书
Only appends rows for TrustMRR slugs whose case file exists and whose
标题 is not already present, so reruns are safe.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG_FILE = os.path.join(ROOT, "pipeline", "trustmrr_slugs.txt")
CASES_DIR = os.path.join(ROOT, "src", "content", "cases")
TSV = os.path.join(ROOT, "cases.tsv")


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
    slugs = set()
    with open(SLUG_FILE) as f:
        slugs.update(s.strip() for s in f if s.strip())
    # existing titles
    existing = set()
    rows = []
    if os.path.exists(TSV):
        with open(TSV, encoding="utf-8") as f:
            for line in f:
                rows.append(line.rstrip("\n"))
                first = line.split("\t")[0].strip()
                if first:
                    existing.add(first)

    today = "2026-09-15"
    added = 0
    for fn in os.listdir(CASES_DIR):
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
        row = "\t".join([name, today, "TrustMRR 导入", note[:60],
                         "✅", "❌", "❌", "❌"])
        rows.append(row)
        existing.add(name)
        added += 1

    with open(TSV, "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")
    print(f"appended {added} rows; tsv now {len(rows)} lines")


if __name__ == "__main__":
    main()
