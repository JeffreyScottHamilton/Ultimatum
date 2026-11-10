#!/usr/bin/env node
// ult-browser: deterministic browser checks on the Playwright library.
// Usage: node ult-browser.mjs <url> [--viewports 375x812,1280x800] [--steps steps.json]
//        [--out dir] [--axe path|auto|off] [--reduced-motion] [--stress] [--allow-external]
// Final line: ULT-BROWSER: PASS|WARN|FAIL (<counts>). Exit 0 / 0 / 1; 3 = Playwright missing.
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';

const require = createRequire(import.meta.url);

function parseArgs(argv) {
  const o = { url: null, viewports: '375x812,1280x800', steps: null, out: null, axe: 'auto',
    reducedMotion: false, stress: false, allowExternal: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const val = () => argv[++i];
    if (a === '--viewports') o.viewports = val();
    else if (a === '--steps') o.steps = val();
    else if (a === '--out') o.out = val();
    else if (a === '--axe') o.axe = val();
    else if (a === '--reduced-motion') o.reducedMotion = true;
    else if (a === '--stress') o.stress = true;
    else if (a === '--allow-external') o.allowExternal = true;
    else if (!a.startsWith('--') && !o.url) o.url = a;
    else { console.error(`ULT-BROWSER: unknown argument ${a}`); process.exit(2); }
  }
  return o;
}

function loadPlaywright() {
  const tries = [() => require('playwright')];
  tries.push(() => {
    const root = execFileSync('npm', ['root', '-g'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
    return createRequire(path.join(root, 'noop.js'))('playwright');
  });
  for (const t of tries) { try { return t(); } catch { /* next */ } }
  return null;
}

function resolveAxe(opt) {
  if (opt === 'off') return null;
  const cands = [];
  if (opt && opt !== 'auto') cands.push(opt);
  if (process.env.ULT_AXE_PATH) cands.push(process.env.ULT_AXE_PATH);
  const bases = [import.meta.url, path.join(process.cwd(), 'noop.js')];
  try {
    const root = execFileSync('npm', ['root', '-g'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
    bases.push(path.join(root, 'noop.js'));
  } catch { /* no npm */ }
  for (const b of bases) {
    try { cands.push(createRequire(b).resolve('axe-core/axe.min.js')); } catch { /* next */ }
  }
  for (const c of cands) {
    try { if (fs.statSync(c).isFile()) return c; } catch { /* next */ }
  }
  return null;
}

// ---- in-page audit (runs inside the browser; must be self-contained) ----
const AUDIT = () => {
  const out = [];
  const add = (id, severity, message, items) => out.push({ id, severity, message, count: items ? items.length : 1, examples: (items || []).slice(0, 8) });
  const desc = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    else if (el.classList && el.classList.length) s += '.' + [...el.classList].slice(0, 2).join('.');
    const t = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 30);
    return t ? `${s} "${t}"` : s;
  };
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && parseFloat(cs.opacity) > 0;
  };
  const all = [...document.body.querySelectorAll('*')].filter((e) => !['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE'].includes(e.tagName));

  // overflow
  const iw = window.innerWidth;
  if (document.documentElement.scrollWidth > iw + 1)
    add('h-overflow', 'fail', `page scrolls horizontally: scrollWidth ${document.documentElement.scrollWidth} > innerWidth ${iw}`);
  const clipped = (el) => {
    for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
      const ox = getComputedStyle(p).overflowX;
      if (ox === 'auto' || ox === 'scroll' || ox === 'hidden' || ox === 'clip') return true;
    }
    return false;
  };
  const over = all.filter((e) => { if (!visible(e)) return false; const r = e.getBoundingClientRect(); return (r.right > iw + 1 || r.left < -1) && !clipped(e); });
  const overTop = over.filter((e) => !over.includes(e.parentElement));
  if (overTop.length) add('element-overflow', 'warn', 'elements extend past the viewport edge', overTop.map(desc));

  // document basics
  if (!document.documentElement.getAttribute('lang')) add('lang', 'fail', '<html> has no lang attribute');
  if (!document.title.trim()) add('title', 'fail', 'document has no <title>');
  const ids = {};
  document.querySelectorAll('[id]').forEach((e) => { ids[e.id] = (ids[e.id] || 0) + 1; });
  const dups = Object.keys(ids).filter((k) => ids[k] > 1);
  if (dups.length) add('duplicate-id', 'fail', 'duplicate id values', dups);

  // headings
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(visible);
  const skips = []; let prev = 0;
  hs.forEach((h) => { const l = +h.tagName[1]; if (prev && l > prev + 1) skips.push(`${h.tagName.toLowerCase()} after h${prev}: ${desc(h)}`); prev = l; });
  if (skips.length) add('heading-order', 'warn', 'heading levels skipped', skips);
  const h1 = hs.filter((h) => h.tagName === 'H1').length;
  if (h1 === 0) add('h1-missing', 'warn', 'no visible h1');
  if (h1 > 1) add('h1-multiple', 'warn', `${h1} visible h1 elements`);

  // images
  const noAlt = [...document.images].filter((i) => !i.hasAttribute('alt') && i.getAttribute('role') !== 'presentation' && i.getAttribute('aria-hidden') !== 'true');
  if (noAlt.length) add('img-alt', 'fail', 'images without an alt attribute', noAlt.map((i) => desc(i) + ' ' + (i.getAttribute('src') || '').slice(0, 40)));
  const broken = [...document.images].filter((i) => i.complete && i.naturalWidth === 0 && i.getAttribute('src'));
  if (broken.length) add('img-broken', 'warn', 'images that failed to render', broken.map((i) => i.getAttribute('src').slice(0, 60)));

  // accessible names
  const textOf = (el) => (el.textContent || '').trim();
  const nameOf = (el) => {
    const al = el.getAttribute('aria-label'); if (al && al.trim()) return al.trim();
    const lb = el.getAttribute('aria-labelledby');
    if (lb) { const t = lb.split(/\s+/).map((id) => { const n = document.getElementById(id); return n ? textOf(n) : ''; }).join(' ').trim(); if (t) return t; }
    if (el.labels && el.labels.length) { const t = [...el.labels].map(textOf).join(' ').trim(); if (t) return t; }
    const tag = el.tagName;
    if (tag === 'INPUT' && ['submit', 'button', 'reset'].includes(el.type) && (el.value || '').trim()) return el.value;
    if (tag === 'INPUT' && el.type === 'image' && (el.alt || '').trim()) return el.alt;
    if (textOf(el)) return textOf(el);
    const img = el.querySelector('img[alt]:not([alt=""]), svg title, [role=img][aria-label]');
    if (img) return 'img';
    if ((el.getAttribute('title') || '').trim()) return el.getAttribute('title');
    return '';
  };
  const named = [...document.querySelectorAll('button, a[href], input:not([type=hidden]), select, textarea, [role=button], [role=link], [role=checkbox], [role=switch], [role=tab], [role=menuitem]')]
    .filter((e) => visible(e) && e.getAttribute('aria-hidden') !== 'true');
  const unnamed = named.filter((e) => !nameOf(e));
  if (unnamed.length) add('accessible-name', 'fail', 'controls without an accessible name', unnamed.map(desc));

  // tap targets
  const small = [], medium = [];
  named.forEach((e) => {
    if (e.tagName === 'INPUT' && ['checkbox', 'radio'].includes(e.type) && e.labels && e.labels.length) return;
    if (e.tagName === 'A' && getComputedStyle(e).display === 'inline' && e.parentElement && textOf(e.parentElement).length > textOf(e).length + 10) return;
    const r = e.getBoundingClientRect(); const m = Math.min(r.width, r.height);
    if (m < 24) small.push(`${desc(e)} ${Math.round(r.width)}x${Math.round(r.height)}`);
    else if (m < 44) medium.push(`${desc(e)} ${Math.round(r.width)}x${Math.round(r.height)}`);
  });
  if (small.length) add('tap-target-small', 'fail', 'interactive targets under 24x24 CSS px', small);
  if (medium.length) add('tap-target-medium', 'warn', 'interactive targets under 44 px (aim for 44)', medium);

  // contrast on solid backgrounds
  const parse = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const blend = (fg, bg) => ({ r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1 });
  const bgOf = (el) => {
    const layers = [];
    for (let p = el; p; p = p.parentElement) {
      const cs = getComputedStyle(p);
      if (cs.backgroundImage !== 'none') return null; // not solid
      const c = parse(cs.backgroundColor);
      if (c && c.a > 0) { layers.push(c); if (c.a >= 1) break; }
    }
    let base = { r: 255, g: 255, b: 255, a: 1 };
    for (let i = layers.length - 1; i >= 0; i--) base = blend(layers[i], base);
    return base;
  };
  const low = [];
  all.forEach((e) => {
    if (!visible(e)) return;
    const own = [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
    if (!own) return;
    const cs = getComputedStyle(e);
    const bg = bgOf(e); if (!bg) return;
    let fg = parse(cs.color); if (!fg) return;
    fg = blend(fg, bg);
    const l1 = lum(fg), l2 = lum(bg);
    const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    const px = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight, 10) >= 700;
    const need = (px >= 24 || (px >= 18.66 && bold)) ? 3 : 4.5;
    if (ratio < need) low.push(`${desc(e)} ${ratio.toFixed(2)}:1 (need ${need})`);
  });
  if (low.length) add('contrast', 'fail', 'text contrast below WCAG AA on solid backgrounds', low);
  const tiny = all.filter((e) => visible(e) && [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()) && parseFloat(getComputedStyle(e).fontSize) < 12);
  if (tiny.length) add('tiny-text', 'warn', 'text smaller than 12px', tiny.map(desc));
  return out;
};

const OVERFLOW_ONLY = () => {
  const iw = window.innerWidth;
  return { scrollWidth: document.documentElement.scrollWidth, innerWidth: iw };
};

// Records pre-focus style for focusables so the Tab walk can tell if focus changed anything.
const SNAPSHOT = () => {
  const key = (el) => { const cs = getComputedStyle(el); return [cs.outlineStyle, cs.outlineWidth, cs.outlineColor, cs.boxShadow, cs.borderTopColor, cs.backgroundColor, cs.textDecorationLine, cs.color].join('|'); };
  window.__ultBase = new Map();
  document.querySelectorAll('a[href],button,input,select,textarea,[tabindex],summary,[contenteditable=true]').forEach((e) => window.__ultBase.set(e, key(e)));
  window.__ultKey = key;
};
const ACTIVE = () => {
  const el = document.activeElement;
  if (!el || el === document.body || el === document.documentElement) return null;
  const cs = getComputedStyle(el);
  const base = window.__ultBase && window.__ultBase.get(el);
  const now = window.__ultKey(el);
  const outline = cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0;
  let d = el.tagName.toLowerCase();
  if (el.id) d += '#' + el.id; else if (el.classList.length) d += '.' + [...el.classList].slice(0, 2).join('.');
  const t = (el.getAttribute('aria-label') || el.textContent || el.value || '').trim().replace(/\s+/g, ' ').slice(0, 30);
  const r = el.getBoundingClientRect();
  return { el: t ? `${d} "${t}"` : d, indicator: outline || (base !== undefined && base !== now), outline, inView: r.bottom > 0 && r.top < innerHeight };
};

const STRESS = () => {
  const long = ' Supercalifragilisticexpialidocious_' + 'W'.repeat(70);
  [...document.body.querySelectorAll('*')].forEach((e) => {
    if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'SVG', 'OPTION'].includes(e.tagName.toUpperCase())) return;
    if (e.children.length === 0 && (e.textContent || '').trim() && e.tagName !== 'INPUT') e.textContent = e.textContent + long;
  });
};

async function runStep(page, step, vp, out, tag) {
  if (step.click !== undefined) { await page.click(step.click, { timeout: 4000 }); return 'click ' + step.click; }
  if (step.press !== undefined) { await page.keyboard.press(step.press); return 'press ' + step.press; }
  if (step.fill !== undefined) { await page.fill(step.fill[0], step.fill[1], { timeout: 4000 }); return `fill ${step.fill[0]}`; }
  if (step.wait !== undefined) { await page.waitForTimeout(Number(step.wait)); return 'wait ' + step.wait; }
  if (step.screenshot !== undefined) {
    const f = `${tag}-${String(step.screenshot).replace(/[^\w.-]+/g, '_')}.png`;
    await page.screenshot({ path: path.join(out, f), fullPage: true });
    return 'screenshot ' + f;
  }
  if (step.expect !== undefined) {
    const e = step.expect; const loc = page.locator(e.selector);
    const fails = [];
    if (e.count !== undefined) { const n = await loc.count(); if (n !== e.count) fails.push(`count expected ${e.count} got ${n}`); }
    if (e.visible !== undefined) { const v = (await loc.count()) ? await loc.first().isVisible() : false; if (v !== e.visible) fails.push(`visible expected ${e.visible} got ${v}`); }
    if (e.text !== undefined) { const t = (await loc.count()) ? (await loc.first().textContent()) || '' : ''; if (!t.includes(e.text)) fails.push(`text expected to contain ${JSON.stringify(e.text)} got ${JSON.stringify(t.trim().slice(0, 80))}`); }
    if (e.focused !== undefined) { const f = (await loc.count()) ? await loc.first().evaluate((el) => el === document.activeElement) : false; if (f !== e.focused) fails.push(`focused expected ${e.focused} got ${f}`); }
    if (fails.length) throw new Error(`expect ${e.selector}: ${fails.join('; ')}`);
    return 'expect ' + e.selector;
  }
  throw new Error('unknown step ' + JSON.stringify(step));
}

async function main() {
  const o = parseArgs(process.argv.slice(2));
  if (!o.url) { console.error('usage: ult-browser.mjs <url> [--viewports WxH,..] [--steps f.json] [--out dir] [--axe path|auto|off] [--reduced-motion] [--stress] [--allow-external]'); process.exit(2); }
  const pw = loadPlaywright();
  if (!pw) { console.log('ULT-BROWSER: SKIP playwright not installed'); process.exit(3); }
  let steps = [];
  if (o.steps) { const j = JSON.parse(fs.readFileSync(o.steps, 'utf8')); steps = Array.isArray(j) ? j : j.steps || []; }
  const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\..*/, '').replace('T', '-');
  const out = path.resolve(o.out || path.join('.ultimatum', 'browser', stamp));
  fs.mkdirSync(out, { recursive: true });
  const target = new URL(o.url);
  const axePath = resolveAxe(o.axe);
  const axeSrc = axePath ? fs.readFileSync(axePath, 'utf8') : null;

  let browser;
  try { browser = await pw.chromium.launch(); }
  catch (e) { console.log(`ULT-BROWSER: SKIP chromium not launchable (${String(e.message).split('\n')[0]})`); process.exit(3); }

  const report = { url: o.url, out, engine: { browser: 'chromium ' + browser.version(), axe: axePath ? { used: 'axe-core', path: axePath } : { used: 'fallback', note: 'axe not available; fallback coverage only' } },
    options: { reducedMotion: o.reducedMotion, stress: o.stress, allowExternal: o.allowExternal }, viewports: [], summary: {} };
  let fails = 0, warns = 0;

  for (const spec of o.viewports.split(',')) {
    const [w, h] = spec.split('x').map(Number);
    const tag = `${w}x${h}`;
    const vr = { viewport: tag, findings: [], console: [], blocked: [], focusWalk: [], steps: [], screenshots: [] };
    const addF = (id, severity, message, examples) => vr.findings.push({ id, severity, message, count: examples ? examples.length : 1, examples: (examples || []).slice(0, 8) });
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: o.reducedMotion ? 'reduce' : 'no-preference', acceptDownloads: false });
    if (!o.allowExternal) {
      await ctx.route('**/*', (route) => {
        const u = new URL(route.request().url());
        if (['data:', 'blob:', 'about:'].includes(u.protocol) || u.origin === target.origin || (u.protocol === 'file:' && target.protocol === 'file:')) return route.continue();
        vr.blocked.push(u.href.slice(0, 120));
        return route.abort('blockedbyclient');
      });
    }
    const page = await ctx.newPage();
    const cerr = [], perr = [], reqf = [], http = [];
    page.on('console', (m) => { if (m.type() === 'error') cerr.push(m.text().slice(0, 200)); });
    page.on('pageerror', (e) => perr.push(String(e.message || e).slice(0, 200)));
    page.on('requestfailed', (r) => { const f = r.failure(); if (f && /blockedbyclient/i.test(f.errorText)) return; if (/favicon\.ico$/.test(r.url())) return; reqf.push(`${r.url().slice(0, 100)} ${f ? f.errorText : ''}`); });
    page.on('response', (r) => { if (r.status() >= 400 && !/favicon\.ico$/.test(r.url())) http.push(`${r.status()} ${r.url().slice(0, 100)}`); });

    try {
      await page.goto(o.url, { waitUntil: 'load', timeout: 20000 });
      await page.waitForTimeout(250);
    } catch (e) {
      addF('load', 'fail', 'page failed to load: ' + String(e.message).split('\n')[0]);
    }

    if (!vr.findings.some((f) => f.id === 'load')) {
      for (const f of await page.evaluate(AUDIT)) vr.findings.push(f);

      if (axeSrc) {
        try {
          await page.addScriptTag({ content: axeSrc });
          const res = await page.evaluate(async () => { const r = await window.axe.run(document); return { v: r.violations.map((x) => ({ id: x.id, impact: x.impact, help: x.help, nodes: x.nodes.slice(0, 5).map((n) => n.target.join(' ')) })) }; });
          for (const v of res.v) addF('axe:' + v.id, ['critical', 'serious'].includes(v.impact) ? 'fail' : 'warn', `${v.impact}: ${v.help}`, v.nodes);
        } catch (e) { addF('axe-error', 'warn', 'axe failed to run: ' + String(e.message).split('\n')[0]); }
      }

      // Tab walk
      await page.evaluate(SNAPSHOT);
      const seen = new Set(); const noInd = [];
      for (let i = 0; i < 40; i++) {
        await page.keyboard.press('Tab');
        const a = await page.evaluate(ACTIVE);
        if (!a) break;
        if (seen.has(a.el)) break;
        seen.add(a.el);
        vr.focusWalk.push({ n: i + 1, el: a.el, indicator: a.indicator });
        if (!a.indicator) noInd.push(a.el);
      }
      if (noInd.length) addF('focus-invisible', 'warn', 'no outline/box-shadow/color change detected on focus', noInd);
      await page.evaluate(() => { if (document.activeElement) document.activeElement.blur(); window.scrollTo(0, 0); });

      const shot = `${tag}-load.png`;
      await page.screenshot({ path: path.join(out, shot), fullPage: true });
      vr.screenshots.push(shot);

      // steps
      for (let i = 0; i < steps.length; i++) {
        try {
          const label = await runStep(page, steps[i], tag, out, tag);
          vr.steps.push({ i, ok: true, action: label });
          if (steps[i].screenshot !== undefined) vr.screenshots.push(label.replace('screenshot ', ''));
        } catch (e) {
          const msg = `step ${i} ${JSON.stringify(steps[i])}: ${String(e.message).split('\n')[0]}`;
          vr.steps.push({ i, ok: false, action: JSON.stringify(steps[i]), message: msg });
          addF('step-failed', 'fail', msg);
          const f = `${tag}-step${i}-failed.png`;
          try { await page.screenshot({ path: path.join(out, f), fullPage: true }); vr.screenshots.push(f); } catch { /* ignore */ }
          break;
        }
      }

      if (o.stress) {
        await page.evaluate(STRESS);
        const m = await page.evaluate(OVERFLOW_ONLY);
        if (m.scrollWidth > m.innerWidth + 1) addF('stress-overflow', 'warn', `long unbroken strings cause horizontal overflow (scrollWidth ${m.scrollWidth} > ${m.innerWidth})`);
        const f = `${tag}-stress.png`;
        await page.screenshot({ path: path.join(out, f), fullPage: true });
        vr.screenshots.push(f);
      }
    }

    if (cerr.length) addF('console-error', 'fail', 'console errors', cerr);
    if (perr.length) addF('page-error', 'fail', 'uncaught page errors', perr);
    if (reqf.length) addF('request-failed', 'fail', 'failed requests', reqf);
    if (http.length) addF('http-error', 'fail', 'HTTP 4xx/5xx responses', http);
    vr.console = cerr;
    if (vr.blocked.length) vr.blocked = [...new Set(vr.blocked)];
    fails += vr.findings.filter((f) => f.severity === 'fail').length;
    warns += vr.findings.filter((f) => f.severity === 'warn').length;
    report.viewports.push(vr);
    await ctx.close();
  }
  await browser.close();

  const verdict = fails ? 'FAIL' : warns ? 'WARN' : 'PASS';
  report.summary = { fail: fails, warn: warns, verdict };
  const rp = path.join(out, 'report.json');
  fs.writeFileSync(rp, JSON.stringify(report, null, 2));

  console.log(`ult-browser ${o.url}  engine: ${report.engine.browser}; a11y: ${report.engine.axe.used}${axePath ? '' : ' (axe not available; fallback coverage only)'}`);
  for (const vr of report.viewports) {
    console.log(`\n[${vr.viewport}] focus order: ${vr.focusWalk.map((f) => f.el + (f.indicator ? '' : ' (no indicator)')).join(' > ') || '(none focusable)'}`);
    for (const f of vr.findings) {
      console.log(`  ${f.severity.toUpperCase()} ${f.id}: ${f.message}${f.count > 1 || f.examples.length ? ` [${f.count}]` : ''}`);
      f.examples.slice(0, 3).forEach((x) => console.log(`      - ${x}`));
    }
    if (!vr.findings.length) console.log('  no findings');
    if (vr.blocked.length) console.log(`  info: blocked ${vr.blocked.length} external request(s); use --allow-external to permit`);
    console.log(`  steps: ${vr.steps.filter((s) => s.ok).length}/${steps.length} ok; screenshots: ${vr.screenshots.join(', ')}`);
  }
  console.log(`\nreport: ${rp}`);
  console.log(`ULT-BROWSER: ${verdict} (fail=${fails} warn=${warns} viewports=${report.viewports.length})`);
  process.exit(fails ? 1 : 0);
}

main().catch((e) => { console.error('ULT-BROWSER: ERROR ' + (e && e.stack || e)); process.exit(2); });
