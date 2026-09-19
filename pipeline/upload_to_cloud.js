#!/usr/bin/env node
// 把 public/mini 上传到微信云开发云存储。
//
// 前置：npm i -g @cloudbase/cli && tcb login（微信扫码授权）
// 用法：CLOUD_ENV=你的环境ID node pipeline/upload_to_cloud.js
//
// 更省事的做法（推荐新手）：直接在微信开发者工具「云开发 → 存储」里，
// 把 public/mini/cases.json 拖到根目录、把 public/mini/covers/ 文件夹拖到 /covers/，
// 不用跑本脚本。
//
// 上传完成后，到「云开发 → 存储」复制文件ID前缀（形如 cloud://环境ID.xxxx/），
// 填进小程序 lib/store.js 的 CLOUD_FILE_BASE（末尾带 /）。

const { execSync } = require('child_process')
const path = require('path')

const CASE_SITE = '/Users/hxw/codebuddy/case-site'
const SRC = path.join(CASE_SITE, 'public', 'mini')
const ENV = process.env.CLOUD_ENV

if (!ENV) {
  console.log('用法: CLOUD_ENV=你的环境ID node pipeline/upload_to_cloud.js')
  process.exit(1)
}
try {
  execSync('tcb --version', { stdio: 'ignore' })
} catch (e) {
  console.log('未检测到 @cloudbase/cli，先执行: npm i -g @cloudbase/cli && tcb login')
  process.exit(1)
}

console.log('上传 cases.json -> 云存储根目录 ...')
execSync(`tcb storage upload ${path.join(SRC, 'cases.json')} cases.json --envId ${ENV}`, { stdio: 'inherit' })

console.log('上传 covers/ -> 云存储 /covers/ ...')
execSync(`tcb storage upload ${path.join(SRC, 'covers')} covers --envId ${ENV}`, { stdio: 'inherit' })

console.log('\n完成。请到「云开发 → 存储」复制文件ID前缀(形如 cloud://%s.xxxx/)，', ENV)
console.log('填进 case-miniprogram/lib/store.js 的 CLOUD_FILE_BASE（末尾带 /）。')
