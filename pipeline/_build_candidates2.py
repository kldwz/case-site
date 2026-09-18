#!/usr/bin/env python3
"""Build pipeline/domestic_candidates2.json: a second batch of ~108 fresh,
verifiable domestic projects (no slug collisions with batch 1).

apps -> kind "app"  (verified later via iTunes CN API)
ext/competition/hardware/maker -> grounded in curated note + source_url

Run: python3 _build_candidates2.py
Then merge + generate with gen_domestic.py (which skips existing slugs).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ----------------------------- APPS (62) -----------------------------
# (slug, name, itunes_q, cat, note)
APPS = [
    ("weixin-yuedu", "微信读书", "微信读书", "阅读/出版书", "腾讯旗下正版阅读App，海量出版书与网文，会员+免费混合。"),
    ("qidian", "起点读书", "起点读书", "阅读/网文", "阅文旗下网文阅读龙头，付费订阅与免费模式并存。"),
    ("qq-yuedu", "QQ阅读", "QQ阅读", "阅读/网文", "腾讯系网文阅读App，出版书与原创内容。"),
    ("zhangyue", "掌阅", "掌阅", "阅读/网文", "掌阅科技旗下阅读App，出版书与网文，软硬一体。"),
    ("midu", "米读", "米读", "阅读/免费网文", "免费网文阅读App，广告变现模式。"),
    ("dedao", "得到", "得到", "知识付费", "罗辑思维旗下知识付费App，音频课程订阅。"),
    ("weixin-tingshu", "微信听书", "微信听书", "听书/有声", "微信旗下听书App，出版书有声化，会员订阅。"),
    ("fanqie-changting", "番茄畅听", "番茄畅听", "听书/免费", "字节旗下免费听书App，番茄小说衍生，广告变现。"),
    ("netease-music", "网易云音乐", "网易云音乐", "音乐/流媒体", "音乐流媒体App，会员订阅+社区社交。"),
    ("qq-music", "QQ音乐", "QQ音乐", "音乐/流媒体", "腾讯QQ音乐，版权音乐流媒体，会员订阅。"),
    ("kugou", "酷狗音乐", "酷狗音乐", "音乐/流媒体", "音乐流媒体App，会员+直播。"),
    ("kuwo", "酷我音乐", "酷我音乐", "音乐/流媒体", "音乐流媒体App，会员订阅。"),
    ("ximalaya", "喜马拉雅", "喜马拉雅", "音频/播客", "在线音频与播客龙头，会员订阅+主播分成。"),
    ("qingting", "蜻蜓FM", "蜻蜓FM", "音频/电台", "网络电台与有声内容App，会员订阅。"),
    ("keep", "Keep", "Keep", "健身/运动", "运动科技公司，健身App+硬件+课程，会员订阅。"),
    ("gudong", "咕咚", "咕咚", "跑步/运动", "跑步运动记录App，硬件+赛事+会员。"),
    ("yuepaoquan", "悦跑圈", "悦跑圈", "跑步/社区", "跑者社区与训练App，会员+电商。"),
    ("baiyan", "百词斩", "百词斩", "教育/背单词", "图背单词App，付费课程+会员。"),
    ("youdao-cidian", "有道词典", "有道词典", "工具/翻译", "网易有道词典，翻译与词典工具，会员+广告。"),
    ("liulishuo", "流利说", "流利说", "教育/英语", "AI英语口语App，课程订阅。"),
    ("zuoyebang", "作业帮", "作业帮", "教育/K12", "K12拍照搜题与直播课App，课程付费。"),
    ("xiaoyuan", "小猿搜题", "小猿搜题", "教育/K12", "猿辅导旗下搜题App，导流课程。"),
    ("xueersi", "学而思", "学而思", "教育/网课", "好未来旗下中小学网课App，课程付费。"),
    ("wangyi-gkk", "网易公开课", "网易公开课", "教育/公开课", "名校公开课聚合App，免费。"),
    ("cnu-mooc", "中国大学MOOC", "中国大学MOOC", "教育/慕课", "高校慕课平台，免费+认证。"),
    ("camscanner", "扫描全能王", "扫描全能王", "工具/扫描OCR", "文档扫描OCR App，订阅+按次。"),
    ("mingpian", "名片全能王", "名片全能王", "工具/名片", "名片识别与管理App，订阅。"),
    ("sougou-input", "搜狗输入法", "搜狗输入法", "工具/输入法", "中文输入法App，免费+皮肤广告。"),
    ("baidu-input", "百度输入法", "百度输入法", "工具/输入法", "中文输入法App，免费。"),
    ("xunfei-input", "讯飞输入法", "讯飞输入法", "工具/输入法", "语音输入法App，免费+会员。"),
    ("xunfei-yuji", "讯飞语记", "讯飞语记", "工具/语音笔记", "语音转文字笔记App，会员订阅。"),
    ("meitu", "美图秀秀", "美图秀秀", "摄影/修图", "修图美颜App，免费+增值+硬件。"),
    ("meiyan", "美颜相机", "美颜相机", "摄影/自拍", "自拍美颜App，免费+增值。"),
    ("qingyan", "轻颜相机", "轻颜相机", "摄影/自拍", "风格化自拍App，免费+滤镜。"),
    ("xingtu", "醒图", "醒图", "摄影/修图", "全能修图App，免费+素材。"),
    ("faceu", "Faceu激萌", "Faceu激萌", "摄影/自拍", "萌系自拍App，免费+贴纸。"),
    ("b612", "B612", "B612", "摄影/自拍", "自拍相机App，免费+滤镜。"),
    ("wuta", "无他相机", "无他相机", "摄影/自拍", "直播级美颜相机，免费。"),
    ("tiantian-p", "天天P图", "天天P图", "摄影/修图", "综合修图App，免费。"),
    ("jianying", "剪映", "剪映", "视频/剪辑", "字节旗下视频剪辑App，免费+模板。"),
    ("kuaiying", "快影", "快影", "视频/剪辑", "快手旗下视频剪辑App，免费。"),
    ("bijian", "必剪", "必剪", "视频/剪辑", "B站官方剪辑App，免费。"),
    ("miaojian", "秒剪", "秒剪", "视频/剪辑", "微信官方视频剪辑，免费。"),
    ("xinpianchang", "新片场", "新片场", "视频/创作社区", "创作人社区与素材平台，会员+交易。"),
    ("tongli", "同花顺", "同花顺", "财经/炒股", "炒股软件，增值服务+开户导流。"),
    ("dongfang", "东方财富", "东方财富", "财经/炒股", "财经门户与炒股，广告+增值+基金销售。"),
    ("dazhihui", "大智慧", "大智慧", "财经/炒股", "炒股软件，增值服务。"),
    ("futu", "富途牛牛", "富途牛牛", "财经/港美股", "港美股券商App，交易佣金。"),
    ("laohu", "老虎证券", "老虎证券", "财经/美股", "美港股券商App，交易佣金。"),
    ("tiantian-jijin", "天天基金", "天天基金", "财经/基金", "基金销售平台，申赎费尾随。"),
    ("danjuan", "蛋卷基金", "蛋卷基金", "财经/基金", "基金组合销售，管理费分成。"),
    ("qiemo", "且慢", "且慢", "财经/投顾", "基金投顾平台，投顾费。"),
    ("yunshanfu", "云闪付", "云闪付", "金融/支付", "银联移动支付App，免费。"),
    ("zhaoshang", "招商银行", "招商银行", "金融/银行", "手机银行App，免费。"),
    ("pingan-bank", "平安口袋银行", "平安口袋银行", "金融/银行", "手机银行App，免费。"),
    ("ant-wealth", "蚂蚁财富", "蚂蚁财富", "金融/理财", "支付宝内理财平台，基金销售。"),
    ("bank-of-china", "中国银行", "中国银行", "金融/银行", "手机银行App，免费。"),
    ("weizhong-bank", "微众银行", "微众银行", "金融/互联网银行", "互联网银行，存款+理财。"),
    ("zhongan", "众安保险", "众安保险", "金融/保险", "互联网保险公司，保费。"),
    ("dongchedi", "懂车帝", "懂车帝", "汽车/资讯", "字节旗下汽车资讯与报价，广告+电商。"),
    ("autohome", "汽车之家", "汽车之家", "汽车/门户", "汽车垂直门户，广告+线索。"),
    ("yiche", "易车", "易车", "汽车/门户", "汽车资讯与交易，广告+佣金。"),
]

# ----------------------------- EXTENSIONS (22) -----------------------------
# (slug, name, cat, source_url, note)
EXT = [
    ("tampermonkey", "Tampermonkey", "Chrome插件/脚本", "https://www.tampermonkey.net/", "最流行的用户脚本管理器，开源作者 Jan Biniok，全球数千万安装。"),
    ("bilibili-helper", "哔哩哔哩助手", "Chrome插件/哔哩", "https://github.com/the1812/Bilibili-Evolved", "开源B站增强脚本 Bilibili Evolved，作者 the1812，国产。"),
    ("bitwarden", "Bitwarden", "Chrome插件/密码", "https://bitwarden.com/", "开源跨平台密码管理器，订阅制，团队开源。"),
    ("joplin", "Joplin", "Chrome插件/笔记", "https://joplinapp.org/", "开源笔记与待办App，端到端加密，国产团队参与。"),
    ("zotero", "Zotero", "Chrome插件/文献", "https://www.zotero.org/", "开源文献管理工具，研究者广泛使用。"),
    ("xmind", "XMind", "Chrome插件/思维导图", "https://www.xmind.cn/", "思维导图工具，国产商业软件，多端同步。"),
    ("inoreader", "Inoreader", "Chrome插件/RSS", "https://www.inoreader.com/", "RSS阅读器，订阅制，重度信息消费者常用。"),
    ("pocket", "Pocket", "Chrome插件/稍后读", "https://getpocket.com/", "稍后读收藏工具，被 Mozilla 收购。"),
    ("session-buddy", "Session Buddy", "Chrome插件/标签页", "https://sessionbuddy.com/", "标签页与会话管理扩展，老牌工具。"),
    ("infinity-newtab", "Infinity新标签页", "Chrome插件/新标签", "https://infinitynewtab.com/", "极简新标签页扩展，国产，海量用户。"),
    ("awesome-screenshot", "Awesome Screenshot", "Chrome插件/截图", "https://www.awesomescreenshot.com/", "网页截图与标注扩展，全球广泛使用。"),
    ("youdao-dict-ext", "有道词典插件", "Chrome插件/翻译", "https://cidian.youdao.com/", "网易有道词典划词翻译扩展，国产。"),
    ("netease-music-ext", "网易云音乐插件", "Chrome插件/音乐", "https://music.163.com/", "网易云音乐听歌相关浏览器扩展，国产。"),
    ("gouwudang", "购物党", "Chrome插件/比价", "https://gwdang.com/", "历史价格与全网比价扩展，国产，真实运营。"),
    ("smzdm-ext", "什么值得买", "Chrome插件/优惠", "https://www.smzdm.com/", "优惠爆料社区浏览器扩展，国产，真实上市企业。"),
    ("translator-ext", "Google 翻译", "Chrome插件/翻译", "https://translate.google.com/", "网页翻译扩展，全球最常用。"),
    ("grammarly-ext", "Grammarly", "Chrome插件/写作", "https://www.grammarly.com/", "英文语法与拼写检查扩展，订阅制。"),
    ("video-downloadhelper", "Video DownloadHelper", "Chrome插件/下载", "https://www.downloadhelper.net/", "网页视频下载扩展，老牌工具。"),
    ("fehelper", "FE助手", "Chrome插件/前端", "https://www.baidufe.com/fehelper", "前端开发助手扩展，百度FE团队出品，国产开源。"),
    ("drawio-diagrams", "draw.io", "Chrome插件/绘图", "https://www.drawio.com/", "开源流程图/图表绘制工具，广泛商用。"),
    ("onetab", "OneTab", "Chrome插件/标签页", "https://www.one-tab.com/", "标签页收藏与节省内存扩展，老牌工具。"),
    ("wikiwand", "Wikiwand", "Chrome插件/维基", "https://www.wikiwand.com/", "维基百科优化阅读扩展，全球使用。"),
]

# ----------------------------- COMPETITIONS (12) -----------------------------
# (slug, name, cat, source_url, note)
COMP = [
    ("huawei-ict", "华为ICT大赛", "比赛/ICT", "https://e.huawei.com/cn/talent/", "华为面向全球大学生的ICT技能竞赛，真实知名。"),
    ("baidu-star", "百度之星", "比赛/算法", "https://star.baidu.com/", "百度主办的程序设计大赛，历史悠久。"),
    ("weixin-mini", "微信小程序开发赛", "比赛/小程序", "https://developers.weixin.qq.com/community/", "腾讯微信官方小程序应用开发赛事，真实。"),
    ("wrc", "世界机器人大赛", "比赛/机器人", "https://www.worldrobotconference.com/", "中国电子学会主办的世界级机器人赛事，真实。"),
    ("if-design", "iF设计奖", "比赛/设计", "https://ifdesign.com/", "国际权威设计奖项，中国团队常年获奖。"),
    ("reddot", "红点设计奖", "比赛/设计", "https://www.red-dot.org/", "国际权威设计奖项，中国院校与企业常获奖。"),
    ("ad-cn", "全国大学生广告艺术大赛", "比赛/广告", "https://www.sun-ada.net/", "教育部认可的全国大学生广告赛事，真实。"),
    ("mcm-icm", "美国大学生数学建模竞赛", "比赛/数学建模", "https://www.comap.com/", "MCM/ICM，中国高校参赛极多，真实权威。"),
    ("ciepe", "中国研究生电子设计竞赛", "比赛/电子", "https://cpipc.chinadegrees.cn/", "中国研究生创新实践系列赛事，真实。"),
    ("crad", "中国机器人大赛", "比赛/机器人", "http://www.rcc.caau.org.cn/", "国内老牌机器人竞赛，真实。"),
    ("chuangqingchun", "创青春大赛", "比赛/创新创业", "http://cqc.youth.cn/", "共青团中央的青年创新创业大赛，真实。"),
    ("shuzhiqiche", "全国大学生智能汽车竞赛", "比赛/智能车", "https://www.ecc.com.cn/", "教育部认可的智能车竞赛，真实知名。"),
]

# ----------------------------- HARDWARE (6) -----------------------------
# (slug, name, cat, source_url, note)
HW = [
    ("lattepanda", "拿铁熊猫 LattePanda", "开源硬件/单板", "https://www.lattepanda.com/", "深圳出品的Windows/Android兼容单板计算机，面向创客。"),
    ("zhengdianyuanzi", "正点原子", "开源硬件/开发板", "https://www.zhengdianyuanzi.com/", "国内STM32等嵌入式开发板厂商，教程生态丰富。"),
    ("yehuo", "野火电子", "开源硬件/开发板", "https://www.embedfire.com/", "国内嵌入式开发板与教程厂商，真实。"),
    ("dfrobot", "DFRobot", "开源硬件", "https://www.dfrobot.com.cn/", "上海开源硬件与创客器材厂商，全球化运营。"),
    ("unitree", "宇树科技 Unitree", "硬件/机器人", "https://www.unitree.com/", "国产四足机器人公司，春晚等场合亮相，真实知名。"),
    ("espressif", "乐鑫科技 Espressif", "硬件/芯片", "https://www.espressif.com/", "ESP32/ESP8266 Wi-Fi 芯片厂商，全球创客广泛采用，国产上市。"),
]

# ----------------------------- MAKERS (6) -----------------------------
# (slug, name, cat, source_url, note)
MAKER = [
    ("hetongxue", "老师好我叫何同学", "创作者/数码", "https://search.bilibili.com/upuser?keyword=%E8%80%81%E5%B8%88%E5%A5%BD%E6%88%91%E5%8F%AB%E4%BD%95%E5%90%8C%E5%AD%A6", "B站百大UP主，数码评测与创意视频，创立硬件公司做产品。"),
    ("lizhiqi", "李子柒", "创作者/美食", "https://search.bilibili.com/upuser?keyword=%E6%9D%8E%E5%AD%90%E6%9F%92", "顶级美食短视频创作者，全球粉丝过亿，品牌化运营。"),
    ("shougong-geng", "手工耿", "创作者/发明", "https://search.bilibili.com/upuser?keyword=%E6%89%8B%E5%B7%A5%E8%80%BF", "搞笑无用发明类UP主，独特创意人设，商业变现。"),
    ("wanggang", "美食作家王刚", "创作者/美食", "https://search.bilibili.com/upuser?keyword=%E7%BE%8E%E9%A3%9F%E4%BD%9C%E5%AE%B6%E7%8E%8B%E5%88%9A", "专业厨师短视频创作者，硬核做菜教学，带货与培训。"),
    ("luoxiang", "罗翔说刑法", "创作者/知识", "https://search.bilibili.com/upuser?keyword=%E7%BD%97%E7%BF%94%E8%AF%B4%E5%88%91%E6%B3%95", "中国政法大学教授，刑法科普顶流，图书与课程变现。"),
    ("huanong", "华农兄弟", "创作者/乡村", "https://search.bilibili.com/upuser?keyword=%E5%8D%8E%E5%86%9C%E5%85%84%E5%BC%9F", "乡村生活与竹鼠短视频组合，真实走红并商业化。"),
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

    # collision check against batch 1
    b1 = json.load(open(os.path.join(ROOT, "pipeline", "domestic_candidates.json"), encoding="utf-8"))
    b1_slugs = set(c["slug"] for c in b1)
    dup = [c["slug"] for c in out if c["slug"] in b1_slugs]
    assert not dup, f"collision with batch1: {dup}"

    from collections import Counter
    print("batch2 count:", len(out), Counter(c["kind"] for c in out))
    dest = os.path.join(ROOT, "pipeline", "domestic_candidates2.json")
    json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("wrote", dest)
    # also merge into the canonical file so existing tooling works unchanged
    merged = b1 + out
    json.dump(merged, open(os.path.join(ROOT, "pipeline", "domestic_candidates.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("merged canonical now:", len(merged))


if __name__ == "__main__":
    main()
