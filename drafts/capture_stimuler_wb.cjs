const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');
const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const urls = [
  'https://web.archive.org/web/2025/https://stimuler.app/',
  'https://web.archive.org/web/2024/https://stimuler.app/',
];
(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'], proxy: { server: 'http://127.0.0.1:55751' } });
  for (const url of urls) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    try {
      console.log('-> ' + url);
      const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
      const status = resp ? resp.status() : 'n/a';
      console.log('   status=' + status);
      await sleep(4000);
      const outPath = OUT + '/stimuler/site.png';
      fs.mkdirSync(OUT + '/stimuler', { recursive: true });
      await page.screenshot({ path: outPath });
      const sz = fs.statSync(outPath).size;
      console.log('   saved ' + outPath + ' (' + sz + ' bytes)');
      if (sz >= 8000) { console.log('OK'); await page.close(); await browser.close(); process.exit(0); }
    } catch (e) {
      console.log('   ERROR: ' + e.message);
    } finally { await page.close(); }
  }
  await browser.close();
  console.log('ALL FAILED');
})();
