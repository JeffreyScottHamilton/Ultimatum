# anthropic-method craft scripts

Stdlib-only Python helpers for `skills/work/references/craft/anthropic-method/`. None of them runs what it reads, and none needs the network (`with_ports.py` only talks to 127.0.0.1).

| Script | What it does | Exit codes |
|---|---|---|
| `skill_lint.py DIR ...` | checks SKILL.md frontmatter keys, name, description and sizes (see `skill-frontmatter.md` § 1) | 0 clean, 1 errors, 2 bad usage |
| `bench_summary.py ROOT` | pass rate, time and tokens per arm from `grading.json` files; flags assertions that never discriminate or flake | 0 printed, 1 no runs, 2 bad usage |
| `trigger_split.py split FILE` / `score FILE` | stratified held-out split of trigger queries; scores runs against a threshold | 0 ok, 1 misses, 2 bad input |
| `mcp_eval_check.py FILE.xml` | shape check for an MCP question-and-answer set; refuses DOCTYPE and entities | 0 clean, 1 errors, 2 unreadable |
| `mcp_smoke.py --server CMD [--call NAME JSON] [--bad-call NAME JSON]` | stdio MCP client: initialize, list tools, call them, expect a bad call to return a tool error, catch stray stdout | 0 pass, 1 a check failed, 3 no answer, 2 bad usage |
| `with_ports.py --server CMD --port N -- CMD` | starts servers without a shell, waits for their ports, runs one command, stops them | the command's code, 3 not ready, 2 bad usage |

Each takes `--self-check`, which runs built-in examples and asserts the result.
