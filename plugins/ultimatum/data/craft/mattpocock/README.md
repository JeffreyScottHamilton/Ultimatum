# Matt Pocock craft scripts

Stdlib-only Python helpers for `skills/work/references/craft/mattpocock/`. Both read text files only, never run what they scan, and need no network.

| Script | What it does | Exit codes |
|---|---|---|
| `ticket_order.py DIR [--done 01,02]` | reads `NN-<slug>.md` tickets with a `Blocked by:` line, prints a dependency order and the ready set, flags cycles and unknown blockers | 0 sound, 1 problem found, 2 bad usage |
| `entry_imports.py --packages src/packages [--root .]` | flags relative imports that reach into a package's subfolders from outside it, or from its `tests/` | 0 clean, 1 violations, 2 bad usage |

Both take `--self-check`, which builds a temporary example and asserts the expected result.
