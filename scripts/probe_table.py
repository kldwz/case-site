#!/usr/bin/env python3
"""探测飞书 docx 表格块的正确创建结构。"""
import os
import random
import string
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from feishu_wiki import Client  # noqa: E402

ID = "".join(random.choices(string.ascii_letters + string.digits, k=26))


def build(doc_id, parent, rows, ncol):
    tbl = "tbl" + ID[:23]
    cells, desc = [], []
    for r, row in enumerate(rows):
        for c in range(ncol):
            cid = f"c{r}{c}" + ID[:24]
            tid = f"t{r}{c}" + ID[:24]
            cells.append(cid)
            desc.append(
                {"block_id": cid, "block_type": 32, "table_cell": {}, "children": [tid]}
            )
            desc.append(
                {
                    "block_id": tid,
                    "block_type": 2,
                    "text": {"elements": [{"text_run": {"content": row[c]}}], "style": {}},
                }
            )
    desc.append(
        {
            "block_id": tbl,
            "block_type": 31,
            "table": {
                "property": {
                    "row_size": len(rows),
                    "column_size": ncol,
                    "column_width": [200] * ncol,
                    "header_row": True,
                    "merge_info": [],
                },
                "cells": cells,
            },
            "children": cells,
        }
    )
    return {
        "children_id": [tbl],
        "index": -1,
        "descendants": desc,
    }


def main():
    cli = Client(os.environ["FEISHU_APP_ID"], os.environ["FEISHU_APP_SECRET"])
    doc = cli.call("POST", "/docx/v1/documents", json={"title": "table probe"})
    doc_id = doc["document"]["document_id"]
    print("probe doc:", doc_id)
    payload = build(doc_id, doc_id, [["项目", "内容"], ["营收模式", "广告变现"]], 2)
    try:
        res = cli.call(
            "POST", f"/docx/v1/documents/{doc_id}/blocks/{doc_id}/descendant", json=payload
        )
        print("OK:", res)
    except Exception as e:
        print("FAIL:", e)


if __name__ == "__main__":
    main()
