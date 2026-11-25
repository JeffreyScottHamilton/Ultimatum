---
name: sync
description: Optional private sync of Ultimatum lessons and project notes through a private git repo you own.
disable-model-invocation: true
argument-hint: "push|pull [private-repo-url]"
---

Arguments: $ARGUMENTS. The repo URL comes from the arguments or `ULTIMATUM_SYNC_REPO`. If neither is set, ask for the URL of a **private** repository the user owns, and stop.

Never use the public Ultimatum repository or any public repo: before pushing, check visibility (`gh repo view <url> --json visibility` or the GitHub tools) and refuse unless it is private.

- **push:** clone or update the repo into `.ultimatum/sync-repo`, run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" sync export --to .ultimatum/sync-repo`, show `git -C .ultimatum/sync-repo status --short`, and only after the user says yes, commit and push.
- **pull:** clone or update into `.ultimatum/sync-repo`, then `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" sync import --from .ultimatum/sync-repo`.

Nothing is synced automatically. Reply in at most 3 lines.
