---
name: coding
description: Shared Coding instructions for the Builder role: reuse first, smallest complete change, run the assigned check. Pairs with one workflow guide.
disable-model-invocation: true
---

# Coding

For a Builder (the Manager or a helper). Inputs: the brief (`.ultimatum/brief.md` when it exists), one guide (`guides/website.md` for sites), the files you own, and the check you must run.

1. **Find what exists:** `ult search`, `ult symbols`, `ult refs`. Reuse or extend the project's components, tokens and helpers before writing new ones. Use an installed library (such as shadcn/ui or Radix) as the project already does; `ult components "<need>"` only when nothing fits.
2. **Smallest complete change.** Match the local style. No unrelated refactors, renames or new dependencies unless the brief asks for them.
3. **Test first** when behaviour is testable. Run the check through `ult run -- <cmd>`. Done means it passes.
4. **Review your `git diff`.** Remove debug code, duplicates and stray edits.
5. **Security overlay:** if the change touches input parsing, auth, secrets, uploads or requests built from input, follow `${CLAUDE_PLUGIN_ROOT}/skills/work/references/security/secure-implementation.md`.
6. **Hand back** at most 10 lines: the files changed, the check with its exit code, and anything open.

A new workflow adds its own guide here (for example data, permissions, loading and error states for apps), not another Coding skill.
