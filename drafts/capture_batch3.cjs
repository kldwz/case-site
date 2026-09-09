const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const TARGETS = [
  ['klar', 'https://klarlabs.ai'],
  ['rox', 'https://rox.com'],
  ['huntress', 'https://huntress.com'],
  ['opencode', 'https://opencode.ai'],
  ['tjm-labs', 'https://www.tjmlabs.com'],
  ['rillet', 'https://rillet.com'],
  ['down-dog', 'https://www.downdogapp.com'],
];

async function shoot(browser, slug, url) {
  const dir = path.join(OUT, slug);
  fs.mkdirSync(dir, { recursive: true });
  const dest = path.join(dir, 'site.png');
  for (let attempt = 1; attempt <= 5; attempt++) {
    let page;
    try {
      page = await browser.newPage({
        viewport: { width: 1280, height: 900 },
        deviceScaleFactor: 2,
        proxy: { server: 'http://127.0.0.1:55751' },
      });
      await page.goto(url, { waitUntil: 'load', timeout: 45000 });
      await page.waitForTimeout(2500);
      await page.screenshot({ path: dest });
      const size = fs.statSync(dest).size;
      await page.close();
      if (size > 15000) {
        console.log(`OK   ${slug.padEnd(12)} ${size} bytes  ${url}`);
        return true;
      }
      console.log(`SMALL ${slug} attempt ${attempt}: ${size} bytes, retry`);
    } catch (e) {
      console.log(`ERR  ${slug} attempt ${attempt}: ${String(e.message).split('\n')[0].slice(0, 90)}`);
      if (page) { try { await page.close(); } catch (_) {} }
    }
    await new Promise(r => setTimeout(r, 2500));
  }
  console.log(`FAIL ${slug}  ${url}`);
  return false;
}

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  for (const [slug, url] of TARGETS) {
    await shoot(browser, slug, url);
  }
  await browser.close();
  console.log('--- done ---');
})();
