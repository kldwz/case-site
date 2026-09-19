#!/usr/bin/env python3
"""把 case-miniprogram 的远程资源（public/mini）同步到腾讯云 COS。

小程序切到远程模式后（lib/store.js 里填了 ASSET_HOST），本脚本把
public/mini/cases.json 与 public/mini/covers/*.jpg 上传到 COS 桶的 mini/ 前缀下：
    mini/cases.json
    mini/covers/<slug>.jpg
小程序端即可通过  https://<bucket>.cos.<region>.myqcloud.com/mini/...  拉取。

配置（任选其一）：
  A. 环境变量：
       export COS_SECRET_ID=xxx
       export COS_SECRET_KEY=yyy
       export COS_BUCKET=case-mini-1250000000
       export COS_REGION=ap-guangzhou        # 桶所在地域
  B. 同目录新建 cos_config.py：
       SECRET_ID="xxx"; SECRET_KEY="yyy"; BUCKET="case-mini-1250000000"; REGION="ap-guangzhou"

依赖：pip3 install cos-python-sdk-v5
用法：python3 pipeline/upload_to_cos.py
"""
import os, sys, glob

CASE_SITE = "/Users/hxw/codebuddy/case-site"
SRC = os.path.join(CASE_SITE, "public", "mini")
PREFIX = "mini"   # COS 上的目标前缀

# ---- 读取配置 ----
SECRET_ID = os.environ.get("COS_SECRET_ID")
SECRET_KEY = os.environ.get("COS_SECRET_KEY")
BUCKET = os.environ.get("COS_BUCKET")
REGION = os.environ.get("COS_REGION")
cfg_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cos_config.py")
if cfg_py.endswith("cos_config.py") and os.path.exists(cfg_py):
    ns = {}
    exec(open(cfg_py, encoding="utf-8").read(), ns)
    SECRET_ID = SECRET_ID or ns.get("SECRET_ID")
    SECRET_KEY = SECRET_KEY or ns.get("SECRET_KEY")
    BUCKET = BUCKET or ns.get("BUCKET")
    REGION = REGION or ns.get("REGION")

missing = [n for n, v in (("COS_SECRET_ID", SECRET_ID), ("COS_SECRET_KEY", SECRET_KEY),
                          ("COS_BUCKET", BUCKET), ("COS_REGION", REGION)) if not v]
if missing:
    print("缺少配置：", ", ".join(missing))
    print("方式A: export COS_SECRET_ID=... 等环境变量")
    print("方式B: 在 pipeline/cos_config.py 里写 SECRET_ID/SECRET_KEY/BUCKET/REGION")
    sys.exit(1)

try:
    from qcloud_cos import CosConfig, CosS3Client
except ImportError:
    print("缺少依赖，先执行: pip3 install cos-python-sdk-v5")
    sys.exit(1)

config = CosConfig(Region=REGION, SecretId=SECRET_ID, SecretKey=SECRET_KEY)
client = CosS3Client(config)

def upload(local, key):
    client.upload_file(Bucket=BUCKET, LocalFilePath=local, Key=key,
                       EnableMD5=False, progress_callback=None)
    print("->", key)

def main():
    if not os.path.isdir(SRC):
        print("找不到", SRC, "，先跑 gen_miniprogram_data.py + gen_mini_covers.py")
        sys.exit(1)
    # cases.json
    jf = os.path.join(SRC, "cases.json")
    if os.path.exists(jf):
        upload(jf, PREFIX + "/cases.json")
    # covers
    covers = sorted(glob.glob(os.path.join(SRC, "covers", "*.jpg")))
    for c in covers:
        slug = os.path.splitext(os.path.basename(c))[0]
        upload(c, PREFIX + "/covers/" + slug + ".jpg")
    print(f"完成：{len(covers)} 张封面 + cases.json -> cos://{BUCKET}/{PREFIX}/")
    print(f"小程序 ASSET_HOST 应填: https://{BUCKET}.cos.{REGION}.myqcloud.com")

if __name__ == "__main__":
    main()
