const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');
const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const targets = [
  ['baimiao', 'https://apps.apple.com/cn/app/id1249901692'],
  ['panda-sms', 'https://apps.apple.com/cn/app/id1319191852'],
  ['time-block', 'https://apps.apple.com/cn/app/id1086617993'],
  ['sunmao-zheshan', 'https://apps.apple.com/cn/app/id837964581'],
  ['xingse', 'https://apps.apple.com/cn/app/id1018747351'],
  ['dyson-sphere-program', 'https://store.steampowered.com/app/1366540/'],
  ['sultans-game', 'https://store.steampowered.com/app/3117820/'],
  ['chinese-parents', 'https://store.steampowered.com/app/736190/'],
  ['warm-snow', 'https://store.steampowered.com/app/1296830/'],
  ['my-time-at-portia', 'https://store.steampowered.com/app/666140/'],
  ['audionova', 'https://devpost.com/software/audionova'],
  ['neuthera', 'https://devpost.com/software/neuthera-drug-discovery-platform'],
  ['civil-dialog', 'https://devpost.com/software/civil-dialog'],
  ['mochi-reading', 'https://devpost.com/software/mochi-6i7vuk'],
  ['marlin-phishing', 'https://devpost.com/software/marlin'],
  ['snapdragon-translator', 'https://devpost.com/software/snapdragon-ai-multilingual-translator'],
  ['browsegraph', 'https://devpost.com/software/browsegraph'],
  ['opale-prompts', 'https://devpost.com/software/opale'],
];
const PROXIES = ['http://127.0.0.1:1082', 'http://127.0.0.1:55751', null];
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  for (const proxyServer of PROXIES) {
    let browser;
    try {
      browser = await chromium.launch({ args: ['--no-sandbox'], ...(proxyServer ? { proxy: { server: proxyServer } } : {}) });
    } catch (e) { console.log(`launch fail ${proxyServer}: ${e.message}`); continue; }
    console.log(`\n### proxy=${proxyServer || 'DIRECT'}`);
    for (const [slug, url] of targets) {
      const outPath = `${OUT}/${slug}/site.png`;
      if (fs.existsSync(outPath) && fs.statSync(outPath).size > 5000) { console.log(`[${slug}] skip`); continue; }
      fs.mkdirSync(`${OUT}/${slug}`, { recursive: true });
      for (let a = 1; a <= 2; a++) {
        const page = await browser.newPage({ viewport: { width: 1280, height: 860 } });
        try {
          const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
          await sleep(3500);
          await page.screenshot({ path: outPath });
          const sz = fs.statSync(outPath).size;
          console.log(`[${slug}] status=${resp ? resp.status() : 'n/a'} ${sz} bytes`);
          if (sz < 5000) throw new Error('blank');
          break;
        } catch (e) {
          console.log(`[${slug}] attempt ${a} ERR: ${e.message}`);
          await sleep(1200);
        } finally { await page.close(); }
      }
    }
    await browser.close();
    const done = targets.filter(([s]) => { const p = `${OUT}/${s}/site.png`; return fs.existsSync(p) && fs.statSync(p).size > 5000; });
    console.log(`>>> covers ok: ${done.length}/${targets.length}`);
    if (done.length === targets.length) break;
  }
})();
