# Superpowers helpers

Two small scripts used by `skills/work/references/craft/superpowers/debugging-moves.md`. Both are our own code, Python standard library only, with no network access.

| File | What it does | Try it |
|---|---|---|
| `wait_until.py` | polls a condition with a timeout and a description, instead of a fixed sleep | `python3 wait_until.py` runs its self-check |
| `find_polluter.py` | runs test files one at a time and reports the first that creates a given path | `python3 find_polluter.py --artifact .git --glob 'tests/test_*.py' -- python3 -m pytest -q {}` |

`find_polluter.py` never uses a shell: the command is a list and each file name is passed as one argument. It refuses to start when the artifact already exists. Exit codes: 0 culprit found, 1 none found, 2 bad usage or dirty start.
