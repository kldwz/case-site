const { chromium } = require('playwright');
const fs = require('fs');
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--no-proxy-server'] });
  const ctx = await browser.newContext({ userAgent: UA, viewport: { width: 1280, height: 800 } });
  const out = 'public/cases/nomadtable/site.png';
  for (const url of ['https://www.nomadtable.app', 'https://nomadtable.app']) {
    for (let a = 1; a <= 3; a++) {
      try {
        const p = await ctx.newPage();
        await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
        await p.waitForTimeout(4000);
        await p.screenshot({ path: out, fullPage: false });
        const sz = fs.statSync(out).size;
        await p.close();
        console.log(url + ' -> ' + sz + 'B');
        if (sz > 30000) { await browser.close(); process.exit(0); }
      } catch (e) {
        console.log('ERR ' + url + ' a' + a + ': ' + String(e).slice(0, 70));
      }
    }
  }
  await browser.close();
  console.log('FINAL ' + (fs.existsSync(out) ? fs.statSync(out).size : 0));
})();
