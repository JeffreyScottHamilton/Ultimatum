# Anatomy: isometric projection and drawing order

Read when you need the maths for placing parts, or a runnable starting sketch.

## Projection

World: x to the right-front, y to the left-front, z up. For azimuth `a` and elevation `e` a point maps to the screen as:

- `u = (x - y) * cos(a)`
- `d = (x + y) * sin(a)`
- screen x = `ox + s * u`
- screen y = `oy + s * (d * sin(e) - z * cos(e))`

With `a` = 45 degrees and `e` = 30 degrees this is a clean isometric look. Choose `s` (scale) and the offset by projecting the corners of the whole object and fitting them into the card with the margin that gives 55 to 65 percent fill.

## A box is three polygons

Only the top, the face toward +y and the face toward +x can be seen at the default camera. Fill them with the lit, mid and dark tones and stroke with the edge tone.

## Drawing order

Far to near. For boxes that do not overlap in plan, sort by centre `x + y + z`. When two blocks overlap in plan or interlock, the centre sort fails; give those pairs an explicit order, or split one block into two so each piece sorts correctly. A part that the object passes through (a ring on a rod) is split into back and front halves.

## Runnable sketch

`../../../../../data/craft/anatomy/iso-slabs.html` is a single file, no libraries: three blocks, four tones from one light, a depth sort, and a keyboard-operable range input with `aria-valuetext` written on change. It was opened in Chromium through Playwright: nine polygons before and after moving the slider to 30, a working value text, no page errors. Copy it as a starting point for step 4 of `workflow.md`.

## Fitting

1. Project every corner of every part with `s = 1` and `o = 0`.
2. Take the bounding box.
3. Set `s` so the box fills the target share of the card on its tighter side, then centre it.

Recompute on resize only if the viewBox changes. Normally the viewBox is fixed and CSS scales the SVG.

## Turning the camera

Changing the azimuth re-projects stored 3D points and re-sorts. Do it in one place per frame; see `turning-groups.md` for parts that turn, slide or hinge.

Docs for the primitives used: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/polygon and https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Gradients
