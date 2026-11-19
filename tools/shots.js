// Usage: node tools/shots.js out_dir url1 url2 ...  -> desktop (1366x900) + mobile (390x844) screenshots
const { chromium } = require('playwright');
(async () => {
  const [out, ...urls] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--ignore-certificate-errors-spki-list'] });
  for (const u of urls) {
    const name = u.replace(/^https?:\/\//, '').replace(/[^a-z0-9.]/gi, '_').slice(0, 60);
    for (const [tag, vp] of [['d', { width: 1366, height: 900 }], ['m', { width: 390, height: 844 }]]) {
      const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1, isMobile: tag === 'm', userAgent: tag === 'm' ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1' : undefined });
      const p = await ctx.newPage();
      try {
        await p.goto(u, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await p.waitForTimeout(2500);
        const sw = await p.evaluate(() => document.documentElement.scrollWidth);
        await p.screenshot({ path: `${out}/${name}_${tag}.jpg`, type: 'jpeg', quality: 55 });
        console.log(name, tag, 'ok', tag === 'm' ? `scrollWidth=${sw}` : '');
      } catch (e) { console.log(name, tag, 'ERR', e.message.slice(0, 80)); }
      await ctx.close();
    }
  }
  await b.close();
})();
