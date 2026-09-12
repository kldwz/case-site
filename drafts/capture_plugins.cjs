const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');

const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const targets = [
  ['tampermonkey', 'https://www.tampermonkey.net/'],
  ['ublock-origin', 'https://ublockorigin.com/'],
  ['sponsorblock', 'https://sponsor.ajay.app/'],
  ['enhancer-youtube', 'https://www.mrfdev.com/enhancer-for-youtube'],
  ['wappalyzer', 'https://www.wappalyzer.com/'],
  ['momentum', 'https://momentumdash.com/'],
  ['immersive-translate', 'https://immersivetranslate.com/en/'],
  ['singlefile', 'https://github.com/gildas-lormeau/SingleFile'],
  ['vimium', 'https://vimium.github.io/'],
  ['violentmonkey', 'https://violentmonkey.github.io/'],
];
// 依次尝试的代理配置：先本机 1082，再 55751（旧），最后直连
const PROXIES = ['http://127.0.0.1:1082', 'http://127.0.0.1:55751', null];

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  for (const proxyServer of PROXIES) {
    let browser;
    try {
      browser = await chromium.launch({
        args: ['--no-sandbox'],
        ...(proxyServer ? { proxy: { server: proxyServer } } : {}),
      });
    } catch (e) {
      console.log(`launch failed (proxy=${proxyServer}): ${e.message}`);
      continue;
    }
    console.log(`\n### using proxy=${proxyServer || 'DIRECT'}`);
    for (const [slug, url] of targets) {
      const outPath = `${OUT}/${slug}/site.png`;
      if (fs.existsSync(outPath) && fs.statSync(outPath).size > 5000) {
        console.log(`[${slug}] already has cover, skip`);
        continue;
      }
      fs.mkdirSync(`${OUT}/${slug}`, { recursive: true });
      for (let attempt = 1; attempt <= 3; attempt++) {
        const page = await browser.newPage({ viewport: { width: 1280, height: 860 } });
        try {
          const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
          await sleep(3500);
          await page.screenshot({ path: outPath });
          const sz = fs.statSync(outPath).size;
          console.log(`[${slug}] status=${resp ? resp.status() : 'n/a'} saved ${sz} bytes`);
          if (sz < 5000) throw new Error('blank');
          break;
        } catch (e) {
          console.log(`[${slug}] attempt ${attempt} ERROR: ${e.message}`);
          await sleep(1500);
        } finally {
          await page.close();
        }
      }
    }
    await browser.close();
    // 全部拿到图就收工
    const done = targets.filter(([s]) => {
      const p = `${OUT}/${s}/site.png`;
      return fs.existsSync(p) && fs.statSync(p).size > 5000;
    });
    console.log(`\n>>> covers ok: ${done.length}/${targets.length}`);
    if (done.length === targets.length) break;
  }
})();
