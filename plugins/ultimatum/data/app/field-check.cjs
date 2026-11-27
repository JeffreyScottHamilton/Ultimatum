// Field-condition checks against a demo page on a real local server: node field-check.cjs
// Each case sets how the fake API answers; the page must show a useful message, never a blank screen.
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');

let api = (req, res) => send(res, 200, { title: 'Hello' });
const saves = [];
function send(res, code, body, type = 'application/json') {
  res.writeHead(code, { 'content-type': type });
  res.end(typeof body === 'string' ? body : JSON.stringify(body));
}
const server = http.createServer((req, res) => {
  if (req.url === '/') return send(res, 200, fs.readFileSync(__dirname + '/field-demo.html', 'utf8'), 'text/html');
  if (req.url === '/api/save') { saves.push(req.headers['idempotency-key']); return setTimeout(() => send(res, 200, {}), 300); }
  if (req.url.startsWith('/img/')) return req.socket.destroy();          // image that never arrives
  if (req.url.startsWith('/login')) return send(res, 200, 'login page', 'text/html');
  return api(req, res);
});

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const BASE = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  let failed = 0;
  const ok = (name, cond, extra = '') => { console.log((cond ? 'ok   ' : 'FAIL ') + name + extra); if (!cond) failed++; };
  async function page() { const ctx = await browser.newContext(); return { ctx, page: await ctx.newPage() }; }
  const shows = (p, re, ms = 12000) => p.locator('#status').filter({ hasText: re }).waitFor({ timeout: ms }).then(() => true, () => false);

  const cases = [
    ['captive portal answers with HTML', (q, s) => send(s, 200, '<h1>Log in to hotel Wi-Fi</h1>', 'text/html'), /blocking us/],
    ['API takes 30 seconds', (q, s) => setTimeout(() => s.destroyed || send(s, 200, { title: 'late' }), 30000), /too long/],
    ['AI provider rate limit (429)', (q, s) => send(s, 429, { error: 'rate_limited' }), /busy/],
    ['provider down (503)', (q, s) => send(s, 503, {}), /went wrong/],
    ['push link to a deleted post', (q, s) => send(s, 200, { deleted: true }), /no longer available/],
  ];
  for (const [name, handler, want] of cases) {
    api = handler; const { ctx, page: p } = await page();
    await p.goto(BASE + '/'); ok(name, await shows(p, want)); await ctx.close();
  }

  { // offline, then back online
    api = (q, s) => send(s, 200, { title: 'Back' });
    const { ctx, page: p } = await page(); await p.goto(BASE + '/');
    await ctx.setOffline(true); await p.evaluate(() => load());
    ok('offline shows an offline message', await shows(p, /offline/, 5000));
    await ctx.setOffline(false);                       // Chromium fires the page's online event
    ok('back online recovers without a reload', await shows(p, 'Back', 5000)); await ctx.close();
  }
  { // slow 3G: throttling works on real requests only, not on page.route fulfils
    api = (q, s) => send(s, 200, { title: 'Hello' });
    const { ctx, page: p } = await page();
    const cdp = await ctx.newCDPSession(p);
    await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 400, downloadThroughput: 50000, uploadThroughput: 20000 });
    const t = Date.now(); await p.goto(BASE + '/'); const shown = await shows(p, 'Hello');
    const ms = Date.now() - t; ok('usable on slow 3G', shown && ms < 10000, ` (${ms} ms)`); await ctx.close();
  }
  { // double tap sends one request
    saves.length = 0; const { ctx, page: p } = await page(); await p.goto(BASE + '/');
    await p.locator('#save').dblclick(); await p.waitForTimeout(800);
    ok('double tap sends one save', saves.length === 1, ` (${saves.length})`); await ctx.close();
  }
  { // expired session goes to sign-in with the way back
    api = (q, s) => send(s, 401, { error: 'jwt expired' });
    const { ctx, page: p } = await page(); await p.goto(BASE + '/');
    ok('expired login goes to sign-in with next=', await p.waitForURL(/\/login\?next=%2F/, { timeout: 5000 }).then(() => true, () => false)); await ctx.close();
  }
  { // image that never loads leaves its alt text
    api = (q, s) => send(s, 200, { title: 'x' });
    const { ctx, page: p } = await page(); await p.goto(BASE + '/');
    ok('broken image shows its alt text', await p.locator('.img-fallback').waitFor({ timeout: 5000 }).then(() => true, () => false)); await ctx.close();
  }
  { // an uncaught error never leaves a blank screen
    const { ctx, page: p } = await page(); await p.goto(BASE + '/'); await shows(p, 'x');
    await p.evaluate(() => setTimeout(() => { throw new Error('boom'); }));
    ok('uncaught error shows a message', await shows(p, /Reload/, 3000)); await ctx.close();
  }
  await browser.close(); server.close();
  console.log(failed ? `${failed} failed` : 'all passed'); process.exit(failed ? 1 : 0);
})();
