# Anatomy: verifying a figure like a critic

Read when a figure is drawn and you need to prove it is right before it ships.

## Capture

Open the page in a real browser (Playwright, Chromium) and take a screenshot at the card's real size, at phone width, and at 4x device scale for close-ups. Then look at every image. A check that was not looked at is not a check.

## Drive it

Script the controls: press each button, move the slider to each end and the middle, use the keyboard only, wait for the settle, and capture each state. Check that the readout matches the model at each state. Also capture with `prefers-reduced-motion: reduce` set.

## Line ends

For every line, seam and tick row, find where it begins and ends. Each end must sit on an edge, on another part, or fade. A DOM probe: collect line endpoints, project them, and flag any that lie inside a face polygon and not on its border (within half a pixel).

## Audit table

Make a table with one row per check and a count of failures. All counts must be zero:

| Check | Fails when |
|---|---|
| clearance | a pipe is nearer than 1.5 radii to a part it should miss |
| terminals | a pipe end is not on a port |
| loose ends | a line ends in open space |
| folds | a bend folds back on itself |
| self overlaps | a part overlaps its own neighbour wrongly |
| crowding | parts are closer than a readable gap |
| stand-ins | a placeholder shape stands where a real part belongs |
| wobble | a part drifts between frames when it should not |
| seats | a part does not rest on what holds it |
| depth order | a nearer part draws behind a farther one |

If you hand-build with no tool, walk the table by eye on 4x close-ups and write down each result.

## Close-ups

Capture 4x crops of every joint, every curved part and every texture edge. Look for steps in shading, lines that overshoot, gaps at joins and texture that stops mid-face.

## Light-theme check

For effects that change (`webgl-light-theme.md`), capture several frames across a cycle and check that line still meets ink and that contrast holds in every frame, not only the first.

## Review checklist

- One idea; the object matches it part for part.
- True numbers in the readout; none invented.
- Tone hierarchy holds at 1x.
- Nothing passes through anything; depth right from the default view.
- Works by keyboard; names, roles and values exposed.
- Reduced motion gives a complete still.
- Phone width: no clipping, readable text.
- Weight is within budget.
- Passes the lint in `../../website/design-rules.md` §2 (no decorative badge, no mock with unreadable detail, no stock gradient glow).

Faults seen most often, with fixes: `verify-faults.md`.
