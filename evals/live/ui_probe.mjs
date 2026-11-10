// Independent UI grader for the ui-app fixture (does not use ult-browser).
// usage: node ui_probe.mjs <url>   -> prints JSON {checks:{...}} ; exit 0 always
import { createRequire } from 'module';
import { execSync } from 'child_process';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch {
  const root = execSync('npm root -g').toString().trim();
  pw = require(`${root}/playwright`);
}
const url = process.argv[2];
const out = { checks: {}, notes: [] };
const browser = await pw.chromium.launch();
for (const [w, h] of [[375, 812], [1280, 800]]) {
  const tag = `${w}`;
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(url);
  await page.waitForTimeout(300);
  const rows = page.locator('.project-row');
  const before = await rows.count();
  out.checks[`${tag}_rows_present`] = before > 0;
  out.checks[`${tag}_no_h_overflow`] = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
  const del = page.getByRole('button', { name: /delete/i }).first();
  out.checks[`${tag}_delete_button`] = (await del.count()) > 0;
  if (!out.checks[`${tag}_delete_button`]) { await page.close(); continue; }
  const box = await del.boundingBox();
  out.checks[`${tag}_delete_in_viewport`] = !!box && box.x >= 0 && box.x + box.width <= w + 1;
  // keyboard: focus the delete button, Enter opens dialog
  await del.focus();
  await page.keyboard.press('Enter');
  await page.waitForTimeout(250);
  const dialog = page.locator('[role="dialog"], [role="alertdialog"]').first();
  out.checks[`${tag}_dialog_opens_on_enter`] = await dialog.isVisible().catch(() => false);
  out.checks[`${tag}_focus_in_dialog`] = await page.evaluate(() => !!document.activeElement?.closest('[role="dialog"],[role="alertdialog"]'));
  await page.keyboard.press('Escape');
  await page.waitForTimeout(250);
  out.checks[`${tag}_escape_closes`] = !(await dialog.isVisible().catch(() => false));
  out.checks[`${tag}_escape_keeps_row`] = (await rows.count()) === before;
  // confirm path (mouse is fine here)
  await del.click();
  await page.waitForTimeout(250);
  const confirm = page.locator('[role="dialog"] button, [role="alertdialog"] button').filter({ hasText: /delete|confirm|yes|remove/i }).first();
  if (await confirm.count()) {
    await confirm.click();
    await page.waitForTimeout(400);
    out.checks[`${tag}_confirm_removes_row`] = (await rows.count()) === before - 1;
    out.checks[`${tag}_toast_shown`] = await page.locator('[role="status"], [role="alert"], .toast').first().isVisible().catch(() => false);
  } else {
    out.checks[`${tag}_confirm_removes_row`] = false;
    out.notes.push(`${tag}: no confirm button found in dialog`);
  }
  out.checks[`${tag}_no_page_errors`] = errors.length === 0;
  if (errors.length) out.notes.push(...errors.slice(0, 3));
  await page.close();
}
await browser.close();
console.log(JSON.stringify(out));
