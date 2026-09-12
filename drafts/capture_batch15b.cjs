const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');
const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';

const targets = [
  ['flodesk', ['https://flodesk.com/', 'https://flodesk.com', 'https://www.flodesk.com/', 'https://flodesk.com/pricing']],
  ['fella-health', ['https://www.fellahealth.com/', 'https://fellahealth.com/', 'https://www.fellahealth.com']],
];

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--no-proxy-server'] });
  for (const [slug, urls] of targets) {
    fs.mkdirSync(`${OUT}/${slug}`, { recursive: true });
    let ok = false;
    for (const url of urls) {
      for (let attempt = 1; attempt <= 10 && !ok; attempt++) {
        const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, userAgent: UA });
        try {
          console.log(`[${slug}] try ${attempt} -> ${url}`);
          const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
          console.log(`   status=${resp ? resp.status() : 'n/a'}`);
          await sleep(8000);
          const outPath = `${OUT}/${slug}/site.png`;
          await page.screenshot({ path: outPath, fullPage: false });
          const sz = fs.statSync(outPath).size;
          console.log(`   saved ${sz} bytes`);
          if (sz < 30000) { fs.unlinkSync(outPath); throw new Error('too small: ' + sz); }
          ok = true;
        } catch (e) {
          console.log(`   ERR: ${e.message}`);
          await sleep(2000);
        } finally {
          await page.close();
        }
      }
      if (ok) break;
    }
    if (!ok) console.log(`!! FAILED ${slug}`);
  }
  await browser.close();
  console.log('DONE');
})();
