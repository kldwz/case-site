const { chromium } = require('playwright');
const fs = require('fs');
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--no-proxy-server'] });
  const ctx = await browser.newContext({ userAgent: UA, viewport: { width: 1280, height: 800 } });
  const out = 'public/cases/workhero/site.png';
  const url = 'https://www.workhero.pro';
  for (let a = 1; a <= 4; a++) {
    try {
      const p = await ctx.newPage();
      await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 }).catch(async () => {
        // networkidle 超时则退回 load 再等
        await p.goto(url, { waitUntil: 'load', timeout: 60000 });
      });
      // 等待已知 hero 文本或至少让字体/CSS 就绪
      await p.waitForTimeout(6000);
      await p.screenshot({ path: out, fullPage: false });
      const sz = fs.statSync(out).size;
      await p.close();
      console.log('attempt ' + a + ' -> ' + sz + 'B');
      if (sz > 60000) { await browser.close(); process.exit(0); }
    } catch (e) {
      console.log('ERR a' + a + ': ' + String(e).slice(0, 70));
    }
  }
  await browser.close();
  console.log('FINAL ' + (fs.existsSync(out) ? fs.statSync(out).size : 0));
})();
