# Local web app test recipes

Read when you need to script a check against a web app on this machine: picking an approach, starting its servers around the test, and writing a script that looks before it acts. What to check once the page is up (viewports, keyboard, console, accessibility) is in `../../browser-verification.md`.

## 1. Pick the approach

| What you have | Do |
|---|---|
| a static HTML file | read the file for selectors, then open it with a `file://` URL; no server needed |
| an app whose server is already running | script against its URL |
| an app that needs one or more servers | start them with `with_ports.py` (§ 2), then script |
| `ult-browser.mjs` covers the check | use it (`../../browser-verification.md` § 1) and skip the custom script |

## 2. Servers around the test

A test that starts a dev server by hand leaves it running when the test fails, and the next run finds the port taken. `with_ports.py` starts each server, waits until its port accepts connections, runs your command, then stops the servers whatever happened:

```
python3 plugins/ultimatum/data/craft/anthropic-method/with_ports.py \
  --server "npm run dev --prefix api" --port 3001 \
  --server "npm run dev --prefix web" --port 5173 \
  --timeout 60 -- node checks/smoke.cjs http://127.0.0.1:5173/
```

- Exit code is the command's own; 3 means a server never opened its port, exited early, or found its port already taken.
- Server commands run without a shell. Wrap in `sh -c '...'` only when you need shell syntax, and never build that string from untrusted text.
- Run `--help` on a helper like this before reading its source. Its interface is what you need; its insides cost tokens.

## 3. Look, then act

On a page that renders with script, the HTML you fetched is not the page. Wait for the element the app draws, list what is there, then act with locators taken from that list. Guessing selectors from the source fails on generated class names and late renders.

```js
const { chromium } = require('playwright');
(async () => {
  const url = process.argv[2];
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(url);
  await page.getByRole('button').first().waitFor();          // look: wait for what the app draws
  console.log('buttons:', JSON.stringify(await page.getByRole('button').allInnerTexts()));
  await page.getByRole('button', { name: 'Add one' }).click(); // act: use a name seen above
  await page.getByRole('button', { name: 'Add one' }).click();
  const n = await page.locator('#n').innerText();
  console.log('count after two clicks:', n, 'console errors:', errors.length);
  await browser.close();
  process.exit(n === '2' && errors.length === 0 ? 0 : 1);
})();
```

Run under `with_ports.py` against a scratch page whose button appears 300 ms after load, it printed `buttons: ["Add one"]` and `count after two clicks: 2 console errors: 0`, exit 0. Save it as `.cjs`: an ES module import does not find a globally installed Playwright.

- Waiting for network idle is a fallback for pages with no stable element to wait for. It hangs on pages that poll or stream.
- Prefer role and name locators; they are what a screen reader sees and survive restyling.
- Fail with a non-zero exit, never only a log line, so the caller can tell.
- Evidence rule: report the printed lines and the exit code, and say which URL and which build were tested.
