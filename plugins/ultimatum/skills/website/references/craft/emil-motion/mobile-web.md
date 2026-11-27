# Making a web page feel native on a phone

Read when a page works on desktop but feels wrong on a phone: sticky hover, grey flash on tap, a bar under the URL bar, zoom on focus, lag, page scrolling behind a sheet, content under the notch. Match the symptom in the table, then read its section. Lookup form: `../../../../../data/craft/emil-motion/symptoms.csv` (group `mobile`).

Local-business sites are mostly viewed on phones, so this is not optional: the call button, booking form and map must be right here first. Related: `../taste/accessibility.md` for target sizes and focus.

## Hard rules

1. Every fix has a reason; apply it where the reason applies. `user-select: none` is right on a button and wrong on body text.
2. Use capability queries (`hover`, `pointer`, `env()`, `dvh`), never user-agent or screen-width guesses for touch.
3. Touch and mouse overlap (tablets with trackpads, laptops with touchscreens), so branch on what the input can do, not on the device model.
4. Zoom stays on. Settings such as `user-scalable=no` or `maximum-scale=1` fail WCAG 1.4.4; the real remedy is a larger input font.
5. Desktop emulation hides the on-screen keyboard, safe areas, rubber banding, the tap delay and sticky hover. Try a real phone, or state that you did not.

## Symptoms

| Symptom | Fix |
|---|---|
| Hover stuck after a tap | Put every `:hover` rule inside `@media (hover: hover) and (pointer: fine)` |
| Grey or blue flash on tap | `-webkit-tap-highlight-color: transparent`, then give every tappable its own `:active` |
| Layout the wrong height | `100dvh` for an app shell; `100svh` or `min-height: 100svh` for a hero |
| Page zooms on input focus | Inputs at least 16 px |
| Taps feel slow | Style `:active` or react on pointer down, and set `touch-action: manipulation` |
| Pull-to-refresh or rubber band hijacks | `overscroll-behavior: none` on the root, `contain` on inner scrollers |
| Content under the notch | `viewport-fit=cover` plus `env(safe-area-inset-*)` padding |
| Long press selects a button label | `user-select: none` and `-webkit-touch-callout: none` on controls only |
| Carousel scrolls the page | `touch-action: pan-y` on a horizontal gesture surface |
| Status bar colour wrong | `theme-color` meta per colour scheme |
| Fine in Chrome, wrong on phone | Real device |

## Why each one happens

- Hover: touch has no hover, so browsers fake it and keep the state until the next tap. Press feedback goes through `:active`, which works on all inputs. In Tailwind v4 the `hover:` variant already applies this gate.
- `100vh` is the tallest the viewport gets (URL bar hidden), so on load the page overflows. `dvh` follows the bar; right for an app shell, but it causes shifts on marketing pages mid-scroll, where `svh` is stable.
- iOS zooms into inputs under 16 px and does not zoom back. Where a smaller desktop size is wanted, apply 16 px under `@media (pointer: coarse)`. Also set `inputmode` (`numeric`, `decimal`), `type="email"` or `"tel"`, and `autocapitalize`/`autocorrect` off for usernames and codes. That serves booking and checkout forms directly.
- Press feedback that waits for `click` fires when the finger leaves, which reads as lag. Keep it at 100 to 160 ms, ease-out, with the house tokens (`easing-and-duration.md`).
- `touchmove` plus `preventDefault()` to stop scroll chaining is slow and breaks scrolling; use `overscroll-behavior`.
- Without `viewport-fit=cover` all `env(safe-area-inset-*)` values are 0. Fixed headers, bottom bars, toasts and sheets are where they matter.
- `touch-action` lists the gestures the browser keeps. On a horizontal carousel, `pan-y` leaves vertical scrolling to the browser. `none` means your script owns every axis; use it only on a drag surface. For plain carousels prefer native scroll with `scroll-snap-type: x mandatory` and `scroll-snap-align: start`.
- `theme-color` should match the colour at the very top of the page, not the brand colour. If the theme switches by class, update the meta from script.

## Floor to set before building components

```html
<meta name="viewport" content="viewport-fit=cover, width=device-width, interactive-widget=resizes-content, initial-scale=1">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0a0a0a" media="(prefers-color-scheme: dark)">
```

```css
html { -webkit-text-size-adjust: 100%; -webkit-tap-highlight-color: transparent; }
:is(input, textarea, select) { font-size: 1rem; } /* 16px at the default root size */
:is(button, a, [role="button"]) { touch-action: manipulation; }
@media (hover: hover) and (pointer: fine) { /* every :hover rule goes in here */ }
```

With `interactive-widget=resizes-content`, Android Chrome shrinks the layout viewport when the keyboard opens, as iOS already does, so pinned bottom inputs follow along. `overscroll-behavior: none` on the root suits an app; on a content page leave the browser's pull-to-refresh alone.

## Never ship

Blocked zoom. Ungated `:hover`. `100vh` on an app shell or bottom-pinned bar. `100dvh` on a hero. Press feedback only on `click`. Scroll control by `touchmove` listeners. Text that is content made unselectable.

## Test on hardware

Phone on USB or Wi-Fi, dev server bound to the network, open by LAN address. iOS: Safari Develop menu. Android: `chrome://inspect`. Use an older phone, the keyboard open, landscape once, and the installed web app mode if you ship one. Docs: https://developer.mozilla.org/en-US/docs/Web/CSS/overscroll-behavior and https://developer.mozilla.org/en-US/docs/Web/CSS/env
