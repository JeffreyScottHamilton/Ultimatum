# Small UI details that read as quality

Read when a screen looks nearly right but off: numbers wobbling, a heading too loose, a gradient with a visible edge, a timestamp that says "340 days ago". Each is a one-line fix. They sit next to motion because they are found in the same polish pass.

On marketing and local-business pages the type tokens in `../taste/system.md` set size and tracking first; these fixes sit under them.

## The list

| Symptom | Fix | Why |
|---|---|---|
| Numbers jitter as they change | `font-variant-numeric: tabular-nums` | Equal-width digits keep columns and counters still. Not every font has them; check the face. |
| Large heading looks loose | Tighten tracking to about `-0.02em` on display sizes, and loosen slightly on small caps | Space between letters reads wider as type grows. |
| Body copy awkward to read | `max-width: 65ch` | Lines past about 65 characters tire the eye. |
| Button feels dead | `transform: scale(0.97)` on `:active`, 100 to 160 ms | Tells the finger the press landed. |
| Avatar squashed to an oval | `flex-shrink: 0` on it | Flex parents shrink fixed boxes first. |
| Gradient fade shows a hard edge | Add intermediate stops that follow an ease curve | A two-stop gradient has a visible start line. |
| Change still feels rough | A short `filter: blur(2px)` during it, removed at the end | Hides the instant where two states fail to line up. Keep it brief; see `performance.md` for the cost. |
| Dropdown sluggish | Ease-out under 300 ms | Ease-in delays the first visible movement. |
| Popover grows from the wrong corner | `transform-origin` at the trigger; modals stay centred | Matches where the eye just was. |
| "1 members" | `Intl.PluralRules` | Hardcoded plurals fail at 1 and in other languages. |
| Old timestamps read "340 days ago" | Absolute date after about a week | Long relative spans cannot be compared at a glance. |

## Transform notes

- `translateY(100%)` moves by the element's own height, so a sheet of any size can start fully off-screen with no pixel value.
- `scale()` scales children, text and border radius included. Do not scale a container to resize its layout.
- 3D: set `perspective` on the parent and `transform-style: preserve-3d` where children share the space. A smaller perspective value deepens the effect; keep it gentle.
- Percent values in `translate` are relative to the element, not the parent.

## Eased gradient fade (runnable)

```css
.fade-bottom {
  background: linear-gradient(to bottom,
    rgb(255 255 255 / 0) 0%,
    rgb(255 255 255 / .013) 8%,
    rgb(255 255 255 / .049) 16%,
    rgb(255 255 255 / .104) 25%,
    rgb(255 255 255 / .175) 35%,
    rgb(255 255 255 / .259) 45%,
    rgb(255 255 255 / .352) 55%,
    rgb(255 255 255 / .648) 75%,
    rgb(255 255 255 / .85) 90%,
    #fff 100%);
}
```

Adjust the stops to a smooth curve for your colours; the point is that no stop jumps. Put it over scrolling content only where something actually overlaps; do not add a divider line and a fade together.

## Reading list

- MDN `font-variant-numeric`: https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric
- MDN `Intl.PluralRules`: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules
- MDN `transform-origin`: https://developer.mozilla.org/en-US/docs/Web/CSS/transform-origin
