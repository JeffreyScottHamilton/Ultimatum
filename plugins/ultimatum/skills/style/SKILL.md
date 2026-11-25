---
name: style
description: Opt-in setup that adds Ultimatum's shared answer style to your normal Claude Code chats (~/.claude/CLAUDE.md), keeping your own instructions.
disable-model-invocation: true
---

1. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" style status` and show the result.
2. Ask once: "Add Ultimatum's shared style (plain answers first, reuse, plan-and-check) to ~/.claude/CLAUDE.md? Your existing text stays as it is." Only on yes, run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" style apply`.
3. To undo at any time: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" style remove`.
Reply in at most 4 lines.
