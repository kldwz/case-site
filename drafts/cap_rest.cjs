const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const TARGETS = [
  ['rillet', 'https://rillet.com'],
  ['down-dog', 'https://www.downdogapp.com'],
];

async function shoot(browser, slug, url) {
  const dir = path.join(OUT, slug);
  fs.mkdirSync(dir, { recursive: true });
  const dest = path.join(dir, 'site.png');
  for (let attempt = 1; attempt <= 4; attempt++) {
    let page;
    try {
      page = await browser.newPage({
        viewport: { width: 1280, height: 900 },
        deviceScaleFactor: 2,
        proxy: { server: 'http://127.0.0.1:55751' },
      });
      await page.goto(url, { waitUntil: 'load', timeout: 40000 });
      await page.waitForTimeout(2500);
      await page.screenshot({ path: dest });
      const size = fs.statSync(dest).size;
      await page.close();
      if (size > 15000) {
        console.log('OK ' + slug + ' ' + size + ' bytes');
        return true;
      }
      console.log('SMALL ' + slug + ' attempt ' + attempt + ': ' + size);
    } catch (e) {
      const msg = String(e.message).split('\n')[0].slice(0, 80);
      console.log('ERR ' + slug + ' attempt ' + attempt + ': ' + msg);
      if (page) { try { await page.close(); } catch (_) { /* ignore */ } }
    }
    await new Promise(function (r) { setTimeout(r, 2000); });
  }
  console.log('FAIL ' + slug + ' ' + url);
  return false;
}

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  for (const pair of TARGETS) {
    await shoot(browser, pair[0], pair[1]);
  }
  await browser.close();
  console.log('--- done ---');
})();
