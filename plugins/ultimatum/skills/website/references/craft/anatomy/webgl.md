# Anatomy: a WebGL layer inside an SVG figure

Read when part of a figure needs light, fluid, glow or heat that SVG shapes cannot give.

## When

Only for effects with a physical source: a flame, caustics, a hot filament, fluid. Not for decoration. Everything else stays SVG.

## The three-layer stack

1. Back SVG: the parts behind the effect.
2. A canvas with the shader, sized to the figure.
3. Front SVG: the parts in front of the effect.

The effect appears to sit inside the object because the back and front layers wrap it.

## The camera contract

The shader must use the same camera as the SVG: same azimuth, elevation and scale. Write the projection once as a shared constant in GLSL and in JS, and give the shader a way to turn a screen pixel into a ray and intersect the floor. If the two disagree by a pixel, the effect floats off its part. Check at 1x and 4x.

## Ray-marching

A distance-field march per pixel is fine for small canvases. Cap the step count, shrink the canvas to the effect's box, and render at reduced resolution on weak devices.

## Rules

- **No pops.** Every parameter eases; nothing appears or vanishes in one frame.
- **No hard cut-offs.** Fade at the canvas edge and at distance.
- **Tonemap and dither.** Map HDR values to display range and add a little noise to prevent banding in gradients.
- **Render only while it matters:** on screen, tab visible, and the effect changing. Otherwise draw once and stop.
- **Fallback.** If WebGL is missing or the context is lost, show a flat SVG stand-in that is still a correct picture. Never an empty box.
- **Reduced motion.** Draw one still frame.

## Budget

Treat a canvas as a heavy item for the page (`../taste/performance.md` §WebGL). Count it against the page's effect cap (`../../website/design-rules.md` §3).

## Colour on the light theme

See `webgl-light-theme.md`: a shader that adds light on a dark ground needs a different method on paper.

Docs: https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API and https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/getContextAttributes
