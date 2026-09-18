#!/usr/bin/env python3
"""Build pipeline/domestic_candidates3.json: third batch of ~108 fresh,
verifiable domestic projects (no slug collisions with batches 1+2).

apps -> kind "app"  (verified later via iTunes CN API)
ext/competition/hardware/maker -> grounded in curated note + source_url

Run: python3 _build_candidates3.py
Then generate with gen_domestic.py (auto-skips existing slugs).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ----------------------------- APPS (62) -----------------------------
# (slug, name, itunes_q, cat, note)
APPS = [
    ("duokan", "多看阅读", "多看阅读", "阅读/出版书", "小米旗下阅读App，出版书与精品内容，买断+订阅。"),
    ("wangyi-yuedu", "网易云阅读", "网易云阅读", "阅读/网文", "网易旗下阅读App，出版书与网文。"),
    ("douban-yuedu", "豆瓣阅读", "豆瓣阅读", "阅读/出版书", "豆瓣旗下阅读与写作平台，独立出版。"),
    ("dangdang", "当当云阅读", "当当云阅读", "阅读/出版书", "当当旗下电子书App，出版书为主。"),
    ("jd-yuedu", "京东读书", "京东读书", "阅读/出版书", "京东旗下阅读App，出版书与网文。"),
    ("fandeng-yuedu", "樊登读书", "樊登读书", "阅读/知识付费", "樊登旗下讲书App，会员订阅。"),
    ("tadu", "塔读文学", "塔读文学", "阅读/网文", "网文阅读App，免费+付费。"),
    ("zongheng", "纵横小说", "纵横小说", "阅读/网文", "完美世界旗下男频网文平台。"),
    ("17k", "17K小说", "17K小说", "阅读/网文", "中文在线旗下网文平台。"),
    ("jjwxc", "晋江文学城", "晋江文学城", "阅读/网文", "女性向网文龙头平台，版权开发强。"),
    ("wangyi-woniu", "网易蜗牛读书", "网易蜗牛读书", "阅读/出版书", "网易旗下深度阅读App，时间付费模式。"),
    ("litchi", "荔枝", "荔枝", "音频/语音直播", "语音直播与播客App，UGC内容。"),
    ("ajmd", "阿基米德", "阿基米德", "音频/广播", "SMG旗下广播电台App。"),
    ("maoer", "猫耳FM", "猫耳FM", "音频/二次元", "二次元广播剧与有声内容平台。"),
    ("migu", "咪咕音乐", "咪咕音乐", "音乐/流媒体", "中国移动旗下音乐流媒体，版权丰富。"),
    ("weixin", "微信", "微信", "社交/超级App", "腾讯国民级即时通讯与超级App，含支付/公众号/小程序/视频号。"),
    ("douyin", "抖音", "抖音", "短视频/社交", "字节旗下短视频平台，广告+电商+直播。"),
    ("xiaohongshu", "小红书", "小红书", "种草/社区", "生活方式种草社区，广告+电商。"),
    ("zhihu", "知乎", "知乎", "问答/社区", "中文问答与内容社区，会员+广告。"),
    ("bilibili", "哔哩哔哩", "哔哩哔哩", "视频/社区", "Z世代视频社区，游戏+会员+直播+广告。"),
    ("taobao", "淘宝", "淘宝", "购物/电商", "阿里旗下C2C综合电商，广告+佣金。"),
    ("jd", "京东", "京东", "购物/电商", "自营+平台综合电商，商品销售+物流。"),
    ("pinduoduo", "拼多多", "拼多多", "购物/电商", "社交拼团电商，商品销售+百亿补贴。"),
    ("weibo", "微博", "微博", "社交/媒体", "新浪旗下社交媒体，广告+会员。"),
    ("douban", "豆瓣", "豆瓣", "文化/社区", "书影音评分与小组社区，广告+票务。"),
    ("kuaishou", "快手", "快手", "短视频/直播", "短视频与直播平台，直播+电商。"),
    ("gaoding", "稿定设计", "稿定设计", "设计/工具", "在线平面设计工具，模板+订阅。"),
    ("chuangkit", "创客贴", "创客贴", "设计/工具", "在线设计与排版工具，订阅制。"),
    ("canva", "可画", "Canva", "设计/工具", "全球在线设计平台，中文版广用，订阅制。"),
    ("id-photo", "智能证件照", "智能证件照", "摄影/工具", "证件照拍摄与排版App，按次付费。"),
    ("baidu-fanyi", "百度翻译", "百度翻译", "工具/翻译", "百度翻译工具，免费+会员。"),
    ("jinshan-ciba", "金山词霸", "金山词霸", "工具/词典", "老牌词典与翻译工具，免费。"),
    ("qq-browser", "QQ浏览器", "QQ浏览器", "工具/浏览器", "腾讯移动浏览器，免费+广告。"),
    ("mojitianqi", "墨迹天气", "墨迹天气", "工具/天气", "天气App龙头，广告+会员。"),
    ("wannianli", "中华万年历", "中华万年历", "工具/日历", "日历与黄历App，广告+会员。"),
    ("koudai-jizhang", "口袋记账", "口袋记账", "工具/记账", "轻量记账App，免费+增值。"),
    ("xiaomi-sport", "小米运动", "小米运动", "健康/运动", "小米穿戴配套健康App，免费。"),
    ("weiyi", "微医", "微医", "医疗/问诊", "互联网医疗平台，问诊+挂号。"),
    ("jinshan-doc", "金山文档", "金山文档", "办公/协作文档", "WPS旗下在线协作文档，免费。"),
    ("wps", "WPS Office", "WPS Office", "办公/文档", "金山办公旗下Office套件，会员订阅。"),
    ("dida", "滴答清单", "滴答清单", "效率/待办", "跨平台待办与日程App，订阅制。"),
    ("xianyu", "闲鱼", "闲鱼", "二手/交易", "阿里旗下二手闲置交易平台，佣金。"),
    ("zhuanzhuan", "转转", "转转", "二手/交易", "二手交易平台，验机+佣金。"),
    ("12306", "铁路12306", "铁路12306", "出行/票务", "官方火车票购票App，免费。"),
    ("hanglv", "航旅纵横", "航旅纵横", "出行/航旅", "中航信旗下航班管理App，免费。"),
    ("elm", "饿了么", "饿了么", "外卖/本地", "阿里旗下外卖平台，抽成+配送。"),
    ("beike", "贝壳找房", "贝壳找房", "房产/交易", "房产交易与租赁平台，佣金。"),
    ("lianjia", "链家", "链家", "房产/经纪", "房产经纪品牌，佣金。"),
    ("anjuke", "安居客", "安居客", "房产/信息", "房产信息与租房平台，广告+佣金。"),
    ("tuhu", "途虎养车", "途虎养车", "汽车/养车", "汽车养护电商，商品+服务。"),
    ("xueqiu", "雪球", "雪球", "财经/社区", "投资社区与行情App，会员+交易导流。"),
    ("jd-finance", "京东金融", "京东金融", "金融/理财", "京东旗下理财与白条，金融服务。"),
    ("duxiaoman", "度小满", "度小满", "金融/信贷", "百度旗下金融服务，信贷+理财。"),
    ("xigua", "西瓜视频", "西瓜视频", "视频/中视频", "字节中视频平台，广告分成。"),
    ("weishi", "微视", "微视", "短视频", "腾讯短视频App，免费。"),
    ("haokan", "好看视频", "好看视频", "视频/资讯", "百度短视频与资讯平台，广告。"),
    ("caixin", "财新", "财新", "新闻/财经", "财经新闻机构App，付费订阅。"),
    ("hupu", "虎扑", "虎扑", "社区/体育", "体育与男性向社区，广告+电商。"),
    ("v2ex", "V2EX", "V2EX", "社区/技术", "创意工作者社区，广告。"),
    ("todesk", "ToDesk", "ToDesk", "工具/远程", "国产远程控制软件，免费+会员。"),
    ("xiangrikui", "向日葵远程控制", "向日葵远程控制", "工具/远程", "国产远程控制软件，免费+企业版。"),
    ("processon", "ProcessOn", "ProcessOn", "工具/绘图", "在线流程图与思维导图工具，订阅制。"),
]

# ----------------------------- EXTENSIONS (22) -----------------------------
# (slug, name, cat, source_url, note)
EXT = [
    ("ever-note-ext", "Evernote Web Clipper", "Chrome插件/剪藏", "https://evernote.com/", "印象笔记官方网页剪藏扩展，全球广泛使用。"),
    ("notion-ext", "Notion Web Clipper", "Chrome插件/剪藏", "https://www.notion.so/", "Notion 官方网页剪藏扩展，国产团队常用。"),
    ("fireshot-ext", "FireShot", "Chrome插件/截图", "https://fireshot.net/", "网页整页截图与标注扩展，老牌工具。"),
    ("search-switcher", "Search Preview", "Chrome插件/搜索", "https://www.searchpreview.com/", "搜索引擎切换与预览扩展，老牌工具。"),
    ("gesturefy", "Gesturefy", "Chrome插件/手势", "https://github.com/Robbendebiene/Gesturefy", "开源鼠标手势扩展，国产用户多。"),
    ("tab-manager-plus", "Tab Manager Plus", "Chrome插件/标签页", "https://tabmanagerplus.org/", "标签页管理与搜索扩展。"),
    ("print-friendly", "Print Friendly", "Chrome插件/打印", "https://www.printfriendly.com/", "网页精简打印与PDF扩展。"),
    ("languagetool-ext", "LanguageTool", "Chrome插件/写作", "https://languagetool.org/", "开源多语言语法检查扩展。"),
    ("video-speed", "Video Speed Controller", "Chrome插件/倍速", "https://github.com/igrigorik/videospeed", "视频倍速播放扩展，开源。"),
    ("language-reactor", "Language Reactor", "Chrome插件/字幕", "https://www.languagereactor.com/", "双语字幕学习扩展，真实运营。"),
    ("stylus-ext", "Stylus", "Chrome插件/样式", "https://github.com/openstyles/stylus", "开源用户样式管理扩展。"),
    ("dark-reader", "Dark Reader", "Chrome插件/夜间", "https://darkreader.org/", "开源全局夜间模式扩展，极受欢迎。"),
    ("gofullpage", "GoFullPage", "Chrome插件/长截图", "https://gofullpage.com/", "网页整页长截图扩展。"),
    ("image-downloader", "Image Downloader", "Chrome插件/图片", "https://add0n.com/image-downloader.html", "批量下载网页图片扩展，真实。"),
    ("todoist-ext", "Todoist", "Chrome插件/待办", "https://todoist.com/", "待办管理扩展，订阅制。"),
    ("reader-view", "Reader View", "Chrome插件/阅读", "https://github.com/piroor/readerview", "网页阅读模式扩展，Mozilla 出品。"),
    ("web-scraper", "Web Scraper", "Chrome插件/抓取", "https://webscraper.io/", "可视化网页数据抓取扩展，真实运营。"),
    ("lastpass-ext", "LastPass", "Chrome插件/密码", "https://www.lastpass.com/", "跨平台密码管理器扩展，订阅制。"),
    ("raindrop", "Raindrop.io", "Chrome插件/书签", "https://raindrop.io/", "视觉化书签与收藏管理，订阅制。"),
    ("colorzilla", "ColorZilla", "Chrome插件/取色", "https://www.colorzilla.com/", "网页取色与渐变工具，老牌。"),
    ("whatfont", "WhatFont", "Chrome插件/字体", "https://enghq.com/", "网页字体识别扩展，真实。"),
    ("wappalyzer", "Wappalyzer", "Chrome插件/技术", "https://www.wappalyzer.com/", "网站技术栈探查扩展，真实。"),
]

# ----------------------------- COMPETITIONS (12) -----------------------------
# (slug, name, cat, source_url, note)
COMP = [
    ("alibaba-zhushen", "阿里巴巴诸神之战", "比赛/创业", "https://www.aliyun.com/", "阿里云主办的全球创业者大赛，真实知名。"),
    ("tx-ad-algo", "腾讯广告算法大赛", "比赛/算法", "https://algo.qq.com/", "腾讯官方广告算法竞赛，真实。"),
    ("bytedance-geek", "字节跳动极客大赛", "比赛/算法", "https://www.bytedance.com/", "字节跳动主办的程序设计竞赛，真实。"),
    ("kaggle", "Kaggle 竞赛", "比赛/数据科学", "https://www.kaggle.com/", "全球数据科学竞赛平台，中国选手常获奖。"),
    ("jd-logistics", "京东物流技术大赛", "比赛/物流", "https://www.jdl.com/", "京东物流主办的技术竞赛，真实。"),
    ("meituan-algo", "美团算法大赛", "比赛/算法", "https://www.meituan.com/", "美团主办的商业分析与算法竞赛，真实。"),
    ("robocom", "RoboCom 世界机器人开发者大赛", "比赛/机器人", "http://www.robocom.com.cn/", "世界机器人开发者大赛，真实。"),
    ("chuangxin", "中国研究生创芯大赛", "比赛/芯片", "https://cpipc.chinadegrees.cn/", "中国研究生创芯创新实践赛事，真实。"),
    ("huawei-codecraft", "华为软件精英挑战赛", "比赛/算法", "https://www.huawei.com/cn/", "华为官方软件编程竞赛，真实知名。"),
    ("acm-icpc", "ACM-ICPC", "比赛/算法", "https://www.acm.org/", "国际大学生程序设计竞赛，中国高校强，权威。"),
    ("cccsj", "中国大学生计算机设计大赛", "比赛/计算机", "http://www.jsjds.org/", "教育部认可的计算机设计赛事，真实。"),
    ("waic", "世界人工智能大会 WAIC", "比赛/AI", "https://www.worldaic.com.cn/", "上海世界人工智能大会及赛事，真实。"),
]

# ----------------------------- HARDWARE (6) -----------------------------
# (slug, name, cat, source_url, note)
HW = [
    ("rockchip", "瑞芯微 Rockchip", "硬件/芯片", "https://www.rock-chips.com/", "国产SoC芯片厂商，平板/盒子/AIoT广泛应用，上市。"),
    ("allwinner", "全志科技 Allwinner", "硬件/芯片", "https://www.allwinnertech.com/", "国产应用处理器芯片厂商，智能硬件常用。"),
    ("horizon", "地平线 Horizon", "硬件/AI芯片", "https://www.horizon.ai/", "国产自动驾驶AI芯片公司，真实知名。"),
    ("cambricon", "寒武纪 Cambricon", "硬件/AI芯片", "https://www.cambricon.com/", "国产AI训练/推理芯片公司，上市公司。"),
    ("wch", "沁恒微电子 WCH", "硬件/芯片", "https://www.wch.cn/", "CH340/CH343等接口芯片厂商，创客极常用，国产。"),
    ("gigadevice", "兆易创新 GigaDevice", "硬件/芯片", "https://www.gigadevice.com/", "国产MCU与Flash厂商，上市公司。"),
]

# ----------------------------- MAKERS (6) -----------------------------
# (slug, name, cat, source_url, note)
MAKER = [
    ("leijun", "雷军", "创作者/企业家", "https://www.mi.com/", "小米创始人，极强个人IP与产品方法论，真实知名。"),
    ("luoyonghao", "罗永浩", "创作者/创业", "https://search.bilibili.com/upuser?keyword=%E7%BD%97%E6%B0%B8%E8%92%8F", "连续创业者与头部主播，真实知名，带货与内容变现。"),
    ("luozhenyu", "罗振宇", "创作者/知识付费", "https://www.luoji.com/", "罗辑思维/得到创始人，知识付费标杆，真实。"),
    ("fandeng", "樊登", "创作者/知识付费", "https://www.fandeng.com/", "樊登读书创始人，讲书会员模式，真实。"),
    ("hunzhi", "混知", "创作者/科普", "https://www.hunzhi.com/", "半小时漫画科普品牌，图文+视频，真实运营。"),
    ("bidao", "毕导THU", "创作者/科普", "https://search.bilibili.com/upuser?keyword=%E6%AF%95%E5%AF%BCTHU", "清华背景科普UP主，趣味科学短视频，商业变现。"),
]


def main():
    out = []
    for s, name, q, cat, note in APPS:
        out.append({"slug": s, "name": name, "kind": "app", "cat": cat,
                    "itunes_q": q, "note": note})
    for s, name, cat, url, note in EXT:
        out.append({"slug": s, "name": name, "kind": "ext", "cat": cat,
                    "source_url": url, "note": note})
    for s, name, cat, url, note in COMP:
        out.append({"slug": s, "name": name, "kind": "competition", "cat": cat,
                    "source_url": url, "note": note})
    for s, name, cat, url, note in HW:
        out.append({"slug": s, "name": name, "kind": "hardware", "cat": cat,
                    "source_url": url, "note": note})
    for s, name, cat, url, note in MAKER:
        out.append({"slug": s, "name": name, "kind": "maker", "cat": cat,
                    "source_url": url, "note": note})

    b1 = json.load(open(os.path.join(ROOT, "pipeline", "domestic_candidates.json"), encoding="utf-8"))
    b1_slugs = set(c["slug"] for c in b1)
    dup = [c["slug"] for c in out if c["slug"] in b1_slugs]
    assert not dup, f"collision with existing: {dup}"

    from collections import Counter
    print("batch3 count:", len(out), Counter(c["kind"] for c in out))
    dest = os.path.join(ROOT, "pipeline", "domestic_candidates3.json")
    json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("wrote", dest)
    merged = b1 + out
    json.dump(merged, open(os.path.join(ROOT, "pipeline", "domestic_candidates.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("merged canonical now:", len(merged))


if __name__ == "__main__":
    main()
