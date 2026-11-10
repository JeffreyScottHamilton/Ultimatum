# Browser verification

"It renders" is not proof. Prove the UI in a real browser: layout at more than one size, real interaction, console clean, keyboard path works, accessibility checked, and the screenshots actually looked at. Name what you did not check.

## 1. ult-browser

```
node "${CLAUDE_PLUGIN_ROOT}/scripts/ult-browser.mjs" <url> \
  [--viewports 375x812,1280x800] [--steps steps.json] [--out dir] \
  [--axe path|auto|off] [--reduced-motion] [--stress] [--allow-external]
```

- Needs the Playwright library with a Chromium browser (global install is fine; the script also looks under `npm root -g`). If missing it prints `ULT-BROWSER: SKIP playwright not installed` and exits 3. Then say browser verification was **not run** and fall back to section 11. Do not install Playwright or browsers unless the user asks.
- Start the app first (dev server in background; use `ult run` for noisy output), then pass its URL. `file:///...html` works for static pages.
- Output: a compact summary, `<out>/report.json`, PNGs, and a last line `ULT-BROWSER: PASS|WARN|FAIL (fail=N warn=M viewports=K)`. Exit 0 for PASS/WARN, 1 for FAIL, 3 for SKIP.
- Default out dir: `.ultimatum/browser/<timestamp>` under the cwd. Network: only the target's origin is allowed; other origins are aborted and listed as `blocked` (use `--allow-external` only when the page truly needs them and the user accepts it).
- Per viewport it checks: console errors, page errors, failed requests, HTTP 4xx/5xx, horizontal overflow (page and elements), images without `alt` or broken, small tap targets (<24 px FAIL, <44 px WARN), controls without accessible names, duplicate ids, `lang`, `<title>`, heading order, contrast on solid backgrounds, a Tab walk (focus order and whether focus visibly changes anything), a load screenshot.
- `--axe auto` looks for axe-core via `ULT_AXE_PATH`, `require.resolve('axe-core')`, the cwd project, then the global npm root. It never downloads. The summary line names the engine; if it says `fallback`, report "axe not available; fallback coverage only". Do not claim an axe pass.
- `--reduced-motion` emulates `prefers-reduced-motion: reduce`. `--stress` appends 100+ unbroken characters to every text leaf and re-checks overflow (a WARN means long content breaks the layout; fix with `min-width: 0`, `overflow-wrap: anywhere`, truncation).

### Steps file

A JSON array run in each viewport, in order; the first failing step stops the run and is a FAIL naming the step index and message.

```json
[
  {"click": "button[aria-haspopup=dialog]"},
  {"expect": {"selector": "dialog[open]", "visible": true}},
  {"press": "Tab"},
  {"press": "Escape"},
  {"expect": {"selector": "dialog[open]", "count": 0}},
  {"expect": {"selector": "button[aria-haspopup=dialog]", "focused": true}},
  {"fill": ["input[name=q]", "a very long search term"]},
  {"screenshot": "after-close"},
  {"wait": 200}
]
```

`expect` keys: `visible` (bool), `count` (n), `text` (substring of the first match), `focused` (bool). Steps are JSON, so write literal strings. Use stable selectors (roles, `data-testid`, ids), not generated class names.

## 2. Viewports

Pick at least two that matter: a phone (375x812) and a desktop (1280x800). Add 768x1024 when the layout has a tablet breakpoint, 320x640 for the narrowest supported width, and 1920x1080 for wide layouts. Say which you ran. Layout that "should" work at an untested width is unverified.

## 3. Real interaction

Click, type and press keys through the steps file or a Playwright snippet; do not call handlers from the console. For every feature, drive the happy path, one error path (invalid input, failed request) and one cancel path (Escape, Cancel). After the action, assert the visible outcome (text, count, state), not just "no exception".

## 4. Keyboard

- Tab order follows reading order; the summary's `focus order` line must match the visual order and contain every control you expect. A control missing from it is not keyboard reachable.
- Each focus stop shows an indicator. `(no indicator)` entries are warnings: fix with `:focus-visible` styles of 3:1 contrast, never `outline: none` alone.
- Enter/Space activate buttons; Enter activates links; Escape closes overlays.
- **Dialogs:** after opening, focus is inside the dialog; Tab cycles within it (trap) or the background is inert; Escape closes; focus returns to the opening control. Assert with `focused: true` expects on the first field before and the trigger after.
- Menus/tabs/listboxes: arrow keys per the ARIA pattern, or use native elements.
- No keyboard trap outside intentional modals.

## 5. Screenshots: read them back

Open each PNG (the Read tool shows images). Look for: clipped or overlapping text, content under fixed headers, empty areas where media failed, unreadable contrast, misaligned edges, a spinner left on screen, a layout that differs between viewports unexpectedly. Quote what you saw in the report ("375px: table scrolls inside its container, header intact"). A screenshot never opened is not evidence.

## 6. Console, page and network errors

Any `console-error`, `page-error`, `request-failed` or `http-error` is a FAIL and must be fixed or explained as environmental (for example a missing API in a static fixture). Do not waive them to get a green line. A blocked external origin is information: decide whether it is a real dependency (fonts, analytics) or an accidental one.

## 7. Accessibility

Automated tools catch roughly a third of issues. With axe present, treat `critical`/`serious` as FAIL and `moderate`/`minor` as WARN. Without axe the fallback covers names, alt, lang, title, ids, heading order, tap size, contrast on solid backgrounds, focus visibility. Always add the manual criteria:

- **Names and roles:** every control announces purpose; icons-only buttons have `aria-label`; landmarks (`header`, `nav`, `main`) exist once.
- **Forms:** each field has a visible label tied by `for`/wrapping; errors are text, tied via `aria-describedby`, announced (`role=alert` or live region); required state not color-only.
- **Contrast** on gradients and images (the fallback skips non-solid backgrounds): sample by eye or measure.
- **Zoom/reflow:** 200% zoom and 320 px width without two-axis scrolling.
- **Motion:** with `--reduced-motion`, nothing essential depends on animation and nothing large moves.
- **Status changes** (toasts, async results) are announced without stealing focus.

## 8. Stress content

Run `--stress`, then try by hand or in steps: empty list, one item, 1000 items, very long names, missing image, slow and failing network (Playwright `route` in a custom snippet), double-click on submit, RTL text. These are where real UIs break; the happy-path screenshot proves little.

## 9. Cookies, storage and auth redirects

For login, session or consent features, inspect rather than assume. Snippet (Playwright library, run with `node`):

```js
const ctx = page.context();
console.log((await ctx.cookies()).map(c => ({name: c.name, httpOnly: c.httpOnly, secure: c.secure, sameSite: c.sameSite, expires: c.expires})));  // never print values
console.log(await page.evaluate(() => Object.keys(localStorage)));
```

- Session cookies should be `HttpOnly`, `Secure` (on HTTPS), with a deliberate `SameSite`. Raw `Set-Cookie` headers: `curl -sI <url>` or response headers via `page.on('response')`.
- Tokens in `localStorage` are readable by any script on the page; flag it.
- Auth redirects: request a protected URL logged out and confirm redirect to login and back (`page.url()` after navigation); confirm logout clears the cookie and that Back does not show cached private data.
- Redact values in the report. The UI is not the boundary: also call the endpoint without the session (see `ui.md` section 8).

## 10. Performance and memory

- **Quick:** in-page `PerformanceObserver` for `largest-contentful-paint` and `layout-shift`. Budget: LCP 2.5 s or better, CLS 0.1 or less, on a throttled profile when comparing; headless CPU timings are only comparable page to page.
- **Chrome DevTools MCP present** (check your tool list for `chrome-devtools`): use `performance_start_trace` / `performance_stop_trace` and `performance_analyze_insight` for LCP breakdown and render-blocking; `take_memory_snapshot` for heap snapshots; `lighthouse_audit` for an overall audit. Name the tool you used.
- **Leaks without DevTools:** repeat the interaction (open/close dialog, navigate away/back) 20-50 times in a Playwright snippet and compare `document.querySelectorAll('*').length` and `performance.memory.usedJSHeapSize` (Chromium; needs `--enable-precise-memory-info`) before and after a forced GC (`--js-flags=--expose-gc`, `gc()`). Steady growth with each cycle means detached nodes or unremoved listeners; look for `addEventListener` without cleanup, timers, subscriptions, and portals.
- **Images/fonts:** serve right-sized images with `width`/`height` (prevents CLS), `loading=lazy` below the fold, `font-display: swap`/`optional`.

## 11. Without a browser

State "not browser-verified". Do the cheap substitutes: run the component/unit tests, lint, type-check, build, and read the CSS for the states in `ui.md` section 4. Describe the exact manual steps for the user (URL, viewport, what to press, expected result). Do not describe visual outcomes as observed.

## 12. Reporting

`ULT-BROWSER: <line>` verbatim; viewports and steps run; engine (axe or fallback); what the screenshots showed; waivers in the `ui.md` format; not verified (perf, memory, real devices, screen reader). Keep `report.json` path so findings can be re-read with `ult`.
