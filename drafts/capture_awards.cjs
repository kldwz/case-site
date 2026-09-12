const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');
const targets = [
  ['audionova','https://devpost.com/software/audionova'],
  ['snapdragon-translator','https://devpost.com/software/snapdragon-ai-multilingual-translator'],
  ['civil-dialog','https://devpost.com/software/civil-dialog'],
  ['neuthera','https://devpost.com/software/neuthera-drug-discovery-platform'],
  ['opale','https://devpost.com/software/opale'],
  ['marlin-phishing','https://devpost.com/software/marlin'],
  ['browsegraph','https://devpost.com/software/browsegraph'],
  ['canvas-insights','https://devpost.com/software/canvas-student-insights-with-ai'],
  ['mochi-readability','https://devpost.com/software/mochi-6i7vuk'],
];
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  for (const [slug, url] of targets) {
    const p = await b.newPage({ viewport: { width: 1280, height: 860 } });
    try {
      const r = await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await new Promise(x => setTimeout(x, 3500));
      fs.mkdirSync(`/Users/hxw/codebuddy/case-site/public/cases/${slug}`, { recursive: true });
      await p.screenshot({ path: `/Users/hxw/codebuddy/case-site/public/cases/${slug}/site.png` });
      console.log(slug, 'status', r && r.status(), fs.statSync(`/Users/hxw/codebuddy/case-site/public/cases/${slug}/site.png`).size);
    } catch (e) { console.log(slug, 'ERR', e.message.slice(0,80)); }
    await p.close();
  }
  await b.close();
})();
