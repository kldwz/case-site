#!/usr/bin/env python3
"""把 case-miniprogram 的远程资源（public/mini）同步到七牛云 Kodo。

小程序切到远程模式后（lib/store.js 里填了 ASSET_HOST = 七牛 CDN 域名），
本脚本把 public/mini/cases.json 与 public/mini/covers/*.jpg 上传到七牛空间，
key 定为：
    mini/cases.json
    mini/covers/<slug>.jpg
小程序端即可通过  https://<七牛CDN域名>/mini/...  拉取（store.js 的拼接口径一致）。

配置（任选其一）：
  A. 环境变量：
       export QINIU_AK=xxxx
       export QINIU_SK=yyyy
       export QINIU_BUCKET=case-mini
       export QINIU_DOMAIN=https://xxxx.clouddn.com   # 七牛给的融合 CDN 域名
  B. 同目录新建 qiniu_config.py：
       AK="xxx"; SK="yyy"; BUCKET="case-mini"; DOMAIN="https://xxxx.clouddn.com"

依赖：pip3 install qiniu
用法：python3 pipeline/upload_to_qiniu.py
"""
import os, sys, glob

CASE_SITE = "/Users/hxw/codebuddy/case-site"
SRC = os.path.join(CASE_SITE, "public", "mini")
PREFIX = "mini"

AK = os.environ.get("QINIU_AK")
SK = os.environ.get("QINIU_SK")
BUCKET = os.environ.get("QINIU_BUCKET")
DOMAIN = os.environ.get("QINIU_DOMAIN")
cfg_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qiniu_config.py")
if os.path.exists(cfg_py):
    ns = {}
    exec(open(cfg_py, encoding="utf-8").read(), ns)
    AK = AK or ns.get("AK")
    SK = SK or ns.get("SK")
    BUCKET = BUCKET or ns.get("BUCKET")
    DOMAIN = DOMAIN or ns.get("DOMAIN")

missing = [n for n, v in (("QINIU_AK", AK), ("QINIU_SK", SK),
                          ("QINIU_BUCKET", BUCKET), ("QINIU_DOMAIN", DOMAIN)) if not v]
if missing:
    print("缺少配置：", ", ".join(missing))
    print("方式A: export QINIU_AK=... 等环境变量")
    print("方式B: 在 pipeline/qiniu_config.py 里写 AK/SK/BUCKET/DOMAIN")
    sys.exit(1)

try:
    from qiniu import Auth, put_file
except ImportError:
    print("缺少依赖，先执行: pip3 install qiniu")
    sys.exit(1)

auth = Auth(AK, SK)

def upload(local, key):
    token = auth.upload_token(BUCKET, key, 3600)
    ret, info = put_file(token, key, local, version="v2")
    if info is not None and info.status_code == 200:
        print("->", key)
    else:
        print("FAIL", key, info)

def main():
    if not os.path.isdir(SRC):
        print("找不到", SRC, "，先跑 gen_miniprogram_data.py + gen_mini_covers.py")
        sys.exit(1)
    jf = os.path.join(SRC, "cases.json")
    if os.path.exists(jf):
        upload(jf, PREFIX + "/cases.json")
    covers = sorted(glob.glob(os.path.join(SRC, "covers", "*.jpg")))
    for c in covers:
        slug = os.path.splitext(os.path.basename(c))[0]
        upload(c, PREFIX + "/covers/" + slug + ".jpg")
    print(f"完成：{len(covers)} 张封面 + cases.json -> 七牛空间 {BUCKET}/mini/")
    d = DOMAIN.rstrip("/")
    print(f"小程序 ASSET_HOST 应填: {d}")
    print(f"列表地址自检: {d}/{PREFIX}/cases.json")

if __name__ == "__main__":
    main()
