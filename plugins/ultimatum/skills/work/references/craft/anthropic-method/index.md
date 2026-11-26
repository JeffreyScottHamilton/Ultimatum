# Anthropic method craft: skills, evals, MCP servers, web app tests

Read when a skill, an eval run, an MCP server or a local web app test needs more than the base files give: frontmatter rules, a run workspace and grading record, trigger tuning, tool design details, a question-and-answer eval set, or a server-then-test recipe.

Rebuilt from the ideas in anthropics/skills at commit e4bb5d9 (Apache-2.0 per skill folder: skill-creator, mcp-builder, webapp-testing, frontend-design). All wording and code here are ours. The base rules live in `../../skill-author.md`, `../../skill-evaluation.md`, `../../mcp-build.md` and `../../browser-verification.md`; these files only add what those leave out.

- `skill-frontmatter.md`: allowed keys and limits, folder layout for variants, writing style that explains instead of shouting, and updating a skill someone else installed.
- `eval-workspace.md`: one folder per iteration and arm, which baseline to compare against, the grading record, grader, blind comparison and post-hoc analysis roles, and what to read in a benchmark.
- `trigger-tuning.md`: building a trigger query set, a held-out split, repeated runs with a threshold, and a tuning loop that picks by held-out score.
- `mcp-tool-design.md`: coverage versus workflow tools, naming, hint annotations, response formats, size limits, the two error channels, stdout on stdio, SDK lines, and a self-check client.
- `mcp-eval-set.md`: ten read-only questions that prove a server is usable, how to write them, and the file shape.
- `webapp-recipes.md`: choosing an approach by page type, servers started and stopped around a test, look-then-act scripts, and helper scripts treated as black boxes.
- `design-brief-pass.md`: the two-pass design plan reviewed against the brief, and the few design and copy points the website craft files do not already make.

Scripts: `../../../../../data/craft/anthropic-method/` (`skill_lint.py`, `bench_summary.py`, `trigger_split.py`, `mcp_eval_check.py`, `with_ports.py`).

Not rebuilt, with reasons: `later.md`.
