# Later: source tooling, assets and fixtures not shipped

Read when a rule elsewhere points here, or when planning what to build next. These items come from the source skill. Under this plugin's rules (stdlib-only Python toolbelt, no network, never run or install third-party scripts or hooks) they are not adopted. Each row says what it did and what stands in now.

## Tooling

| Source tool | Did | Stand-in now | To ship it |
|---|---|---|---|
| lint script (static), partly done | read stylesheets, markup and class strings against about 90 gates | `../design-review-qa/page-lint.md` checks the machine-checkable gates 2a, 2b and 7a and the matching slop tells; the rest stay with `gates.md` by hand or by a reviewer | more gates in `page_lint.py` |
| render lint | drove headless Chrome at 8 widths to catch overflow, wrapping, sticky stacking, contrast | Playwright by hand (`responsive.md`, `imagery.md`) | a Python Playwright script, run by the user |
| theme tool | dealt, scaffolded, checked, drew, validated themes and logged picks | `themes.md` and `themes.csv`, choose and write by hand | a stdlib script filtering the CSV and emitting a token file |
| capture script | started a product and screenshotted its screens | the Playwright snippet in `imagery.md` | a Python capture helper |
| picture script | rendered each theme's reference picture | none | Python plus Playwright |
| image generator script | called an image API for comps and stills | the harness's own image tool (`comp.md`) | network is out of scope for the toolbelt |
| reference checker | verified links in the reference files | `tests/test_craft_hallmark.py` checks local references and https links | already partly done |
| install and hook scripts | wired the skill and a post-edit lint hook into several agents | none; hooks are the user's setting, never added by a skill | n/a |
| agent metadata file | listing for another agent platform | n/a | n/a |

## Assets and fixtures

- **Photo library:** a 755-photo list of public-domain and share-alike Wikimedia Commons files with tones and credit data, used to fill slots. Rules for using photos and crediting them are in `imagery.md`; the list itself is not shipped. To ship: a pinned subset with licence lines, written fresh.
- **Theme bodies and pictures:** 50 full theme files and 50 reference pictures. Header facts are in `themes.csv`; bodies and pictures are not shipped. To ship: write bodies by `themes.md`, render pictures with Playwright.
- **Exemplar pages:** four full-page examples, one per genre, used as the bar in reviews. Not shipped; the review prompts (`review-prompts.md`) stand in.
- **Test fixtures:** sample pages that exercise lint gates (eyebrow pass and fail, Tailwind pass and fail, kept-wiring before and after, waiver). Not shipped; the gate table carries each tell and fix.
- **Unit tests for the Node tools:** not applicable.

## Other surfaces

- Slides, mobile apps and video are not covered by the source's website rules, so nothing is set aside for them here. For video on a website see `../taste/later.md`.
- Per-harness behaviour (Codex, OpenCode, Cursor) is summarised in `flow-branches.md`; platform-specific install steps are not shipped.
