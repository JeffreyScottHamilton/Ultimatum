# Scroll choreography: one earned pattern

Read only when content has a sequence worth pinning or scrubbing. The default is none: the one-time reveal in `craft-motion.md` is the norm.

## Rules

- One scroll-linked pattern per page; it counts as one of the three motion ideas.
- Never on body text. Targets are structure: a pinned section, one display element, a 2px spine.
- It does not replace the hero entrance, and no element carries both.
- The base CSS shows the finished page. The effect lives inside `@supports (animation-timeline: view())` and `@media (prefers-reduced-motion: no-preference) and (min-width: 40rem)`. Reduced motion, phones and old browsers see the complete static page (WCAG 2.3.3).
- Declare `animation-timeline` and `animation-range` after the `animation` shorthand, which resets them.
- Use `linear`: scrubbing maps distance to progress.
- Docs: https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline

## Pinned chapter

A tall track owns a named view timeline; the steps inside the sticky pane read slices of it (a stuck element cannot drive its own `view()`).

```css
.chapter { min-height: 280vh; }
.chapter__pin { position: sticky; top: var(--space-xl); }
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) and (min-width: 40rem) {
    .chapter { view-timeline: --chapter block; }
    .chapter__steps li { animation: step linear both; animation-timeline: --chapter; }
    .chapter__steps li:nth-child(1) { animation-range: contain 5% contain 30%; }
    .chapter__steps li:nth-child(2) { animation-range: contain 30% contain 55%; }
    .chapter__steps li:nth-child(3) { animation-range: contain 55% contain 80%; }
    @keyframes step { from { opacity: .2; transform: translateY(8px); } to { opacity: 1; transform: none; } }
  }
}
```

## Scrubbed headline

One mid-page statement heading (never the hero h1) wipes in with a `clip-path` on `view()`, range `entry 20% cover 45%`, from `inset(0 100% 0 0)` to `inset(0)`.

## Progress spine

A fixed 2px rule at the left whose `::after` scales on `scaleY` from 0 to 1 with `animation-timeline: scroll(root)`. Hidden under 40rem. A functional indicator.

## Sticky diptych

Two columns (5fr/7fr), one pane `position: sticky` below any sticky nav, the other scrolling figures that fade in on their own `view()` with range `entry 0% entry 60%`. Under 60rem: one column, `position: static`.

## Fallback

Without `animation-timeline`, use only the once-only IntersectionObserver reveal, never a scroll listener or scrub polyfill. Hide `[data-reveal]` only under a `.js` class that the script adds, so no-script visitors see everything (see `craft-motion.md`).

```js
if (!CSS.supports("animation-timeline: view()")) {
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add("is-seen"); io.unobserve(e.target); }
  }), { rootMargin: "0px 0px -20%" });
  document.querySelectorAll("[data-reveal]").forEach((el) => io.observe(el));
}
```

Local and app notes: a pinned chapter suits "how it works" on a service page; do not pin a booking form or pricing table, where people need to compare and scroll freely.
