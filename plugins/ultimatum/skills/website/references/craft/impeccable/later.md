# Impeccable: left for later

Read when you want to know which parts of Impeccable were not rebuilt here and what each would take.

These need tooling we do not ship (a native engine, a live browser bridge, hooks or image generation) or are product plumbing rather than design knowledge. None of the source's code was run or copied.

| Item | What it is | What it would take |
|---|---|---|
| Native detector engine (`crates/`) | a Rust rule engine that scans HTML and CSS for slop patterns | partly done: `../design-review-qa/page-lint.md` (stdlib, 18 rules); judged tells stay in `../design-review-qa/slop-tells.md` |
| `live`, `live-setup` | a browser bridge that edits a running page and syncs back to source | an MCP or Playwright bridge; out of scope for a stdlib toolbelt |
| `hooks` | edit-time hooks that run the detector on every write | a hook plus the checker above; project settings change, so the user's yes |
| `doctor` | a health check of the install | only useful with the engine |
| `generate`, asset producer helper | image generation for comps and plates | an image model and its credentials |
| `visualize` plates and provenance | three comps, one approval, the comp becomes the spec | partly covered by `direction-process.md`; plate files need image tooling |
| `component-review` UI | a local review page with bundled fonts (OFL-1.1) | a page of our own; we would not ship their fonts |
| `region-map`, diff reports | per-region comparison of build and comp | screenshot diff tooling |
| Concept seed roll, build phases and state file | a seeded random pick of worlds and a phase tracker | a small state file under `.ultimatum/`; no design value without the rest |
| `document`, `extract`, `init` templates | writing DESIGN.md and PRODUCT.md from a codebase | a template in our own words; partly covered by `direction-process.md` § Three places for truth |
| Manual-edit applier and documenter helpers | helpers that apply hand edits and write the design file | worker briefs of our own |
| Provider folders (cursor, vscode, extension, hermes) | packaging for other editors | not needed for this plugin |
| Command menu and routing | the source's command list and dispatcher | our router is `../../../SKILL.md`; a proposed diff, not an edit |
| `optimize` specifics | speed checklist | already in `../taste/performance.md` and `../emil-motion/performance.md`; marked merged, nothing to add |
