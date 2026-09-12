const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');
const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const targets = [
  ['baimiao', 'https://apps.apple.com/cn/app/id1249901692'],
  ['panda-sms', 'https://apps.apple.com/cn/app/id1319191852'],
  ['time-block', 'https://apps.apple.com/cn/app/id1086617993'],
  ['jiangmu', 'https://apps.apple.com/cn/app/id1489424663'],
  ['xiaorichang', 'https://apps.apple.com/cn/app/id1263789061'],
  ['dyson-sphere', 'https://store.steampowered.com/app/1366540/'],
  ['sultans-game', 'https://store.steampowered.com/app/3117820/'],
  ['warm-snow', 'https://store.steampowered.com/app/1296830/'],
  ['chinese-parents', 'https://store.steampowered.com/app/736190/'],
  ['taiwu', 'https://store.steampowered.com/app/838350/'],
];
const PROXIES = ['http://127.0.0.1:1082', 'http://127.0.0.1:55751', null];
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  for (const proxyServer of PROXIES) {
    let browser;
    try { browser = await chromium.launch({ args: ['--no-sandbox'], ...(proxyServer ? { proxy: { server: proxyServer } } : {}) }); }
    catch (e) { console.log('launch fail', proxyServer); continue; }
    console.log(`\n### proxy=${proxyServer || 'DIRECT'}`);
    for (const [slug, url] of targets) {
      const outPath = `${OUT}/${slug}/site.png`;
      if (fs.existsSync(outPath) && fs.statSync(outPath).size > 5000) { console.log(`[${slug}] skip`); continue; }
      fs.mkdirSync(`${OUT}/${slug}`, { recursive: true });
      for (let attempt = 1; attempt <= 3; attempt++) {
        const page = await browser.newPage({ viewport: { width: 1280, height: 860 } });
        try {
          const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 50000 });
          await sleep(4000);
          await page.screenshot({ path: outPath });
          const sz = fs.statSync(outPath).size;
          console.log(`[${slug}] status=${resp ? resp.status() : 'n/a'} ${sz} bytes`);
          if (sz < 5000) throw new Error('blank');
          break;
        } catch (e) {
          console.log(`[${slug}] attempt ${attempt} ERR ${e.message.slice(0, 80)}`);
          await sleep(1500);
        } finally { await page.close(); }
      }
    }
    await browser.close();
    const done = targets.filter(([s]) => { const p = `${OUT}/${s}/site.png`; return fs.existsSync(p) && fs.statSync(p).size > 5000; });
    console.log(`\n>>> covers ok: ${done.length}/${targets.length}`);
    if (done.length === targets.length) break;
  }
})();
