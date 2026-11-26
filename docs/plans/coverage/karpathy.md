# Karpathy guidelines rebuild: skipped

Source: multica-ai/andrej-karpathy-skills at commit 2c60614.

**Not rebuilt.** The repository has no LICENSE file at this commit. Its files are `CLAUDE.md`, `CURSOR.md`, `EXAMPLES.md`, `README.md`, `README.zh.md` and `skills/`; a search for any file named like `licen*` found none. `README.md` has a "License" heading that names MIT, but the coding-skills brief says a repository without a LICENSE file is not used, so nothing was read past the licence check and nothing was written from it.

What would unblock it: the upstream adds a LICENSE file (MIT, Apache-2.0 or BSD); then pin the new commit and rebuild (think before coding, simplicity, surgical changes, checkable goals).

Already covered elsewhere without this source: the simplicity ladder and stop rules in `plugins/ultimatum/skills/work/references/craft/caveman/task-stances.md` (on branch `claude/rebuild-caveman`), surgical fixes in `debugging.md`, checkable goals in `feature-planning.md` and `tdd.md`.

Proposed shared-file edit: in `plugins/ultimatum/data/upstreams.json`, the `karpathy-guidelines` entry says `"licence": "MIT (stated in README)"` and `"decision": "adapt"`; propose `"decision": "skip"` with note "no LICENSE file at 2c60614" until one is added. Both CREDITS.md files list it (row: `2c606141936f`, "MIT (stated in README)"); propose changing the licence cell to "no LICENSE file; not used" until upstream adds one.
