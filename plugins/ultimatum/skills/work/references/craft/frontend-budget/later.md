# Frontend budget: not rebuilt, and why

Read when you wonder whether something from the frontend-stack plugin was left out on purpose.

| Item | Why not here |
|---|---|
| The task-to-skill routing table for the third-party packs the source bundles | it names packs Ultimatum does not ship; `house-packs.md` maps our own packs instead |
| Conflict rulings that name specific third-party packs | rewritten as general patterns (`house-packs.md` § 3); the pack-by-pack version only fits that bundle |
| Identity flow (naming, reference board, concepts, brand, landing) | out of the brief's scope (load budget and precedence); the website skill's directions and critic cover the route |
| Base paths for each broad complaint | the general rule lives in (`phase-routing.md` § 4); the per-area question lists are out of scope |
| Reference gallery of inspected sites | a dated list of other companies' sites; it ages fast and is out of scope |
| Settings-page flow, landing anatomy, developer-tool landing | now in the website skill: `website/references/craft/pages/` (0.0.42) |
| Design director and UI reviewer agents | Ultimatum has its own agents; changing `agents/*.md` is a shared-file edit |
| Upstream sync script, lock file and its workflow | it downloads from the network; the toolbelt has no network access |
| Token counting with an external tokenizer | needs a third-party package; `load_budget.py` gives a stdlib estimate |
| Hook binary and image scraper | skipped by the brief; never run |
| Hand-off to a companion product stack | names a marketplace outside this plugin |
| Paid or external design services the source routes to | they send the brief off the machine; out of scope, and would need the user's yes |
