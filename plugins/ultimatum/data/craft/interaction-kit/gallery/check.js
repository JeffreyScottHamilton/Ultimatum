const { chromium } = require('playwright');
const fs = require('fs');
// Serve this folder over http first (axe needs it): python3 -m http.server 8765
const path = require('path');
const axe = fs.readFileSync(path.join(__dirname, 'node_modules/axe-core/axe.min.js'), 'utf8');
const url = process.env.KIT_URL || 'http://127.0.0.1:8765/index.html';
const shots = path.join(__dirname, 'shots');
fs.mkdirSync(shots, { recursive: true });
let failed = false;
(async () => {
  const b = await chromium.launch();
  for (const [name, vp, reduced, dark] of [['phone', { width: 390, height: 844 }, 'no-preference', false], ['desktop', { width: 1280, height: 900 }, 'no-preference', false], ['desktop-reduced', { width: 1280, height: 900 }, 'reduce', false], ['phone-dark', { width: 390, height: 844 }, 'no-preference', true]]) {
    const p = await b.newPage({ viewport: vp, reducedMotion: reduced });
    const errs = [];
    p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text()); });
    p.on('pageerror', e => errs.push('pageerror: ' + e.message));
    await p.goto(url); await p.waitForTimeout(800);
    if (dark) { await p.click('button[role=switch]'); await p.waitForTimeout(500); }
    const overflow = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    // interactions
    await p.click('button[role=tab]:nth-child(2)'); await p.keyboard.press('ArrowLeft');
    const tabSel = await p.evaluate(() => document.activeElement?.getAttribute('aria-selected'));
    await p.click('text=Show toast'); await p.waitForTimeout(400);
    const toast = await p.locator('section[aria-label=Notifications] li').count();
    await p.click('text=Open drawer'); await p.waitForTimeout(500);
    const dlg = await p.evaluate(() => !!document.activeElement?.closest('[role=dialog]'));
    await p.keyboard.press('Escape'); await p.waitForTimeout(500);
    const back = await p.evaluate(() => document.activeElement?.textContent);
    await p.keyboard.press('Control+k'); await p.waitForTimeout(300);
    await p.keyboard.type('tog'); await p.keyboard.press('Enter'); await p.waitForTimeout(300);
    const darkNow = await p.evaluate(() => document.documentElement.classList.contains('dark'));
    if (darkNow !== !dark) errs.push('cmd palette did not toggle theme');
    if (darkNow !== dark) { await p.click('button[role=switch]'); await p.waitForTimeout(400); }
    await p.click('text=Hold to delete', { delay: 50 }).catch(()=>{});
    await p.addScriptTag({ content: axe });
    const r = await p.evaluate(async () => (await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice'] })).violations.map(v => v.id + ' x' + v.nodes.length + ' ' + v.nodes.slice(0,2).map(n=>n.target.join(' ')).join(' | ')));
    await p.screenshot({ path: path.join(shots, `${name}.png`), fullPage: true });
    if (overflow > 0 || errs.length || r.length || tabSel !== 'true' || toast < 1 || !dlg) failed = true;
    console.log(JSON.stringify({ name, overflow, tabSel, toast, dialogFocus: dlg, focusBack: back, errs, axe: r }));
    await p.close();
  }
  await b.close();
  process.exit(failed ? 1 : 0);
})();
