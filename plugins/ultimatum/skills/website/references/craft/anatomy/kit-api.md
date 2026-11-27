# Anatomy: the source kit and our stand-ins

Read when deciding whether to hand-write a figure or reach for a drawing kit, and what a kit gives you.

## What the upstream kit offers

The Anatomy project ships a Node kit (MIT) of modules. We do not install or run it. What it does, by module, so you can design the same jobs by hand:

| Module | Job |
|---|---|
| iso kit | world to screen, slabs, cylinders, extrusions, knurl rings, coils, tick rows, seams; turns parts into SVG strings and plate HTML |
| lathe | profiles revolved into bands, ribs, rods, saddles and spheres |
| tube | pipes as pieces with gaps, breaks and rings, so a pipe can pass behind or through a collar |
| audit | records every part and pipe, settles depth order, and reports clearance, loose ends, folds, overlaps, crowding, stand-in coverage, wobble and seats |
| canvas painter | the same geometry painted to a canvas for heavy scenes |
| gl and gl shared | WebGL layer registered to the SVG (see `webgl.md`) |
| turn modules | groups of parts that turn, slide or hinge (see `turning-groups.md`) |
| styles | the base CSS for the figure card |
| pdf button | a print button wired to the sheet builder (see `print-sheets.md`) |
| React helpers | a draw wrapper and a live wrapper (see `react.md`) |

## What we ship instead

| Need | Our stand-in |
|---|---|
| projection, boxes, depth sort | `iso-math.md` and the runnable `iso-slabs.html` |
| curved shading | gradient rules in `craft-shading.md` |
| clearance, loose ends, folds, overlaps, crowding, stand-ins, wobble, seats, depth order | `figure_audit.py` over the figure's JSON scene (`audit.md`); line ends and close-ups by eye (`verify.md`) |
| motion loop | the pattern in `motion.md` |

Everything the kit does beyond that is in `later.md` with an honest note on why we did not rebuild it.

## Rules a kit enforces that you must keep by hand

- Build geometry once, then transform.
- Give every part and pipe a name so a failure can say which one.
- Treat an audit or review failure as a drawing fault, not a threshold to raise.
- Keep part counts within the tier (`when-and-sizing.md`).

## Choosing

Hand-write when the figure has under about 40 parts and no pipes or turning parts. Past that, the work of order, clearance and checks grows quickly; say so to the owner and either budget for it or reduce the figure.
