---
name: review
description: Shared Review instructions: check code, browser behaviour or security protections as the change needs, and report specific problems with how to see them.
disable-model-invocation: true
---

# Review

Used by Default, Website and Motion, or alone. Check what the change needs, nothing more. Refs: `${CLAUDE_PLUGIN_ROOT}/skills/work/references/`.

- **Code:** read the diff and the code around it (callers, tests); run the tests through `ult run -- <cmd>`; `ult arch check --changed`. Look for unmet requirements, broken callers, empty and edge cases, duplicate helpers.
- **Browser** (sites and UI): follow `browser-verification.md`. Open the real page, run each check in the brief: main actions, 375 px and 1280 px, a keyboard path, console errors, axe-core when available. Read screenshots back.
- **Security:** `security/change-review.md` with `security/coverage-model.md` (OWASP-informed). Name the boundary and the evidence.
- **Before landing:** two-pass pre-landing review with quoted evidence and fix-first batching: `../work/references/craft/gstack-eng/pre-landing-review.md`.

Report each problem, tagged **Important**, **Nit** or **Pre-existing** (`ship.md` §1): what is wrong, where (`file:line`, page and steps, or timestamp), how sure you are, a fix. List "checked and passed" apart from "not checked".

Report to the Manager (as `ultimatum:reviewer`: in your hand-back), who marks blockers and sends them back; recheck each fix. Open blockers stop delivery (`ult loop` tracks it).
