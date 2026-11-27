# Anatomy rebuild: coverage map

Source: Anatomy at commit 1482e84 (MIT, checked). Ours: `plugins/ultimatum/skills/website/references/craft/anatomy/` and `plugins/ultimatum/data/craft/anatomy/`.

## How this map was made

- The inventory is generated from a walk of the source tree at the pinned commit (`.git` excluded). Example folders and the scripts folder are counted by folder, not read line by line.
- Items for the reference files are their section headings, each assigned to the file that covers it. Rows marked `covered (check)` hold the idea in the named file, but the section pointer may be the nearest rather than the exact one, or the source section was only skimmed.
- Status values: `covered` (same idea, our words), `expanded` (we add rules, for example WCAG 2.2, reduced motion, local-business use, the anti-generic lint), `merged with X` (folded into X), `later` (in `later.md`, not shipped), `not applicable`.
- Overlap with existing files is handled by pointer: motion, accessibility, performance and the lint are cited from `../taste/` and `design-rules.md`, not copied. The merge points: `craft-card.md` with `taste/system.md` and `icons-and-diagrams.md`; `motion.md` with `taste/motion.md`; `accessibility-and-limits.md` with `taste/accessibility.md`; `webgl.md` with `taste/performance.md` §WebGL.
- Item text is our own short summary and passes the same copy check as the craft files.
- Not verified: the 13 external links in the craft files could not be fetched here (the proxy refused the connection). Section 3 to 4 of the source 3D reference (the authoring API) was not read line by line; it is covered through the kit reference.

## Source inventory

173 files. Folders are counted, not listed.

| Folder | Files | Bytes |
|---|---|---|
| `./` | 9 | 91999 |
| `references/` | 10 | 310151 |
| `agents/` | 1 | 120 |
| `kit/` | 16 | 704017 |
| `.github/` | 10 | 162907 |
| `scripts/` | 59 | 329308 |
| `examples/desk-computer/` | 3 | 497810 |
| `examples/ripple-tank/` | 6 | 1071479 |
| `examples/push-button/` | 7 | 2392251 |
| `examples/arcade-cabinet/` | 11 | 7042314 |
| `examples/test-rig/` | 8 | 52594 |
| `examples/spot-plate/` | 8 | 59773 |
| `examples/raptor-engine/` | 9 | 11267452 |
| `examples/dial-indicator/` | 3 | 287950 |
| `examples/turning-dial/` | 8 | 3342857 |
| `tests/` | 4 | 27143 |
| `evals/` | 1 | 8226 |

## Item map

### SKILL.md

| # | Source item | Our file § | Status |
|---|---|---|---|
| SKI1 | The one idea | when-and-sizing.md §What this craft is | covered |
| SKI2 | Workflow | workflow.md §The order | covered |
| SKI3 | Setup | later.md §Source tooling | later (installer and Node setup; never run) |
| SKI4 | Craft rules (short | craft-rules.md §Solids, not wireframes | expanded |
| SKI5 | WebGL inside the | webgl.md §The three-layer stack | covered |
| SKI6 | 3D: figures that | turning-groups.md §Group kinds | covered |
| SKI7 | Printable sheets (A4) | print-sheets.md §Three formats | covered |
| SKI8 | References | index.md §Files | covered |

### references/craft.md

| # | Source item | Our file § | Status |
|---|---|---|---|
| CRA1 | Contents | parts-recipes.md §Parts on a flat body | covered (check) |
| CRA2 | What "crafted" means | craft-rules.md §Solids, not wireframes | covered |
| CRA3 | Anti-patterns | verify-faults.md §When it still looks off | merged with craft-rules.md |
| CRA4 | Parts vocabulary, with | parts-recipes.md §Parts on a flat body | covered (check) |
| CRA5 | Base plate on | parts-recipes.md §Parts on a flat body | covered (check) |
| CRA6 | Ruler strip and | parts-recipes.md §Parts on a flat body | covered (check) |
| CRA7 | Seams, welds and | parts-recipes.md §Parts on a flat body | covered (check) |
| CRA8 | Rod out of | parts-recipes.md §Round and turned parts | covered |
| CRA9 | Rails, end stops | parts-recipes.md §Parts on a flat body | covered (check) |
| CRA10 | Post, collar, clamp | parts-recipes.md §Parts on a flat body | covered (check) |
| CRA11 | Knurled knob with | parts-recipes.md §Round and turned parts | covered |
| CRA12 | Coil spring around | iso-math.md §Drawing order | covered |
| CRA13 | Dial gauge (face | parts-recipes.md §Round and turned parts | covered |
| CRA14 | Drawer with a | parts-recipes.md §Parts on a flat body | covered (check) |
| CRA15 | Turntable with degree | parts-recipes.md §Round and turned parts | covered |
| CRA16 | Perforations, vents and | parts-recipes.md §Parts on a flat body | covered (check) |
| CRA17 | Lamp, probe and | parts-recipes.md §Parts on a flat body | covered (check) |
| CRA18 | Tones | craft-rules.md §Four tones | covered |
| CRA19 | Painter's order | iso-math.md §Drawing order | covered |
| CRA20 | Camera and composition | iso-math.md §Fitting | covered |
| CRA21 | Themes | craft-card.md §Light and dark | covered |
| CRA22 | Round parts and | parts-recipes.md §Round and turned parts | covered |
| CRA23 | Turned parts: think | parts-recipes.md §Think in meridians | covered |
| CRA24 | Parts on a | parts-recipes.md §Think in meridians | covered |
| CRA25 | Pipes | craft-rules.md §Pipes | expanded |
| CRA26 | Choosing waypoints | parts-recipes.md §Pipe runs | covered |
| CRA27 | Contacts and junctions | parts-recipes.md §Pipe runs | covered |
| CRA28 | Clearance and crossings | craft-rules.md §Pipes | covered |
| CRA29 | Shading and textures | craft-shading.md §Curved parts shade smoothly | covered |
| CRA30 | Harness routing | parts-recipes.md §Pipe runs | covered |
| CRA31 | Exploded views | motion.md §Exploded view | covered |
| CRA32 | Screens and things | parts-recipes.md §Screens and things on faces | covered |
| CRA33 | Shaders | webgl.md §When | merged with webgl.md |

### references/kit.md

| # | Source item | Our file § | Status |
|---|---|---|---|
| KIT1 | Contents | kit-api.md §What the upstream kit offers | later (module, see later.md §Kit modules) |
| KIT2 | Types | kit-api.md §What the upstream kit offers | later (typed module) |
| KIT3 | Camera | iso-math.md §Projection | covered |
| KIT4 | Solids | iso-math.md §A box is three polygons | covered |
| KIT5 | Lines on faces | craft-shading.md §Textures end on edges or fade | covered |
| KIT6 | Parts library | parts-recipes.md §Parts on a flat body | covered |
| KIT7 | Moving things | motion.md §One loop | covered |
| KIT8 | SVG strings (framework-free) | iso-math.md §Runnable sketch | covered |
| KIT9 | Card and page | craft-card.md §Parts of the card | covered |
| KIT10 | React components | react.md §Layout for one figure | covered |
| KIT11 | Round parts on | kit-api.md §What the upstream kit offers | later (module, see later.md §Kit modules) |
| KIT12 | Pipes, tubes and | kit-api.md §What the upstream kit offers | later (module, see later.md §Kit modules) |
| KIT13 | The audit (kit/audit.mjs) | audit.md, verify.md §Audit table | expanded (`figure_audit.py`, 0.0.41) |
| KIT14 | The WebGL layer | webgl.md §The camera contract | covered |
| KIT15 | Tools | later.md §Source tooling | later |
| KIT16 | Turning groups (kit/turn.mjs, | turning-groups.md §Group kinds | covered |
| KIT17 | turning(P, { recorder, | kit-api.md §What the upstream kit offers | expanded (`figure_draw.py`, 0.0.51, `draw.md`) |
| KIT18 | TURN (runtime) | kit-api.md §What the upstream kit offers | expanded (`figure_draw.py`, 0.0.51, `draw.md`) |
| KIT19 | Orbit audit (kit/turn-audit.mjs) | turning-groups.md §Orbit audit | expanded (`figure_draw.py turn --orbit`, 0.0.51) |

### references/motion.md

| # | Source item | Our file § | Status |
|---|---|---|---|
| MOT1 | Principles | motion.md §Time | expanded |
| MOT2 | Pointer | motion.md §Controls | covered |
| MOT3 | Keyboard and accessibility | motion.md §Controls | covered |
| MOT4 | Vanilla loop (framework-free) | motion.md §One loop | covered |
| MOT5 | React loop | react.md §Server and client split | covered |
| MOT6 | Shapes that change | motion.md §Weight | covered |
| MOT7 | Envelopes for one-shot | motion.md §Time | covered |
| MOT8 | Critically damped settle | motion.md §Time | covered |
| MOT9 | Exploded views | motion.md §Exploded view | covered |
| MOT10 | Depth re-sorting of | motion.md §Exploded view | covered |
| MOT11 | Turning by hand | turning-groups.md §Group kinds | covered |
| MOT12 | Arming | motion.md §Visibility and arming | covered |
| MOT13 | Taking over from | motion.md §Idle tour | covered |
| MOT14 | Announcing phases | motion.md §Controls | covered |
| MOT15 | CSS motion | motion.md §Weight | covered |

### references/print.md

| # | Source item | Our file § | Status |
|---|---|---|---|
| PRI1 | The three formats | print-sheets.md §Three formats | covered |
| PRI2 | The spec | print-sheets.md §What a sheet spec needs | covered |
| PRI3 | Check it | print-sheets.md §Check | covered |
| PRI4 | A PDF link | print-sheets.md §Do it by hand | covered (check) |
| PRI5 | Longer detailed sheets | print-sheets.md §Three formats | covered |

### references/publish.md

| # | Source item | Our file § | Status |
|---|---|---|---|
| PUB1 | Steps | publish.md §Steps | expanded |
| PUB2 | What the gallery | publish.md §What a shared figure must not contain | covered |

### references/react.md

| # | Source item | Our file § | Status |
|---|---|---|---|
| REA1 | File layout for | react.md §Layout for one figure | covered |
| REA2 | The server/client split | react.md §Server and client split | covered |
| REA3 | The large-page key-warning | react.md §The key-warning trap | covered |
| REA4 | Styles | react.md §Styles | covered |
| REA5 | Readout | react.md §Readout and names | covered |
| REA6 | Hydration | react.md §Server and client split | covered |

### references/verify.md

| # | Source item | Our file § | Status |
|---|---|---|---|
| VER1 | Capture | verify.md §Capture | covered |
| VER2 | Drive | verify.md §Drive it | covered |
| VER3 | Line ends | verify.md §Line ends | covered |
| VER4 | Audit | verify.md §Audit table | covered |
| VER5 | Orbit (3D figures) | turning-groups.md §Orbit audit | covered |
| VER6 | Checklist for 3D | turning-groups.md §Orbit audit | covered (check) |
| VER7 | Close-ups | verify.md §Close-ups | covered |
| VER8 | Light-theme shaders | verify.md §Light-theme check | covered |
| VER9 | The review checklist | verify.md §Review checklist | expanded |
| VER10 | Common faults and | verify-faults.md | expanded |

### references/walkthrough.md

| # | Source item | Our file § | Status |
|---|---|---|---|
| WAL1 | Truth | walkthrough.md §The shape of a plan | covered |
| WAL2 | Object | walkthrough.md §The shape of a plan | covered |
| WAL3 | Parts list (53 | walkthrough.md §The shape of a plan | merged with workflow.md |
| WAL4 | Camera and layout | walkthrough.md §The shape of a plan | covered |
| WAL5 | Geometry (geometry.ts, pose.ts) | walkthrough.md §The shape of a plan | covered |
| WAL6 | Painter's order (live.tsx) | walkthrough.md §The shape of a plan | covered |
| WAL7 | Live behaviour (live.tsx) | walkthrough.md §The shape of a plan | covered |
| WAL8 | Card | craft-card.md §Parts of the card | merged with craft-card.md |

### references/webgl.md

| # | Source item | Our file § | Status |
|---|---|---|---|
| WEB1 | Contents | webgl.md §Rules | covered |
| WEB2 | When a shader | webgl.md §When | covered |
| WEB3 | The layer stack | webgl.md §The three-layer stack | covered |
| WEB4 | Worked case: the | webgl.md §The three-layer stack | covered (check) |
| WEB5 | Worked case: the | webgl.md §The three-layer stack | covered (check) |
| WEB6 | The camera contract | webgl.md §The camera contract | covered |
| WEB7 | Ray-marching in the | webgl.md §Ray-marching | covered |
| WEB8 | Registering shader content | webgl.md §The camera contract | covered |
| WEB9 | API and a | later.md §Kit modules | later (own shader sample not written) |
| WEB10 | Craft rules, each | webgl.md §Rules | covered |
| WEB11 | Nothing pops | webgl.md §Rules | covered |
| WEB12 | No hard spatial | webgl.md §Rules | covered |
| WEB13 | World space, in | webgl.md §Rules | covered |
| WEB14 | Layering and blending | webgl.md §Rules | covered |
| WEB15 | Tonemap and dither | webgl.md §Rules | covered |
| WEB16 | Render only while | webgl.md §Rules | covered |
| WEB17 | Reduced motion | webgl.md §Rules | covered |
| WEB18 | Fallback | webgl.md §Rules | covered |
| WEB19 | Light theme | webgl-light-theme.md §Ink on paper | covered |
| WEB20 | Ink on paper | webgl-light-theme.md §Ink on paper | covered (check) |
| WEB21 | Ink grows with | webgl-light-theme.md §Ink on paper | covered (check) |
| WEB22 | A ground for | webgl-light-theme.md §Ink on paper | covered (check) |
| WEB23 | Recipes by phenomenon | webgl-light-theme.md §Ink on paper | covered (check) |
| WEB24 | The SVG and | webgl-light-theme.md §Ink on paper | covered (check) |
| WEB25 | Where the ink | webgl-light-theme.md §Ink on paper | covered (check) |
| WEB26 | What the reviewers | webgl-light-theme.md §Ink on paper | covered (check) |
| WEB27 | Shaders on a | turning-groups.md §Materials | merged with turning-groups.md |
| WEB28 | Verify | verify.md §Light-theme check | covered |
| WEB29 | Performance | webgl.md §Budget | covered |

### references/3d.md

| # | Source item | Our file § | Status |
|---|---|---|---|
| 3D.1 | Contents | index.md §Files | covered |
| 3D.2 | When a figure | when-and-sizing.md §Do not use it when | covered |
| 3D.3 | The model | turning-groups.md §Group kinds | covered |
| 3D.4 | A minimal page | later.md §Kit modules | later (engine page) |
| 3D.5 | The authoring API | later.md §Kit modules | later (engine API) |
| 3D.6 | Scene | later.md §Kit modules | later |
| 3D.7 | Constructors | later.md §Kit modules | later |
| 3D.8 | Details (in the | later.md §Kit modules | later |
| 3D.9 | Runtime (kit/turn.mjs, inlined | later.md §Kit modules | later |
| 3D.10 | Part kinds and | turning-groups.md §Shape rules that keep depth correct | covered (check) |
| 3D.11 | Materials | turning-groups.md §Materials | covered |
| 3D.12 | Free groups: parts | turning-groups.md §Group kinds | covered |
| 3D.13 | Hinge chains: hands | turning-groups.md §Group kinds | covered |
| 3D.14 | Painter's order and | turning-groups.md §Shape rules that keep depth correct | covered |
| 3D.15 | Shading and fades | turning-groups.md §Shape rules that keep depth correct | covered (check) |
| 3D.16 | Static layers and | turning-groups.md §Shape rules that keep depth correct | covered (check) |
| 3D.17 | Shaders that follow | turning-groups.md §Materials | merged with webgl.md |
| 3D.18 | The orbit audit | turning-groups.md §Orbit audit | covered |
| 3D.19 | Browser checks | verify.md §Capture | covered |
| 3D.20 | Performance | turning-groups.md §Budgets | covered |
| 3D.21 | Known limits | turning-groups.md §Known limits | covered |

### kit/ code (hand-mapped)

| # | Source item | Our file § | Status |
|---|---|---|---|
| K1 | iso-kit.mjs / iso-kit.ts | kit-api.md | later (port) |
| K2 | lathe.mjs | kit-api.md | later |
| K3 | tube.mjs | kit-api.md | later |
| K4 | audit.mjs | audit.md | expanded (own `figure_audit.py` on a JSON scene, 0.0.41) |
| K5 | canvas-painter.mjs | later.md | later |
| K6 | gl.mjs, gl-shared.mjs | webgl.md | later (rules shipped, code not) |
| K7 | turn.mjs | turning-groups.md | later |
| K8 | turn-build.mjs | turning-groups.md | later |
| K9 | turn-fixed.mjs | turning-groups.md | later |
| K10 | turn-audit.mjs | turning-groups.md §Orbit audit | later |
| K11 | iso.css | craft-card.md | later (own CSS on our tokens) |
| K12 | pdf-button.mjs | print-sheets.md | later |
| K13 | react/draw.tsx, react/live.tsx | react.md | later (pattern only) |

### scripts/ (hand-mapped, 59 files)

| # | Source item | Our file § | Status |
|---|---|---|---|
| T1 | capture.mjs, drive.mjs, session.mjs, chrome-port.mjs | verify.md §Capture | merged with verify.md (Playwright by hand) |
| T2 | lines.mjs, line-ends.mjs | verify.md §Line ends | covered (check) |
| T3 | print.mjs, print-sheet.mjs | print-sheets.md | later (print CSS stand-in) |
| T4 | publish.mjs | publish.md | later (never run; rules shipped) |
| T5 | fingerprint.mjs, inline-kit.mjs | later.md §Source tooling | later |
| T6 | turn-bench.mjs, turn-check.mjs, turn-fidelity.mjs | turning-groups.md §Budgets | later |
| T7 | about 45 *.test.mjs files | later.md §Source tooling | later (tests of source tooling) |

### Other (hand-mapped)

| # | Source item | Our file § | Status |
|---|---|---|---|
| O1 | examples/ (9 figure folders) | later.md §Examples and assets | later |
| O2 | evals/evals.json | later.md §Evals | later |
| O3 | README, CONTRIBUTING, CHANGELOG, LICENSE | not a craft source | not applicable (project docs; MIT licence checked) |
| O4 | .github/ workflows | later.md §Source tooling | later (CI for the source) |
| O5 | agents/openai.yaml | not a craft source | not applicable (agent metadata) |
| O6 | tests/fixtures/ (4 PNGs) | later.md §Source tooling | later (fixtures for source tests) |

## Totals

| Status | Rows |
|---|---|
| covered | 104 |
| later | 36 |
| covered (check) | 25 |
| merged | 7 |
| expanded | 8 |
| not applicable | 2 |
| total | 182 |
