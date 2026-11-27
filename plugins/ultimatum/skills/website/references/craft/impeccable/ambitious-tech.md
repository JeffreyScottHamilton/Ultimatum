# Ambitious browser techniques: when and how to go further

Read when the brief asks for a moment that ordinary CSS and transitions cannot deliver, and you must pick a heavier technique without hurting speed or access.

Motion craft (curves, springs, gestures, reduced motion) is in `../emil-motion/index.md`, and its frame budget in `../emil-motion/performance.md`; the authored-scene rules for marketing pages are in `../taste/moments-and-scenes.md`. Where motion goes in the first place is in `delight-and-onboarding.md` § Motion thesis. This file covers the heavy tools.

## Propose before building

The technique is the riskiest choice on the page, so do not pick it alone. Offer two or three directions in a line each (what the user sees, the technique, the cost on a mid-range phone) and wait for a choice. Skip this only when the user already named the effect.

## The toolkit

| Want | Tool | Notes |
|---|---|---|
| Continuity between views or states | View Transitions API | same-document in current Chromium, Safari and Firefox; cross-document for multi-page sites in Chromium and Safari. Wrap in a feature check. <https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API> |
| Entry animation for something just shown | `@starting-style` with `transition-behavior: allow-discrete` | animates from `display: none` and for popovers and dialogs |
| Animation tied to scroll | `animation-timeline: scroll()` or `view()` | runs off the main thread; give a static fallback with `@supports` <https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline> |
| Animating a custom property (gradient stop, angle) | `@property` with a declared syntax | an unregistered property jumps rather than tweens |
| Interruptible sequenced motion | Web Animations API | promises, reverse, playback rate; no library needed |
| Particles, generative art, 3D | Canvas 2D, WebGL, WebGPU | WebGPU only with a WebGL or static fallback |
| Texture, displacement, light | SVG filters, CSS `backdrop-filter`, blend modes | cost grows with the filtered area; keep regions small |
| Thousands of rows | virtual scrolling, `content-visibility: auto` | keep keyboard and find-in-page working |
| Heavy computation | Web Workers, OffscreenCanvas, WebAssembly | keep the main thread for input |
| Sound | Web Audio API | only after a user gesture, with a visible toggle, never against mute |

## Rules that keep it safe

- **Progressive enhancement.** The page reads and works with the effect missing: no JavaScript, an old browser, reduced motion, a low-power device. Detect support (`@supports`, `'startViewTransition' in document`) before calling.
- **Budget.** Hold 60 frames per second on a mid-range phone. Animate `transform` and `opacity`; never layout properties in a loop.
- **Load late.** Initialise heavy scenes when they near the viewport; fetch the library on demand; show a poster frame first.
- **Pause what nobody sees.** Stop render loops when the element leaves the viewport (`IntersectionObserver`) or the tab is hidden (`visibilitychange`).
- **Reduced motion.** Swap travel and parallax for a crossfade or a still; keep feedback.
- **Access.** Canvas content needs a text alternative; controls inside a scene stay reachable by keyboard; nothing flashes more than three times a second (WCAG 2.3.1).
- **Clean up.** Release GPU contexts, workers and listeners when the component unmounts.

## Never

- Block the content behind a loading animation.
- Hijack scrolling speed or direction.
- Autoplay sound.
- Ship a WebGL scene where a picture would say the same.
- Add a large dependency for one effect the platform already offers.

## Four tests before shipping

1. **Wow test**: would someone show this to a colleague? If not, it is cost without return.
2. **Removal test**: take it out. If nothing is lost, leave it out.
3. **Device test**: run it on a throttled mid-range phone (`chromium` CPU throttle 4x is a floor, not a substitute for hardware). Measure frames, not feelings.
4. **Context test**: does it fit the page mode? Operate and Read surfaces rarely earn any of this.

Report which browsers and devices were actually tested, and which paths fell back.
