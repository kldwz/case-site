#!/usr/bin/env python3
"""把 case-site 的案例 Markdown 写成飞书知识库（wiki）下的 docx 文档。

用法：
    export FEISHU_APP_ID=cli_xxx
    export FEISHU_APP_SECRET=xxx
    export FEISHU_WIKI_NODE_TOKEN=T6GHwFC1JiZvvpkkNuBcQ9QqnSg

    python3 scripts/feishu_wiki.py --dry-run            # 只解析，不写飞书
    python3 scripts/feishu_wiki.py --limit 10           # 写 cases.tsv 前 10 篇
    python3 scripts/feishu_wiki.py --slugs shipfast,flomo

依赖：requests；权限：应用需具备 docx:document / wiki:wiki，并被加为知识库成员（可编辑）。
"""

import argparse
import json
import os
import random
import re
import string
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "src" / "content" / "cases"
ASSETS_DIR = ROOT / "src" / "assets"
TSV = ROOT / "cases.tsv"
STATE_FILE = ROOT / "logs" / "feishu_wiki_state.json"

BASE = "https://open.feishu.cn/open-apis"

# ---------------- 基础 HTTP ----------------


class FeishuError(Exception):
    pass


class Client:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self._token = None
        self.session = requests.Session()

    def token(self):
        if self._token:
            return self._token
        r = self.session.post(
            f"{BASE}/auth/v3/tenant_access_token/internal",
            json={"app_id": self.app_id, "app_secret": self.app_secret},
            timeout=20,
        )
        d = r.json()
        if d.get("code") != 0:
            raise FeishuError(f"取 token 失败: {d}")
        self._token = d["tenant_access_token"]
        return self._token

    def call(self, method, path, **kw):
        for attempt in range(6):
            r = self.session.request(
                method,
                f"{BASE}{path}",
                headers={"Authorization": "Bearer " + self.token()},
                timeout=40,
                **kw,
            )
            d = r.json()
            code = d.get("code")
            if code == 0:
                return d.get("data", {})
            if code in (1254290, 1254291, 99991400):  # 限流
                time.sleep(2 * (attempt + 1))
                continue
            raise FeishuError(f"{method} {path} -> {d}")
        raise FeishuError(f"{method} {path} 重试后仍失败（限流）")


# ---------------- Markdown 解析 ----------------

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def split_frontmatter(text):
    m = FM_RE.match(text)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[m.end() :]


INLINE_RE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\)|https?://\S+)")


def inline_elements(s):
    """返回 docx text_run 元素列表。"""
    out = []
    pos = 0
    for m in INLINE_RE.finditer(s):
        if m.start() > pos:
            out.append({"text_run": {"content": s[pos : m.start()]}})
        tok = m.group(0)
        if tok.startswith("**") and tok.endswith("**"):
            out.append(
                {"text_run": {"content": tok[2:-2], "text_element_style": {"bold": True}}}
            )
        elif tok.startswith("`") and tok.endswith("`"):
            out.append(
                {
                    "text_run": {
                        "content": tok[1:-1],
                        "text_element_style": {"inline_code": True},
                    }
                }
            )
        elif tok.startswith("["):
            mm = re.match(r"\[([^\]]+)\]\(([^)]+)\)", tok)
            out.append(
                {
                    "text_run": {
                        "content": mm.group(1),
                        "text_element_style": {"link": {"url": mm.group(2)}},
                    }
                }
            )
        else:
            out.append(
                {"text_run": {"content": tok, "text_element_style": {"link": {"url": tok}}}}
            )
        pos = m.end()
    if pos < len(s):
        out.append({"text_run": {"content": s[pos:]}})
    return out or [{"text_run": {"content": ""}}]


def text_block(content, list_type=None):
    b = {"block_type": 2, "text": {"elements": inline_elements(content), "style": {}}}
    return b


def parse_body(md):
    """把 markdown 正文解析成 (blocks) ，其中 table 用特殊 dict 标记，稍后单独创建。"""
    blocks = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if not s:
            i += 1
            continue

        # 代码块
        if s.startswith("```"):
            lang = s[3:].strip()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            blocks.append(
                {
                    "block_type": 14,
                    "code": {"language": lang_code(lang), "wrap_content": "\n".join(buf)},
                }
            )
            continue

        # 分隔线
        if re.fullmatch(r"-{3,}|\*{3,}", s):
            blocks.append({"block_type": 22, "divider": {}})
            i += 1
            continue

        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)", s)
        if m:
            level = len(m.group(1))
            bt = {1: 3, 2: 4, 3: 5}.get(level, 6)
            blocks.append(
                {
                    "block_type": bt,
                    f"heading{bt - 2}": {
                        "elements": inline_elements(m.group(2).strip()),
                        "style": {},
                    },
                }
            )
            i += 1
            continue

        # 表格
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*[-:| ]+\|", lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            blocks.append({"_table": parse_table(rows)})
            continue

        # 引用
        if s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            body = " ".join(x for x in buf if x)
            blocks.append(
                {"block_type": 34, "quote_container": {}, "_children": [text_block(body)]}
            )
            continue

        # 列表
        m = re.match(r"^[-*+]\s+(.*)", s)
        if m:
            blocks.append(
                {
                    "block_type": 12,
                    "bullet": {
                        "elements": inline_elements(m.group(1).strip()),
                        "style": {},
                    },
                }
            )
            i += 1
            continue

        m = re.match(r"^\d+[.)]\s+(.*)", s)
        if m:
            blocks.append(
                {
                    "block_type": 13,
                    "ordered": {
                        "elements": inline_elements(m.group(1).strip()),
                        "style": {},
                    },
                }
            )
            i += 1
            continue

        # 图片：本地图缺失就跳过，只记日志
        if s.startswith("!["):
            alt = re.match(r"!\[([^\]]*)\]", s)
            print(f"  · 跳过图片 {alt.group(1) if alt else ''}")
            i += 1
            continue

        blocks.append(text_block(s))
        i += 1

    return blocks


LANG_MAP = {
    "python": 11,
    "py": 11,
    "js": 12,
    "javascript": 12,
    "ts": 13,
    "typescript": 13,
    "bash": 17,
    "sh": 17,
    "shell": 17,
    "json": 14,
    "go": 18,
    "java": 19,
    "sql": 20,
    "html": 21,
    "css": 22,
}


def lang_code(lang):
    return LANG_MAP.get(lang.lower(), 1)  # 1 = plaintext


def parse_table(rows):
    def cells(row):
        row = row.strip().strip("|")
        return [c.strip() for c in row.split("|")]

    data = [cells(r) for r in rows if not re.fullmatch(r"[-:| ]+", r.replace("|", "|"))]
    data = [r for r in data if not all(re.fullmatch(r":?-{2,}:?", c or "-") for c in r)]
    if not data:
        return None
    ncol = max(len(r) for r in data)
    data = [r + [""] * (ncol - len(r)) for r in data]
    return data


# ---------------- 写入飞书 ----------------


def archive_table(fm):
    rows = [["项目", "内容"]]
    for key in ("一句话", "营收模式", "月收入估算", "流量来源", "分类", "数据口径", "原文链接", "创始人地区"):
        v = fm.get(key)
        if v:
            rows.append([key, v])
    return rows if len(rows) > 1 else None


def nid():
    return "".join(random.choices(string.ascii_letters, k=1)) + "".join(
        random.choices(string.ascii_letters + string.digits, k=25)
    )


def flatten(block, out):
    """把一块（含嵌套/表格）摊平成 descendants 列表，返回临时 block_id。"""
    tid = nid()

    if "_table" in block:
        data = block["_table"]
        nrow, ncol = len(data), len(data[0])
        cell_ids = []
        for r in range(nrow):
            for c in range(ncol):
                cid, xid = nid(), nid()
                cell_ids.append(cid)
                out.append(
                    {"block_id": cid, "block_type": 32, "table_cell": {}, "children": [xid]}
                )
                out.append(
                    {
                        "block_id": xid,
                        "block_type": 2,
                        "text": {"elements": inline_elements(data[r][c]), "style": {}},
                    }
                )
        out.append(
            {
                "block_id": tid,
                "block_type": 31,
                "table": {
                    "property": {
                        "row_size": nrow,
                        "column_size": ncol,
                        "column_width": [max(80, int(600 / ncol))] * ncol,
                        "header_row": True,
                    },
                    "cells": cell_ids,
                },
                "children": cell_ids,
            }
        )
        return tid

    d = {"block_id": tid, "block_type": block["block_type"]}
    child_ids = []
    for k, v in block.items():
        if k in ("block_type", "_children"):
            continue
        d[k] = v
    for ch in block.get("_children", []):
        child_ids.append(flatten(ch, out))
    if child_ids:
        d["children"] = child_ids
    out.append(d)
    return tid


def write_doc(cli, doc_id, blocks, chunk=8):
    index = 0
    buf = []
    for b in blocks:
        buf.append(b)
        if len(buf) >= chunk:
            index = _flush(cli, doc_id, buf, index)
            buf = []
    if buf:
        _flush(cli, doc_id, buf, index)


def _flush(cli, doc_id, blocks, index):
    descendants = []
    top_ids = [flatten(b, descendants) for b in blocks]
    cli.call(
        "POST",
        f"/docx/v1/documents/{doc_id}/blocks/{doc_id}/descendant",
        json={"children_id": top_ids, "index": index, "descendants": descendants},
    )
    time.sleep(0.3)
    return index + len(top_ids)


# ---------------- 主流程 ----------------


def load_order(limit=None):
    order = []
    if TSV.exists():
        for line in TSV.read_text(encoding="utf-8").splitlines()[1:]:
            cols = line.split("\t")
            if cols:
                order.append(cols[0].strip())
    slugs = []
    files = {p.stem: p for p in CONTENT_DIR.glob("*.md")}
    for title in order:
        # cases.tsv 里是标题，需要按 frontmatter name 匹配到文件
        for stem, p in files.items():
            fm, _ = split_frontmatter(p.read_text(encoding="utf-8"))
            if fm.get("name") == title and p not in slugs:
                slugs.append(p)
                break
    # cases.tsv 只登记了部分案例，剩下的按文件名补在后面
    for p in sorted(files.values()):
        if p not in slugs:
            slugs.append(p)
    return slugs[:limit] if limit else slugs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--slugs", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--parent", default=os.environ.get("FEISHU_WIKI_NODE_TOKEN", ""))
    args = ap.parse_args()

    if args.slugs:
        paths = [CONTENT_DIR / f"{s.strip()}.md" for s in args.slugs.split(",")]
    else:
        paths = load_order(args.limit)

    print(f"待处理 {len(paths)} 篇")

    if args.dry_run:
        for p in paths:
            fm, body = split_frontmatter(p.read_text(encoding="utf-8"))
            blocks = parse_body(body)
            print(f"[dry-run] {fm.get('name', p.stem)}: {len(blocks)} blocks")
        return

    app_id = os.environ["FEISHU_APP_ID"]
    app_secret = os.environ["FEISHU_APP_SECRET"]
    parent = args.parent
    if not parent:
        sys.exit("缺少 FEISHU_WIKI_NODE_TOKEN")

    cli = Client(app_id, app_secret)
    node = cli.call("GET", f"/wiki/v2/spaces/get_node?token={parent}")
    space_id = node["node"]["space_id"]
    print(f"知识库 space_id={space_id}, 父节点={parent}")

    state = {}
    if STATE_FILE.exists():
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))

    for p in paths:
        fm, body = split_frontmatter(p.read_text(encoding="utf-8"))
        title = fm.get("name") or p.stem
        if state.get(p.stem):
            print(f"跳过（已写）{title} -> {state[p.stem]}")
            continue
        print(f"写入：{title}")
        created = cli.call(
            "POST",
            f"/wiki/v2/spaces/{space_id}/nodes",
            json={
                "obj_type": "docx",
                "node_type": "origin",
                "parent_node_token": parent,
                "title": title,
            },
        )
        node_token = created["node"]["node_token"]
        doc_id = created["node"]["obj_token"]

        blocks = []
        at = archive_table(fm)
        if at:
            blocks.append({"_table": at})
        blocks += parse_body(body)
        write_doc(cli, doc_id, blocks)

        state[p.stem] = node_token
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(
            json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"  ✓ https://feishu.cn/wiki/{node_token}")


if __name__ == "__main__":
    main()
