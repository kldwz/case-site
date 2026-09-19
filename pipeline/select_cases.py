#!/usr/bin/env python3
"""Stage 1 - select ~80 curated mini-program cases from the full 1256 pool.

Strategy (per approved product plan):
- Hard denylist big-name / common / list apps + companies (domestic super-apps and
  a few famous overseas mega-tools) so the set teaches *vertical / niche* discovery.
- Drop 获奖作品 and competition/award/person entries (not buildable products) via regex.
- Drop donate-only 无收入 plugins.
- Prioritise cases with *verified revenue* (monthly 月收入估算 starts with $), since
  those convert to concrete RMB figures that motivate readers.
- Keep a domestic slice (国内 indie not denylisted) even when revenue is undisclosed,
  shown honestly as 未披露 - so 国内 is represented.
- Sort each region by *founding* date desc (newer first). Founding date read ONLY from
  平台数据/创始人地区 anchored on 创立/成立/上架/上线 - never the 数据口径 sync ts.

Outputs pipeline/curated_slugs.txt (one slug per line, in display order).
"""
import os, re, glob
from collections import Counter

CASE_SITE = "/Users/hxw/codebuddy/case-site"
PIPE = os.path.join(CASE_SITE, "pipeline")
TARGET = 80
OVERSEAS_CAP = 56
DOMESTIC_CAP = 24

DENY = set("""
微信 支付宝 淘宝 天猫 京东 拼多多 美团 大众点评 百度 阿里 钉钉 飞书 抖音 今日头条
西瓜视频 快手 哔哩哔哩 b站 小红书 微博 知乎 豆瓣 陌陌 探探 携程 去哪儿 同程 饿了么
口碑 高德 百度地图 百度网盘 百度输入法 百度翻译 网易 网易云音乐 网易考拉 网易严选
网易公开课 小米 小米运动 小米ve 红米 华为 荣耀 oppo vivo 360 奇虎 搜狗 讯飞 科大讯飞
有道 金山 wps 猎豹 暴风 迅雷 优酷 爱奇艺 腾讯视频 搜狐 新浪 凤凰 当当 亚马逊 沃尔玛
工商银行 建设银行 农业银行 中国银行 交通银行 招商银行 平安 平安口袋银行 微众银行
众安保险 蚂蚁 蚂蚁财富 蛋卷基金 天天基金 且慢 雪球 同花顺 东方财富 富途 老虎证券
大智慧 度小满 京东金融 广发 华泰 中信 国信 招商证券 汽车之家 贝壳 链家 安居客
58同城 赶集 百姓网 滴滴 曹操 首汽 ofo 哈啰 摩拜 铁路12306 航旅纵横 飞常准 墨迹天气
天气通 彩云天气 彩云小译 彩云 美图秀秀 美颜相机 轻颜相机 无他相机 醒图 天天p图
faceu 激萌 b612 camera360 剪映 快影 秒剪 必剪 云剪 好看视频 微视 火山 懂车帝 易车
keep 咕咚 悦跑圈 乐心 华为运动 喜马拉雅 蜻蜓fm 懒人听书 酷狗 酷我 qq音乐 荔枝 猫耳fm
番茄小说 七猫小说 起点读书 起点 阅文 掌阅 晋江文学城 纵横小说 塔读文学 得间小说 米读
微信读书 微信听书 樊登读书 樊登 得到 美篇 简书 薄荷健康 每日瑜伽 可画 创客贴 稿定设计
canva 蓝湖 processon 亿图 百度脑图 扫描全能王 名片全能王 扫描宝 qq浏览器 uc浏览器
360浏览器 夸克 百度浏览器 小猿搜题 作业帮 学而思 猿辅导 流利说 百词斩 有道词典 金山词霸
小红书 美篇 手机管家 腾讯手机管家 360手机卫士 应用宝 豌豆荚 百度手机助手 百度贴吧
百度之星 阿里云天池 阿里聚安全 阿里巴巴诸神之战 华为昇腾 华为软件 华为开发者 华为ict
华为iot 华为杯 腾讯tctf 腾讯云开发者 腾讯开悟 腾讯广告算法 腾讯小程序 腾讯微信小程序
字节跳动前端 字节跳动极客 字节跳动青训 百度ai studio 京东探索者 京东物流 京东读书
京东金融 拼多多算法 快手算法 美团ai 美团算法 搜狗算法 商汤ai 旷视算法 科大讯飞ai
携程算法 滴滴盖亚 大疆 robomaster 大疆 微信小程序开发 vivo originos oppo coloros
小米vela 鸿蒙开发者 荣耀magicos 华为鲲鹏 昇腾 寒武纪 瑞芯微 全志科技 rockchip esp32
乐鑫 合宙 沁恒 微雪 野火电子 正点原子 矽递 seeed 矽速 sipeed m5stack 拿铁熊猫 lattepanda
跃昉 bananapi dfrobot 兆易创新 gigadevice 地平线 horizon 宇树科技 unitree 稚晖君 何同学
罗永浩 罗振宇 罗翔 李子柒 影视飓风 华农兄弟 美食作家王刚 手工耿 混知 毕导 回形针 差评
爱范儿 极客公园 虎嗅 36氪 雷锋网 品玩 量子位 机器之心 新片场 人人都是产品经理 csdn
掘金 阮一峰 冯大辉 曹政 图灵奖 未来科学大奖 邵逸夫奖 吴文俊 科学探索奖 光华龙腾奖
红点设计奖 达摩院青橙奖 if设计奖 金点设计奖 红星奖 梁思成建筑奖 长江学者 国家自然科学奖
国家科技进步奖 国家技术发明奖 中国专利奖 中国质量奖 求是杰出 王选奖 青橙奖 中国好设计
台湾金点 中国创新设计红星 中国设计智造大奖 达摩院 邵逸夫 吴文俊人工智能 光华龙腾 梁思成
长江学者 国家杰出青年 国家优秀青年 国家海外高层次人才 青年千人 千人计划 杰青 acm fellow
ieee fellow ccf acm kaggle 蓝桥杯 数学建模 挑战杯 互联网+ 创青春 中国创新创业大赛
中国研究生 中国大学生 全国大学生 中国青少年 中国机器人大赛 robocom robocon 世界机器人大赛
世界人工智能大会 waic 华为软件精英 百度之星 科大讯飞ai大赛 商汤ai大赛 旷视算法 腾讯广告算法
携程算法 滴滴盖亚 京东探索者 拼多多算法 快手算法 美团算法 美团ai 搜狗算法 字节跳动前端
字节跳动极客 字节跳动青训 百度ai studio 华为ict 华为iot 华为开发者大赛 华为杯 腾讯tctf
腾讯云开发者 腾讯开悟 腾讯小程序开发 vivo originos oppo coloros 小米vela 鸿蒙开发者
荣耀magicos 华为鲲鹏 昇腾 寒武纪 瑞芯微 rockchip esp32 乐鑫 合宙 沁恒 微雪 野火电子
正点原子 矽递 seeed 矽速 sipeed m5stack 拿铁熊猫 lattepanda 跃昉 bananapi dfrobot 兆易创新
gigadevice 地平线 horizon 宇树科技 unitree 白描 万能 万能命令 万能遥控器 万能导航 二维码生成器
截图插件 图片助手 视频下载助手 猫抓 油猴 tampermonkey stylus colorzilla onetab session buddy
web scraper video downloadhelper video speed controller image downloader awesome screenshot
print friendly reader view whatfont wikiwand wikiart gofulpage gesturefy infinity新标签页 侧边翻译
划词翻译 search preview lastpass 1password dashlane enpass bitwarden notion evernote onenote
goodnotes 熊掌记 todoist ticktick things microsoft google apple facebook twitter instagram
whatsapp telegram discord slack zoom skype youtube github gitlab stackoverflow medium substack
patreon kickstarter indiegogo gofundme onlyfans tiktok snapchat pinterest reddit linkedin quora
yahoo bing duckduckgo cloudflare aws azure gcp heroku vercel netlify shopify wordpress wix
squarespace webflow stripe paypal lemonsqueezy paddle gumroad figma grammarly dropbox box trello
asana signal pinterest
汽水音乐 汽水儿 番茄畅听 酷安 最美应用 少数派 小宇宙
""".split())

COMP_RE = re.compile(
    r"大赛|竞赛|挑战赛|奖项|评比|评奖|杯赛|论坛|峰会|研讨会|Workshop|选拔赛|邀请赛|"
    r"决赛|总决赛|初赛|半决赛|黑客松|hackathon|获奖|RoboCon|ICPC|CSP|CCF|ACM|Kaggle|"
    r"蓝桥|数学建模|创新创业|创客|青训营|奖|学者|教授|院士|研究院|实验室|基金会|基金|"
    r"人才|Fellow|大会|嘉年华|开放日|开发者大赛|算法大赛|AI大赛|网络安全|机器人大赛|"
    r"智能汽车|电子设计|结构设计|物理实验|化工设计|嵌入式|集成电路|FPGA|物联网|"
    r"创新创业大赛|机器人及人工智能|研究生数学|研究生创芯|研究生电子|高校计算机",
    re.I,
)

def denied(name):
    n = name.lower()
    for d in DENY:
        if d and re.search(re.escape(d), n):
            return True
    return False

def fm_and_body(txt):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", txt, re.S)
    if not m:
        return {}, txt
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body

DATE_RE = re.compile(r"(20\d{2})[-/年.](\d{1,2})(?:[-/月.](\d{1,2}))?")
def launch_yyyymmdd(fm):
    for field in ("平台数据", "创始人地区"):
        m = re.search(r"(?:创立|成立|上架|上线|发布)[^0-9]*" + DATE_RE.pattern,
                      " " + fm.get(field, ""))
        if m:
            return int(f"{m.group(1)}{int(m.group(2)):02d}{int(m.group(3) or 1):02d}")
    return 0

def usd_amount(s):
    m = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", s)
    return float(m.group(1).replace(",", "")) if m else None

def main():
    files = sorted(glob.glob(os.path.join(CASE_SITE, "src/content/cases/*.md")))
    rows = []
    for f in files:
        slug = os.path.splitext(os.path.basename(f))[0]
        fm, _ = fm_and_body(open(f, encoding="utf-8").read())
        name = fm.get("name", "")
        if not name:
            continue
        typ = fm.get("类型", "")
        region = "国内" if (typ == "国内实践" or "国内" in fm.get("分类", "")) else "国外"
        if typ == "获奖作品":
            continue
        if COMP_RE.search(name):
            continue
        if denied(name):
            continue
        rev = fm.get("月收入估算", "")
        if "无收入" in rev or ("捐赠" in rev and "未披露" in rev):
            continue
        amt = usd_amount(rev) if rev.startswith("$") else None
        verified = amt is not None and amt > 0
        rows.append({
            "slug": slug, "name": name, "type": typ, "region": region,
            "verified": verified, "amt": amt or 0,
            "date": launch_yyyymmdd(fm),
        })

    ov_ver = sorted([r for r in rows if r["region"] == "国外" and r["verified"]], key=lambda r: r["date"], reverse=True)
    ov_oth = sorted([r for r in rows if r["region"] == "国外" and not r["verified"]], key=lambda r: r["date"], reverse=True)
    dn_all = sorted([r for r in rows if r["region"] == "国内"], key=lambda r: r["date"], reverse=True)

    curated = ov_ver[:OVERSEAS_CAP] + dn_all[:DOMESTIC_CAP]
    pools = [ov_oth, dn_all[DOMESTIC_CAP:], ov_ver[OVERSEAS_CAP:]]
    i = 0
    while len(curated) < TARGET and i < 2000:
        for p in pools:
            if len(curated) >= TARGET:
                break
            if i < len(p) and p[i] not in curated:
                curated.append(p[i])
        i += 1

    seen, final = set(), []
    for r in curated:
        if r["slug"] not in seen:
            seen.add(r["slug"]); final.append(r)
    curated = final[:TARGET]

    with open(os.path.join(PIPE, "curated_slugs.txt"), "w", encoding="utf-8") as f:
        for r in curated:
            f.write(r["slug"] + "\n")

    print(f"pool after filters: {len(rows)}  ->  curated {len(curated)}")
    print("region:", dict(Counter(r["region"] for r in curated)))
    print("verified-revenue:", sum(1 for r in curated if r["verified"]), "/", len(curated))
    print("date range:", min(r["date"] for r in curated), "->", max(r["date"] for r in curated))
    print("domestic names:", [r["name"] for r in curated if r["region"] == "国内"][:24])
    print("\nnewest 10:")
    for r in sorted(curated, key=lambda r: r["date"], reverse=True)[:10]:
        tag = f"${r['amt']:.0f}" if r["verified"] else "未披露"
        print(f"  {r['date']}  [{r['region']} {tag}]  {r['name']}")

if __name__ == "__main__":
    main()
