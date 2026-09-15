#!/usr/bin/env python3
# patch_gh_stats.py - 等 GitHub API 限流解除后抓取精确数据，回填 __GH__ 占位符 + 追加 tsv
import json, os, re, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS = os.path.join(ROOT, "pipeline", "oss_facts.json")
CASES = os.path.join(ROOT, "src", "content", "cases")
TSV = os.path.join(ROOT, "cases.tsv")

def gh_get(path):
    url = "https://api.github.com" + path
    req = urllib.request.Request(url, headers={"User-Agent": "case-site", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def rate_remaining():
    try:
        d = gh_get("/rate_limit")["rate"]
        return d["remaining"], d["reset"]
    except Exception:
        return 0, int(time.time()) + 60

def wait_for_quota(n):
    rem, reset = rate_remaining()
    if rem < n:
        sleep_for = max(reset - int(time.time()), 1) + 5
        print(f"  GitHub 限流中：剩余 {rem}，等待 {sleep_for}s 至重置…")
        time.sleep(min(sleep_for, 60*60))

def fetch_repo(repo):
    d = gh_get(f"/repos/{repo}")
    lic = (d.get("license") or {}).get("spdx_id") or "自定义"
    created = (d.get("created_at") or "")[:10]
    return {
        "stars": d.get("stargazers_count"),
        "forks": d.get("forks_count"),
        "lic": lic,
        "created": created,
    }

def patch_md(slug, plat):
    p = os.path.join(CASES, slug + ".md")
    lines = open(p, encoding="utf-8").read().splitlines()
    out = []
    for ln in lines:
        if ln.startswith("平台数据:"):
            out.append(f"平台数据: GitHub {plat['stars']:,} star · {plat['forks']:,} fork · {plat['lic']} · 仓库创建于 {plat['created']}（2026-09-15 抓取）")
        else:
            out.append(ln)
    open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"  patched {slug}: {plat['stars']:,} star / {plat['forks']:,} fork / {plat['lic']}")

def fm_field(path, key):
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"^%s:\s*(.+)$" % re.escape(key), txt, re.M)
    return m.group(1).strip() if m else ""

def append_tsv():
    rows = []
    facts = json.load(open(FACTS, encoding="utf-8"))
    for f in facts:
        slug = f["slug"]
        mp = os.path.join(CASES, slug + ".md")
        if not os.path.exists(mp):
            continue
        oneliner = fm_field(mp, "一句话")
        note = f"开源变现线：{oneliner}"
        rows.append("\t".join([f["name"], "2026-09-15", "开源变现线", note, "✅", "❌", "❌", "❌"]))
    if not rows:
        print("  无 tsv 行"); return
    with open(TSV, "a", encoding="utf-8") as fh:
        fh.write("\n" + "\n".join(rows) + "\n")
    print(f"  appended {len(rows)} 行到 cases.tsv")

def main():
    facts = json.load(open(FACTS, encoding="utf-8"))
    pending = [f for f in facts if f.get("github_note") == "__GH__"]
    print(f"需回填 GitHub 数据的案例：{len(pending)}")
    wait_for_quota(len(pending))
    for f in pending:
        for attempt in range(5):
            try:
                plat = fetch_repo(f["repo"])
                patch_md(f["slug"], plat)
                break
            except Exception as e:
                rem, reset = rate_remaining()
                if rem < 1:
                    print(f"  {f['slug']} 限流，等待…")
                    time.sleep(max(reset - int(time.time()), 1) + 5)
                else:
                    print(f"  {f['slug']} 抓取失败重试: {e}")
                    time.sleep(3)
        else:
            print(f"  !! {f['slug']} 多次失败，跳过")
    append_tsv()
    print("patch + tsv 完成")

if __name__ == "__main__":
    main()
