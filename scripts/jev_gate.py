#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jev_gate.py — 公众号草稿发布前门禁：用 Jev(score + noul) 给草稿打
「爆款潜力 / 清晰度 / 发布就绪度」三维判断，输出 PASS / REVIEW 结论。

依赖：Python 标准库即可（urllib）。key 从受保护文件读取，不进环境变量、不进日志。
用法：python3 scripts/jev_gate.py <草稿md路径>
"""
import json
import sys
import os
import urllib.request

KEY_PATH = os.path.expanduser("~/.workbuddy/.secrets/typesafe.key")
API = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-1.13.0"


def read_key():
    with open(KEY_PATH) as f:
        return f.read().strip()


def extract(md_path):
    text = open(md_path, encoding="utf-8").read()
    title = ""
    body = []
    for ln in text.splitlines():
        if ln.startswith("# ") and not title:
            title = ln[2:].strip()
        else:
            body.append(ln)
    body_text = "\n".join(body).strip()
    # 控制上下文：Jev 直连 state+最长question 有上限，截断保安全
    if len(body_text) > 3000:
        body_text = body_text[:3000] + "...(truncated)"
    return title, body_text


def build_request(title, body):
    return {
        "model": MODEL,
        "state": {
            "article_title": title,
            "article_body_excerpt": body,
            "audience": "打工人/非技术小白，关注用AI给自己加杠杆",
        },
        "questions": {
            "viral_potential": {
                "type": "score",
                "instructions": "Score the viral/spread potential of this WeChat article for its target audience.",
                "criteria": [
                    "纯个人记录或流水账，没有可引发他人共鸣或转发的钩子",
                    "有信息增量，但缺少情绪钩子或具体场景，传播依赖读者主动兴趣",
                    "有明确的痛点/反差/第一人称动作，能引发'我也是'或'收藏'冲动",
                    "强情绪+具体数字/场景+结果反转，具备自发转发（朋友圈/群聊）潜质",
                ],
            },
            "clarity": {
                "type": "score",
                "instructions": "Score how clear and readable this article is for a non-technical working-class reader.",
                "criteria": [
                    "大量专业术语或抽象表述，非技术读者难以理解",
                    "意思能看懂，但结构松散或啰嗦，需要读者自己梳理",
                    "结构清晰、口语化，非技术读者能顺畅读完并理解",
                    "一眼就懂，人味足，且给出明确可执行的下一步",
                ],
            },
            "ready_to_publish": {
                "type": "noul",
                "instructions": "Is this draft publish-ready (clear CTA, no factual holes, reader knows what to do next)?",
                "criteria": {
                    "true": "草稿具备清晰CTA、内容无事实硬伤、读者知道看完该做什么",
                    "false": "草稿缺失关键要素（无CTA/有事实风险/读者不知所措）",
                },
            },
        },
    }


def call(req, key):
    data = json.dumps(req).encode("utf-8")
    r = urllib.request.Request(
        API,
        data=data,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def grade(ans):
    vp = ans["viral_potential"]
    cl = ans["clarity"]
    rt = ans["ready_to_publish"]
    rec = "PASS"
    notes = []
    if vp["score"] < 2:
        rec = "REVIEW"
        notes.append("爆款潜力偏低(<2)")
    if cl["score"] < 2:
        rec = "REVIEW"
        notes.append("清晰度偏低(<2)")
    if vp.get("confidence", 1) < 0.5 or cl.get("confidence", 1) < 0.5:
        rec = "REVIEW"
        notes.append("某项置信度低，建议人工复核")
    if rt["noul"] < 0.5:
        rec = "REVIEW"
        notes.append("发布就绪度低")
    return rec, notes


def main():
    md = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "/Users/hxw/wechat_workspace/documents/23-360-ai-pitfalls-guide.md"
    )
    title, body = extract(md)
    req = build_request(title, body)
    ans = call(req, read_key())
    rec, notes = grade(ans["answers"])
    print("标题:", title)
    print(
        "爆款潜力:",
        ans["answers"]["viral_potential"]["score"],
        "conf=",
        ans["answers"]["viral_potential"].get("confidence"),
    )
    print(
        "清晰度:",
        ans["answers"]["clarity"]["score"],
        "conf=",
        ans["answers"]["clarity"].get("confidence"),
    )
    print("发布就绪:", ans["answers"]["ready_to_publish"]["noul"])
    print("GATE:", rec, ("| " + "; ".join(notes)) if notes else " 全部达标")
    print("usage:", ans.get("usage"))


if __name__ == "__main__":
    main()
