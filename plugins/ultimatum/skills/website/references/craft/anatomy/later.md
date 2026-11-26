# Anatomy: set aside for later

Read when someone asks why a source tool or module has no stand-in here, or wants to pick one up.

Nothing below is installed or run. The upstream kit is Node code; our toolbelt is standard-library Python with no network, and the sizes below are far past a cheap rewrite.

## Kit modules

| Module (upstream) | Size | What it does | Our stand-in now | To ship it |
|---|---|---|---|---|
| iso kit (.mjs and .ts) | 35 KB | solids, ticks, coils, SVG output | `iso-math.md`, `iso-slabs.html` | port projection, slab, cylinder, knurl and coil to a small own module, with tests |
| lathe | 48 KB | revolved profiles | gradient rules in `craft-shading.md` | own revolve helper with a ring and band test |
| tube | 14 KB | pipes with gaps and rings | clearance rules in `craft-rules.md` | own tube path builder plus clearance probe |
| audit | 93 KB | records parts, checks clearance, folds, loose ends, depth | table in `verify.md` | own recorder and a few checks, one at a time |
| turn, turn build, turn fixed, turn audit | 140 KB, 66 KB, 147 KB, 57 KB | turning groups and their audit | `turning-groups.md` as a design guide | needs a design of our own; large |
| canvas painter | 28 KB | the same geometry on canvas | none | own canvas path painter |
| gl and gl shared | 9 KB each | WebGL layer registered to the SVG | `webgl.md` rules | own shader layer sample |
| styles (CSS) | small | the figure card | `craft-card.md` | own CSS file on our tokens |
| React draw and live | small | server-safe draw and client loop | `react.md` | own React sample, needs Node |
| pdf button | 1 KB | link to the sheet | `print-sheets.md` print CSS | trivial once a sheet exists |

## Source tooling

| Source tool | Did | Our stand-in now |
|---|---|---|
| capture script | screenshots of a page and its parts | Playwright by hand (`verify.md`) |
| drive script | scripted actions and waits | Playwright by hand |
| line-end check | finds lines that stop mid-face | by eye on close-ups, DOM probe described in `verify.md` |
| fingerprint, inline kit | detect kit changes, inline it into pages | none needed |
| print script and sheet spec | build A4 sheets from a figure | print stylesheet in `print-sheets.md` |
| publish script | send a figure to a community repo | rules and consent steps in `publish.md`; never run |
| session script, chrome port | headless browser plumbing | none |
| turn bench, check, fidelity | performance and fidelity of turning groups | measure by hand |
| about 25 unit test files | test the scripts above | none (tests of source tooling) |

## Examples and assets

Nine built example folders (about 25 MB) of figures: a dial indicator, a desk computer, an arcade cabinet, a push button, a rocket engine, a ripple tank, a spot plate, a test rig and a turning dial. Not copied. Their lessons are in the craft files; the test rig is described in `walkthrough.md`.

## Evals

The source has a small file of example prompts and expectations. Not adopted: it tests the source's own pipeline.
