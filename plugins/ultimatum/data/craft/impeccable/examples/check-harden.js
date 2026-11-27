// Checks harden-demo.html in Chromium. Usage: node check-harden.js [path-to-html]
// Needs the playwright package (NODE_PATH pointing at a global install is fine).
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const file = path.resolve(process.argv[2] || path.join(__dirname, 'harden-demo.html'));
  const browser = await chromium.launch();
  const phone = { width: 390, height: 844 };
  const page = await browser.newPage({ viewport: phone });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto('file://' + file);
  const fails = [];
  let checks = 0;
  const ok = (cond, msg) => { checks++; if (!cond) fails.push(msg); };

  // 1. Long name truncates inside the row instead of pushing the badge out.
  const row = await page.evaluate(() => {
    const r = document.getElementById('row').getBoundingClientRect();
    const b = document.querySelector('#row .badge').getBoundingClientRect();
    const n = document.getElementById('name');
    return { badgeInside: b.right <= r.right + 0.5, truncated: n.scrollWidth > n.clientWidth };
  });
  ok(row.badgeInside, 'badge pushed outside the row');
  ok(row.truncated, 'long name did not truncate');

  // 2. Logical border lands on the reading-start side in both directions.
  const sides = await page.evaluate(() => ['note-ltr', 'note-rtl'].map(id => {
    const s = getComputedStyle(document.getElementById(id));
    return { left: s.borderLeftWidth, right: s.borderRightWidth };
  }));
  ok(sides[0].left === '4px' && sides[0].right === '0px', 'LTR marker not on the left');
  ok(sides[1].right === '4px' && sides[1].left === '0px', 'RTL marker not on the right');
  const flipped = await page.evaluate(() => getComputedStyle(document.getElementById('arrow-rtl')).transform);
  ok(flipped.startsWith('matrix(-1'), 'RTL arrow not mirrored');

  // 3. Locale formatting.
  const fmt = await page.evaluate(() => Object.fromEntries([...document.querySelectorAll('#formats li')].map(li => [li.dataset.k, li.textContent])));
  ok(/[۰-۹]/.test(fmt['fa-IR']), 'fa-IR digits are not Eastern Arabic-Indic');
  ok(fmt['de-DE'].includes('1.234,50'), 'de-DE grouping wrong: ' + fmt['de-DE']);
  ok(fmt['ar-plural'].includes('2=two') && fmt['ar-plural'].includes('5=few') && fmt['ar-plural'].includes('11=many'), 'Arabic plural categories missing');
  ok(fmt['zwnj'].endsWith('kept'), 'ZWNJ lost');

  // 4. Popover escapes the clipped card.
  await page.click('#open-menu');
  const pop = await page.evaluate(() => {
    const m = document.getElementById('menu'), c = document.getElementById('clip').getBoundingClientRect();
    const r = m.getBoundingClientRect();
    const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return { open: m.matches(':popover-open'), onTop: m.contains(top), outside: r.bottom > c.bottom || r.top < c.top || r.left < c.left };
  });
  ok(pop.open && pop.onTop, 'popover not visible on top');
  ok(pop.outside, 'popover stayed inside the clipped card');
  await page.keyboard.press('Escape');

  // 5. Drag ends cleanly on pointercancel, then works again.
  const box = await page.locator('#track').boundingBox();
  const midY = box.y + box.height / 2;
  const mouse = page.mouse;
  await mouse.move(box.x + 10, midY);
  await mouse.down();
  await mouse.move(box.x + 120, midY);
  ok((await page.textContent('#drag-state')) === 'dragging', 'drag did not start');
  await page.evaluate(() => {
    const t = document.getElementById('track');
    t.dispatchEvent(new PointerEvent('pointercancel', { pointerId: 1, bubbles: true }));
  });
  const afterCancel = await page.textContent('#drag-state');
  ok(afterCancel.startsWith('idle'), 'drag did not end on cancel: ' + afterCancel);
  await mouse.up();
  await mouse.move(box.x + 200, midY);
  await mouse.down();
  ok((await page.textContent('#drag-state')) === 'dragging', 'second drag failed after cancel');
  await mouse.up();

  ok(errors.length === 0, 'page errors: ' + errors.join('; '));
  await browser.close();
  if (fails.length) { console.log('FAIL\n- ' + fails.join('\n- ')); process.exit(1); }
  console.log('harden-demo: all ' + checks + ' checks passed');
})();
