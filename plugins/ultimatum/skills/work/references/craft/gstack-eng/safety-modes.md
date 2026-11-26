# Safety modes: caution prompts and an edit boundary

Read when the user asks for extra care around destructive commands, wants edits kept inside one folder for a while, or is working against shared or production data.

Two modes, usable apart or together. Neither is a security boundary: they catch slips by a careful agent, not an attacker. Real protection is permissions, backups and review.

## 1. Caution mode: classify before running

Before any shell command in this mode, put it in one of three tiers.

| Tier | Meaning | Examples |
|---|---|---|
| deny | stop, say why, offer a safer form | recursive delete aimed at `/`, `~` or `$HOME`; a force push to the default branch |
| ask | state what it destroys and get the user's yes first | recursive delete of anything else, `DROP TABLE`/`DROP DATABASE`, `TRUNCATE`, `git push --force` to a feature branch, `git reset --hard`, `git checkout .` or `git restore .`, `git clean -fd`, `kubectl delete`, `docker rm -f`, `docker system prune`; on Windows `Remove-Item -Recurse -Force`, `rd /s`, `Format-Volume` |
| allow | run as normal | everything else, plus deleting known build output (`node_modules`, `dist`, `build`, `.cache`, `__pycache__`, `coverage`, `.next`, `target`) |

Rules that keep the tiers sound:
- Judge the whole command line. `a && rm -rf x` is as risky as its riskiest part; so is a pipe into `sh`.
- Treat obfuscation as ask: `eval`, `iex`, `-EncodedCommand`, base64 piped to a shell, or a variable you cannot resolve in the target path.
- `--force-with-lease` is never deny; it is ask on a shared branch and allow on your own.
- The deny tier only matches simple, unambiguous commands. Anything cleverer drops to ask, never to allow.
- A project may add its own patterns (a prod database name, a bucket). Added rules can only tighten; they never remove a built-in rule.
- The build-output exception applies only when every target is in that list. `rm -rf dist src` is ask.

When asking: name the command, what it removes or rewrites, whether it can be undone, and a safer form (`git stash` before `reset --hard`, a `--dry-run` first, `SELECT count(*)` before `DELETE`).

## 2. Edit boundary: one folder only

The user names a folder; edits go only there until they lift it.
- Resolve both sides before comparing: expand `~`, make relative paths absolute from the working directory, collapse `..`, follow symlinks.
- Compare with a trailing separator, so a boundary of `/repo/src` does not admit `/repo/src-old`.
- Applies to every file-writing tool (edit, write, notebook edit). If a path cannot be read from the request, refuse the edit rather than guess.
- Shell commands can still write anywhere. Say so when the boundary is set, and keep shell writes inside it by choice.
- Lifting it takes the user's own words. Investigation does not end it; finishing a sub-task does not end it.

## 3. Doing it with a hook (only on request)

Claude Code can enforce either mode with a `PreToolUse` hook that returns a permission decision (`allow`, `ask` or `deny`) as JSON. Installing a hook changes the user's settings, so do it only when they ask (Ultimatum rule 5), and show them the exact settings change first. Hook docs: https://code.claude.com/docs/en/hooks.

`../../../../../data/craft/gstack-eng/command_guard.py` holds the tiers and the path check as plain functions with a `--self-check`. It reads one command or path from its arguments and prints the tier; it never runs the command. A hook would call it on the tool input it receives, which is untrusted text: parse it as JSON, fail closed (ask) on anything it cannot parse.

## 4. Report

When a mode is active, say so at the start of each report, and list every ask-tier command with the user's answer.
