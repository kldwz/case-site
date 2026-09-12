const { chromium } = require('playwright');
const fs = require('fs');

const PROXY = 'http://127.0.0.1:1082';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';

(async () => {
  const browser = await chromium.launch({
    args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'],
    proxy: { server: PROXY }
  });
  const ctx = await browser.newContext({ userAgent: UA, viewport: { width: 1280, height: 800 } });
  await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); });
  const urls = ['https://ambitio.in', 'https://www.ambitio.in'];
  const out = 'public/cases/ambitio/site.png';
  let ok = false;
  for (const url of urls) {
    for (let attempt = 1; attempt <= 3 && !ok; attempt++) {
      try {
        const page = await ctx.newPage();
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
        // wait up to 18s for Cloudflare challenge to finish; check title/url
        for (let i = 0; i < 18; i++) {
          await page.waitForTimeout(1000);
          const t = (await page.title() || '').toLowerCase();
          const u = page.url();
          if (!t.includes('just a moment') && !t.includes('verifying') && !t.includes('attention required') && !u.includes('challenge')) break;
        }
        await page.waitForTimeout(2500);
        await page.screenshot({ path: out, fullPage: false });
        const sz = fs.statSync(out).size;
        const t = ((await page.title()) || '').toLowerCase();
        console.log(`attempt${attempt} ${url} size=${sz}B title=${(await page.title()).slice(0,60)}`);
        if (sz > 30000 && !t.includes('just a moment') && !t.includes('verifying')) { ok = true; console.log(`OK ambitio <- ${url} (${sz}B)`); }
        await page.close();
      } catch (e) {
        console.log(`ERR ambitio ${url} attempt${attempt}: ${String(e).slice(0,80)}`);
      }
    }
    if (ok) break;
  }
  if (!ok) console.log('FAIL ambitio');
  await browser.close();
})();
