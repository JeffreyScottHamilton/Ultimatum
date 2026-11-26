# Craft: motion, the hero entrance and state feedback

Read when deciding what moves on a page, how long it takes and what shows under reduced motion. The theme's own motion rules outrank everything here (`themes.md`); scroll stories are in `scroll-choreography.md`, small widgets in `microinteractions.md`.

## Who decides

The theme's motion section first; a shape's reveal runs only where the theme allows one; the genre default only where the theme is silent.

## The hero entrance

- One settle of 0.4 to 0.8s including stagger, starting from an already visible default. A fade with an 8px rise counts as one motion.
- Never a fade, a sweep and a scale on one element. No bounce, no starfield, no mouse parallax, no auto-rotating carousel.
- Before shipping the hero visual: it shows the real thing, is big, holds the accent under its footprint, weighs under 2 MB, and has a reduced-motion fallback that changes the visual, never the copy.

## Rules for every page

- **Animate only `transform` and `opacity`;** blur, `clip-path`, mask and shadow may join when smooth on that element alone (MDN on performance: https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/CSS_JavaScript_animation_performance).
- **Easing tokens:** an out curve for arrivals, an in curve for exits, in-out for toggles. Never the browser `ease`; `linear` only for progress and scrubbing; no overshoot on UI state (gate 12).
- **Durations:** micro 120ms (press, tick, colour), short 220ms (hover, tooltip, menu), long 420ms (modal, drawer, accordion, reveal). Exits run at 60 to 75% of the enter. Stagger 30 to 50ms between rows, 60 to 100ms between blocks, 500ms in total at most, once.
- **One reveal per page,** staggered by an index custom property, 0.4 to 0.8s in all, content visible without it (gate 62). Under reduced motion every reveal shows its end state at once; anything that must still run (a loader, a 150ms fade) opts out with a keep-motion class.
- **Scroll:** IntersectionObserver for reveals and thresholds (https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API); a passive, frame-throttled scroll listener only where direction matters; scroll-scrubbed motion is one pattern from `scroll-choreography.md` and no more (F8).
- **State feedback:** hover is one signal that raises contrast (a colour step, or a 1px lift at micro duration on a control that keeps its colour). Tooltips wait 800 to 1000ms on hover and 0 on focus. Focus rings never animate. Menus, modals and accordions follow `microinteractions.md`.
- **Never:** parallax, custom cursors, cursor followers, a marquee that will not pause on hover and focus, `will-change` on a whole class, a pulsing dot, a caret blinking more than five beats, an infinite loop other than a loader. Allowed loops: one small loop of 4s or less, or one ambient loop of 8s or slower a theme declares. Every loop stops under reduced motion and off-screen; one past 5 seconds has a visible pause control (WCAG 2.2.2: https://www.w3.org/TR/WCAG22/#pause-stop-hide).

## A reveal that survives no script

```html
<style>
  .js .reveal { opacity: 0; transform: translateY(8px); transition: opacity .42s ease-out, transform .42s ease-out; }
  .js .reveal.in { opacity: 1; transform: none; }
  @media (prefers-reduced-motion: reduce) { .js .reveal { opacity: 1; transform: none; transition: none; } }
</style>
<script>document.documentElement.classList.add('js')</script>
```

Without the `js` class nothing is hidden, which is what gate 62 asks for.

## Overlap

Merged with `../taste/motion.md` (durations, triggers, reduced motion) and `../../website/design-rules.md` § 2 (sections that fade in the same way every time). The reduced-motion rule is also a WCAG 2.2 item (2.3.3 and 2.2.2) tied in `../taste/accessibility.md`.
