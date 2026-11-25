---
name: setup
description: One-time setup so Ultimatum updates itself (local CLI, cloud and running sessions).
disable-model-invocation: true
---

1. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" update status`.
2. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" update setup` and show its steps.
3. If auto-update is off and this is a local CLI session, ask once: "Turn on auto-update for the Ultimatum marketplace in ~/.claude/settings.json?" Only on yes, run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" update setup --apply`, then tell the user to run `/reload-plugins`.
4. Cloud sessions: tell the user to add Ultimatum at claude.ai/customize/plugins; cloud sessions download the latest version at start.
5. Fallback any time: `claude plugin update ultimatum@ultimatum`, then `/reload-plugins`.
Reply in at most 4 lines.
