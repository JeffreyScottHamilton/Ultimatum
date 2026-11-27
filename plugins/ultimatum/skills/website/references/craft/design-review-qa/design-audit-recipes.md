# Design audit recipes: extracting the rendered design with Playwright

Read when an audit needs facts, not impressions: fonts in use, colour count, heading scale, spacing values, tap-target sizes, sideways overflow, console errors, reduced-motion behaviour. One script reads a local page at three widths and writes screenshots plus a JSON file. It changes nothing on the page.

## What it measures

| Output | Meaning | Flag when |
|---|---|---|
| `families` | first font family of each of the first 800 elements, with counts | more than 3 |
| `colourCount`, `topColours` | distinct text and background colours | more than about 12 non-grey |
| `spacing` | most common padding and margin values | values off a 4 or 8 px scale |
| `headings`, `skippedLevel`, `h1Count` | heading sizes, order, count of `h1` | a skipped level, not exactly one `h1` |
| `smallTargets` | controls under 44 px on the short side (links inside running text are exempt) | any, at 375 wide |
| `overflowing`, `scrollsSideways` | elements past the viewport edge | any, at any width |
| `zoomLocked` | viewport meta blocks zoom | true |
| `consoleErrors` | `console.error` and uncaught exceptions during load | any new one |
| `reducedMotion` | the query matches when emulated, and `.fade` has no transition | transition still runs |

## The script

Needs Playwright with Chromium (`../../../../work/references/browser-verification.md` says what to do when it is missing: report browser checks as not run). Serve the page on `127.0.0.1` first. The script refuses other hosts.

```js
// design-audit.mjs <url> <outDir>: read-only design facts at three widths.
import { chromium } from 'playwright';
import fs from 'node:fs';

const [url, out = '.ultimatum/design-audit'] = process.argv.slice(2);
if (!url || !/^https?:\/\/(127\.0\.0\.1|localhost)[:/]/.test(url)) {
  console.error('usage: node design-audit.mjs http://127.0.0.1:PORT/ [outDir]  (local pages only)');
  process.exit(2);
}
fs.mkdirSync(out, { recursive: true });

// Runs inside the page. Returns plain JSON.
const facts = () => {
  const els = [...document.querySelectorAll('body *')].slice(0, 800);
  const cs = (e) => getComputedStyle(e);
  const count = (list) => Object.entries(list.reduce((m, k) => ((m[k] = (m[k] || 0) + 1), m), {}))
    .sort(([, x], [, y]) => y - x);
  const families = count(els.map((e) => cs(e).fontFamily.split(',')[0].trim().replace(/["']/g, '')));
  const colours = count(els.flatMap((e) => [cs(e).color, cs(e).backgroundColor])
    .filter((c) => !c.endsWith(', 0)')));
  const spacing = count(els.flatMap((e) => ['paddingTop', 'paddingLeft', 'marginTop', 'marginBottom']
    .map((p) => cs(e)[p])).filter((v) => v !== '0px'));
  const headings = Array.from(document.querySelectorAll(':is(h1, h2, h3, h4, h5, h6)'), (h) => ({
    level: Number(h.localName.slice(1)), text: h.innerText.trim().slice(0, 40), size: cs(h).fontSize, wrap: cs(h).textWrap }));
  const levels = headings.map((h) => h.level);
  const skipped = levels.some((l, i) => i > 0 && l - levels[i - 1] > 1);
  const small = [...document.querySelectorAll('button, a[href], input, select, textarea, [role=button]')]
    .map((e) => ({ e, r: e.getBoundingClientRect() }))
    .filter(({ e, r }) => r.width > 0 && !e.closest('p,li') && Math.min(r.width, r.height) < 44)
    .map(({ e, r }) => `${e.tagName.toLowerCase()} "${(e.textContent || e.name || '').trim().slice(0, 20)}" ${r.width.toFixed(0)}x${r.height.toFixed(0)}`);
  const wide = els.filter((e) => { const { width, right } = e.getBoundingClientRect(); return width > 0 && right > innerWidth + 1; })
    .map((e) => e.tagName.toLowerCase() + (e.className ? '.' + e.className : '')).slice(0, 5);
  const vp = document.querySelector('meta[name=viewport]')?.content || '';
  return {
    families, colourCount: colours.length, topColours: colours.slice(0, 5), spacing: spacing.slice(0, 8),
    headings, skippedLevel: skipped, h1Count: levels.filter((l) => l === 1).length,
    smallTargets: small, overflowing: wide, scrollsSideways: document.documentElement.scrollWidth > innerWidth,
    zoomLocked: /user-scalable\s*=\s*no|maximum-scale\s*=\s*1(\.0)?\b/.test(vp),
    lang: document.documentElement.lang || null, title: document.title,
    reducedMotionMatches: matchMedia('(prefers-reduced-motion: reduce)').matches,
  };
};

const browser = await chromium.launch();
const report = {};
try {
  const sizes = { desktop: [1440, 900], tablet: [768, 1024], mobile: [375, 812] };
  for (const [name, [width, height]] of Object.entries(sizes)) {
    const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
    page.on('pageerror', (e) => errors.push('uncaught: ' + e.message));
    await page.goto(url, { waitUntil: 'load' });
    report[name] = { ...(await page.evaluate(facts)), consoleErrors: errors };
    await page.screenshot({ path: `${out}/${name}.png`, fullPage: true });
    await ctx.close();
  }
  // Same page with reduced motion emulated, to confirm the query is honoured.
  const rm = await browser.newContext({ reducedMotion: 'reduce' });
  const p2 = await rm.newPage();
  await p2.goto(url);
  report.reducedMotion = await p2.evaluate(() => ({
    matches: matchMedia('(prefers-reduced-motion: reduce)').matches,
    fadeTransition: getComputedStyle(document.querySelector('.fade') || document.body).transitionDuration }));
  await rm.close();
} finally { await browser.close(); }

fs.writeFileSync(`${out}/facts.json`, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report.mobile).slice(0, 1200));
console.log('reducedMotion', JSON.stringify(report.reducedMotion));
console.log('desktop overflow:', report.desktop.scrollsSideways, '| mobile overflow:', report.mobile.scrollsSideways);
```

Run it with `node design-audit.mjs http://127.0.0.1:PORT/ .ultimatum/design-audit`. Change the `.fade` selector to a real animated element of the page you audit.

**Ran:** against a one-page scratch site with planted flaws (three font families, a 600 px block on a phone, 20 px links, a skipped heading level, a console error, a `.fade` class with `transition: all`). It reported the three families, the overflow on the mobile run only, seven small targets, the skipped level, the console error, and a `0s` transition under emulated reduced motion. Desktop showed no sideways scroll.

## Notes

- Computed styles, not source, so the result is what a visitor gets. Shadow DOM and styles injected later may be missed; say so in the report.
- Capped at 800 elements to stay quick on large pages; raise the cap for a Deep audit.
- Checks it does not do: contrast (use `ult-browser.mjs` and axe, see `../../../../work/references/browser-verification.md`), focus order, and screenshots read back with your own eyes. Read each saved screenshot and cite it in the finding.
- Saving the rendered HTML for a rule-by-rule scan is optional; never keep a saved page that carries session data.
