# Craft: motion, the hero entrance and state feedback

Read when deciding what moves on a page, how long it takes and what shows under reduced motion. The theme's own motion rules outrank everything here (`themes.md`); scroll stories are in `scroll-choreography.md`, small widgets in `microinteractions.md`.

## Who decides

Defer to the theme's motion section; a page shape's reveal runs only if the theme permits one, and the genre default applies only if the theme says nothing.

## Hero entrance

- One entrance only, 0.4–0.8 seconds including any stagger, starting from a visible default state. A fade combined with an 8px rise counts as one motion.
- One element never combines a fade, a sweep and a scale. No bounce, no starfield, no mouse parallax, no auto-rotating carousel.
- Before shipping the hero visual: it shows the real thing, is big, holds the accent under its footprint, weighs under 2 MB, and has a reduced-motion fallback that changes the visual, never the copy.

## Rules for every page

- **Animate `transform` and `opacity` by default.** Blur, `clip-path`, masks and shadows may join once they run smoothly on that element alone (MDN on performance: https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/CSS_JavaScript_animation_performance).
- **Easing tokens:** decelerate arrivals, accelerate exits, use in-out for toggles. Never the default `ease`; reserve `linear` for progress and scrubbing; no overshoot for interface state (gate 12).
- **Durations:** micro 120ms (press, tick, colour), short 220ms (hover, tooltip, menu), long 420ms (modal, drawer, accordion, reveal). Exits take 60–75% of the entrance time. Stagger rows by 30–50ms and blocks by 60–100ms, capped at 500ms overall and played once.
- **One reveal for the page,** staggered through an index custom property and lasting 0.4–0.8s in total, with content visible when it does not run (gate 62). With reduced motion, reveals jump to their end state; anything essential (a loader, a 150ms fade) opts out through a keep-motion class.
- **Scroll:** use IntersectionObserver for reveals and thresholds (https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API); add a passive scroll listener, throttled per frame, only where direction matters; scroll-scrubbed motion uses a single pattern from `scroll-choreography.md` (F8).
- **State feedback:** hover gives a single contrast-raising cue, either a colour step or, for a control that keeps its colour, a 1px lift at micro speed. Tooltips wait 800–1000ms on hover and appear instantly on focus. Focus rings stay static. Menus, modals and accordions follow `microinteractions.md`.
- **Avoid:** parallax, custom or following cursors, a marquee that keeps going when hovered or focused, `will-change` applied to a whole class, pulsing dots, a text caret that blinks beyond five beats, and endless loops apart from a loader. Loops that are allowed: one small loop of four seconds or under, or one slow ambient loop (eight seconds or more) that a theme declares. Every loop halts under reduced motion and when off screen, and any running longer than five seconds gets a visible pause control (WCAG 2.2.2: https://www.w3.org/TR/WCAG22/#pause-stop-hide).

## A reveal that survives no script

```html
<style>
  .js .reveal { opacity: 0; translate: 0 8px; transition: opacity .4s ease-out, translate .4s ease-out; }
  .js .reveal.in { opacity: 1; translate: 0 0; }
  @media (prefers-reduced-motion: reduce) { .js .reveal { opacity: 1; translate: none; transition: none; } }
</style>
<script>document.documentElement.className += ' js'</script>
```

Without the `js` class nothing is hidden, which is what gate 62 asks for.

## Overlap

Merged with `../taste/motion.md` (durations, triggers, reduced motion) and `../../website/design-rules.md` § 2 (sections that fade in the same way every time). The reduced-motion rule is also a WCAG 2.2 item (2.3.3 and 2.2.2) tied in `../taste/accessibility.md`.
