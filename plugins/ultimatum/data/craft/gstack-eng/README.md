# gstack engineering craft scripts

Stdlib-only Python helpers for `skills/work/references/craft/gstack-eng/`. Neither runs what it reads, and neither needs the network.

| Script | What it does | Exit codes |
|---|---|---|
| `command_guard.py cmd '<command>'` | sorts a shell command into deny, ask or allow (see `safety-modes.md` § 1) | 0 allow, 1 ask or deny, 2 bad usage |
| `command_guard.py path FILE --boundary DIR` | says whether a path resolves inside an edit boundary (symlinks, `..`, `~` resolved) | 0 inside, 1 outside, 2 bad usage |
| `command_guard.py hook [--boundary DIR]` | reads a PreToolUse JSON payload on stdin and prints a decision; fails closed to ask | 0 printed, 2 bad usage |
| `retro_stats.py LOG [--gap 45] [--json]` | summarises `git log --numstat` text: commits, kinds, sessions, hotspots, sizes, focus, streak | 0 printed, 1 no commits, 2 bad usage |

Both take `--self-check`, which runs built-in examples and asserts the expected result. Installing `command_guard.py` as a hook changes the user's settings: only on their request.
