const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');
const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const tries = [
  { proxy: false, url: 'https://stimuler.app' },
  { proxy: false, url: 'https://www.stimuler.app' },
  { proxy: true,  url: 'https://stimuler.app' },
  { proxy: true,  url: 'https://www.stimuler.app' },
];
(async () => {
  for (const t of tries) {
    let browser;
    try {
      browser = await chromium.launch({ args: ['--no-sandbox'], ...(t.proxy ? { proxy: { server: 'http://127.0.0.1:55751' } } : {}) });
      const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
      console.log(`try proxy=${t.proxy} -> ${t.url}`);
      const resp = await page.goto(t.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      const status = resp ? resp.status() : 'n/a';
      console.log(`   status=${status}`);
      await sleep(3500);
      const outPath = `${OUT}/stimuler/site.png`;
      fs.mkdirSync(`${OUT}/stimuler`, { recursive: true });
      await page.screenshot({ path: outPath });
      const sz = fs.statSync(outPath).size;
      console.log(`   saved ${outPath} (${sz} bytes)`);
      if (sz >= 5000) { console.log('OK'); await browser.close(); process.exit(0); }
    } catch (e) {
      console.log(`   ERROR: ${e.message}`);
    } finally {
      if (browser) await browser.close();
    }
  }
  console.log('ALL FAILED');
})();
