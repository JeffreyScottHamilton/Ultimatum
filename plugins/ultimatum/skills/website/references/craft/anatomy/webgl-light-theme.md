# Anatomy: shader effects on a light page

Read when a WebGL effect must sit on a white or pale ground, or when a glow looks washed out.

## The problem

Light added to a dark ground is easy: brighter means more. On paper, adding light does nothing visible; the ground is already near white. So the effect must be drawn as ink, and light is shown by how much ink is left.

## Ink on paper

- Compute the effect the usual way, then convert: ink amount grows where light would be strong. A hot spot is the densest ink, or the most saturated colour, not the brightest pixel.
- Use a subtractive blend: multiply the ground by a colour per pixel. Pure white ground times a tint gives the tint.
- Give the ink a tone that matches the figure's edge colour so lines and ink read as one drawing.

## A darker ground for the light

Where an effect needs to glow (a lamp, a flame), put a darker local ground behind it: a recessed panel or a shaded chamber that is part of the object. The glow then lives against that ground, and the page stays light.

## Recipes by phenomenon

| Phenomenon | Light-theme treatment |
|---|---|
| Flame or heat | saturated warm ink, densest in the core, fades to nothing at the rim |
| Water or caustics | thin cool ink lines and a faint fill, no white highlights |
| Glow from a lamp | a dark pocket around the lamp, warm ink falling off with distance |
| Smoke or steam | pale grey ink, low opacity, soft edges |
| Electric arc | a thin dark core line with a coloured halo of ink |

## Line meets ink

Where a drawn edge line crosses an ink area, keep the line on top and at full strength, or the part loses its shape. Check each frame of a changing effect, not only the first (`verify.md` §Light-theme check).

## Contrast

Ink that carries meaning must reach 3:1 against the paper. Decorative wisps may be fainter, but nothing needed to read the figure may rely on them.
