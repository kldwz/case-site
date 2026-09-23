#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jev_demos.py — 把 Jev 案例库里最贴「打工人AI自救」的 3 种用法跑给旺旺看：
  ① 规则门禁 (noul)：草稿是否违反我的写作规则（AI味词/编造数据/编号标题/早抛方案名词）
  ② 模型路由器 (choice)：给定任务，从我的模型阵容里挑最合适的
  ③ 标题钩子分类 (choice)：把我的真实标题按钩子类型打标，生成内容地图
key 从受保护文件读取，不进环境变量、不进日志。
"""
import json
import sys
import urllib.request
import os

KEY_PATH = os.path.expanduser("~/.workbuddy/.secrets/typesafe.key")
API = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-1.13.0"


def read_key():
    with open(KEY_PATH) as f:
        return f.read().strip()


def call(req):
    data = json.dumps(req).encode("utf-8")
    r = urllib.request.Request(
        API,
        data=data,
        headers={"Authorization": "Bearer " + read_key(), "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def wrap(resp):
    return resp.get("answers", {}), resp.get("usage", {})


# ───────────────────────── ① 规则门禁 ─────────────────────────
def demo_guard(md_path):
    text = open(md_path, encoding="utf-8").read()
    body = text[:3000]
    req = {
        "model": MODEL,
        "state": {"article_body": body},
        "questions": {
            "ai_flavor": {
                "type": "noul",
                "instructions": "这篇公众号草稿是否含有明显的「AI味」夸张/套路词（如「细思极恐」「动辄」「彻底改变」「让人脊背一凉」「堪称」等）？",
                "criteria": {
                    "true": "出现上述 AI 套路词或类似空洞夸张表达，读起来像机器生成",
                    "false": "语言平实接地气，无典型 AI 套路词",
                },
            },
            "fake_data": {
                "type": "noul",
                "instructions": "这篇草稿是否编造或未经核实就写了具体数字/案例（如凭空说『月入十万』『300个案例』却没有真实来源）？",
                "criteria": {
                    "true": "出现了无真实来源、疑似编造的具体数字或案例",
                    "false": "数字/案例都有真实依据或明确标注为举例",
                },
            },
            "numbered_title": {
                "type": "noul",
                "instructions": "这篇草稿是否使用了「一、二、三」式编号小标题（用户明确不喜欢这种 low 的排版）？",
                "criteria": {
                    "true": "正文用了 一、二、三 或 1. 2. 3. 编号标题",
                    "false": "用自然段落衔接，没有编号标题",
                },
            },
            "early_solution": {
                "type": "noul",
                "instructions": "这篇草稿是否在开头/困扰段就过早抛出方案名词（如 GitHub、Obsidian 等），而不是等说方案时自然引出？",
                "criteria": {
                    "true": "开头困扰段就提前抛出技术/产品名词",
                    "false": "方案名词在说方案时才自然出现",
                },
            },
        },
    }
    ans, usage = wrap(call(req))
    print("\n========== ① 规则门禁（noul，0~1 越高越「中招」）==========")
    for q, label in [
        ("ai_flavor", "AI味词"),
        ("fake_data", "编造数据"),
        ("numbered_title", "编号标题"),
        ("early_solution", "早抛方案名词"),
    ]:
        v = ans[q]["noul"]
        flag = "⚠️ 命中" if v >= 0.5 else "✅ 干净"
        print(f"  {label:<8}: {v:.2f}  {flag}")
    print("  usage:", usage)
    return ans


# ───────────────────────── ② 模型路由器 ─────────────────────────
def demo_router():
    roster = {
        "claude_ccr": "Claude（经 ccr 代理，强推理/长文/复杂任务）",
        "deepseek": "DeepSeek（中文通用，便宜，日常主力）",
        "siliconflow": "SiliconFlow（中文通用，便宜，备选）",
        "qwen_vl": "Qwen2.5-VL-72B（视觉/截图理解专用）",
        "jev": "Jev（结构化判断/路由/分类，极便宜）",
    }
    req = {
        "model": MODEL,
        "state": {"available_models": roster, "context": "一人公司主理人，成本敏感，已有上述模型订阅"},
        "questions": {
            "t_longform": {
                "type": "choice",
                "instructions": "任务：写一篇 2300 字公众号深度叙事长文。从可用模型里挑最合适的执行者。",
                "criteria": {k: v for k, v in roster.items() if k in ("claude_ccr", "deepseek", "siliconflow")},
            },
            "t_vision": {
                "type": "choice",
                "instructions": "任务：看一张产品截图并描述里面有什么、哪里有 bug。从可用模型里挑最合适的。",
                "criteria": {k: v for k, v in roster.items() if k in ("qwen_vl", "claude_ccr")},
            },
            "t_classify": {
                "type": "choice",
                "instructions": "任务：把 200 条读者留言按意图（售前/吐槽/退款/其他）分类，拿不准的标 needs_review。挑最合适的。",
                "criteria": {k: v for k, v in roster.items() if k in ("jev", "deepseek")},
            },
            "t_chat": {
                "type": "choice",
                "instructions": "任务：中文多轮闲聊答疑。挑最合适的。",
                "criteria": {k: v for k, v in roster.items() if k in ("deepseek", "siliconflow", "claude_ccr")},
            },
        },
    }
    ans, usage = wrap(call(req))
    print("\n========== ② 模型路由器（choice，概率最高=推荐）==========")
    task_labels = {
        "t_longform": "写长文",
        "t_vision": "看图说话",
        "t_classify": "留言分类",
        "t_chat": "中文闲聊",
    }
    for q, lbl in task_labels.items():
        a = ans[q]
        probs = a.get("probabilities", {})
        best = max(probs, key=probs.get)
        top3 = sorted(probs.items(), key=lambda x: -x[1])[:3]
        print(f"  [{lbl}] → 推荐 {best}  (conf={a.get('confidence'):.2f})")
        print(f"        {', '.join(f'{k}:{v:.2f}' for k,v in top3)}")
    print("  usage:", usage)
    return ans


# ───────────────────────── ③ 标题钩子分类 ─────────────────────────
def demo_hooks():
    titles = [
        ("09", "一人公司忙成狗？这两个开源项目白送你 270 个 AI 员工"),
        ("17", "我，赛博乞丐，每天打卡领 token，一个月没花一分钱"),
        ("20", "别人说 AI 副业月入十万，我查了 15 个方向的真实数据，做成 PDF 免费送"),
        ("23", "大厂流出的这份AI避坑指南，7个坑打工人全中"),
        ("13", "副业没方向？我用 WorkBuddy 扒了 300 多个老外赚钱案例，脑子终于通了"),
        ("12", "电脑卡了半年，我以为是老了，结果真凶是 C 盘只剩 5.8 G"),
    ]
    hook_types = {
        "pain_scene": "具体痛点场景（打工人/电脑卡/副业没方向）",
        "number": "具体数字钩子（7个坑/300案例/15方向/5.8G）",
        "first_person": "第一人称动词（我查了/我让AI/我以为是）",
        "reversal": "结果反转（脑子终于通了/真凶是C盘）",
        "suspense": "悬念提问（副业没方向？）",
    }
    req = {
        "model": MODEL,
        "state": {"hook_types": hook_types},
        "questions": {
            f"h_{num}": {
                "type": "choice",
                "instructions": f"这个公众号标题最主打哪种钩子类型？标题：「{t}」",
                "criteria": hook_types,
            }
            for num, t in titles
        },
    }
    ans, usage = wrap(call(req))
    print("\n========== ③ 标题钩子分类（choice，内容地图）==========")
    for num, t in titles:
        a = ans[f"h_{num}"]
        print(f"  {num} | {t[:24]}… → {a['choice']} ({a.get('confidence'):.2f})")
    print("  usage:", usage)
    return ans


if __name__ == "__main__":
    md = sys.argv[1] if len(sys.argv) > 1 else "/Users/hxw/wechat_workspace/documents/23-360-ai-pitfalls-guide.md"
    demo_guard(md)
    demo_router()
    demo_hooks()
