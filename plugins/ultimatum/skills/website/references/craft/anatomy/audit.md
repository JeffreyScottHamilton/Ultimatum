# Anatomy: running the figure audit

Read when a figure is drawn from parts and pipes and you want the audit table in `verify.md` counted by a script instead of by eye.

## Build once, audit the same data

Keep the figure's geometry in one JSON scene. The page draws from it (inline it in a `<script type="application/json">` or import it), and the audit reads the same file, so what is checked is what is drawn. Positions are world units; the camera is the default one in `iso-math.md` (looking from +x, +y and above).

```bash
python3 ../../../../../data/craft/anatomy/figure_audit.py scene.json
```

It prints one count per check and then each fault by name. Exit 0 means every count is zero, 1 means faults, 2 means a bad argument or a scene it cannot read. `--json` gives `{counts, faults}`, `--only clearance,seats` narrows the run, `--checks` lists the checks. Standard library only; it reads the one file and nothing else.

## The scene

| Key | What it holds |
|---|---|
| `parts` | list of `{name, at: [x, y, z], size: [w, d, h]}`; the box runs from `at` to `at + size` |
| part `on` | the part it rests on; its bottom must meet that part's top, and it must sit over it in plan |
| part `ports` | named points pipes connect to, e.g. `{"out": [4, 2.5, 3]}` |
| part `fixed` | true when the part must not move in any frame |
| part `stand_in` | true while a placeholder shape stands in for the real part |
| `joins` | pairs of parts that are meant to touch or interlock; overlap and crowding skip them |
| `min_gap` | the smallest readable gap between parts that do not touch (default 0.5) |
| `pipes` | list of `{name, from: "part.port", to: "part.port", radius, points: [[x, y, z], ...]}` |
| pipe `passes` | parts the pipe is meant to run through (a collar, a wall), skipped by clearance |
| `order` | the draw order, far to near, as part names |
| `frames` | optional list of `{part: [x, y, z]}` positions per animation frame |

Start from `../../../../../data/craft/anatomy/examples/clean-scene.json`; `faulty-scene.json` beside it trips every check once or more.

## What each check means

The check names match the audit table in `verify.md`:

- **clearance:** pipe segments are sampled along their length; any point closer than 1.5 radii to a part other than its two ends (and `passes`) fails.
- **terminals** and **loose-ends:** each pipe end must name a port that exists and sit on it (within the pipe radius).
- **folds:** a turn sharper than 135 degrees between two segments.
- **overlaps** and **crowding:** every pair of parts not in `joins`: sharing volume, or a gap above zero but under `min_gap`.
- **stand-ins:** any part still flagged as a placeholder.
- **wobble:** a `fixed` part whose position in a frame differs from its scene position.
- **seats:** a part whose `on` partner is missing, not under it in plan, or not at its bottom.
- **depth-order:** for each pair whose screen outlines overlap and that are separated on one axis, the nearer one must come later in `order`. Pairs that interlock cannot be ordered this way: split one, or list them in `joins` and check the close-up by eye.

## What it cannot see

Shading, line ends on faces, texture edges, curved parts and anything drawn without a part in the scene. Those stay on the close-up and line-end checks in `verify.md`. A fault is a drawing fault: fix the scene, never raise a limit to pass.
