---
name: rollback
description: Go back to an earlier Ultimatum version.
disable-model-invocation: true
argument-hint: "[version]"
---

Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" update status`. Then tell the user, in at most 4 lines:
- Earlier versions stay cached for about 14 days under `~/.claude/plugins/cache/ultimatum/ultimatum/<version>`; list the ones present with `ls`.
- To run a cached version for a session: `claude --plugin-dir ~/.claude/plugins/cache/ultimatum/ultimatum/<version>`. For an older one, clone the repo at that version's commit and point `--plugin-dir` at its `plugins/ultimatum`.
- Turn auto-update off first in `/plugin` → Marketplaces, or it will move forward again.
Do not change settings yourself.
