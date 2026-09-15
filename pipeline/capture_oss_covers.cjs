const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');

const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const targets = [
  ['supabase', 'https://supabase.com', 'Supabase', '开源 PostgreSQL 后端平台'],
  ['posthog',  'https://posthog.com',  'PostHog',  '开源产品分析平台'],
  ['cal-com',  'https://cal.com',      'Cal.com',  '开源日程调度'],
  ['dub',      'https://dub.co',       'Dub',      '开源链接管理'],
  ['appwrite', 'https://appwrite.io',  'Appwrite', '开源后端开发平台'],
  ['twenty',   'https://twenty.com',   'Twenty',   '开源 CRM'],
  ['plane',    'https://plane.so',     'Plane',    '开源项目管理'],
];

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

function placeholderHtml(name, tagline) {
  return `data:text/html,` + encodeURIComponent(`<!doctype html><html><head><meta charset="utf-8">
<style>
  *{margin:0;box-sizing:border-box}
  body{width:1280px;height:860px;display:flex;flex-direction:column;justify-content:center;
    background:linear-gradient(135deg,#0f172a 0%,#1e293b 45%,#0ea5e9 100%);
    color:#e2e8f0;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;padding:90px}
  .kicker{font-size:26px;letter-spacing:6px;color:#7dd3fc;opacity:.9}
  .name{font-size:120px;font-weight:800;margin:18px 0 10px;color:#fff;line-height:1.05}
  .tag{font-size:40px;color:#cbd5e1}
  .foot{position:absolute;bottom:70px;font-size:22px;color:#94a3b8}
</style></head><body>
  <div class="kicker">开源变现案例</div>
  <div class="name">${name}</div>
  <div class="tag">${tagline}</div>
  <div class="foot">官网截图抓取受限 · 2026-09-15</div>
</body></html>`);
}

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  for (const [slug, url, name, tagline] of targets) {
    const dir = `${OUT}/${slug}`;
    fs.mkdirSync(dir, { recursive: true });
    const page = await browser.newPage({ viewport: { width: 1280, height: 860 } });
    let real = false;
    try {
      await page.goto(url, { waitUntil: 'load', timeout: 35000 });
      await page.waitForTimeout(2500);
      await page.screenshot({ path: `${dir}/site.png` });
      real = true;
    } catch (e) {
      try {
        await page.goto(placeholderHtml(name, tagline), { waitUntil: 'load', timeout: 15000 });
        await page.waitForTimeout(400);
        await page.screenshot({ path: `${dir}/site.png` });
      } catch (e2) { console.error(`  !! ${slug} 占位也失败: ${e2.message}`); }
    }
    await page.close();
    const sz = fs.existsSync(`${dir}/site.png`) ? fs.statSync(`${dir}/site.png`).size : 0;
    console.log(`  ${slug}: ${real ? 'REAL' : 'PLACEHOLDER'} (${sz} bytes)`);
  }
  await browser.close();
  console.log('covers done');
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
