const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const seen = new Set();
  const pages = [
    'https://devpost.com/hackathons',
    'https://devpost.com/hackathons?challenge_type[]=all&sort=recent',
    'https://devpost.com/hackathons?status=upcoming',
    'https://devpost.com/hackathons?status=past',
  ];
  for (const url of pages) {
    const p = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
    try {
      await p.goto(url, { waitUntil: 'load', timeout: 60000 });
      await sleep(4000);
      // 滚动到底，触发懒加载
      for (let i = 0; i < 8; i++) {
        await p.mouse.wheel(0, 3000);
        await sleep(1200);
      }
      const links = await p.evaluate(() => {
        const out = [];
        document.querySelectorAll('a[href]').forEach(a => {
          const h = a.getAttribute('href');
          if (!h) return;
          const m1 = h.match(/^https:\/\/([a-z0-9-]+)\.devpost\.com\/?$/);
          if (m1) out.push({ type: 'sub', slug: m1[1] });
          const m2 = h.match(/^\/hackathons\/([a-z0-9-]+)/);
          if (m2) out.push({ type: 'path', slug: m2[1] });
        });
        return out;
      });
      links.forEach(l => seen.add(l.type + ':' + l.slug));
      console.log(`${url} -> links=${links.length}`);
    } catch (e) { console.log(`${url} ERR ${e.message.slice(0, 80)}`); }
    await p.close();
    await sleep(1500);
  }
  await browser.close();
  const arr = [...seen].map(s => { const [t, slug] = s.split(':'); return { t, slug }; })
    .filter(x => !['api', 'help', 'info', 'secure', 'www', 'assets'].includes(x.slug));
  fs.writeFileSync('/tmp/devpost_events.json', JSON.stringify(arr, null, 1));
  console.log('\n赛事候选:', arr.length);
  arr.forEach(x => console.log(' ', x.t, x.slug));
})();
