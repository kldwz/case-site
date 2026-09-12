const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');
const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

const targets = [
  ['hightouch', ['https://hightouch.com/']],
  ['fable-security', ['https://fablesecurity.com/', 'https://www.fablesecurity.com/']],
  ['oligo', ['https://www.oligo.security/', 'https://oligo.security/']],
  ['skello', ['https://www.skello.io/', 'https://skello.io/']],
  ['hyperverge', ['https://www.hyperverge.co/', 'https://hyperverge.co/']],
  ['heyreach', ['https://heyreach.io/', 'https://www.heyreach.io/']],
  ['screen-studio', ['https://screen.studio/', 'https://www.screen.studio/']],
];

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--no-proxy-server'] });
  for (const [slug, urls] of targets) {
    fs.mkdirSync(`${OUT}/${slug}`, { recursive: true });
    const outPath = `${OUT}/${slug}/site.png`;
    let ok = false;
    for (const url of urls) {
      for (let attempt = 1; attempt <= 8 && !ok; attempt++) {
        const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, userAgent: UA });
        try {
          console.log(`[${slug}] attempt ${attempt} -> ${url}`);
          const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
          console.log(`   status=${resp ? resp.status() : 'n/a'}`);
          await sleep(5000);
          await page.screenshot({ path: outPath, fullPage: false });
          const sz = fs.statSync(outPath).size;
          console.log(`   saved ${sz} bytes`);
          if (sz < 30000) { fs.unlinkSync(outPath); throw new Error('too small/blank'); }
          ok = true;
        } catch (e) {
          console.log(`   ERROR: ${e.message}`);
          await sleep(1500);
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
