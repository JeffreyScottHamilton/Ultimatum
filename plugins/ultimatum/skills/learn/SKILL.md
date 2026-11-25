---
name: learn
description: Review Ultimatum's local observations and lessons, and submit a sanitized improvement proposal as a pull request after approval.
disable-model-invocation: true
argument-hint: "[add <lesson> | propose | submit <id> | prune]"
---

Arguments: $ARGUMENTS
- none: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" learn list` and `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" learn proposals`; summarize in at most 5 lines.
- `add <lesson>`: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" learn add "<lesson>" --scope project`.
- `propose`: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" learn propose`, then show the new proposal's `.md` file verbatim.
- `submit <id>`: show the proposal `.md` verbatim and ask "Open this as a pull request on JeffreyScottHamilton/Ultimatum?". Only on yes: create a branch `learn/<id>` with the proposal added under `proposals/<id>.md` (only that file; no other project data), open a PR whose body is the proposal text plus "Submitted with /ultimatum:learn", then `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" learn proposals --clear <id>`. If GitHub access is missing, give the user the file path and the repo's new-issue URL instead.
- `prune`: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" learn prune`.
Proposals hold only counts, categories and template sentences; if one contains anything else, stop and tell the user.
