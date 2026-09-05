#!/usr/bin/env python3
"""
write_cases.py - 从 inbox/YYYY-MM-DD.json 候选生成中文案例文章

用法:
  python3 pipeline/write_cases.py                 # 处理今天的 inbox
  python3 pipeline/write_cases.py --date 2026-09-05   # 处理指定日期
  python3 pipeline/write_cases.py --limit 3        # 最多处理 3 条（测试用）

流程:
  1. 读 inbox/<date>.json 候选
  2. 跳过已有案例（src/content/cases/ 里已存在 slug 或标题重复）
  3. 对每个候选，构造 prompt，用 `claude -p`（Claude Code 无头模式）生成案例
  4. 解析 frontmatter（8 字段）+ 正文，写入 src/content/cases/<slug>.md
  5. 追加一行到 cases.tsv（写完整篇文章后才追加）

数字规矩: 有公开来源标来源，没有写「未官方披露 / 未知」，绝不编造精确数字
"""
import argparse, json, os, re, subprocess, sys, datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
CASES_DIR = ROOT / "src" / "content" / "cases"
TSV = ROOT / "cases.tsv"
PUBLIC_CASES = ROOT / "public" / "cases"

# 8 个 frontmatter 字段（必须全部产出，未知填「未知」）
FIELDS = ["name", "一句话", "创始人地区", "营收模式", "月收入估算", "流量来源", "可迁移点", "原文链接", "数据口径", "分类", "封面"]

SYSTEM_PROMPT = """你是一个独立开发者收入案例库的资深编辑。你的任务：把一个「挣钱案例候选」写成一篇标准的中文案例文章。

硬性要求：
1. 语言简单明了，讲透三个问题：**它怎么赚钱、流量从哪来、普通人能学什么**
2. 所有数字必须有公开来源才写，没有就写「未官方披露 / 未知」，**绝对不编造精确数字**
3. 输出严格的 YAML frontmatter + Markdown 正文

frontmatter 必须包含以下 8 个字段（未知填「未知」）：
---
name: <案例名>
一句话: <一句话概括，讲清它靠什么赚钱>
创始人地区: <创始人/团队地区；未知填「未知」>
营收模式: <怎么赚钱，如广告/订阅/买断>
月收入估算: <有来源写具体数字+来源；没有写「未官方披露」>
流量来源: <流量从哪来，如SEO/口碑/社区>
可迁移点: <普通人能学到的 2-4 点，顿号分隔>
原文链接: <候选的 link>
数据口径: <数据来源说明，如「trustmrr 公开数据」或「未官方披露」>
分类: <标签，如「工具站 / 广告变现 / 英文」或「Chrome 插件 / 开源捐赠 / 英文」>
封面: /cases/<slug>/site.png
---

正文结构（Markdown，参考示例风格）：
# <案例名>：<吸引人的标题>

## 产品/网站是什么
用 2-3 段讲清楚这是什么东西，普通人能怎么用。

## 怎么赚的钱
拆解商业模式。有公开收入数字就写，没有就明确说「未官方披露」。

## 流量从哪来
讲流量来源，如 SEO / 社区 / 口碑 / 投放。

## 这个案例能学到什么
2-4 条可迁移的经验，对想做小生意/独立开发的人。

## 来源与数据
列出信息来源和数字口径。

> 一句话总结

注意：
- 正文用简洁中文，不要翻译腔
- 封面路径中的 <slug> 用英文小写连字符（如 dark-reader、calculator-net）
- 图片标签 `![案例名官网](/cases/<slug>/site.png)` 放在「产品/网站是什么」一节开头
"""


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", type=str, default=None, help="inbox 日期，默认今天")
    ap.add_argument("--limit", type=int, default=0, help="最多处理几条，0=全部")
    ap.add_argument("--claude-bin", type=str, default="claude", help="claude CLI 路径")
    return ap.parse_args()


def slugify(title):
    """把标题转成英文小写连字符 slug。中文标题用拼音? 不,用可读的英文名"""
    # 去掉 emoji / 特殊字符
    t = re.sub(r"[^\w\s-]", "", title).strip().lower()
    # 非 ASCII（中文等）直接跳过，用域名或随机
    ascii_part = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    if ascii_part:
        return ascii_part[:60].strip("-")
    return f"case-{datetime.date.today().isoformat()}"


def get_domain_slug(candidate):
    """优先用域名当 slug 基础，最稳（如 covai.es -> covai）"""
    link = candidate.get("link", "")
    try:
        netloc = urlparse(link).netloc
        # 去掉 www. 和 端口，取主域名第一段
        domain = netloc.lower().replace("www.", "")
        domain = domain.split(":")[0].split(".")[0]
        if domain:
            return domain
    except Exception:
        pass
    return slugify(candidate.get("title", "case"))


def already_exists(candidate):
    """检查是否已有同名案例"""
    link = candidate.get("link", "")
    name = candidate.get("title", "").strip()
    if not name:
        return True
    for md in CASES_DIR.glob("*.md"):
        text = md.read_text()
        if link and link in text:
            return True
        if name.lower() in text.lower() and "name:" in text:
            return True
    return False


def build_prompt(candidate):
    """构造发送给 claude -p 的完整 prompt"""
    return f"""请把下面这个「挣钱案例候选」写成一篇标准中文案例文章。

候选信息：
- 标题：{candidate.get('title', '')}
- 链接：{candidate.get('link', '')}
- 来源：{candidate.get('source', '')}
- 摘要：{candidate.get('summary', '')}
- 发布时间：{candidate.get('published', '')}
- 地区：{candidate.get('category', '')}

请按系统要求输出案例文章（frontmatter + 正文）。
"""


def call_claude(prompt, claude_bin):
    """调用 claude -p 无头模式生成文章。--bare 隔离项目上下文，避免读到 CLAUDE.md 等污染输出"""
    try:
        r = subprocess.run(
            [claude_bin, "-p", prompt, "--output-format", "text", "--bare"],
            capture_output=True, text=True, timeout=300, check=False,
        )
        if r.returncode != 0:
            print(f"    ! claude 调用失败: {r.stderr[:200]}", file=sys.stderr)
            return None
        return r.stdout.strip()
    except subprocess.TimeoutExpired:
        print("    ! claude 调用超时（180s）", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(f"    ! 找不到 claude CLI: {claude_bin}", file=sys.stderr)
        return None


def parse_frontmatter(md_text):
    """从生成的文章提取 frontmatter 字段"""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", md_text, re.DOTALL)
    if not m:
        return None, md_text
    fm, body = m.group(1), m.group(2)
    fields = {}
    for line in fm.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields, body


def write_case(candidate, fields, body, slug, claude_bin, quiet=False):
    """写入 src/content/cases/<slug>.md，封面图占位"""
    # 校验必要字段
    missing = [f for f in ["name", "一句话", "营收模式"] if not fields.get(f)]
    if missing:
        print(f"    ! 缺字段 {missing}，跳过写入", file=sys.stderr)
        return False

    # 封面路径：用 slug 子目录
    cover = f"/cases/{slug}/site.png"
    if "封面" in fields:
        cover = fields["封面"]
    fields["封面"] = cover

    # 组装 frontmatter
    fm_lines = ["---"]
    for f in FIELDS:
        if f == "封面":
            continue
        fm_lines.append(f"{f}: {fields.get(f, '未知')}")
    fm_lines.append(f"封面: {cover}")
    fm_lines.append("---")

    content = "\n".join(fm_lines) + "\n\n" + body.strip() + "\n"

    # 写入
    md_path = CASES_DIR / f"{slug}.md"
    md_path.write_text(content)
    print(f"  ✓ 已写入 {md_path}")

    # 占位封面图目录
    pub = PUBLIC_CASES / slug
    pub.mkdir(parents=True, exist_ok=True)
    (pub / "site.png").write_text("", encoding="utf-8") if not (pub / "site.png").exists() else None

    return True


def append_to_tsv(candidate, fields):
    """追加一行到 cases.tsv（写完整篇文章后）"""
    name = fields.get("name", candidate.get("title", "")).strip().replace("\t", " ")
    date = datetime.date.today().isoformat()
    source = candidate.get("source", "").replace("\t", " ")
    note = fields.get("一句话", "")[:50].replace("\t", " ").replace("\n", " ")
    row = f"{name}\t{date}\t{source}\t{note}\t❌\t❌\t❌\n"
    TSV.parent.mkdir(parents=True, exist_ok=True)
    if not TSV.exists():
        TSV.write_text("标题\t创建时间\t来源\t备注\t推送网站\t推送公众号\t推送头条号\n", encoding="utf-8")
    with TSV.open("a", encoding="utf-8") as f:
        f.write(row)
    print(f"  ✓ 已追加到 cases.tsv: {name}")


def main():
    args = parse_args()
    date = args.date or datetime.date.today().isoformat()
    inbox_file = INBOX / f"{date}.json"
    if not inbox_file.exists():
        print(f"没有找到 inbox/{date}.json", file=sys.stderr)
        sys.exit(1)

    with open(inbox_file) as f:
        candidates = json.load(f)

    if args.limit:
        candidates = candidates[: args.limit]

    ok = 0
    for i, c in enumerate(candidates, 1):
        name = c.get("title", "")
        print(f"[{i}/{len(candidates)}] {name} ({c.get('source','')})")

        if already_exists(c):
            print(f"  - 跳过：已存在")
            continue

        slug = get_domain_slug(c)
        if not slug:
            print(f"  ! 无法生成 slug，跳过")
            continue

        prompt = build_prompt(c)
        out = call_claude(prompt, args.claude_bin)
        if not out:
            continue

        fields, body = parse_frontmatter(out)
        if not fields:
            print("    ! 输出格式错误（无 frontmatter），跳过")
            continue

        if not write_case(c, fields, body, slug, args.claude_bin):
            print("    ! 写入失败，不追加汇总表")
            continue
        append_to_tsv(c, fields)
        ok += 1

    print(f"\n完成：成功写入 {ok} 篇案例")


if __name__ == "__main__":
    main()
