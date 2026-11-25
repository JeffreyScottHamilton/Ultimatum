---
name: budget
description: Show how many tokens this chat uses per turn and what costs the most.
disable-model-invocation: true
---

Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" budget --record` and show its output as-is. If it says HIGH, add one line: run `/ultimatum:work resume` in a fresh chat after `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" handoff write`.
