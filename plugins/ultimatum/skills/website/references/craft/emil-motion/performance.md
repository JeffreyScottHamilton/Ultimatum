# Animation performance: why frames drop

Read when motion stutters, a drag gets laggier as content grows, or jank only shows while a page loads. Page-level budgets (bytes, requests, WebGL) are in `../taste/performance.md`; this file covers only whether each animation frame finishes in time. Symptom lookup: `../../../../../data/craft/emil-motion/symptoms.csv`.

Name the cause before touching code; "I added `will-change` and it feels better" explains nothing. Mark each finding as read from the code or still needing a recording on a real phone, since a quick laptop hides nearly all of these problems.

## Budget

60 fps leaves 16.7 ms per frame; a 120 Hz screen leaves 8.3 ms. Design for the smaller. One layout pass on a complex page can take over 100 ms: a dozen missed frames, not one.

## What you animate

| Tier | Properties | Cost |
|---|---|---|
| Compositor only | `transform`, `opacity`; in current Chrome and Firefox also `filter`, `clip-path`, `background-color` (test per browser) | cheapest, own layer |
| Paint, then composite | `box-shadow`, `border-radius`, `color` | repainted on each frame |
| Layout, then paint, then composite | `height`, `width`, `margin`, `padding`, `left`, `top`, `border-width` | costliest, and pushes neighbours around |

Move down a tier where you can:

| Instead of | Animate |
|---|---|
| width, height or padding to grow | `scale()` |
| top, left or margin to move | `translate()` (percent is of own size) |
| display or visibility swap | `opacity` |
| box-shadow | `filter: drop-shadow()` on the element, or fade a pre-shadowed layer |

- A sidebar animating `margin-left` re-lays out the page beside it each frame; `translateX` does not.
- A small absolutely positioned element with no children can animate `width` without visible cost, and keeps its corner radius where `scale` would smear it. Still prefer the cheap form: only one of the two cannot regress on a slow device.
- Docs: https://web.dev/articles/animations-guide and https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/CSS_JavaScript_animation_performance

## Where it runs

Script that moves things every frame competes with all other main-thread work. Which driver:

| Driver | Thread |
|---|---|
| `requestAnimationFrame` loops, libraries' layout animations | main thread |
| Web Animations API, a library that hands off to it | can run on the compositor |
| CSS transitions and keyframes | can run on the compositor |

- The trap is motion playing during a busy page: route changes, a tab indicator during navigation, anything alongside fetching or hydration. A tab indicator driven by script stalls exactly when the next page loads; a CSS transition keeps moving.
- In Motion, `opacity`, `transform`, `clip-path` and `filter` go to the Web Animations API. The `x`, `y`, `scale`, `rotate` shorthands are compositor-accelerated from 14.2 on HTML elements; on older versions animate a full `transform` string when it must survive a busy thread. Whatever the version, these stay on the main thread: per-frame motion-value writes, inertia, `onUpdate`, `transformTemplate`, and layout animations (`layout`, `layoutId`). Check the library version you actually have.
- Acceleration is progressive enhancement. A browser may decline it in some cases (percent transforms historically); correctness wins, so keep `translateY(100%)` for elements of unknown size.
- A workable division: CSS for plain motion and for whatever must run while scripts are busy; a library for springs, shared layout, exits of unmounted components and momentum.

## Do not animate through state

A hand-written loop calling `setState` each frame re-renders at 60 Hz and blows the budget. Search for state setters called inside `requestAnimationFrame`, `pointermove`, `scroll` and drag handlers.

```js
// drops frames: one render per frame
setOffset(next);
// smooth: no render
node.style.transform = `translateY(${next}px)`;
```

## Two traps that use transform and still drop frames

1. Inherited custom properties. Writing `--drag: 40px` on a parent and reading it in children's `transform` restyles every descendant on every change; cost grows with content. Set `transform` on the moving element instead. Suspect this whenever a transform animation gets worse as content grows.
2. Blur. `filter: blur()` gets expensive fast, worst in Safari. Keep animated blur below 20 px; a crossfade only needs 2 to 5 px.

## will-change

A browser may hand an animation to the GPU mid-flight, and the hand-off can shift the element by a pixel. `will-change: transform` promotes it early. Add it only once you have seen the shift or measured dropped frames. A browser promotes elements that animate transform or opacity by itself, and each extra layer spends GPU memory. Put it on the animating element, never on `*` or large containers. It earns its place on an expensive paint such as a large blurred element, kept small. Docs: https://developer.mozilla.org/en-US/docs/Web/CSS/will-change

## Diagnose in this order

1. Which properties animate? Expand `transition: all` and library shorthands into what they truly animate. Layout first, then shadow and radius.
2. Does jank coincide with a busy page? Move to CSS or the Web Animations API.
3. Does React re-render each frame?
4. Does it get worse as the page fills up? Suspect an inherited variable, or too many nodes moving at once.
5. Is a custom property itself animated, or a library shorthand on an old version?
6. Any animated blur over 20 px?
7. Still shifting or stuttering after that: put `will-change: transform` on that one element.

Prove it with a recording, not a hunch: the Performance panel lists long tasks and missed frames; the Animations panel can slow playback down. Profile a mid-range phone through remote debugging; throttling the desktop CPU imitates a slow processor, not a weak GPU or short memory.

## Report one finding like this

The element and `file:line`, the cause from the list above, one line each for before and after, and a tag: "from code" or "needs device recording". Sort by cost, layout ahead of paint and a busy main thread ahead of an idle one.

## Long lists

Virtualise long lists so only visible rows render (a library choice: `libraries-and-toasts.md`). Do not stagger or animate thousands of rows.
