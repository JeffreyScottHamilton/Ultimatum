---
name: status
description: Show Ultimatum's version, update state, lessons and pending proposals. Use when the user asks which Ultimatum version is installed or whether it is up to date.
---

Run these and summarize in at most 5 lines (no commentary):
1. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" update status`
2. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" learn list --scope project` (count only)
3. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" learn proposals`
4. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" context`
