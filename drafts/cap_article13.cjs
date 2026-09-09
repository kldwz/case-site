const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');
const OUT = '/Users/hxw/wechat_workspace/documents/shots';
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--no-sandbox'] }); // localhost: 不走代理

  // 1. 首页
  let p = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2 });
  await p.goto('http://localhost:4411/', { waitUntil: 'load', timeout: 30000 });
  await sleep(2500);
  await p.screenshot({ path: `${OUT}/13-01-home.png` });
  console.log('home', fs.statSync(`${OUT}/13-01-home.png`).size);
  await p.close();

  // 2. 案例详情页
  p = await browser.newPage({ viewport: { width: 1280, height: 1000 }, deviceScaleFactor: 2 });
  await p.goto('http://localhost:4411/cases/getdavid/', { waitUntil: 'load', timeout: 30000 });
  await sleep(2000);
  await p.screenshot({ path: `${OUT}/13-02-case.png` });
  console.log('case', fs.statSync(`${OUT}/13-02-case.png`).size);
  await p.close();

  // 3. 真实配置文件片段（渲染真实 sources.yaml 内容）
  const yaml = fs.readFileSync('/Users/hxw/codebuddy/case-site/pipeline/config/sources.yaml', 'utf8')
    .split('\n').slice(17, 34).join('\n')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
    body{margin:0;background:#1e1e2e;font-family:"SF Mono",Menlo,monospace;padding:28px 32px}
    pre{color:#cdd6f4;font-size:15px;line-height:1.65;margin:0;white-space:pre}
    .k{color:#89b4fa}.c{color:#6c7086}.s{color:#a6e3a1}
  </style></head><body><pre>${yaml}</pre></body></html>`;
  fs.writeFileSync('/tmp/src_preview.html', html);
  p = await browser.newPage({ viewport: { width: 900, height: 620 }, deviceScaleFactor: 2 });
  await p.goto('file:///tmp/src_preview.html', { waitUntil: 'load' });
  await sleep(500);
  await p.screenshot({ path: `${OUT}/13-03-sources.png` });
  console.log('sources', fs.statSync(`${OUT}/13-03-sources.png`).size);
  await p.close();

  await browser.close();
  console.log('DONE');
})();
