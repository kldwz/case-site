const { chromium } = require('playwright');
const fs = require('fs');

// slug -> 候选官网 URL（多 URL 兜底，按序尝试）
const TARGETS = {
  boredhumans: ['https://boredhumans.com', 'https://www.boredhumans.com'],
  'build-concierge': ['https://www.buildconcierge.com', 'https://buildconcierge.com'],
  outward: ['https://www.outwardintelligence.com', 'https://outwardintelligence.com'],
  ambitio: ['https://ambitio.in', 'https://www.ambitio.in'],
  spott: ['https://spott.io', 'https://www.spott.io'],
  jaceai: ['https://www.jace.ai', 'https://jace.ai'],
  acquire: ['https://acquire.com', 'https://www.acquire.com'],
};

const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--no-proxy-server'] });
  const ctx = await browser.newContext({ userAgent: UA, viewport: { width: 1280, height: 800 } });
  for (const [slug, urls] of Object.entries(TARGETS)) {
    const out = `public/cases/${slug}/site.png`;
    let ok = false;
    for (const url of urls) {
      for (let attempt = 1; attempt <= 4 && !ok; attempt++) {
        try {
          const page = await ctx.newPage();
          await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
          await page.waitForTimeout(2500);
          await page.screenshot({ path: out, fullPage: false });
          const sz = fs.statSync(out).size;
          if (sz > 30000) { ok = true; console.log(`OK ${slug} <- ${url} (${sz}B)`); }
          else console.log(`SMALL ${slug} ${url} (${sz}B) retry`);
          await page.close();
        } catch (e) {
          console.log(`ERR ${slug} ${url} attempt${attempt}: ${String(e).slice(0, 80)}`);
        }
      }
      if (ok) break;
    }
    if (!ok) console.log(`FAIL ${slug}`);
  }
  await browser.close();
  console.log('DONE');
})();
