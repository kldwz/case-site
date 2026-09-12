const { chromium } = require('playwright');
const fs = require('fs');

const TARGETS = {
  serviceform: ['https://serviceform.com', 'https://www.serviceform.com'],
  workhero: ['https://www.workhero.pro', 'https://workhero.pro'],
  nexlev: ['https://www.nexlev.io', 'https://nexlev.io'],
  sublaunch: ['https://sublaunch.com', 'https://www.sublaunch.com'],
  meltflex: ['https://www.meltflexai.com', 'https://meltflexai.com'],
  netris: ['https://netris.io', 'https://www.netris.io'],
  nomadtable: ['https://www.nomadtable.com', 'https://nomadtable.com'],
};

const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';

// 两种网络模式：直连（清代理） / 系统代理 1082
const MODES = [
  { name: 'direct', args: ['--no-sandbox', '--no-proxy-server'], proxy: null },
  { name: 'proxy', args: ['--no-sandbox'], proxy: { server: 'http://127.0.0.1:1082' } },
];

async function shoot(ctx, slug, url, out) {
  const page = await ctx.newPage();
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(3500);
    await page.screenshot({ path: out, fullPage: false });
    const sz = fs.statSync(out).size;
    await page.close();
    return sz;
  } catch (e) {
    try { await page.close(); } catch (_) {}
    throw e;
  }
}

(async () => {
  for (const mode of MODES) {
    console.log(`\n===== MODE: ${mode.name} =====`);
    const browser = await chromium.launch({ args: mode.args, proxy: mode.proxy || undefined });
    const ctx = await browser.newContext({ userAgent: UA, viewport: { width: 1280, height: 800 } });

    for (const [slug, urls] of Object.entries(TARGETS)) {
      const out = `public/cases/${slug}/site.png`;
      // 已有足够大的封面就跳过
      if (fs.existsSync(out) && fs.statSync(out).size > 30000) {
        console.log(`SKIP ${slug} (already ${fs.statSync(out).size}B)`);
        continue;
      }
      let ok = false;
      for (const url of urls) {
        for (let attempt = 1; attempt <= 3 && !ok; attempt++) {
          try {
            const sz = await shoot(ctx, slug, url, out);
            if (sz > 30000) { ok = true; console.log(`OK ${slug} <- ${url} (${sz}B)`); }
            else console.log(`SMALL ${slug} ${url} (${sz}B) retry`);
          } catch (e) {
            console.log(`ERR ${slug} ${url} a${attempt}: ${String(e).slice(0, 70)}`);
          }
        }
        if (ok) break;
      }
      if (!ok) console.log(`PENDING ${slug}`);
    }
    await browser.close();
  }

  console.log('\n===== FINAL =====');
  for (const slug of Object.keys(TARGETS)) {
    const out = `public/cases/${slug}/site.png`;
    const sz = fs.existsSync(out) ? fs.statSync(out).size : 0;
    console.log(`${sz > 30000 ? 'OK  ' : 'FAIL'} ${slug} ${sz}B`);
  }
})();
