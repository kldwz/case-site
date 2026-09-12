const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');

const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const PROXY = 'http://127.0.0.1:55751';
const targets = [
  ['evenup', 'https://evenuplaw.com'],
  ['balthazar', 'https://balthazar.app'],
  ['omnidocs', 'https://omnidocs.com'],
];

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch({
    args: ['--no-sandbox'],
    proxy: { server: PROXY },
  });
  for (const [slug, url] of targets) {
    fs.mkdirSync(`${OUT}/${slug}`, { recursive: true });
    let ok = false;
    for (let attempt = 1; attempt <= 8 && !ok; attempt++) {
      const page = await browser.newPage({
        viewport: { width: 1280, height: 900 },
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
      });
      try {
        console.log(`[${slug}] attempt ${attempt} -> ${url}`);
        const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
        const status = resp ? resp.status() : 'n/a';
        console.log(`   status=${status}`);
        if (status >= 400) throw new Error('bad status ' + status);
        await sleep(4000);
        const outPath = `${OUT}/${slug}/site.png`;
        await page.screenshot({ path: outPath });
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
    if (!ok) console.log(`!! FAILED ${slug}`);
  }
  await browser.close();
  console.log('DONE');
})();
