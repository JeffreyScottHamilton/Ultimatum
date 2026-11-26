# Performance

Read before handing over any page, and while building anything heavy: big photographs, fonts, effects, renders or video.

## Budgets

Measured at 1440 and 390 in a headless browser. Sizes are KiB (1024 bytes). A warning needs a fix or a written reason; a failure blocks the hand-over.

| Check | Warn above | Fail above |
|---|---|---|
| Transfer, text gzipped | 1,500 | 3,000 |
| All images / largest image | 1,200 / 350 | 2,400 / 700 |
| JavaScript parsed / CSS | 450 / 120 | 900 / 250 |
| Requests | 60 | 110 |
| Font families / files / bytes | 2 / 4 / 160 | 3 / 6 / 320 |
| Images without width and height (or `aspect-ratio`) | 0 | 3 |
| Images below the fold not lazy | 0 | 3 |
| Images over 2.2× their shown width (img, CSS background, SVG) | 0 | 3 |
| Photos as CSS backgrounds below the fold (cannot be lazy) | 0 | 3 |
| Live WebGL contexts at any moment | | 4 |
| WebGL contexts made over a full scroll | 12 | 24 |
| Long tasks / total blocking time (median, WebGL off) | 8 / 1.5 s | 20 / 4 s |
| First and largest contentful paint (median) | 2.5 / 4.5 s | 4.5 / 8 s |
| Cumulative layout shift (median) | 0.1 | 0.25 |
| Effect or component module loaded but never mounted | 0 | 2 |
| Broken requests, sideways overflow | | any |

Field targets for comparison (Core Web Vitals, 75th percentile): LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less. https://web.dev/articles/vitals

## Measure

- Load each page three times at each width and take the median of timings. Counts and bytes are exact on one load.
- Lab paint times compare pages with each other; they are not field data. On a busy machine treat a timing failure as a warning and re-run.
- Fix every failure, then re-measure. Quote the numbers you saw, never a guess.

```js
// node measure.mjs http://localhost:8080/  (Playwright Chromium; prints one line per width)
import { chromium } from 'playwright';
const url = process.argv[2];
const browser = await chromium.launch();
for (const width of [1440, 390]) {
  const page = await browser.newPage({ viewport: { width, height: 900 } });
  let bytes = 0, requests = 0, failed = 0;
  page.on('response', async r => { requests++; if (r.status() >= 400) failed++;
    try { bytes += (await r.body()).length; } catch {} });
  await page.goto(url, { waitUntil: 'networkidle' });
  const m = await page.evaluate(async () => {
    // LCP entries only reach a buffered observer; give up after a second if none was recorded.
    const lcp = await Promise.race([new Promise(r => setTimeout(() => r(null), 1000)),
      new Promise(r => new PerformanceObserver(l => r(Math.round(l.getEntries().at(-1).startTime)))
        .observe({ type: 'largest-contentful-paint', buffered: true }))]);
    const imgs = [...document.images];
    return {
      noSize: imgs.filter(i => !i.getAttribute('width') && getComputedStyle(i).aspectRatio === 'auto').length,
      oversize: imgs.filter(i => i.clientWidth && i.naturalWidth > 2.2 * i.clientWidth).length,
      eagerBelow: imgs.filter(i => i.getBoundingClientRect().top > innerHeight && i.loading !== 'lazy').length,
      overflow: document.documentElement.scrollWidth > innerWidth,
      lcp,
    };
  });
  console.log(width, { kib: Math.round(bytes / 1024), requests, failed, ...m });
  await page.close();
}
await browser.close();
```

Layout shift needs a `PerformanceObserver` registered before load (`page.addInitScript`); paint entries likewise. https://developer.mozilla.org/en-US/docs/Web/API/LayoutShift

## Images

- AVIF or WebP through `srcset`, at most 2× the shown width: a full-bleed hero is 2880w at 1440 and 780w at 390.
- Hero under 400 KiB; every other photograph under 250 KiB; all images on the page under 2,400 KiB.
- A photo natural width under 0.75× its shown width is upscaled: replace it.
- Every image slot has `src`, `width` and `height` (or an `aspect-ratio` box) and a flat fill while it loads (`../../website/design-rules.md` §7).
- Below the fold: `loading="lazy"`. The hero image: eager, with `fetchpriority="high"`.
- Photographs are `<img>`, not CSS backgrounds, so they can be lazy and sized.
- Responsive images: https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images

## Fonts

- At most four font files. Preload the two used above the fold. `font-display: swap`. Load only the weights in use; subset where the licence allows. The house font rules are in `../../website/craft.md` §2.

## Layout shift

- Keep CLS under 0.1. Reserve space for every image, embed, banner and late widget.
- Animate only `transform` and `opacity` (`motion.md` § Tokens). `background-position` only on small spans of text. Never animate width, height, top, left or margins.
- The house motion limits are in `../../website/libraries.md`.

## Scripts

- Modules, deferred. No loader or gate before the page shows.
- No layout reads (`getBoundingClientRect`, `offsetHeight`) inside pointer-move or scroll handlers. The one allowed scroll read is passive and writes a custom property once per frame (`motion.md` § Scroll).
- Non-tech pages load no animation library and no WebGL. A 3D product render is about 2 MB with its poster, and only when the brief asks for 3D (`objects.md`).
- A page may mark its first screen as built (`document.documentElement.dataset.ready = '1'`) so effects mount after it and measurement can stop waiting.
- Video is tech only (`later.md` § Video).

## WebGL

Tech pages only.

- At most four live contexts at once, counting effects, parts, objects and renders. Each shows a poster first.
- Mount late with `IntersectionObserver` near the viewport; observers may mount and unmount but never drive motion.
- About 1.5 megapixels in total; device pixel ratio at most 1.5. Ray marching, particles and noise render at 50% resolution, capped at 30 fps; lower the ratio when frames run slow.
- Every WebGL piece has a still fallback for no WebGL2, a failed shader, phones and reduced motion.
- Draw a still ground once, copy it to an image, and release the context (`WEBGL_lose_context`).
- Pause off screen and in a hidden tab (`visibilitychange`).
- Measuring with WebGL off is only a proxy for CPU cost; shader compile time on the GPU is not measured by these checks.
- WebGL best practices: https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices
