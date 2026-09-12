const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');
const PROXIES = ['http://127.0.0.1:1082', 'http://127.0.0.1:55751', null];
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  let browser;
  for (const p of PROXIES) {
    try { browser = await chromium.launch({ args: ['--no-sandbox'], ...(p ? { proxy: { server: p } } : {}) }); break; }
    catch (e) { console.log('launch fail', p, e.message); }
  }
  if (!browser) { console.log('NO BROWSER'); return; }
  const out = [];
  for (let page = 1; page <= 4; page++) {
    const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    try {
      await p.goto(`https://devpost.com/software?page=${page}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await sleep(2500);
      const items = await p.evaluate(() => {
        const res = [];
        document.querySelectorAll('a[href^="/software/"]').forEach((a) => {
          const href = a.getAttribute('href');
          if (!href || href.startsWith('/software/new') || href.startsWith('/software/search')) return;
          const card = a.closest('div.gallery-item') || a.parentElement;
          const text = (card ? card.innerText : a.innerText || '').replace(/\s+/g, ' ').trim();
          if (!text) return;
          const m = text.match(/(Winner|Finalist|Honorable Mention|Runner Up|Grand Prize|1st place|2nd place|3rd place)/i);
          res.push({ url: 'https://devpost.com' + href, text: text.slice(0, 300), award: m ? m[1] : null });
        });
        return res;
      });
      console.log(`page ${page}: ${items.length} items, awarded=${items.filter(i => i.award).length}`);
      out.push(...items);
    } catch (e) { console.log(`page ${page} ERR ${e.message}`); }
    await p.close();
    await sleep(1200);
  }
  await browser.close();
  // 去重
  const seen = new Set(); const uniq = [];
  for (const it of out) { if (!seen.has(it.url)) { seen.add(it.url); uniq.push(it); } }
  fs.writeFileSync('/tmp/devpost_list.json', JSON.stringify(uniq, null, 1));
  console.log('total uniq', uniq.length, 'awarded', uniq.filter(i => i.award).length);
})();
