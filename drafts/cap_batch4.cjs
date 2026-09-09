const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');

const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const PROXY = 'http://127.0.0.1:55751';
const targets = [
  ['rogo', 'https://rogo.ai'],
  ['headshotpro', 'https://headshotpro.com'],
  ['crustdata', 'https://crustdata.com'],
  ['design-arena', 'https://designarena.ai'],
  ['clipto', 'https://clipto.ai'],
  ['bustem', 'https://bustem.com'],
  ['beehiiv', 'https://beehiiv.com'],
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
    for (let attempt = 1; attempt <= 6 && !ok; attempt++) {
      const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
      try {
        console.log(`[${slug}] attempt ${attempt} -> ${url}`);
        const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
        const status = resp ? resp.status() : 'n/a';
        console.log(`   status=${status}`);
        await sleep(3500);
        const outPath = `${OUT}/${slug}/site.png`;
        await page.screenshot({ path: outPath });
        const sz = fs.statSync(outPath).size;
        console.log(`   saved ${outPath} (${sz} bytes)`);
        if (sz < 5000) throw new Error('screenshot too small, likely blank');
        ok = true;
      } catch (e) {
        console.log(`   ERROR: ${e.message}`);
        await sleep(1500);
      } finally {
        await page.close();
      }
    }
    if (!ok) console.log(`!! FAILED ${slug}`);
  }
  await browser.close();
  console.log('DONE');
})();
