# Anatomy: parts that turn, slide, hinge or move free

Read when a figure's parts must rotate or shift in 3D, or the camera orbits, and the 2D painter's order is no longer enough.

The source labels this area beta. Treat it as a design guide for hand-built work; we do not ship its engine (`later.md`).

## Group kinds

| Kind | Motion |
|---|---|
| turn | spins about a fixed axis (a dial, wheel, drum) |
| slide | moves along an axis (a piston, drawer) |
| hinge | swings about an edge (a lid, flap) |
| free | any transform you set each frame |

A group holds parts that move together. Nested groups are fine; each has one parent.

## Shape rules that keep depth correct

- **Convex parts.** Make each piece convex. A convex piece has a clean depth against every other piece; a concave one can be both behind and in front of a neighbour. Split concave shapes into convex slices.
- **Flush contacts.** Parts that touch share an exact plane. A gap of a sliver shows as a line; an overlap flickers in the sort.
- **Separating planes.** Order two convex pieces by the plane that separates them: whichever side the camera is on decides which draws first. This is exact for convex pairs.

## Bend radius for tubes

A tube that bends needs radius R of at least `2r / sin^2(e - theta)`, where r is the tube radius, e the camera elevation and theta the tube's tilt. Below that the near side folds. Since the bound grows near theta = e, avoid tubes whose tilt matches the camera elevation, or thicken the bend.

## Materials

Describe each group's surface with a base colour and a gloss. The four-tone rule from `craft-rules.md` applies per frame: recompute the tones from the face normal and the light each time the group turns, so a turning dial's faces brighten and darken as they swing round.

## Orbit audit

If the camera can orbit, sample it at many azimuths (a full circle in steps of a few degrees) and at the elevation limits. At each sample check order, clearance and folds. A figure that is right at 45 degrees and wrong at 50 is not finished.

## Budgets

Each group costs re-projection and re-sorting every frame. Count polygons that change, not total. A rough ceiling: under about 600 changing polygons per frame on a mid phone. Measure; do not guess (`../taste/performance.md` §Measure).

## Known limits

- Concave interlocking shapes can need hand-set order.
- Very close camera angles near the pole of the orbit make faces degenerate; clamp elevation.
- Transparency between turning parts is unreliable. Avoid it.
- Large counts need canvas, not SVG (`webgl.md`).
