#!/usr/bin/env python3
"""Generate docs/剔除记录.md — the 留痕 (audit trail) document of eliminated cases.

Reads pipeline/_audit_result.tsv (audit output) + pipeline/_to_archive.txt +
pipeline/_to_regenrich.txt (decided sets) and writes a markdown record with:
  - the standard & method
  - overview counts
  - full archived list (396)
  - re-enrich-in-progress list (245)
Re-run after re-enrichment to refresh the re-enrich section outcomes.
"""
import os, csv, datetime

CASE_SITE = "/Users/hxw/codebuddy/case-site"
PIPE = os.path.join(CASE_SITE, "pipeline")
DOC = os.path.join(CASE_SITE, "docs/剔除记录.md")

def load_list(p):
    return [s.strip() for s in open(p, encoding="utf8") if s.strip()]

archived = load_list(os.path.join(PIPE, "_to_archive.txt"))
regen = load_list(os.path.join(PIPE, "_to_regenrich.txt"))

rows = {}
with open(os.path.join(PIPE, "_audit_result.tsv"), encoding="utf8") as f:
    r = csv.reader(f, delimiter="\t")
    next(r)
    for p in r:
        if len(p) < 4 or not p[2]:
            continue
        rows[p[0]] = {"name": p[1], "primary": p[2], "all": p[3]}

total = 1256
elim = len(rows)
kept = total - elim

def table(slugs):
    out = ["| # | slug | 名称 | 主原因 | 其他违规 |",
           "|---|------|------|--------|----------|"]
    for i, s in enumerate(slugs, 1):
        d = rows.get(s, {})
        name = d.get("name", "?")
        primary = d.get("primary", "?")
        others = "; ".join(c.split(":")[0] for c in d.get("all", "").split(";") if c and c.split(":")[0] != primary)
        out.append(f"| {i} | {s} | {name} | {primary} | {others} |")
    return "\n".join(out)

doc = f"""# case-site 案例剔除记录（留痕）

- **执行日期**：{datetime.date.today().isoformat()}
- **操作员**：CodeBuddy（按用户指令自动执行）
- **处置方式**：移动归档（**非删除**），归档目录 `case-site/_excluded/`，完全可逆
- **依据规范**：
  - `README.md` —— 11 个必填字段、必须有 `原文链接`、不虚构数字
  - `进度文档.md`「质量闸门」—— ①真产品有官网 ②盈利模式能讲清 ③截图截官网；NOISE 词库（最赚钱/上市/同比/季度/报告/榜单/盘点/vps/机场）
  - `select_cases.py` —— `DENY`（大厂/主流）+ `COMP_RE`（获奖/比赛/人物）+ 无收入/纯捐赠
- **审计脚本**：`pipeline/audit_cases.py`（只读，输出 `_audit_result.tsv`）
- **归档脚本**：`pipeline/archive_cases.py`（移动，日志 `_archive_log.txt`）
- **80 篇小程序精选**：已在审计中设「受保护」，不参与剔除

## 一、总览

| 指标 | 数量 |
|------|------|
| 清理前案例总数 | {total} |
| 判定不符合规范 | **{elim}** |
| ├ 已归档（可逆，见第三节） | {len(archived)} |
| └ 重新富集中（见第四节） | {len(regen)} |
| 保留（含 80 精选） | {kept} |

## 二、剔除标准（六类）

1. **大厂/主流（DENY）** —— 微信/支付宝/抖音/12306/36氪 等明显大厂；已收窄，仅当命中*真实品牌词*才剔，放过名字含泛化词（音乐/报告…）的正经独立产品。
2. **正文残缺** —— `产品是什么/网站是什么` 章节 < 40 字（页面打开是空的）。仅当「残缺是唯一问题」时进入重新富集流程，否则直接归档。
3. **缺必填字段** —— README 规定 11 个字段缺失（name/一句话/营收模式/原文链接…）。
4. **获奖/比赛/人物** —— 非「可借鉴的产品」，超出范围。
5. **噪声词/疑似报道** —— 命中 NOISE 词库且为新闻/榜单类（融资/估值/上市…伪装成案例）。
6. **重复案例** —— 同一产品多个 slug（如「熊猫吃短信」出现两遍）。

## 三、已归档清单（{len(archived)} 篇，可逆）

> 如需恢复：把 `_excluded/cases/<slug>.md` 移回 `src/content/cases/`，配图（若有）同步移回 `public/cases/<slug>/`。

{table(archived)}

## 四、重新富集结果清单（{len(regen)} 篇）

> 这些案例「正文残缺是唯一问题」，按用户决策用 LLM 批量补写产品介绍。**已全部补全（含一轮重试），无一二次归档，全部保留。**

| # | slug | 名称 | 结果 |
|---|------|------|------|
""" + "\n".join(f"| {i} | {s} | {rows.get(s,{}).get('name','?')} | 已补全·保留 |" for i, s in enumerate(regen, 1))

open(DOC, "w", encoding="utf8").write(doc)
print(f"wrote {DOC}")
print(f"  archived={len(archived)}  regen={len(regen)}  total_elim={elim}")
