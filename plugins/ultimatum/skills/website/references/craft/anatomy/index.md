# Anatomy craft: index

Read when a website, app or docs build might need an explanatory isometric figure: one line per file, with the question it answers. Rebuilt in our own words from the MIT-licensed Anatomy skill (Ryan's anatomy repository, commit 1482e84); the house rules in `../../website/design-rules.md` still win on any conflict.

## Reading order

1. `when-and-sizing.md` → `workflow.md` → `craft-rules.md` → `craft-shading.md` → `parts-recipes.md` → `craft-card.md`.
2. Then only what the figure needs: `motion.md`, `webgl.md`, `react.md`, `turning-groups.md`, `draw.md`.
3. Before hand-over: `verify.md` with `audit.md`, `accessibility-and-limits.md`.

## Files

- `when-and-sizing.md`: Does this page need a figure at all, and how big should it be?
- `workflow.md`: In what order is a figure built, from truth to verified?
- `craft-rules.md`: How must solid parts, lines, pipes and depth be drawn?
- `craft-shading.md`: How are curved parts shaded and textures ended?
- `parts-recipes.md`: What goes into a base, rail, dial, spring or pipe run?
- `craft-card.md`: How is a figure framed with label, hint, readout and caption?
- `iso-math.md`: How do I project, fit and order parts, with a runnable sketch?
- `kit-api.md`: What does the source kit do, and what do we use instead?
- `audit.md`: How do I count the audit table with `figure_audit.py` from the figure's JSON scene?
- `draw.md`: How do I draw the SVG from that scene at any camera or pose, and prove moving parts never collide?
- `motion.md`: How does a figure move, stay light, and respect reduced motion?
- `webgl.md`: How does a shader effect sit inside an SVG figure?
- `webgl-light-theme.md`: How is a glow or flame drawn on a light page?
- `turning-groups.md`: How do parts turn, slide or hinge with correct depth?
- `verify.md`: How do I prove a figure is right before it ships?
- `verify-faults.md`: What does each visible fault mean, and what fixes it?
- `print-sheets.md`: How is a figure turned into a printable sheet?
- `publish.md`: How is a figure shared outside the site, and with what consent?
- `react.md`: How does a figure fit a React or Next.js app?
- `walkthrough.md`: What does a complete figure plan look like?
- `accessibility-and-limits.md`: What must a figure do for access, reduced motion and the business?
- `later.md`: Which source tools and modules are set aside, and why?

Data: `../../../../../data/craft/anatomy/` holds `figures.csv` (named techniques) `iso-slabs.html`, a runnable sketch, `figure_audit.py` and `figure_draw.py`, with example scenes in `examples/`.
