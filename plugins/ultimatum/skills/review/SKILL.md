---
name: review
description: Shared Review instructions: check code, browser behaviour or security protections as the change needs, and report specific problems with how to see them.
disable-model-invocation: true
---

# Review

Used by Default and Website, or on its own. Check what the change needs, nothing more. Refs: `${CLAUDE_PLUGIN_ROOT}/skills/work/references/`.

- **Code:** read the diff and the code around it (callers, tests); run the tests through `ult run -- <cmd>`; `ult arch check --changed`. Look for unmet requirements, broken callers, empty and edge cases, duplicate helpers.
- **Browser** (sites and UI): follow `browser-verification.md`. Open the real page, run each check in the brief: main actions, 375 px and 1280 px, a keyboard path, console errors, axe-core when available. Read screenshots back.
- **Security:** `security/change-review.md` with `security/coverage-model.md` (OWASP-informed). Name the boundary and the evidence.

Report each problem as: what is wrong, where (`file:line`, or the page plus steps to see it), how sure you are, and a suggested fix. List "checked and passed" apart from "not checked". No style nits unless asked.

As a helper: `ultimatum:reviewer`, briefed with the brief path, the diff base and this file.
