# Anatomy: drawing a figure from its scene, and auditing parts that move

Read when a figure is described as a JSON scene and you want the SVG drawn from it, at any camera or pose, or when parts turn, slide or hinge and you need proof they never pass through each other.

`../../../../../data/craft/anatomy/figure_draw.py` is standard-library Python. It reads the same scene file as `figure_audit.py` (`audit.md`), so the figure is built once, drawn from that data, and checked against that data.

## What it draws

- **Parts.** Boxes by default; `"shape": "cylinder"` makes an upright cylinder filling the part's box in plan. Each part is a convex solid, so it shows only the faces turned toward the camera.
- **Turned parts.** `"shape": "lathe"` with `"profile": [[radius, height], ...]` revolves the profile round the upright centre line of the part's box: a kettle body, a knob, a bottle, a dome. Heights run from the bottom of the box and must not go down; two points at the same height make a step (a shoulder or a lip). Each rise becomes one frustum, which keeps depth order and the move checks exact, and the joins between frusta are not painted, so a smooth profile reads as one surface. The script refuses a profile wider than the box, one that goes down, or a radius of zero.
- **Coils.** A pipe may give `"coil": {"at": [x, y, z], "radius": R, "pitch": P, "turns": N}` instead of points (optional `"start"` in degrees and `"steps"` per turn, default 16): a heater element, a spring, a wound cable. `at` is the centre of the bottom of the helix. The script refuses a pitch that lets the turns touch. The back half of a coil wound round a part is hidden by it and the front half drawn over it, because every segment is ordered on its own.
- **Knurl and ticks.** On a cylinder, `"knurl": 24` draws 24 grip ridges up the side and `"ticks": 12` a ring of 12 marks round the top rim (whole numbers, 6 to 120 ridges, 4 to 120 ticks). They turn with the part, so a dial's ticks follow its turn group, and only the ridges facing the camera are drawn. Each is a `<line data-mark="knurl">` or `data-mark="tick"` inside the part's group.
- **Four tones from one light.** Every face gets a lit, mid or dark fill from its angle to a single light, and every edge the part's edge tone (`craft-rules.md` § Four tones). Set the base with `"color"`; the other three are derived from it. Cylinder sides hide their seams so the band reads as one curved surface.
- **Depth order.** Two parts that overlap on screen are ordered by a plane that separates them: whichever side the camera sits on is drawn last. This is exact for convex solids at any camera angle, which a centre sort is not (`iso-math.md` § Drawing order). Pipes are ordered the same way, one segment at a time.
- **Pipes.** Each pipe is a round-capped stroke as wide as its radius, with an edge stroke behind it.
- **Labels.** A part with `"label"` gets a leader from the centre of its largest visible face to a column on the right. A face that another part sits on is skipped, so a label never points at a lid when it names the box beneath.
- **Access.** The SVG has `role="img"`, a `<title>` and a `<desc>` (the scene's `title` and `description`, or a list of part names). Add the readout and caption in the card (`craft-card.md`).

```bash
python3 figure_draw.py draw examples/turning-scene.json --out fig.svg
python3 figure_draw.py draw examples/turning-scene.json --out back.svg --az 225
python3 figure_draw.py draw examples/turning-scene.json --out open.svg --pose lid-hinge=60
```

Run these from `data/craft/anatomy/` in the installed plugin. `--az` and `--el` set the camera (default 45 and 30, the isometric look; elevation must stay between 5 and 85). `--pose GROUP=VALUE` places a moving group; repeat it for several groups. `--size 640x480` sets the viewBox. Every `<g>` carries `data-part`, `data-pipe` or `data-label`, so a test or a motion script can find each piece.

Exit 0 means the drawing has an exact order. Exit 1 means some parts could not be ordered (they interlock or intersect); the SVG is still written using depth as the fallback, and the parts are named. Split one of them into convex pieces. Exit 2 means bad arguments or a bad scene.

## Moving groups in the scene

```json
"groups": [
  {"name": "lid-hinge", "kind": "hinge", "parts": ["lid"], "axis": [1, 0, 0],
   "pivot": [0, 0, 3], "range": [0, 100]},
  {"name": "dial-turn", "kind": "turn", "parts": ["dial"], "axis": [0, 0, 1],
   "pivot": [7.8, 2.3, 0], "range": [0, 360]}
]
```

- `turn` and `hinge` rotate in degrees about the line through `pivot` along `axis` (right hand rule). The two differ only in intent: a turn spins about its own centre, a hinge swings about an edge.
- `slide` moves in world units along `axis`; it needs no pivot.
- `range` is the travel from low to high. The default pose is the low end.
- Ports on a moving part move with it. A pipe that rides with the group names it in `"group"`. A flexible hose sets `"flex": true`; then only its length is checked.

## Auditing the motion

```bash
python3 figure_draw.py turn examples/turning-scene.json
python3 figure_draw.py turn scene.json --steps 36 --orbit --json
```

Each group is swept through its range in `--steps` even steps (default 24) while the others stay at rest. At each step:

| Check | What it catches |
|---|---|
| `collision` | a moving part passes through a part it is not joined to |
| `crowding` | a moving part comes closer than `min_gap` to a part it is not joined to |
| `order-cycle` | no draw order works at some pose or camera; split a part |
| `tether` | a pipe end leaves its port when the group moves, or a hose stretches |
| `fixed-in-group` | a part marked fixed is listed in a moving group |

`--orbit` also turns the camera through a full circle in the same number of steps, at each elevation listed in the scene's `"camera": {"el": [20, 40]}` (30 when absent), with every group at rest and then at the top of its range. That is the orbit audit `turning-groups.md` asks for, run rather than described.

Each fault is reported once, at the first pose where it shows, so the report says where to look: `collision: lid / post (lid-hinge at 95.8)` means the lid meets the post near the top of its swing. Exit 0 means every count is zero.

The example scene fails on purpose: the lid swings into a post, and a rigid lead is torn off the dial as it turns. Moving the post back, limiting the hinge to 40 degrees and making the lead a hose with slack gives a clean run; the tests do exactly that.

## How the checks decide

Distances use separating axes: the face normals of both solids and the cross products of their edges. For convex solids the largest gap along those axes is zero or less exactly when they touch or intersect, so `collision` has no false alarms or misses at the sampled poses. Above zero it is a lower bound on the true gap, so `crowding` can report a pair slightly early; treat it as a prompt to look.

Sampling sees only the poses it lands on. A thin part moving fast between two samples can pass through another unseen. Raise `--steps` until the counts stop changing, and at least until one step moves no part further than its own thinnest side.

## What it does not do

- Tubes that bend smoothly, knurl or ticks on a turned part, and turned parts on a tilted axis (a hinge group can tilt one, but the scene stores it upright). Draw those by hand with `craft-shading.md` and `parts-recipes.md`. `figure_audit.py` checks a turned or round part by its box, so its clearance and crowding counts near a curve err on the cautious side; `figure_draw.py turn` uses the true shape.
- Leaders that cross other parts. The label column is placed, but whether a leader runs across a part is a judgement; look at it (`verify.md`).
- Animation. The drawer writes one pose. A motion loop re-runs the projection per frame in the page (`motion.md`); the stored scene and `data-part` names make that a small step.
- Canvas or WebGL output (`webgl.md`).

## Order of work

1. Write the scene with true sizes (`workflow.md`).
2. `figure_audit.py scene.json` until the static counts are zero (`audit.md`).
3. `figure_draw.py turn scene.json --orbit` until the motion counts are zero.
4. `figure_draw.py draw` at the camera you will ship, look at it at full size and at phone size, then put it in the card.
