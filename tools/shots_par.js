// Parallel screenshots: node tools/shots_par.js out_dir urls.txt [concurrency]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [out, list, conc = '5'] = process.argv.slice(2);
  const urls = fs.readFileSync(list, 'utf8').split('\n').filter(Boolean);
  const b = await chromium.launch();
  let i = 0;
  async function worker() {
    while (i < urls.length) {
      const u = urls[i++];
      const name = u.replace(/^https?:\/\//, '').replace(/[^a-z0-9.]/gi, '_').slice(0, 60);
      if (fs.existsSync(`${out}/${name}_m.jpg`)) continue;
      for (const [tag, vp] of [['d', { width: 1366, height: 900 }], ['m', { width: 390, height: 844 }]]) {
        const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1, isMobile: tag === 'm' });
        const p = await ctx.newPage();
        try {
          await p.goto(u, { waitUntil: 'domcontentloaded', timeout: 25000 });
          await p.waitForTimeout(2000);
          const sw = await p.evaluate(() => document.documentElement.scrollWidth);
          await p.screenshot({ path: `${out}/${name}_${tag}.jpg`, type: 'jpeg', quality: 55 });
          console.log(name, tag, 'ok', tag === 'm' ? `scrollWidth=${sw}` : '');
        } catch (e) { console.log(name, tag, 'ERR', e.message.slice(0, 80)); }
        await ctx.close();
      }
    }
  }
  await Promise.all(Array.from({ length: +conc }, worker));
  await b.close();
})();
