# Measuring React performance: get the number before and after

Read before claiming a React change made something faster or smaller; a fix without a before-and-after number is a guess.

Rule: one change, one measurement, same conditions (production build, same data, same device or throttle). Write both numbers in the report.

## 1. Build output: first-load JavaScript per route

- Next.js: `next build` prints each route's size and first-load JS. Copy the table before the change and after.
- Vite: `vite build` prints chunk sizes; add `rollup-plugin-visualizer` for a treemap.
- Budget: set a number per route (for example 150 KB gzipped first-load on a content page) and treat a rise as a review question.

## 2. Bundle analyzer: what is inside the chunk

- Next.js: `@next/bundle-analyzer`, run with `ANALYZE=true next build`. Newer Next.js versions also ship `next experimental-analyze`; check your version's docs.
- Look for: a whole icon or date library where one function was needed, the same package twice at two versions, server-only code (database clients, secrets helpers) in a client chunk, and large JSON imported into a component.
- `source-map-explorer` works on any build that emits source maps.

## 3. Server and request timing: waterfalls

- Browser Network panel, waterfall column: requests that start only after the previous one ends are the smell.
- On the server, wrap suspect calls with timing and log the route total. `console.time` is enough for a check; for a lasting view, add a `Server-Timing` response header or OpenTelemetry spans (Next.js has `instrumentation.ts`).
- Compare route time against the slowest single call. A total near the sum of calls means serial awaits (`worked-fixes.md` § 1).

## 4. React Profiler: render cost

- React DevTools, Profiler tab: record one interaction (a keystroke, a click), stop, read the flame chart.
- Turn on "Record why each component rendered". Props that change every render (new objects, new functions) and context updates show up here.
- Turn on "Highlight updates when components render" for a quick visual of how far a change spreads.
- In code: `<Profiler id="list" onRender={(id, phase, ms) => ...}>` logs commit time for a subtree; useful in a test or a debug build.
- Measure in a production profiling build where you can; development mode is several times slower and double-renders under Strict Mode.

## 5. Browser Performance panel: long tasks and interactions

- Record with CPU throttled (4x or 6x) to approximate a mid-range phone.
- Long tasks (over 50 ms) block input. Find the React commit or script inside each one.
- Interaction to Next Paint (INP): the panel's Interactions track shows each input's delay, processing and presentation time.

## 6. Field data: what real users get

- `web-vitals` library: report LCP, INP and CLS to your analytics. Lab numbers find the cause; field numbers say whether users noticed.
- Thresholds Google publishes as "good": LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less, measured at the 75th percentile. Check the current values on web.dev before quoting them in a report.
- Vercel Speed Insights, Chrome UX Report (CrUX) and most analytics tools show these per route.

## 7. Lighthouse: a repeatable lab score

- `npx lighthouse <url> --preset=desktop` or the mobile default. Run three times and take the median; single runs vary.
- Use it in CI with a budget file to catch regressions, not as the only proof of a fix.

## Report template

```
Change: moved 'use client' from page to AddToCart button
Measure: next build, /products first-load JS
Before: 212 KB   After: 141 KB   (same commit except this change)
```
