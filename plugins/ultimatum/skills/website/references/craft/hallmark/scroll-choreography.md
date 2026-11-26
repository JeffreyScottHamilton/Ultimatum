# Scroll choreography: one earned pattern

Read only when the content is a sequence that earns pinning or scrubbing. Usually skip it: the single reveal in `craft-motion.md` is the baseline.

## Rules

- One scroll-linked pattern per page; it counts as one of the three motion ideas.
- Keep it off paragraphs. It may act on structure: one pinned section, a single display element, or a thin progress line.
- It does not replace the hero entrance, and no element carries both.
- Base CSS draws the finished page. Wrap the effect in a support query for `animation-timeline` plus a no-preference motion query and a 40rem minimum width, so reduced-motion users, phones and older browsers get the full static page (WCAG 2.3.3).
- Declare `animation-timeline` and `animation-range` after the `animation` shorthand, which resets them.
- Use `linear`: scrubbing maps distance to progress.
- Docs: https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline

## Pinned chapter

The tall wrapper owns a named view timeline and each step inside the sticky pane reads a slice of it, because a stuck element cannot time itself.

```css
.chapter { min-height: 280vh; }
.chapter__pin { position: sticky; top: 2rem; }
@media (min-width: 40rem) and (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .chapter { view-timeline: --story block; }
    .chapter__steps li {
      animation: rise linear both; animation-timeline: --story;
      animation-range: contain calc(var(--i) * 25% + 5%) contain calc(var(--i) * 25% + 30%);
    }
    .chapter__steps li:nth-child(1) { --i: 0; }
    .chapter__steps li:nth-child(2) { --i: 1; }
    .chapter__steps li:nth-child(3) { --i: 2; }
    @keyframes rise { from { opacity: .25; translate: 0 10px; } to { opacity: 1; translate: 0 0; } }
  }
}
```

## Scrubbed headline

One mid-page statement heading (never the hero h1) wipes in with a `clip-path` on `view()`, range `entry 20% cover 45%`, from `inset(0 100% 0 0)` to `inset(0)`.

## Progress spine

A fixed 2px rule at the left whose `::after` scales on `scaleY` from 0–1 with `animation-timeline: scroll(root)`. Hidden under 40rem. A functional indicator.

## Sticky diptych

Two columns (5fr/7fr), one pane `position: sticky` below any sticky nav, the other scrolling figures that fade in on their own `view()` with range `entry 0% entry 60%`. Under 60rem: one column, `position: static`.

## Fallback

Without `animation-timeline`, use only the once-only IntersectionObserver reveal, never a scroll listener or scrub polyfill. Hide `[data-reveal]` only under a `.js` class that the script adds, so no-script visitors see everything (see `craft-motion.md`).

```js
if (!CSS.supports("animation-timeline", "view()")) {
  const watcher = new IntersectionObserver((entries, obs) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add("is-seen");
      obs.unobserve(entry.target);
    }
  }, { rootMargin: "0px 0px -15% 0px" });
  document.querySelectorAll("[data-reveal]").forEach((node) => watcher.observe(node));
}
```

Local and app notes: a pinned chapter suits "how it works" on a service page; do not pin a booking form or pricing table, where people need to compare and scroll freely.
