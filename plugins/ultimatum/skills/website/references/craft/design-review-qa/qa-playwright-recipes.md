# QA recipes with Playwright

Read when you need to actually poke a running page: links, dead buttons, empty form submits, console and network errors. Pairs with `qa-modes-and-loop.md` (what to test) and `../../../../work/references/browser-verification.md` (the standard checks and `ult-browser.mjs`).

## One-page sweep (local pages only)

The script below was run against a scratch page with planted flaws (a 404 link, a button that does nothing, a form that swallows an empty submit, a `console.error`) and reported each one. It refuses any host except `127.0.0.1` and `localhost`, and lists, never clicks, controls whose label suggests logging out, deleting, paying or cancelling. Save it as `qa-sweep.mjs` next to a Playwright install ([Playwright library docs](https://playwright.dev/docs/library)).

```js
// qa-sweep.mjs <url> <outDir>: one page, read-and-poke. Local pages only.
import { chromium } from 'playwright';
import fs from 'node:fs';

const [url, out = '.ultimatum/qa-sweep'] = process.argv.slice(2);
if (!url || !/^https?:\/\/(127\.0\.0\.1|localhost)[:/]/.test(url)) {
  console.error('usage: node qa-sweep.mjs http://127.0.0.1:PORT/page [outDir]  (local pages only)');
  process.exit(2);
}
fs.mkdirSync(out, { recursive: true });
// Controls whose name suggests a destructive or session-ending action are listed, never clicked.
const RISKY = /log-?out|sign-?out|delet|remov|cancel|unsubscribe|pay|buy/i;

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
const page = await ctx.newPage();
const findings = [];
const consoleErrors = [];
const failedRequests = [];
page.on('console', (m) => m.type() === 'error' && consoleErrors.push(m.text()));
page.on('pageerror', (e) => consoleErrors.push('uncaught: ' + e.message));
page.on('response', (r) => r.status() >= 400 && failedRequests.push(`${r.status()} ${r.url()}`));

try {
  await page.goto(url, { waitUntil: 'load' });
  await page.screenshot({ path: `${out}/initial.png`, fullPage: true });

  // 1. Same-origin links, checked with HEAD through the page's own request context.
  const hrefs = await page.$$eval('a[href]', (as) => [...new Set(as.map((a) => a.href))]);
  for (const h of hrefs.filter((h) => new URL(h).origin === new URL(url).origin && !RISKY.test(h))) {
    const r = await ctx.request.head(h).catch(() => null);
    if (!r || r.status() >= 400) findings.push({ kind: 'broken-link', where: h, status: r ? r.status() : 'ERR' });
  }

  // 2. Dead buttons: a click that changes no text, no URL and no hidden-element count.
  const state = () => page.evaluate(() =>
    document.body.innerText + '|' + location.href + '|' + document.querySelectorAll('[hidden]').length);
  for (const b of await page.$$('button:not([type=submit]):not([disabled])')) {
    const label = (await b.textContent()).trim();
    if (RISKY.test(label)) { findings.push({ kind: 'not-clicked', where: label }); continue; }
    const before = await state();
    await b.click({ timeout: 2000 }).catch(() => {});
    await page.waitForTimeout(250);
    if ((await state()) === before) findings.push({ kind: 'dead-button', where: label });
  }

  // 3. Empty submit on every form: did anything tell the person why nothing happened?
  for (const f of await page.$$('form')) {
    const submit = await f.$('[type=submit]');
    if (!submit) continue;
    const before = await page.evaluate(() => document.body.innerText);
    await submit.click();
    await page.waitForTimeout(250);
    const blocked = await f.evaluate((el) => !el.checkValidity());
    const told = (await page.evaluate(() => document.body.innerText)) !== before;
    if (!blocked && !told) findings.push({ kind: 'silent-empty-submit', where: await f.evaluate((el) => el.id || 'form') });
  }
  await page.screenshot({ path: `${out}/after.png`, fullPage: true });
} finally {
  await browser.close();
}
const result = { url, findings, consoleErrors, failedRequests };
fs.writeFileSync(`${out}/sweep.json`, JSON.stringify(result, null, 2));
console.log(JSON.stringify(result));
```

Run: `node qa-sweep.mjs http://127.0.0.1:3000/ .ultimatum/qa/sweep`. Exit 2 means the URL was refused. Output is JSON with `findings`, `consoleErrors`, `failedRequests`, and two screenshots.

## Reading the result

- `broken-link`: file as functional, severity by how central the link is (`qa-taxonomy.md`).
- `dead-button`: confirm by hand before filing; a button that only plays an animation or copies to the clipboard changes none of the three things the script watches.
- `silent-empty-submit`: the form accepted an empty submit and told nobody why. UX, medium unless it is the booking or sign-up form.
- `not-clicked`: a control the script skipped on purpose. Test it by hand only on a local target.
- Console errors and 4xx/5xx responses: category console; one finding per root cause.

## Other small checks

- **Console after each step:** keep `page.on('console')` and `page.on('pageerror')` attached for the whole session and print what is new after every interaction, not once at the end ([Page events](https://playwright.dev/docs/api/class-page#page-event-console)).
- **Phone width:** `browser.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true })`, then compare `document.documentElement.scrollWidth` with `innerWidth`; a larger scroll width is a sideways scroll bug. The audit script in `design-audit-recipes.md` already does this.
- **Tab path:** press Tab repeatedly and log `document.activeElement` each time; a repeat inside a modal is correct, a repeat outside is a trap.
- **State after reload and back:** fill a form, reload, press back; note what survives. Lost state is functional.
- **Network failure:** `context.setOffline(true)` then retry the action; an error message that says what to do is the pass.
- **Slow load:** report the `load` event time and the number of requests (`page.on('requestfinished')` count) rather than a feeling.

## Limits

The sweep reads one page. It does not log in, follow multi-step flows or judge visual quality. Use `flows-and-consistency.md` for flows and `design-audit-recipes.md` for the visual pass. Never point it at a production site you do not own.
