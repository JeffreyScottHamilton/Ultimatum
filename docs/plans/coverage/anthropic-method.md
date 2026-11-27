# Anthropic method rebuild: coverage map

Source: anthropics/skills at commit e4bb5d9. There is no root LICENSE; each in-scope folder (skill-creator, mcp-builder, webapp-testing, frontend-design) has an Apache-2.0 `LICENSE.txt`, read at that commit. Ours: `plugins/ultimatum/skills/work/references/craft/anthropic-method/` and `plugins/ultimatum/data/craft/anthropic-method/`.

## How this map was made

- Items are the main sections of skill-creator (with its agents and reference notes), mcp-builder (with its best-practice and evaluation notes), webapp-testing and frontend-design. Office documents, brand guidelines and canvas fonts are out of scope by the brief.
- Status: `covered` (same idea, our words, in a new file), `expanded` (we add to it: a runnable stdlib script, the untrusted-input rule, the security overlay, the ask-first rule for paid runs), `merged` (already in an existing reference, so not repeated), `later` (in `later.md`, not shipped).
- Base references checked for overlap: `skill-author.md`, `skill-evaluation.md`, `mcp-build.md`, `browser-verification.md`, and the website craft files for design.
- Not verified: the source's external links and SDK snippets were not followed or run; none of the source's scripts were run. Our six scripts are new code, checked by their self-checks and the tests below. The Playwright recipe ran against a local demo page only.

## Items

| Source item | Status | Where |
|---|---|---|
| skill-creator: capture intent and interview | merged | skill-author.md § 1 |
| skill-creator: frontmatter fields and limits | expanded | skill-frontmatter.md § 1 (skill_lint.py) |
| skill-creator: name and description rules | expanded | skill-frontmatter.md § 1 (skill_lint.py) |
| skill-creator: compatibility field | covered | skill-frontmatter.md § 1 |
| skill-creator: progressive disclosure levels | merged | skill-author.md § 4 |
| skill-creator: body under 500 lines | expanded | skill-frontmatter.md § 1 (skill_lint.py warns) |
| skill-creator: references with a contents list past 300 lines | expanded | skill-frontmatter.md § 2 (skill_lint.py) |
| skill-creator: per-variant reference files | covered | skill-frontmatter.md § 2 |
| skill-creator: scripts and assets folders, bundle repeated helpers | covered | skill-frontmatter.md § 2 |
| skill-creator: explain why instead of shouting | expanded | skill-frontmatter.md § 3 (skill_lint.py counts shouty words) |
| skill-creator: updating an existing skill, keep its name | expanded | skill-frontmatter.md § 4 (untrusted-text rule added) |
| skill-creator: capture a skill from the conversation | covered | skill-frontmatter.md § 5 |
| skill-creator: write test prompts first | merged | skill-author.md § 2 |
| skill-creator: with-skill vs without-skill runs | merged | skill-author.md § 6; skill-evaluation.md § 2 |
| skill-creator: iteration workspace layout | covered | eval-workspace.md § 1 |
| skill-creator: baseline choice (no skill vs old snapshot) | covered | eval-workspace.md § 2 |
| skill-creator: grading record shape | expanded | eval-workspace.md § 3 (evidence field required) |
| skill-creator: assertions that discriminate | merged | skill-evaluation.md § 3 |
| skill-creator: grader role | covered | eval-workspace.md § 4 |
| skill-creator: blind comparator role | covered | eval-workspace.md § 4 |
| skill-creator: post-hoc analyst role | covered | eval-workspace.md § 4 |
| skill-creator: benchmark aggregation, mean and spread | expanded | eval-workspace.md § 5 (bench_summary.py) |
| skill-creator: flaky and non-discriminating assertion notes | expanded | eval-workspace.md § 5 (bench_summary.py flags) |
| skill-creator: timing and token capture | expanded | eval-workspace.md § 5 (bench_summary.py) |
| skill-creator: HTML eval viewer | later | later.md |
| skill-creator: iterate on feedback, generalise | merged | skill-author.md § 7 |
| skill-creator: trigger query set, near misses | covered | trigger-tuning.md § 1 |
| skill-creator: train/test split and repeated runs | expanded | trigger-tuning.md § 2 (trigger_split.py) |
| skill-creator: pick by held-out score | expanded | trigger-tuning.md § 3 (trigger_split.py score) |
| skill-creator: model-driven description rewrite loop | later | later.md |
| skill-creator: .skill packaging | later | later.md |
| skill-creator: platform-specific notes | later | later.md |
| mcp-builder: research the API, plan coverage | merged | mcp-build.md § 1 |
| mcp-builder: coverage vs workflow tools | covered | mcp-tool-design.md § 1 |
| mcp-builder: tool naming with service prefix | covered | mcp-tool-design.md § 2 |
| mcp-builder: annotations (read-only, destructive, idempotent, open-world) | expanded | mcp-tool-design.md § 3 (hints are not security) |
| mcp-builder: structured output, response format, pagination, size cap | covered | mcp-tool-design.md § 4 |
| mcp-builder: actionable error messages | expanded | mcp-tool-design.md § 5 (protocol vs tool error table) |
| mcp-builder: input schemas with constraints | merged | mcp-build.md § 3 |
| mcp-builder: stdio vs streamable HTTP | expanded | mcp-tool-design.md § 6 (security overlay: token audience, Origin, loopback, DNS rebinding) |
| mcp-builder: auth and secrets in env | merged | mcp-build.md § 5 |
| mcp-builder: SDK choice and versions | covered | mcp-tool-design.md § 7 |
| mcp-builder: test with an inspector or client | expanded | mcp-tool-design.md § 8 (mcp_smoke.py) |
| mcp-builder: Python and TypeScript server listings | later | later.md |
| mcp-builder: evaluation question properties | covered | mcp-eval-set.md § 1 |
| mcp-builder: how to write eval questions | covered | mcp-eval-set.md § 2 |
| mcp-builder: eval XML file | expanded | mcp-eval-set.md § 3 (mcp_eval_check.py refuses entities) |
| mcp-builder: running the eval | expanded | mcp-eval-set.md § 4 (costs money, ask first) |
| mcp-builder: eval harness script | later | later.md |
| webapp-testing: decision tree static vs dynamic | covered | webapp-recipes.md § 1 |
| webapp-testing: server lifecycle helper | expanded | webapp-recipes.md § 2 (with_ports.py: no shell, port-in-use refusal, group kill) |
| webapp-testing: reconnaissance then action | expanded | webapp-recipes.md § 3 (run example) |
| webapp-testing: wait for network idle | covered | webapp-recipes.md § 3 |
| webapp-testing: selectors and console capture | merged | browser-verification.md § 3, § 6 |
| webapp-testing: example scripts | later | later.md |
| frontend-design: design thinking before code | covered | design-brief-pass.md § 3 |
| frontend-design: ground in purpose and audience | covered | design-brief-pass.md § 2 |
| frontend-design: typography, colour, motion, layout | merged | design-brief-pass.md § 1 (website craft) |
| frontend-design: avoid generic AI look | merged | design-brief-pass.md § 1 (slop-tells) |
| frontend-design: match complexity to the vision | covered | design-brief-pass.md § 4 |
| frontend-design: palette and type advice | later | later.md |
| docx, pdf, pptx, xlsx | later | later.md (out of scope) |
| brand-guidelines, canvas fonts | later | later.md (out of scope) |

Counts: covered 21 / expanded 20 / merged 12 / later 10 (63 rows).
