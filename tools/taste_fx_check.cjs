#!/usr/bin/env node
// Check the Taste kit's WebGL effects in a real browser.
//
//   node tools/taste_fx_check.cjs /abs/path/kit/effects/index.html
//
// Checks that each frame mounts near the screen within the budget (4 contexts,
// 1.5 MP), settles and stops asking for frames, releases its context off
// screen, logs nothing, and keeps its poster under reduced motion, at 390px,
// without WebGL2 and when a shader fails. Set SHOT_DIR to keep screenshots.
// Exit 0 all pass, 1 a check failed, 2 the run broke. A test-time tool: it
// needs the preinstalled Playwright and Chromium and is not part of the toolbelt.
'use strict';
const { chromium } = require('playwright');
const path = require('path');
const url = 'file://' + path.resolve(process.argv[2] || '');
const shots = process.env.SHOT_DIR;
const state = (page) => page.$$eval('.fx', (els) => els.map((e) => ({ fx: e.dataset.fx, state: e.dataset.fxState || '', canvas: !!e.querySelector('canvas'),
  px: e.querySelector('canvas') ? e.querySelector('canvas').width * e.querySelector('canvas').height : 0 })));
let bad = 0;
const check = (ok, msg) => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${msg}`); if (!ok) bad++; };
(async () => {
  const browser = await chromium.launch();
  const open = async (opts, init) => {
    const ctx = await browser.newContext(opts);
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', (m) => { if ((m.type() === 'error' || m.type() === 'warning') && !m.text().includes('GPU stall due to ReadPixels') /* Chromium's note when a screenshot reads a WebGL canvas */) errors.push(m.text()); });
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.addInitScript(() => {
      window.__raf = 0; const raf = window.requestAnimationFrame.bind(window);
      window.requestAnimationFrame = (f) => { window.__raf++; return raf(f); };
    });
    if (init) await page.addInitScript(init);
    await page.goto(url);
    return { page, errors, ctx };
  };
  // 1. desktop: each frame mounts as it nears the screen
  {
    const { page, errors, ctx } = await open({ viewport: { width: 1440, height: 900 } });
    const seen = new Set(); let maxPx = 0, maxLive = 0;
    for (let i = 0; i < 3; i++) {
      await page.locator('.fx').nth(i).scrollIntoViewIfNeeded();
      await page.waitForTimeout(700);
      const s = await state(page);
      s.filter((x) => x.canvas).forEach((x) => seen.add(x.fx));
      maxLive = Math.max(maxLive, s.filter((x) => x.canvas).length);
      maxPx = Math.max(maxPx, s.reduce((a, x) => a + x.px, 0));
    }
    check(seen.size === 3, `1440: all three mounted (${[...seen].join(', ')})`);
    check(maxLive <= 4, `1440: live contexts at most 4 (max ${maxLive})`);
    check(maxPx <= 1.5e6, `1440: canvas pixels within 1.5 MP (max ${maxPx})`);
    if (shots) await page.screenshot({ path: shots + '/fx-1440-running.png' });
    await page.waitForTimeout(8800);
    const s = await state(page);
    const visible = s.filter((x) => x.canvas);
    check(visible.length > 0 && visible.every((x) => x.state === 'settled'), `1440: on-screen effects settled (${visible.map((x) => x.fx + '=' + x.state).join(', ')})`);
    const r0 = await page.evaluate(() => window.__raf); await page.waitForTimeout(1000);
    const r1 = await page.evaluate(() => window.__raf);
    check(r1 === r0, `1440: no frames requested after settling (${r1 - r0})`);
    await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(700);
    const top = await state(page);
    check(!top[2].canvas && top[2].state === 'unmounted', `1440: off-screen frame released (${top[2].state})`);
    if (shots) await page.screenshot({ path: shots + '/fx-1440-top.png' });
    check(errors.length === 0, `1440: no console errors or warnings ${errors.join(' | ')}`);
    await ctx.close();
  }
  // 2-3. reduced motion and phone: posters only
  for (const [label, opts] of [['reduced motion', { viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' }],
                                ['390 phone', { viewport: { width: 390, height: 844 } }]]) {
    const { page, errors, ctx } = await open(opts);
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight / 2)); await page.waitForTimeout(800);
    const s = await state(page);
    check(s.every((x) => !x.canvas && x.state === 'poster: still'), `${label}: posters only (${s.map((x) => x.state).join(', ')})`);
    if (shots && label === '390 phone') await page.screenshot({ path: shots + '/fx-390.png', fullPage: true });
    check(errors.length === 0, `${label}: no console errors ${errors.join(' | ')}`);
    await ctx.close();
  }
  // 4. no WebGL2, 5. shader build fails
  const noGl = () => { const g = HTMLCanvasElement.prototype.getContext; HTMLCanvasElement.prototype.getContext = function (k, o) { return k === 'webgl2' ? null : g.call(this, k, o); }; };
  const badShader = () => { const g = HTMLCanvasElement.prototype.getContext; HTMLCanvasElement.prototype.getContext = function (k, o) {
    const c = g.call(this, k, o); if (k === 'webgl2' && c) { const src = c.shaderSource.bind(c); c.shaderSource = (sh, t) => src(sh, t + '\nnot glsl'); } return c; }; };
  for (const [label, init, want] of [['no webgl2', noGl, 'poster: no webgl2'], ['shader fails', badShader, 'poster: shader failed']]) {
    const { page, errors, ctx } = await open({ viewport: { width: 1440, height: 900 } }, init);
    await page.waitForTimeout(800);
    const s = await state(page);
    check(!s[0].canvas && s[0].state === want, `${label}: first frame keeps its poster (${s[0].state})`);
    check(errors.length === 0, `${label}: no console errors ${errors.join(' | ')}`);
    await ctx.close();
  }
  await browser.close();
  console.log(bad ? `${bad} failed` : 'all passed');
  process.exit(bad ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
