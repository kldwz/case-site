const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');

const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
// 直连（无代理）：本机出口对部分站点可达但抖动，靠重试兜底
const targets = [
  ['sanas', 'https://sanas.ai'],
  ['veed', 'https://veed.io'],
  ['reclaim', 'https://reclaim.ai'],
  ['prohance', 'https://prohance.ai'],
  ['picturethis', 'https://picturethisai.com'],
  ['cognition', 'https://cognition.ai'],
  ['langdock', 'https://langdock.com'],
];

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  for (const [slug, url] of targets) {
    fs.mkdirSync(`${OUT}/${slug}`, { recursive: true });
    let ok = false;
    for (let attempt = 1; attempt <= 6 && !ok; attempt++) {
      const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
      try {
        console.log(`[${slug}] attempt ${attempt} -> ${url}`);
        const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
        const status = resp ? resp.status() : 'n/a';
        console.log(`   status=${status}`);
        await sleep(4000);
        const outPath = `${OUT}/${slug}/site.png`;
        await page.screenshot({ path: outPath, fullPage: false });
        const sz = fs.statSync(outPath).size;
        console.log(`   saved ${outPath} (${sz} bytes)`);
        if (sz < 8000) throw new Error('screenshot too small, likely blank');
        ok = true;
      } catch (e) {
        console.log(`   ERROR: ${e.message}`);
        await sleep(2000);
      } finally {
        await page.close();
      }
    }
    if (!ok) console.log(`!! FAILED ${slug}`);
  }
  await browser.close();
  console.log('DONE');
})();
