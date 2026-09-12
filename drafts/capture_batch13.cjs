const { chromium } = require('/Users/hxw/.workbuddy/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');

const OUT = '/Users/hxw/codebuddy/case-site/public/cases';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';
const targets = [
  ['wispr-flow', ['https://wisprflow.ai', 'https://www.wisprflow.ai']],
  ['coderabbit', ['https://www.coderabbit.ai', 'https://coderabbit.ai']],
  ['tern-group', ['https://www.terngroup.com', 'https://tern.group', 'https://www.tern.group', 'https://tern-group.com']],
  ['geviti', ['https://www.gogeviti.com', 'https://gogeviti.com']],
  ['terrafirma', ['https://www.terrafirma.com', 'https://terrafirma.build', 'https://www.terrafirma.build', 'https://terrafirma.io']],
  ['alta', ['https://www.altahq.com', 'https://altahq.com']],
  ['sapiom', ['https://www.sapiom.ai', 'https://sapiom.ai']],
];

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch({
    args: ['--no-sandbox', '--no-proxy-server'],
  });
  for (const [slug, urls] of targets) {
    fs.mkdirSync(`${OUT}/${slug}`, { recursive: true });
    let ok = false;
    for (const url of urls) {
      for (let attempt = 1; attempt <= 6 && !ok; attempt++) {
        const page = await browser.newPage({
          viewport: { width: 1280, height: 900 },
          userAgent: UA,
        });
        try {
          console.log(`[${slug}] attempt ${attempt} -> ${url}`);
          const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
          const status = resp ? resp.status() : 'n/a';
          console.log(`   status=${status}`);
          await sleep(5000);
          const outPath = `${OUT}/${slug}/site.png`;
          await page.screenshot({ path: outPath, fullPage: false });
          const sz = fs.statSync(outPath).size;
          console.log(`   saved ${outPath} (${sz} bytes)`);
          if (sz < 5000) {
            fs.unlinkSync(outPath);
            throw new Error('screenshot too small, likely blank');
          }
          ok = true;
        } catch (e) {
          console.log(`   ERROR: ${e.message}`);
          await sleep(1500);
        } finally {
          await page.close();
        }
      }
      if (ok) break;
    }
    if (!ok) console.log(`!! FAILED ${slug}`);
  }
  await browser.close();
  console.log('DONE');
})();
