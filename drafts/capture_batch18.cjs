const { chromium } = require('playwright');

const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';

const TARGETS = [
  { slug: 'instantly', urls: ['https://instantly.ai', 'https://www.instantly.ai'] },
  { slug: 'lovable', urls: ['https://lovable.dev', 'https://www.lovable.dev'] },
  { slug: 'reweb', urls: ['https://reweb.so', 'https://www.reweb.so'] },
  { slug: 'vellum', urls: ['https://www.vellum.ai', 'https://vellum.ai'] },
  { slug: 'salesrobot', urls: ['https://salesrobot.co', 'https://www.salesrobot.co'] },
  { slug: 'infracost', urls: ['https://www.infracost.io', 'https://infracost.io'] },
  { slug: 'gojiberry', urls: ['https://www.gojiberry.ai', 'https://gojiberry.ai'] },
];

const fs = require('fs');

async function shoot(page, url) {
  let lastErr;
  for (let attempt = 1; attempt <= 6; attempt++) {
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await page.waitForTimeout(3500);
      const buf = await page.screenshot({ fullPage: false, type: 'png' });
      if (buf.length < 30000) {
        lastErr = new Error(`too small ${buf.length} @ ${url}`);
        await page.waitForTimeout(2000);
        continue;
      }
      return buf;
    } catch (e) {
      lastErr = e;
      await page.waitForTimeout(1500);
    }
  }
  throw lastErr || new Error('failed ' + url);
}

(async () => {
  const browser = await chromium.launch({
    args: ['--no-sandbox', '--no-proxy-server'],
  });
  const page = await browser.newPage({ userAgent: UA, viewport: { width: 1366, height: 900 } });
  await page.context().setExtraHTTPHeaders({ 'Accept-Language': 'en-US,en;q=0.9' });

  for (const t of TARGETS) {
    let saved = false;
    for (const url of t.urls) {
      try {
        const buf = await shoot(page, url);
        fs.writeFileSync(`${OUT}/${t.slug}/site.png`, buf);
        console.log(`OK ${t.slug} <- ${url} (${buf.length}B)`);
        saved = true;
        break;
      } catch (e) {
        console.log(`FAIL ${t.slug} @ ${url}: ${e.message}`);
      }
    }
    if (!saved) console.log(`!! ${t.slug} ALL URLS FAILED`);
  }
  await browser.close();
  console.log('DONE');
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
