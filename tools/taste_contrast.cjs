#!/usr/bin/env node
// Measure text contrast on the real pixels of a page.
//
//   node tools/taste_contrast.cjs PAGE.html [--min 4.5] [--widths 1440,390]
//
// Every element marked [data-check] is measured. Its text is made transparent,
// the boxes its text occupies are screenshotted, and the text colour (with its
// alpha and any ancestor opacity) is scored against every background pixel
// under it with the WCAG 2 contrast formula. The lowest score counts, so grain,
// gradients and photos are measured where they are worst.
//
// Exit codes: 0 all pass, 1 a ratio below --min, 2 bad arguments or no targets.
// A test-time tool: it needs the preinstalled Playwright and Chromium. It is not
// part of the plugin's stdlib toolbelt and makes no network requests of its own.
'use strict';
const path = require('path');
const { chromium } = require('playwright');

function args(argv) {
  const out = { min: 4.5, widths: [1440, 390], file: null };
  const rest = [...argv];
  while (rest.length) {
    const flag = rest.shift();
    if (flag === '--min') out.min = Number(rest.shift());
    else if (flag === '--widths') out.widths = String(rest.shift()).split(',').map(Number);
    else if (out.file === null) out.file = flag;
    else return null;
  }
  if (!out.file || !(out.min > 0) || out.widths.some((w) => !(w > 0))) return null;
  return out;
}

// Runs in the page: find targets, their colours and their text boxes.
function collect() {
  const parse = (c) => {
    const m = c.match(/[\d.]+/g).map(Number);
    return { r: m[0], g: m[1], b: m[2], a: m.length > 3 ? m[3] : 1 };
  };
  return [...document.querySelectorAll('[data-check]')].map((el, i) => {
    let alpha = 1;
    for (let n = el; n; n = n.parentElement) alpha *= Number(getComputedStyle(n).opacity);
    const fg = parse(getComputedStyle(el).color);
    fg.a *= alpha;
    const range = document.createRange();
    range.selectNodeContents(el);
    const boxes = [...range.getClientRects()]
      .flatMap((b) => (b.width > 1 && b.height > 1
        ? [{ x: b.left + scrollX, y: b.top + scrollY, width: b.width, height: b.height }] : []));
    const where = el.closest('[data-ground-name]');
    el.setAttribute('data-check-id', String(i));
    return { id: i, label: (where ? where.dataset.groundName + ': ' : '') + el.tagName.toLowerCase()
      + (el.className ? '.' + el.className : ''), fg, boxes };
  });
}

// Runs in a blank page: lowest contrast of fg over the pixels of a PNG.
async function worst({ b64, fg }) {
  const blob = await (await fetch(`data:image/png;base64,${b64}`)).blob();
  const bmp = await createImageBitmap(blob);
  const canvas = new OffscreenCanvas(bmp.width, bmp.height);
  const ctx = canvas.getContext('2d');
  ctx.drawImage(bmp, 0, 0);
  const data = ctx.getImageData(0, 0, bmp.width, bmp.height).data;
  // WCAG 2 relative luminance of an sRGB triple (0-255 channels).
  const channel = (c) => {
    const s = c / 255;
    return s > 0.04045 ? Math.pow((s + 0.055) / 1.055, 2.4) : s / 12.92;
  };
  const luminance = (rgb) => [0.2126, 0.7152, 0.0722].reduce((sum, k, j) => sum + k * channel(rgb[j]), 0);
  const ink = [fg.r, fg.g, fg.b];
  let low = Infinity;
  for (let p = 0; p + 3 < data.length; p += 4) {
    const under = [data[p], data[p + 1], data[p + 2]];
    const seen = ink.map((c, j) => c * fg.a + under[j] * (1 - fg.a)); // text blended over the pixel
    const [dark, light] = [luminance(seen), luminance(under)].sort((m, n) => m - n);
    low = Math.min(low, (light + 0.05) / (dark + 0.05));
  }
  return low;
}

async function main() {
  const opt = args(process.argv.slice(2));
  if (!opt) {
    console.error('usage: node tools/taste_contrast.cjs PAGE.html [--min 4.5] [--widths 1440,390]');
    return 2;
  }
  const url = 'file://' + path.resolve(opt.file);
  const browser = await chromium.launch();
  const scratch = await browser.newPage();
  let failed = 0, measured = 0;
  try {
    for (const width of opt.widths) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      await page.goto(url);
      await page.waitForTimeout(5000); // let one-shot motion (e.g. the liquid drift) settle
      const targets = await page.evaluate(collect);
      await page.addStyleTag({ content: '[data-check], [data-check] * { color: transparent !important; '
        + 'text-shadow: none !important; -webkit-text-fill-color: transparent !important; caret-color: transparent !important; }' });
      for (const t of targets) {
        let low = Infinity;
        for (const box of t.boxes) {
          const shot = await page.screenshot({ clip: box, fullPage: true });
          low = Math.min(low, await scratch.evaluate(worst, { b64: shot.toString('base64'), fg: t.fg }));
        }
        if (!t.boxes.length) continue;
        measured++;
        const ok = low >= opt.min;
        if (!ok) failed++;
        console.log(`${ok ? 'ok  ' : 'FAIL'} ${String(width).padStart(4)}px ${low.toFixed(2).padStart(6)}:1  ${t.label}`);
      }
      await page.close();
    }
  } finally {
    await browser.close();
  }
  if (!measured) { console.error('no [data-check] text found'); return 2; }
  console.log(`${measured} measured, ${failed} below ${opt.min}:1`);
  return failed ? 1 : 0;
}

main().then((code) => process.exit(code), (err) => { console.error(err); process.exit(2); });
