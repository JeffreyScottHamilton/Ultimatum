# Real-world conditions: phones, bad networks and things that vanish

Read this when an app talks to an API, takes payments or sends notifications, before the browser check in `checklist.md`. The happy path on office Wi-Fi proves little; these eleven situations are what real users hit in the first week. Each says what goes wrong, what to build, and how to test it.

A worked example runs all of them: `data/app/field-demo.html` (a small page that handles each case) and `data/app/field-check.cjs` (Playwright against a local server; `node field-check.cjs` prints one line per case and exits 0 when all pass). Copy the pattern for the real app: point it at the preview server and change the selectors.

## The rule behind all of them

Every request has a timeout, an error message a person can act on, and a retry path. No state is a blank screen. Nothing the user typed is lost.

## The eleven

1. **Wi-Fi switches to mobile data.** Requests in flight die with a network error. Build: retry safe requests (GET, and writes with an idempotency key) once or twice with backoff; keep form input in memory or `sessionStorage` until the server confirms. Test: start a request, `context.setOffline(true)`, then `false`; the page recovers without a reload.
2. **On slow 3G.** The page works, but the first view takes seconds. Build: a small first load (see `launch-load.md` items 9 and 10), skeletons instead of spinners for content, buttons that respond at once. Test: throttle with the Chrome DevTools Protocol, `Network.emulateNetworkConditions` with high latency and low throughput. Throttling only applies to real network requests; a response faked with `page.route().fulfill()` skips it, so test against a real server.
3. **Hotel or café Wi-Fi blocks the API.** Captive portals and filters answer with their own HTML login page, often with status 200. Build: check the `content-type` before parsing JSON and say "This network is blocking us; try mobile data". Serve the API from the site's own domain on port 443 (a path such as `/api`) rather than a separate host or port.
4. **The API takes 30 seconds.** Build: a client timeout (`fetch(url, { signal: AbortSignal.timeout(8000) })`), a message with a retry button, and anything genuinely slow moved to a background job that the page polls (`launch-load.md` item 12). Check the host's function time limit too.
5. **The AI provider is down or rate-limited.** Build: a timeout, a plain "We're busy" message on 429 and 5xx, no credits charged for a failed call, and optionally a second provider or a smaller model as fallback. Keep the user's prompt so they can resend it.
6. **The same request twice.** Double taps, retries and impatient refreshes. Build: disable the button while pending; send an `Idempotency-Key` header (a fresh `crypto.randomUUID()` per user action) and store it with a unique constraint so the server ignores the repeat; pass the key on to Stripe calls. Test: double-click and count requests at the server.
7. **Login expires.** Build: let the auth client refresh the session; on a 401 that survives one refresh, keep the draft, send the user to sign in with `?next=` set to the current path (paths only, see `auth.md`), and bring them back. Test: answer one request with 401 and check the redirect and the draft.
8. **An image never loads.** Build: `width` and `height` on every image so nothing jumps, real `alt` text, and an `error` handler that swaps in a plain box showing the alt text. Test: close the connection for image URLs.
9. **An error leaves a blank screen.** Build: an error boundary around each page (React error boundaries; in Next.js, `error.tsx` per route and `global-error.tsx`), a window `error` and `unhandledrejection` handler that shows "Something went wrong, reload" and reports the error, and an error state for every data fetch. Test: throw inside a timer and check the message appears.
10. **A push notification opens a deleted post.** Build: the deep-link route checks that the item exists and is visible to this user; if not, show "This is no longer available" with a link home, never a crash or an empty layout. Expire or withdraw notifications when the item is deleted, where the platform allows.
11. **No signal right after paying.** The card was charged but the phone never saw the success page. Build: fulfil orders from the payment webhook on the server, not from the redirect (`stripe.md`); make fulfilment idempotent; on the next app open, show the order status from the server; send a confirmation email. Test: complete a test-mode checkout, close the tab before the redirect, and check the order is fulfilled and visible.

## Done means

`field-check.cjs` (or the app's own version of it) passes on the preview build, the results are pasted into the launch notes, and each of the eleven has a one-line note: built, tested how, or not applicable and why.
