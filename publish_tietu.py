#!/usr/bin/env python3
# 公众号「贴图」素材库上传器（旺旺版）
# 流程：挑未发布 case → 真实截图 + 钩子标题 合成竖版贴图
#      → 调 material/add_material 上传到公众号「永久素材库」
#      → 生成「对普通人的启发」描述文案(供你建贴图时粘贴到图片下方)
#      → 你在 App 建「图片消息/贴图」时，直接从素材库选这张图 + 把文案贴到下方即可
#      （微信无图片消息发布 API，所以「发布」这步必须你在 App 点一下）
#
# 用法：
#   手动指定： python publish_tietu.py --slug cursor \
#       --kicker "AI 编程编辑器 · Cursor" \
#       --title "4个MIT毕业生，靠AI帮人写代码\n3年把估值干到 293 亿" \
#       --desc "可选，不填则自动生成"
#   每日自动： python publish_tietu.py --auto
import sys, os, re, json, glob, argparse, requests
from pathlib import Path
from datetime import date
from PIL import Image, ImageDraw, ImageFont

# 微信 material API 出口策略：
#  - 默认：强制走本机直连（pop 掉系统代理 HTTP_PROXY=127.0.0.1:1082），用家里公网 IP 命中白名单。
#  - 若设置了 WX_PROXY（固定 IP 的出口代理，如家里静态 IP / 一台 VPS 的代理）：用它做出口，
#    彻底解决动态 IP 每天变、白名单反复失效的问题（get_token 与 upload_material 共用 env 代理）。
WX_PROXY = os.environ.get("WX_PROXY")
if WX_PROXY:
    # 用固定出口代理，不 pop；让 requests 走 WX_PROXY
    os.environ["HTTP_PROXY"] = WX_PROXY
    os.environ["HTTPS_PROXY"] = WX_PROXY
else:
    for _p in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        os.environ.pop(_p, None)

CASE_SITE = Path("/Users/hxw/codebuddy/case-site")
SKILL_SCRIPTS = Path("/Users/hxw/.workbuddy/skills/wechat-writer-publisher/scripts")
TRACK = CASE_SITE / "wechat_uploaded.json"
sys.path.insert(0, str(SKILL_SCRIPTS))
import publish as WX   # get_token / CONFIG

FONT = "/System/Library/Fonts/PingFang.ttc"
BRAND = "打工人AI自救 · 每天一个真实赚钱的 AI 案例"
ACCENT = (230, 96, 58)
DARK = (18, 20, 38)
LIGHT = (245, 246, 250)
MUTED = (165, 170, 190)


def font(size, bold=False):
    return ImageFont.truetype(FONT, size, index=1 if bold else 0)


def gradient_bg(W, H, top, bottom):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / max(1, H - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    return img


def wrap(text, draw, fnt, max_w):
    lines = []
    for raw in text.split("\n"):
        if not raw:
            lines.append(""); continue
        cur = ""
        for ch in raw:
            if draw.textlength(cur + ch, font=fnt) <= max_w:
                cur += ch
            else:
                lines.append(cur); cur = ch
        lines.append(cur)
    return lines


def make_tietu(site_png, kicker, title, hook, out_png, brand=BRAND):
    W, H = 1080, 1440
    canvas = gradient_bg(W, H, (16, 18, 34), (34, 24, 52))
    d = ImageDraw.Draw(canvas)

    # 顶部标题区
    d.rectangle([0, 0, W, 8], fill=ACCENT)
    d.text((64, 70), kicker, font=font(36), fill=ACCENT)
    ty = 130
    for raw in title.replace("\\n", "\n").split("\n"):
        for ln in wrap(raw, d, font(70, bold=True), W - 128)[:2]:
            d.text((64, ty), ln, font=font(70, bold=True), fill=LIGHT)
            ty += 86
    d.line([64, ty + 12, W - 64, ty + 12], fill=(255, 255, 255), width=1)

    # 截图卡片
    shot = Image.open(site_png).convert("RGB")
    sw, sh = shot.size
    nw = W - 128
    nh = int(sh * (nw / sw))
    max_h = 720
    if nh > max_h:
        crop = int((nh - max_h) / 2)
        shot = shot.resize((nw, nh)).crop((0, crop, nw, crop + max_h))
    else:
        shot = shot.resize((nw, nh))
    sx, sy = 64, ty + 44
    canvas.paste(shot, (sx, sy))
    d.rectangle([sx - 4, sy - 4, sx + shot.width + 4, sy + shot.height + 4], outline=(255, 255, 255), width=2)

    # 底部钩子条
    by = sy + shot.height + 40
    d.text((64, by), "💡 普通人能学的一招", font=font(34, bold=True), fill=ACCENT)
    hy = by + 52
    for ln in wrap(hook, d, font(36), W - 128)[:3]:
        d.text((64, hy), ln, font=font(36), fill=LIGHT)
        hy += 50
    d.line([64, H - 70, W - 64, H - 70], fill=(255, 255, 255), width=1)
    d.text((64, H - 58), brand, font=font(30), fill=MUTED)

    out_png.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_png, "PNG")
    return out_png


def make_text_card(idx, title, blocks, out_png, brand=BRAND):
    """纯文字贴图：浅色底 + 顶部色条 + 大标题 + 多段正文。
    blocks: list of (subtitle, text) 或 ('', text) 表示无小标题的段落。"""
    W, H = 1080, 1440
    canvas = Image.new("RGB", (W, H), (248, 249, 252))
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, 0, W, 14], fill=ACCENT)
    d.text((64, 64), f"{idx} · 打工人AI自救", font=font(34, bold=True), fill=ACCENT)
    ty = 118
    for ln in wrap(title, d, font(64, bold=True), W - 128)[:3]:
        d.text((64, ty), ln, font=font(64, bold=True), fill=(28, 30, 46))
        ty += 82
    ty += 6
    d.line([64, ty, W - 64, ty], fill=(210, 212, 222), width=2)
    ty += 44
    for sub, txt in blocks:
        if sub:
            d.text((64, ty), sub, font=font(38, bold=True), fill=ACCENT)
            ty += 54
        for ln in wrap(txt, d, font(40), W - 128):
            d.text((64, ty), ln, font=font(40), fill=(46, 48, 66))
            ty += 58
        ty += 22
    d.line([64, H - 70, W - 64, H - 70], fill=(210, 212, 222), width=1)
    d.text((64, H - 58), brand, font=font(30), fill=MUTED)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_png, "PNG")
    return out_png


def gen_what_how(fm):
    name = fm.get("name", "")
    one = fm.get("一句话", "")
    revenue = fm.get("营收模式", "")
    traffic = fm.get("流量来源", "")
    pts = parse_points(fm.get("可迁移点", ""))
    blocks = [
        ("它到底是什么", one),
        ("怎么赚到钱的", ("赚钱方式：" + revenue) if revenue else ""),
        ("流量从哪来", ("获客打法：" + traffic) if traffic else ""),
        ("关键一招", "；".join(f"{['①','②','③'][i]}{p}" for i, p in enumerate(pts[:3])) if pts else ""),
    ]
    blocks = [(s, t) for s, t in blocks if t]
    return blocks


def gen_inspire(fm):
    pts = parse_points(fm.get("可迁移点", ""))
    text = "\n".join(f"{i}. {p}" for i, p in enumerate(pts[:3], 1)) if pts else fm.get("一句话", "")
    return [("", text)]


def parse_frontmatter(md_path):
    txt = Path(md_path).read_text(encoding="utf-8")
    if not txt.startswith("---"):
        return {}
    block = txt.split("---", 2)[1]
    fm = {}
    for line in block.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def parse_points(text):
    parts = re.split(r"[①②③④⑤]", text or "")
    return [p.strip(" .。、\n") for p in parts if p.strip(" .。、\n")]


def biggest_number(text):
    m = re.search(r'([A-Za-z]{1,6}\s*)?(\d+(?:\.\d+)?\s*[亿万千]\s*(?:美金|美元|美刀|元|RMB)?)', text or "")
    if not m:
        m = re.search(r'(\d+(?:\.\d+)?\s*(?:M|K|m|k)\b)', text or "")
        return m.group(0) if m else ""
    return (m.group(1) or "") + m.group(2)


def auto_title(fm):
    name = fm.get("name", "")
    one = fm.get("一句话", "")
    big = biggest_number(fm.get("月收入估算", "") or one)
    if big:
        title = f"{name}：靠 {big}，杀进 AI 头部"
    else:
        clause = re.split(r'[，,。；（(]', one)[0].strip()
        title = f"{name}：{clause}" if clause else f"{name}：一个被低估的 AI 赚钱样本"
    kicker = (fm.get("分类", "").split("/")[0] or "AI 创业案例") + f" · {name}"
    return kicker, title


def auto_hook(fm):
    pts = parse_points(fm.get("可迁移点", ""))
    return pts[0] if pts else (fm.get("一句话", "")[:40])


def gen_desc(fm):
    name = fm.get("name", "")
    one = fm.get("一句话", "")
    pts = parse_points(fm.get("可迁移点", ""))
    lines = [f"📌 {name}", ""]
    lines.append("【这篇文章讲了啥】")
    lines.append(one[:130])
    lines.append("")
    lines.append("【对普通人的启发】")
    for i, p in enumerate(pts[:3], 1):
        lines.append(f"{i}. {p}")
    lines.append("")
    lines.append("—— 每天一个真实赚钱的 AI 案例 · 打工人AI自救")
    return "\n".join(lines)


def load_track():
    return json.loads(TRACK.read_text(encoding="utf-8")) if TRACK.exists() else {}


def pick_next():
    files = glob.glob(str(CASE_SITE / "src" / "content" / "cases" / "*.md"))
    done = load_track()
    cand = []
    for f in files:
        p = Path(f)
        slug = p.stem
        if slug in done:
            continue
        fm = parse_frontmatter(f)
        if not fm.get("name"):
            continue
        cand.append((p.stat().st_mtime, slug, fm))
    if not cand:
        return None
    cand.sort()  # 最旧的案例优先发
    return cand[0][1], cand[0][2]


def upload_material(token, png):
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=" + token + "&type=image"
    with open(png, "rb") as f:
        r = requests.post(url, files={"media": f}, timeout=60)
    d = r.json()
    if "media_id" not in d:
        print("[错误] 素材上传失败:", d); raise SystemExit(1)
    return d.get("url", ""), d.get("media_id", "")


def run(slug, fm, kicker=None, title=None, desc=None, cover_only=False):
    title = title or auto_title(fm)[1]
    kicker = kicker or auto_title(fm)[0]
    hook = auto_hook(fm)
    site = CASE_SITE / "public" / "cases" / slug / "site.png"
    out_cover = CASE_SITE / "drafts" / "covers" / f"{slug}.tietu.png"
    if not site.exists():
        print("[错误] 找不到截图:", site); raise SystemExit(1)

    print("[1] 合成封面贴图 ->", out_cover)
    make_tietu(site, kicker, title, hook, out_cover)
    imgs = [("封面", out_cover)]

    if not cover_only:
        out_what = CASE_SITE / "drafts" / "covers" / f"{slug}.what.png"
        out_insp = CASE_SITE / "drafts" / "covers" / f"{slug}.inspire.png"
        print("[2] 合成文字图① 这是什么/怎么做的 ->", out_what)
        make_text_card("01", f"{fm.get('name','')}：到底是什么、怎么做的", gen_what_how(fm), out_what)
        print("[3] 合成文字图② 对普通人的启发 ->", out_insp)
        make_text_card("02", "对普通人有什么启发", gen_inspire(fm), out_insp)
        imgs += [("文字图①", out_what), ("文字图②", out_insp)]

    token = WX.get_token()
    print("[*] access_token 获取成功")

    uploaded = []
    for label, p in imgs:
        url, media_id = upload_material(token, str(p))
        uploaded.append((label, p, media_id, url))
        print(f"    ↑ {label} 已上传素材库 media_id={media_id}")

    # 文案存档（可选：在 App 里贴到图片下方，或直接用上面两张文字图）
    desc = desc or gen_desc(fm)
    desc_path = CASE_SITE / "drafts" / "tietu_desc" / f"{slug}.txt"
    desc_path.parent.mkdir(parents=True, exist_ok=True)
    desc_path.write_text(desc, encoding="utf-8")

    print("\n================ 贴图标题 ================")
    print(title.replace("\\n", "\n"))
    print("================ 已上传素材库（共 %d 张）================" % len(uploaded))
    for label, p, media_id, url in uploaded:
        print(f"  [{label}] {p.name}  media_id={media_id}")
    print("================ 启发文案（可直接用文字图②，或贴到图片下方）================")
    print(desc)
    print("==========================================")
    return uploaded, desc_path


def mark_done(slug):
    t = load_track()
    t[slug] = date.today().isoformat()
    TRACK.write_text(json.dumps(t, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[记录] wechat_uploaded.json 已标记", slug)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug")
    ap.add_argument("--kicker")
    ap.add_argument("--title", help="可用 \\n 换行")
    ap.add_argument("--desc")
    ap.add_argument("--cover-only", action="store_true", help="只生成封面，不生成两张文字图")
    ap.add_argument("--auto", action="store_true", help="自动挑下一篇未发的 case")
    a = ap.parse_args()

    if a.auto:
        nxt = pick_next()
        if not nxt:
            print("🎉 所有 case 都已上传素材库了。"); raise SystemExit(0)
        slug, fm = nxt
        print("▶ 自动挑选:", slug, "|", fm.get("name", ""))
        run(slug, fm, cover_only=a.cover_only)
        mark_done(slug)
    else:
        if not a.slug:
            ap.error("需 --slug（或加 --auto）")
        md = CASE_SITE / "src" / "content" / "cases" / f"{a.slug}.md"
        if not md.exists():
            print("[错误] 找不到案例:", md); raise SystemExit(1)
        fm = parse_frontmatter(md)
        run(a.slug, fm, a.kicker, a.title, a.desc, cover_only=a.cover_only)
        mark_done(a.slug)
