#!/usr/bin/env python3
"""Batch 4 (~100) domestic candidates, heavily weighted to 大奖类
(competitions / awards / prizes). Collision-checked against canonical
slugs AND existing case-file names, then merged into canonical.

Run: python3 _build_candidates4.py
"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def S(q):  # baidu search url (always valid, honest fallback)
    from urllib.parse import quote
    return "https://www.baidu.com/s?wd=" + quote(q)

# ----------------------------- COMPETITIONS / AWARDS (大奖类) -----------------------------
# (slug, name, cat, url, note)
COMPS = [
    ("lanqiao", "蓝桥杯大赛", "比赛获奖项目 / 软件算法 / 高校", "https://www.lanqiao.cn/",
     "蓝桥杯全国软件和信息技术专业人才大赛，工业和信息化部人才交流中心主办，面向高校学生的软件与信息技术竞赛，含软件、电子、嵌入式等赛项。"),
    ("ccf-ccsp", "CCF CSP / CCSP", "比赛获奖项目 / 软件能力 / 高校", "https://www.ccf.org.cn/",
     "中国计算机学会 CSP 软件能力认证与 CCSP 大学生计算机系统与程序设计竞赛，考察算法与系统能力。"),
    ("ccpc", "中国大学生程序设计竞赛 CCPC", "比赛获奖项目 / 算法 / 高校", "https://www.ccpc.io/",
     "中国大学生程序设计竞赛（CCPC），ICPC 风格的算法竞赛，由高校轮流承办。"),
    ("xiniuniao", "腾讯犀牛鸟创新大赛", "比赛获奖项目 / 产业创新 / 企业", "https://www.tencent.com/",
     "腾讯犀牛鸟创新人才与精英人才计划相关赛事，面向青年学者与学生的研究与创新竞赛。"),
    ("ascend-ai", "华为昇腾AI创新大赛", "比赛获奖项目 / AI 算子 / 企业", "https://www.hiascend.com/",
     "华为昇腾 AI 处理器生态的应用与算子创新大赛，鼓励基于昇腾芯片开发 AI 应用。"),
    ("kunpeng", "华为鲲鹏应用创新大赛", "比赛获奖项目 / 基础软件 / 企业", "https://www.hikunpeng.com/",
     "基于鲲鹏处理器的软件迁移与应用创新大赛，覆盖政务、金融、运营商等行业场景。"),
    ("harmonyos-dev", "鸿蒙开发者大赛", "比赛获奖项目 / 操作系统 / 企业", "https://developer.huawei.com/",
     "华为 HarmonyOS 鸿蒙生态应用开发大赛，鼓励开发者为鸿蒙系统构建原生应用与元服务。"),
    ("tencent-kaiwu", "腾讯开悟AI大赛", "比赛获奖项目 / 强化学习 / 企业", "https://aiarena.tencent.com/",
     "腾讯『开悟』多智能体强化学习开放平台主办的 AI 大赛，基于游戏环境训练智能体。"),
    ("tencent-light", "腾讯Light公益创新挑战赛", "比赛获奖项目 / AI for Good / 企业", "https://www.tencent.com/",
     "腾讯 Light 公益创新挑战赛，用 AI 技术解决教育、环保、文化等社会议题。"),
    ("jd-explore", "京东探索者大赛", "比赛获奖项目 / 电商算法 / 企业", "https://www.jd.com/",
     "京东探索者（JD Explore）人工智能大赛，聚焦零售、物流、供应链等场景的算法问题。"),
    ("didi-gaia", "滴滴盖亚大赛", "比赛获奖项目 / 出行算法 / 企业", "https://www.didiglobal.com/",
     "滴滴盖亚数据开放计划与算法大赛，开放出行轨迹数据供研究者参赛。"),
    ("kuaishou-algo", "快手算法大赛", "比赛获奖项目 / 视频算法 / 企业", "https://www.kuaishou.com/",
     "快手推荐与视频理解算法大赛，聚焦短视频推荐、内容理解与生成。"),
    ("iflytek-contest", "科大讯飞AI大赛", "比赛获奖项目 / 语音 AI / 企业", "https://www.iflytek.com/",
     "科大讯飞语音及人工智能应用大赛，覆盖语音识别、合成、自然语言处理等方向。"),
    ("sensetime-contest", "商汤AI大赛", "比赛获奖项目 / 计算机视觉 / 企业", "https://www.sensetime.com/",
     "商汤科技人工智能算法大赛，聚焦计算机视觉、大模型与多模态应用。"),
    ("megvii-contest", "旷视算法大赛", "比赛获奖项目 / 视觉算法 / 企业", "https://www.megvii.com/",
     "旷视科技计算机视觉算法大赛，面向人脸识别、图像理解等方向。"),
    ("netease-fuxi", "网易伏羲AI大赛", "比赛获奖项目 / 游戏 AI / 企业", "https://www.netease.com/",
     "网易伏羲人工智能大赛，聚焦游戏 AI、虚拟人、强化学习等方向。"),
    ("sogou-algo", "搜狗算法大赛", "比赛获奖项目 / 搜索算法 / 企业", "https://www.sogou.com/",
     "搜狗搜索与输入法算法大赛，覆盖自然语言处理与信息检索。"),
    ("ctrip-algo", "携程算法大赛", "比赛获奖项目 / 旅行算法 / 企业", "https://www.trip.com/",
     "携程旅行算法大赛，聚焦酒店推荐、搜索排序与供需预测。"),
    ("zhihu-algo", "知乎算法大赛", "比赛获奖项目 / 内容推荐 / 企业", "https://www.zhihu.com/",
     "知乎内容推荐与社区算法大赛，聚焦问答质量与信息分发。"),
    ("qihoo-360-ctf", "360安全大赛", "比赛获奖项目 / 安全 / 企业", "https://www.360.cn/",
     "360 安全应急响应与 CTF 网络安全竞赛，面向漏洞挖掘与攻防实战。"),
    ("tctf", "腾讯TCTF网络安全大赛", "比赛获奖项目 / 安全 / 企业", "https://www.tencent.com/",
     "腾讯信息安全争霸赛（TCTF），面向高校与企业安全研究者的 CTF 竞赛。"),
    ("xctf", "XCTF全国网络安全技术大赛", "比赛获奖项目 / 安全 / 高校", "https://www.xctf.org.cn/",
     "国内高校网络安全攻防竞赛联赛，由蓝莲花等战队发起。"),
    ("alibaba-security", "阿里聚安全算法大赛", "比赛获奖项目 / 安全算法 / 企业", "https://www.alibaba.com/",
     "阿里巴巴安全算法大赛，聚焦反欺诈、内容安全与风险识别。"),
    ("baidu-star", "百度之星", "比赛获奖项目 / 算法 / 高校", "https://star.baidu.com/",
     "百度之星程序设计大赛，百度主办的高校算法竞赛，历史悠久。"),
    ("pdd-algo", "拼多多算法大赛", "比赛获奖项目 / 电商算法 / 企业", "https://www.pinduoduo.com/",
     "拼多多算法与数据挖掘大赛，聚焦推荐、搜索与广告预估。"),
    ("bytedance-geek2", "字节跳动青训营大赛", "比赛获奖项目 / 工程 / 企业", "https://www.bytedance.com/",
     "字节跳动青训营与算法大赛，面向高校学生的工程与算法训练。"),
    ("craic", "中国机器人及人工智能大赛", "比赛获奖项目 / 机器人 / 高校", "https://www.craci.net/",
     "中国机器人及人工智能大赛（CRAIC），涵盖机器人、人工智能、数字创意等赛项。"),
    ("robocon-cn", "全国大学生机器人大赛RoboCon", "比赛获奖项目 / 机器人 / 高校", "https://www.cnrobocon.net/",
     "亚太大学生机器人大赛（ABU RoboCon）国内选拔赛，由中央电视台与自动化协会承办。"),
    ("robot-work", "中国工程机器人大赛", "比赛获奖项目 / 机器人 / 高校", "https://www.robotworker.com/",
     "中国工程机器人大赛暨国际公开赛，面向工程应用与搬运算术的机器人竞赛。"),
    ("urc-cn", "国际水中机器人大会URC", "比赛获奖项目 / 机器人 / 高校", S("国际水中机器人大会 URC"),
     "国际水中机器人联盟（URC）赛事，聚焦水下机器人感知、控制与协作。"),
    ("carc", "中国青少年机器人竞赛", "比赛获奖项目 / 机器人 / 青少年", "https://www.caa.org.cn/",
     "中国青少年机器人竞赛（CARC），由中国自动化学会主办，面向中小学的机器人赛事。"),
    ("cumcm", "全国大学生数学建模竞赛", "比赛获奖项目 / 数学建模 / 高校", "https://www.mcm.edu.cn/",
     "高教社杯全国大学生数学建模竞赛（CUMCM），规模最大的本科生学科竞赛之一。"),
    ("sz-cup", "深圳杯数学建模", "比赛获奖项目 / 数学建模 / 高校", "https://www.mcm.edu.cn/",
     "深圳杯数学建模挑战赛，面向全国大学生的数学建模竞赛。"),
    ("huawei-cup-mcm", "华为杯研究生数学建模", "比赛获奖项目 / 数学建模 / 研究生", "https://www.mcm.edu.cn/",
     "『华为杯』中国研究生数学建模竞赛，面向在读研究生的数学建模赛事。"),
    ("cgai", "中国研究生人工智能创新大赛", "比赛获奖项目 / AI / 研究生", "https://www.cie.org.cn/",
     "中国研究生人工智能创新大赛，聚焦 AI 算法与应用创新。"),
    ("icisc", "全国大学生集成电路创新创业大赛", "比赛获奖项目 / 芯片 / 高校", "https://www.icisc.cn/",
     "全国大学生集成电路创新创业大赛，覆盖芯片设计、验证与应用全链条。"),
    ("china-chip", "中国芯集成电路设计大赛", "比赛获奖项目 / 芯片 / 高校", "https://www.icisc.cn/",
     "『中国芯』全国集成电路设计大赛，鼓励自主芯片 IP 与 SoC 设计。"),
    ("embedded-chip", "全国大学生嵌入式芯片与系统设计竞赛", "比赛获奖项目 / 嵌入式 / 高校", "https://www.cie.org.cn/",
     "全国大学生嵌入式芯片与系统设计竞赛，面向 MCU/FPGA 与物联网应用。"),
    ("fpga-contest", "全国大学生FPGA创新设计竞赛", "比赛获奖项目 / FPGA / 高校", "https://www.cie.org.cn/",
     "全国大学生 FPGA 创新设计竞赛，聚焦可编程逻辑器件应用。"),
    ("phys-exp", "全国大学生物理实验竞赛", "比赛获奖项目 / 物理 / 高校", "https://www.moe.gov.cn/",
     "全国大学生物理实验竞赛，考察实验设计、操作与数据处理能力。"),
    ("chem-eng", "全国大学生化工设计竞赛", "比赛获奖项目 / 化工 / 高校", S("全国大学生化工设计竞赛"),
     "全国大学生化工设计竞赛，面向化工类学生的工程设计赛事。"),
    ("struct-design", "全国大学生结构设计竞赛", "比赛获奖项目 / 土木 / 高校", S("全国大学生结构设计竞赛"),
     "全国大学生结构设计竞赛，考察模型结构受力与创意设计。"),
    ("mech-innov", "全国大学生机械创新设计大赛", "比赛获奖项目 / 机械 / 高校", S("全国大学生机械创新设计大赛"),
     "全国大学生机械创新设计大赛，面向机械原理与机构创新的赛事。"),
    ("energy-save", "全国大学生节能减排竞赛", "比赛获奖项目 / 能源 / 高校", S("全国大学生节能减排社会实践与科技竞赛"),
     "全国大学生节能减排社会实践与科技竞赛，聚焦节能与环保科技作品。"),
    ("siemens-cup", "西门子杯中国智能制造挑战赛", "比赛获奖项目 / 智能制造 / 高校", "https://www.siemens.com/",
     "『西门子杯』中国智能制造挑战赛，面向工业自动化与数字化工厂的竞赛。"),
    ("ciscn", "全国大学生信息安全竞赛", "比赛获奖项目 / 安全 / 高校", "https://www.ciscn.com.cn/",
     "全国大学生信息安全竞赛（CISCN），由教育部高等学校信息安全教指委主办。"),
    ("overseas-talent", "中国海外人才创新创业大赛", "比赛获奖项目 / 创业 / 海归", S("中国海外人才创新创业大赛"),
     "中国海外人才创新创业大赛，面向留学人员回国创业的 projects 赛事。"),
    ("zgc-frontier", "中关村国际前沿科技创新大赛", "比赛获奖项目 / 科技 / 区域", S("中关村国际前沿科技创新大赛"),
     "中关村国际前沿科技创新大赛，聚焦人工智能、医药健康、智能制造等前沿领域。"),
    ("shenchuang", "深圳创新创业大赛", "比赛获奖项目 / 创业 / 区域", S("中国深圳创新创业大赛 深创赛"),
     "中国深圳创新创业大赛（深创赛），面向全国及海外的创新创业项目赛事。"),
    ("soda", "上海开放数据创新应用大赛SODA", "比赛获奖项目 / 数据 / 区域", S("上海开放数据创新应用大赛 SODA"),
     "上海开放数据创新应用大赛（SODA），开放政府数据供开发者构建应用。"),
    ("industrial-internet", "中国工业互联网大赛", "比赛获奖项目 / 工业互联网 / 产业", S("中国工业互联网大赛"),
     "中国工业互联网大赛，聚焦制造业数字化转型的 solutions 竞赛。"),
    ("industrial-app", "中国工业APP大赛", "比赛获奖项目 / 工业软件 / 产业", S("中国工业APP大赛"),
     "中国工业 APP 大赛，鼓励面向工业场景的轻量化应用软件。"),
    ("mobile-internet", "全国移动互联创新大赛", "比赛获奖项目 / 移动 / 创业", S("全国移动互联创新大赛"),
     "全国移动互联创新大赛，面向移动应用与物联网创业的赛事。"),
    ("smart-city", "中国智慧城市大赛", "比赛获奖项目 / 城市 / 产业", S("中国智慧城市大赛"),
     "中国智慧城市大赛，聚焦城市治理与智慧应用的创新方案。"),
    ("cvr", "中国虚拟现实大赛CVR", "比赛获奖项目 / VR / 高校", S("中国虚拟现实大赛 CVR"),
     "中国虚拟现实大赛（CVR），聚焦 VR/AR 内容与应用开发。"),
    ("open-source-cn", "中国开源创新大赛", "比赛获奖项目 / 开源 / 社区", S("中国开源创新大赛"),
     "中国开源创新大赛，鼓励开源项目与社区贡献。"),
    ("kechuangzhongguo", "科创中国创新创业大赛", "比赛获奖项目 / 创业 / 科协", S("科创中国创新创业大赛"),
     "『科创中国』创新创业大赛，由中国科协旗下平台主办。"),
    ("study-abroad", "中国留学人员创业大赛", "比赛获奖项目 / 创业 / 海归", S("中国留学人员创业大赛"),
     "中国留学人员创业大赛，面向海外留学人员回国创业项目。"),
    ("youth-sci", "中国科协青年科学家大赛", "比赛获奖项目 / 科研 / 青年", S("中国科协青年科学家大赛"),
     "中国科协青年科学家大赛，面向青年科技工作者的成果评选。"),
    ("cylc", "中国青年创业大赛", "比赛获奖项目 / 创业 / 青年", S("中国青年创业大赛"),
     "中国青年创业大赛，由共青团中央等主办的青年创业赛事。"),
    ("woman-venture", "中国妇女创业创新大赛", "比赛获奖项目 / 创业 / 女性", S("中国妇女创业创新大赛"),
     "中国妇女创业创新大赛，面向女性创业者的项目赛事。"),
    ("dia", "中国设计智造大奖DIA", "大奖类 / 设计 / 奖项", "https://www.dia-cn.com/",
     "中国设计智造大奖（DIA），由中国美术学院主办的国际化设计奖项。"),
    ("redstar", "中国创新设计红星奖", "大奖类 / 设计 / 奖项", S("中国创新设计红星奖"),
     "中国创新设计红星奖，由北京工业设计促进中心主办的设计奖项。"),
    ("goldenpin", "台湾金点设计奖", "大奖类 / 设计 / 奖项", "https://www.goldenpin.org.tw/",
     "台湾金点设计奖（Golden Pin Design Award），面向华语地区的设计奖项。"),
    ("good-design-cn", "中国好设计奖", "大奖类 / 设计 / 奖项", S("中国好设计奖"),
     "『中国好设计』奖，由中国工程院发起的设计奖项评选。"),
    ("guanghua", "光华龙腾奖", "大奖类 / 设计 / 奖项", S("光华龙腾奖 中国设计业十大杰出青年"),
     "光华龙腾奖，评选『中国设计业十大杰出青年』的设计奖项。"),
    ("wuwenjun", "吴文俊人工智能科学技术奖", "大奖类 / AI / 奖项", S("吴文俊人工智能科学技术奖"),
     "吴文俊人工智能科学技术奖，由中国人工智能学会设立，奖励 AI 领域成果。"),
    ("future-prize", "未来科学大奖", "大奖类 / 科学 / 奖项", "https://www.futureprize.org/",
     "未来科学大奖，民间发起的科学奖项，设生命科学、物质科学、数学与计算机奖。"),
    ("xplorer", "科学探索奖", "大奖类 / 科学 / 奖项", "https://www.xplorerprize.org/",
     "科学探索奖，由腾讯基金会发起，面向青年科学家的科研资助奖项。"),
    ("qingcheng", "达摩院青橙奖", "大奖类 / 科学 / 奖项", S("达摩院青橙奖"),
     "达摩院青橙奖，由阿里巴巴达摩院设立，奖励 35 岁以下青年学者。"),
    ("qiushi", "求是杰出科学家奖", "大奖类 / 科学 / 奖项", S("求是杰出科学家奖"),
     "求是杰出科学家奖，由香港求是科技基金会设立。"),
    ("shaw", "邵逸夫奖", "大奖类 / 科学 / 奖项", "https://www.shawprize.org/",
     "邵逸夫奖，表彰天文学、生命科学与数学领域的杰出贡献。"),
    ("turing", "图灵奖", "大奖类 / 计算机 / 奖项", "https://amturing.acm.org/",
     "图灵奖，计算机界最高荣誉，姚期智为首位华人得主。"),
    ("state-top", "国家最高科学技术奖", "大奖类 / 科学 / 奖项", "https://www.most.gov.cn/",
     "国家最高科学技术奖，中国科技领域最高荣誉，每年授予人数极少。"),
    ("natural-award", "国家自然科学奖", "大奖类 / 科学 / 奖项", "https://www.most.gov.cn/",
     "国家自然科学奖，奖励在基础研究中作出重大贡献的科技成果。"),
    ("invent-award", "国家技术发明奖", "大奖类 / 科学 / 奖项", "https://www.most.gov.cn/",
     "国家技术发明奖，奖励重大技术发明成果。"),
    ("progress-award", "国家科技进步奖", "大奖类 / 科学 / 奖项", "https://www.most.gov.cn/",
     "国家科技进步奖，奖励在技术开发与社会公益中有突出效益的成果。"),
    ("cn-patent", "中国专利奖", "大奖类 / 知识产权 / 奖项", "https://www.cnipa.gov.cn/",
     "中国专利奖，由国家知识产权局与世界知识产权组织联合评选。"),
    ("industry-grand", "中国工业大奖", "大奖类 / 工业 / 奖项", S("中国工业大奖"),
     "中国工业大奖，中国工业领域最高奖项。"),
    ("quality-award", "中国质量奖", "大奖类 / 质量 / 奖项", "https://www.samr.gov.cn/",
     "中国质量奖，由国家市场监管总局评选的质量管理奖项。"),
    ("liangsicheng", "梁思成建筑奖", "大奖类 / 建筑 / 奖项", S("梁思成建筑奖"),
     "梁思成建筑奖，中国建筑学界的最高荣誉奖项。"),
    ("standard-award", "中国标准创新贡献奖", "大奖类 / 标准 / 奖项", "https://www.samr.gov.cn/",
     "中国标准创新贡献奖，奖励在标准化工作中作出突出贡献的项目。"),
    ("ccf-award", "CCF王选奖", "大奖类 / 计算机 / 奖项", "https://www.ccf.org.cn/",
     "CCF 王选奖，中国计算机学会设立的计算机领域奖项。"),
    ("ieee-fellow-cn", "IEEE Fellow中国学者", "大奖类 / 学术荣誉 / 学者", "https://www.ieee.org/",
     "IEEE Fellow 为电气电子工程师学会的最高学术荣誉，众多中国学者入选。"),
    ("acm-fellow-cn", "ACM Fellow中国学者", "大奖类 / 学术荣誉 / 学者", "https://www.acm.org/",
     "ACM Fellow 为 ACM 的最高会员荣誉，表彰计算机领域杰出贡献者。"),
    ("nsfc-outstanding", "国家杰出青年科学基金", "大奖类 / 科研资助 / 学者", "https://www.nsfc.gov.cn/",
     "国家杰出青年科学基金（杰青），资助在基础研究方面已取得突出成绩的青年学者。"),
    ("nsfc-key", "国家优秀青年科学基金", "大奖类 / 科研资助 / 学者", "https://www.nsfc.gov.cn/",
     "国家优秀青年科学基金（优青），支持在基础研究方面取得突出成绩的青年学者。"),
    ("thousand-talent", "国家海外高层次人才引进计划", "大奖类 / 人才计划 / 学者", "https://www.most.gov.cn/",
     "国家海外高层次人才引进计划（千人计划），引进高层次海外人才。"),
    ("young-thousand", "青年千人计划", "大奖类 / 人才计划 / 学者", "https://www.most.gov.cn/",
     "青年千人计划，面向海外优秀青年人才的引进计划。"),
    ("changjiang", "长江学者奖励计划", "大奖类 / 人才计划 / 学者", "https://www.moe.gov.cn/",
     "长江学者奖励计划，教育部设立的特聘教授岗位制度。"),
    ("tencent-wnc", "腾讯微信小程序大赛", "比赛获奖项目 / 小程序 / 企业", "https://developers.weixin.qq.com/",
     "微信小程序应用开发赛事，鼓励开发者基于微信生态构建应用。"),
    ("alipay-mini", "支付宝小程序大赛", "比赛获奖项目 / 小程序 / 企业", "https://open.alipay.com/",
     "支付宝小程序开发赛事，面向生活服务与商业场景。"),
    ("douyin-open", "抖音开放平台大赛", "比赛获奖项目 / 短视频 / 企业", "https://open.douyin.com/",
     "抖音开放平台开发者大赛，鼓励基于抖音生态的内容与工具创新。"),
    ("bytedance-fe", "字节跳动前端挑战赛", "比赛获奖项目 / 前端 / 企业", "https://www.bytedance.com/",
     "字节跳动前端技术挑战赛，面向 Web 前端与跨端开发。"),
    ("meituan-ai", "美团AI大赛", "比赛获奖项目 / 生活服务算法 / 企业", "https://www.meituan.com/",
     "美团 AI 大赛，聚焦本地生活场景的算法与机器学习问题。"),
    ("baidu-ai-studio", "百度AI Studio大赛", "比赛获奖项目 / 深度学习 / 企业", "https://aistudio.baidu.com/",
     "百度 AI Studio 深度学习大赛，提供 PaddlePaddle 与算力支持。"),
    ("huawei-iot", "华为IoT大赛", "比赛获奖项目 / 物联网 / 企业", "https://www.huawei.com/",
     "华为物联网开发者大赛，面向智慧城市与行业物联应用。"),
    ("aliyun-dev", "阿里云开发者大赛", "比赛获奖项目 / 云计算 / 企业", "https://www.aliyun.com/",
     "阿里云开发者大赛，聚焦云原生、Serverless 与数据应用。"),
    ("tencent-cloud-dev", "腾讯云开发者大赛", "比赛获奖项目 / 云计算 / 企业", "https://cloud.tencent.com/",
     "腾讯云开发者大赛，面向云原生与 AI 应用开发。"),
    ("kingsoft-wps", "WPS办公软件大赛", "比赛获奖项目 / 办公软件 / 企业", "https://www.wps.cn/",
     "WPS 办公软件创新大赛，鼓励文档、表格、演示相关的插件与模板生态。"),
    ("xiaomi-vela", "小米Vela物联网大赛", "比赛获奖项目 / 物联网 / 企业", "https://www.mi.com/",
     "小米 Vela 物联网操作系统开发者大赛，面向智能家居与穿戴设备。"),
    ("oppo-coloros", "OPPO ColorOS大赛", "比赛获奖项目 / 移动系统 / 企业", "https://www.oppo.com/",
     "OPPO ColorOS 开发者与主题设计大赛，面向系统与视觉创意。"),
    ("vivo-originos", "vivo OriginOS大赛", "比赛获奖项目 / 移动系统 / 企业", "https://www.vivo.com.cn/",
     "vivo OriginOS 开发者与创意大赛，鼓励系统级应用创新。"),
    ("honor-magicos", "荣耀MagicOS大赛", "比赛获奖项目 / 移动系统 / 企业", "https://www.honor.com/",
     "荣耀 MagicOS 开发者大赛，面向跨设备与智慧互联应用。"),
    ("geektime", "极客时间技术大赛", "比赛获奖项目 / 技术社区 / 企业", "https://time.geekbang.org/",
     "极客时间主办的技术竞技与开发者活动，面向工程师成长。"),
    ("juejin", "掘金开发者大赛", "比赛获奖项目 / 技术社区 / 企业", "https://juejin.cn/",
     "掘金社区主办的开发者竞赛，面向前端与移动端创意。"),
    ("csdn", "CSDN开发者大赛", "比赛获奖项目 / 技术社区 / 企业", "https://www.csdn.net/",
     "CSDN 主办的开发者竞赛，覆盖算法、AI 与开源项目。"),
    ("infoq", "InfoQ技术大会挑战赛", "比赛获奖项目 / 技术社区 / 企业", "https://www.infoq.cn/",
     "InfoQ 技术社区主办的技术挑战赛与黑客马拉松。"),
    ("gitcode", "GitCode开源大赛", "比赛获奖项目 / 开源 / 社区", "https://gitcode.net/",
     "GitCode 开源开发者大赛，鼓励国产代码托管平台上的开源项目。"),
    ("gitee", "Gitee开源大赛", "比赛获奖项目 / 开源 / 社区", "https://gitee.com/",
     "Gitee 码云开源大赛，评选优秀国产开源项目。"),
]

# ----------------------------- EXTENSIONS (few) -----------------------------
EXT = [
    ("feishu-doc", "飞书文档插件", "Chrome 扩展 / 协作 / 中文", "https://www.feishu.cn/",
     "飞书文档相关浏览器扩展，便于在网页中快速收藏与插入到飞书云文档。"),
    ("yuque-ext", "语雀浏览器插件", "Chrome 扩展 / 笔记 / 中文", "https://www.yuque.com/",
     "语雀官方浏览器插件，支持网页剪藏与一键保存到知识库。"),
    ("tampermonkey-cn", "油猴中文脚本社区", "Chrome 扩展 / 脚本 / 中文", "https://greasyfork.org/",
     "Tampermonkey 油猴脚本管理器，GreasyFork 上有大量中文用户贡献的脚本。"),
    ("saladict", "沙拉查词", "Chrome 扩展 / 翻译 / 中文", "https://saladict.crimx.com/",
     "沙拉查词，开源的浏览器划词翻译扩展，支持多词典聚合。"),
]

# ----------------------------- HARDWARE (few) -----------------------------
HW = [
    ("esp32-cn", "ESP32国产模组生态", "开源硬件 / 物联网 / 中文", "https://www.espressif.com/",
     "乐鑫 ESP32 系列 Wi-Fi/蓝牙 SoC，催生大量中文创客与开源硬件项目。"),
    ("sipeed", "矽速Sipeed开发板", "开源硬件 / AI oT / 中文", "https://www.sipeed.com/",
     "Sipeed（矽速）出品 RISC-V 与 K210 等低功耗 AI 开发板，面向创客与教学。"),
    ("m5stack", "M5Stack模组", "开源硬件 / 模块化 / 中文", "https://m5stack.com/",
     "M5Stack 模块化堆叠式开发套件，广泛用于原型与工业 IoT 创意。"),
]

# ----------------------------- MAKER (few) -----------------------------
MAKER = [
    ("fengdahui", "冯大辉", "创作者/独立开发 / 技术IP / 中文", "https://dbanotes.net/",
     "冯大辉（Fenng），技术圈知名作者与连续创业者，早期丁香园、无码科技创始人。"),
    ("caoz", "曹政", "创作者/独立开发 / 技术IP / 中文", S("曹政 caoz"),
     "曹政（caoz），资深技术人、站长，以数据分析与技术思考类内容著称。"),
    ("ruanyf", "阮一峰", "创作者/独立开发 / 技术博客 / 中文", "https://www.ruanyifeng.com/",
     "阮一峰，知名技术博客作者，《科技爱好者周刊》主理人，前端与开源布道者。"),
]

def main():
    out = []
    for s, name, cat, url, note in COMPS:
        out.append({"slug": s, "name": name, "kind": "competition", "cat": cat,
                    "source_url": url, "note": note})
    for s, name, cat, url, note in EXT:
        out.append({"slug": s, "name": name, "kind": "ext", "cat": cat,
                    "source_url": url, "note": note})
    for s, name, cat, url, note in HW:
        out.append({"slug": s, "name": name, "kind": "hardware", "cat": cat,
                    "source_url": url, "note": note})
    for s, name, cat, url, note in MAKER:
        out.append({"slug": s, "name": name, "kind": "maker", "cat": cat,
                    "source_url": url, "note": note})

    # load canonical + existing case-file names
    b1 = json.load(open(os.path.join(ROOT, "pipeline", "domestic_candidates.json"), encoding="utf-8"))
    b1_slugs = set(c["slug"] for c in b1)
    existing_names = set()
    import glob, re
    for f in glob.glob(os.path.join(ROOT, "src/content/cases/*.md")):
        m = re.search(r'^name:\s*(.+)$', open(f, encoding="utf-8").read(), re.M)
        if m: existing_names.add(m.group(1).strip())

    cand_slugs = set()
    before = len(out)
    drop = []
    for c in list(out):
        if c["slug"] in b1_slugs or c["slug"] in cand_slugs:
            drop.append(("slug", c["slug"])); out.remove(c); continue
        if c["name"] in existing_names:
            drop.append(("name", c["name"])); out.remove(c); continue
        cand_slugs.add(c["slug"])
    print("preset:", before, "kept:", len(out), "dropped:", drop)
    print("kinds:", Counter(c["kind"] for c in out))

    dest = os.path.join(ROOT, "pipeline", "domestic_candidates4.json")
    json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("wrote", dest)
    merged = b1 + out
    json.dump(merged, open(os.path.join(ROOT, "pipeline", "domestic_candidates.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("merged canonical now:", len(merged))

if __name__ == "__main__":
    main()
