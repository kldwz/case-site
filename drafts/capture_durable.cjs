const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');

const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';
const urls = ['https://www.durable.co/', 'https://durable.co/', 'https://www.durable.co', 'https://durable.co'];

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--no-proxy-server'] });
  let ok = false;
  for (const url of urls) {
    for (let attempt = 1; attempt <= 6 && !ok; attempt++) {
      const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, userAgent: UA });
      try {
        console.log(`[durable] attempt ${attempt} -> ${url}`);
        const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
        const status = resp ? resp.status() : 'n/a';
        console.log(`   status=${status}`);
        await sleep(4000);
        const outPath = `${OUT}/durable/site.png`;
        await page.screenshot({ path: outPath, fullPage: false });
        const sz = fs.statSync(outPath).size;
        console.log(`   saved ${outPath} (${sz} bytes)`);
        if (sz < 5000) throw new Error('screenshot too small, likely blank');
        ok = true;
      } catch (e) {
        console.log(`   ERROR: ${e.message}`);
        await sleep(2000);
      } finally {
        await page.close();
      }
    }
    if (ok) break;
  }
  if (!ok) console.log('!! FAILED durable');
  await browser.close();
  console.log('DONE');
})();
