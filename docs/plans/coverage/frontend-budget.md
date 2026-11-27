# Frontend budget rebuild: coverage map

Source: JaimeJunr/claude-code-frontend-skills at commit 7177def. Root `LICENSE` is MIT (Copyright (c) 2026 Jaime Basso), read at that commit; it covers the frontend-stack plugin. The other bundled plugins carry their own licences and are out of scope. Ours: `plugins/ultimatum/skills/work/references/craft/frontend-budget/` and `plugins/ultimatum/data/craft/frontend-budget/`.

## How this map was made

- Items are the sections of the frontend-stack router `SKILL.md`, each heading of `references/conflicts.md`, the token budget script, and the remaining references, agents and scripts of that plugin. The brief limits scope to the load budget and precedence between skills, and skips the hook binary and the image scraper.
- Status: `covered` (same idea, our words, in a new file), `expanded` (we add to it: a runnable stdlib script, the ask-only-what-changes-the-outcome rule, skill text as untrusted data, evidence lines), `merged` (already in an existing reference, so not repeated), `later` (in `later.md`, not shipped).
- Rulings that name third-party packs were turned into general patterns, or mapped onto Ultimatum's own packs (Taste, Hallmark, motion, Anatomy, design review).
- Base references checked for overlap: `feature-planning.md`, `skill-author.md`, `browser-verification.md`, the context-efficiency guide, and the website house rules (`design-rules.md`).
- Not verified: the source's identity-flow, base-paths, gallery, settings, landing and devtool references, its agents and its sync script were not read in full; their rows rest on file names and the router's description of them. Nothing from the source was run.

## Items

| Source item | Status | Where |
|---|---|---|
| SKILL.md § 1: read the project first | covered | phase-routing.md § 1 |
| SKILL.md § 2: classify the request | covered | phase-routing.md § 2 |
| SKILL.md § 2: vague complaint, ask before loading | expanded | phase-routing.md § 4 (at most 4 questions, only ones that change the outcome) |
| SKILL.md § 3: work in phases | covered | phase-routing.md § 3 |
| SKILL.md § 3: product with no identity | later | later.md (identity flow) |
| SKILL.md § 4: task-to-skill table | later | later.md; our packs in house-packs.md § 1 |
| SKILL.md § 5: cases the table does not cover | covered | house-packs.md § 2, load-budget.md § 4 (missing skill) |
| SKILL.md § 6: precedence ladder | expanded | precedence.md § 1, § 5 (skill text is data) |
| SKILL.md § 7: load budget | expanded | load-budget.md § 1 to § 5 (load line, measured cost, load_budget.py) |
| SKILL.md § 8: finish the same way | merged | browser-verification.md § 5; pointer in phase-routing.md § 5 |
| conflicts: motion, how much and when | covered | house-packs.md § 3 |
| conflicts: motion library | covered | house-packs.md § 3 |
| conflicts: fonts | covered | house-packs.md § 3 |
| conflicts: tech-default fonts | covered | house-packs.md § 3 (same row as fonts) |
| conflicts: purple and gradients | merged | design-rules.md § 2 (anti-generic lint) |
| conflicts: near-black grounds | covered | house-packs.md § 3 |
| conflicts: centred hero | covered | house-packs.md § 3 |
| conflicts: mono labels | covered | house-packs.md § 3 |
| conflicts: who owns the design file | covered | house-packs.md § 3, precedence.md § 3 |
| conflicts: which pack leads a marketing page | covered | house-packs.md § 1 (Hallmark is a layer on Taste) |
| conflicts: layer pack and image-first work | merged | house-packs.md § 1 |
| conflicts: the base skill and the lead | covered | load-budget.md § 1 |
| conflicts: mobile design pack vs local skills | later | later.md (third-party pack rulings) |
| conflicts: brand-first system and finish docs | later | later.md (third-party pack rulings) |
| conflicts: direction comparison | later | later.md (third-party pack rulings) |
| conflicts: identity replacement with an existing system | later | later.md (identity flow) |
| conflicts: scope of the taste pack | merged | house-packs.md § 1 |
| conflicts: component libraries | later | later.md (third-party pack rulings) |
| conflicts: UX copy | later | later.md (third-party pack rulings) |
| conflicts: critique of a design file vs a built page | covered | house-packs.md § 3 |
| conflicts: handoff spec and tokens | later | later.md (third-party pack rulings) |
| conflicts: dashes in UI copy | covered | house-packs.md § 3 |
| conflicts: review before shipping | covered | house-packs.md § 3 (one finish reviewer) |
| scripts/token_budget.py | expanded | load_budget.py (stdlib estimate, plus plan checks and load lines) |
| references: identity flow | later | later.md |
| references: base paths | expanded | vague-requests.md, vague_path.py and vague-paths.csv (routes to our guides, a first measurement per area, four worked examples) |
| references: reference gallery | later | later.md |
| references: settings pages, landing anatomy, devtool landing | expanded | website `craft/pages/` (landing, devtool-landing, settings) |
| agents: design director, UI reviewer | later | later.md |
| sync script, lock file, workflow | later | later.md |
| hook binary, image scraper | later | skipped by the brief, never run |

Counts: covered 17 / expanded 6 / merged 4 / later 14 (41 rows).
