# Claude Code platform and packaging (verified against Claude Code 2.1.321)

Method: local CLI help and real runs in a scratch plugin (`/tmp/claude-0/-home-user-Ultimatum/c051b7f5-1efa-5745-8c75-fc5201ebb861/scratchpad/plat/`, NOT in repo), plus official docs fetched 2026-11-10. Docs moved: plugin docs now live under `https://code.claude.com/docs/en/plugins-reference` (manifest reference), `/plugin-marketplaces` (create-marketplace), `/plugins/marketplace-reference.md`, `/plugin-evals.md`, `/skills`, `/sub-agents`. Paid calls made: two `claude -p` haiku runs (~$0.005 total). No eval was run.

Legend: [CLI] = observed locally; [DOC url] = quoted from docs; [UPSTREAM path] = real example.

## 1. plugin.json and marketplace.json schemas

### plugin.json (at `<plugin>/.claude-plugin/plugin.json`)
[DOC /plugins-reference] "`name` is the only required key." Manifest itself is optional (name then comes from dir/marketplace). Other files go at plugin root, never inside `.claude-plugin/`.

| Field | Type / rule |
|---|---|
| `$schema` | string, ignored |
| `name` | required, kebab-case, no spaces/`@`/`:`/path separators. Reserved: starts with `claude-`, `anthropic-`, `anthropics-`, `cc-plugin-`; or is `claude`, `anthropic`, `claude-code`... => validate ERROR. Contains `claude`/`anthropic` as whole word => warning. `ultimatum` is fine. |
| `displayName` | UI label |
| `version` | string, not checked as semver. "Setting it keeps users on that version until you change it" (no update without bump) |
| `description`, `license` (SPDX), `keywords[]`, `repository` (not validated) | strings |
| `author` | object: `name` required, `email`, `url` optional |
| `homepage` | must parse as URL "or the plugin fails to load" |
| `metadata` | free-form object, not read |
| `icon`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl`, `termsOfServiceUrl` | directory-listing only |
| `defaultEnabled`, `dependencies[]`, `settings` (only `agent`, `subagentStatusLine`), `userConfig`, `channels` | as named |
| `skills` | path or array of dirs; ADDS to default `skills/`. `"./"`/`"."` = plugin root |
| `commands` | path / array / object map; REPLACES default `commands/` |
| `agents` | `.md` file path(s) only (directories not accepted); REPLACES default `agents/` |
| `hooks` | path / inline object / array; merged with `hooks/hooks.json`. File form needs top-level `"hooks"` wrapper |
| `mcpServers`, `lspServers` | path/inline/array, merged with `.mcp.json` / `.lsp.json` |
| `outputStyles`, `workflows`, `experimental.{themes,monitors,evals}` | see doc; `experimental.evals` = alternate eval dir |

Rules: component paths must start with `./`, exist, and stay inside plugin root (`..` is an error). Unknown top-level key => stripped, `validate` warning (so `--strict` fails). Unknown key inside `userConfig`/`channels`/`lspServers`/`monitors` => load error.

Default layout (no manifest key needed): `skills/<n>/SKILL.md`, `commands/`, `agents/*.md`, `hooks/hooks.json`, `.mcp.json`, `bin/` (put on Bash PATH while plugin enabled), `settings.json`. A `CLAUDE.md` at plugin root is NOT loaded (validate warns) - put instructions in a skill.

Real examples: [UPSTREAM obra__superpowers/.claude-plugin/plugin.json] = name, description, version, author{name,email}, homepage, repository, license, keywords, no component paths (defaults). Template for us.

### marketplace.json (at `<root>/.claude-plugin/marketplace.json`)
[DOC /plugins/marketplace-reference.md] Required: `name`, `owner` (`{name, email?, url?}`), `plugins[]`. Optional: `$schema`, `description`, `version`, `metadata.{description,version,pluginRoot}`, `forceRemoveDeletedPlugins`, `allowCrossMarketplaceDependenciesOn`, `renames`. Marketplace `name`: letters/digits/`.`/`_`/`-`; reserved list includes `claude-plugins-official`, `anthropic-*`, `inline`, `builtin`, `skills-dir`, `synced`, `npm`, `github`, `claudeai-*` prefix. Unknown keys => warning only.

Plugin entry: `name` + `source` required; also `description`, `version` (plugin.json wins + validate warns on mismatch), `category`, `tags[]`, `strict` (default true), `author` etc. (any plugin.json field except directory-listing ones), `defaultEnabled`, `dependencies`, `displayName`, `metadata`, `relevance`.

`source` forms: [DOC]
- relative string, must start `./` (or `"."` for root; bare name only with `metadata.pluginRoot`, e.g. `"pluginRoot":"./plugins"` + `"source":"formatter"`); no `..`; forward slashes.
- `{ "source":"github","repo":"o/r","ref":"..","sha":"<40hex>" }`
- `{ "source":"url","url":"https://...git","ref","sha" }`
- `{ "source":"git-subdir","url":"o/r|url","path":"sub","ref","sha" }`
- `{ "source":"npm","package","version","registry" }`, `{ "source":"archive","url","sha256" }`, `{ "source":"command","command","timeout","mode" }`

Entry name must equal plugin.json `name` ("Keep the two names the same"), else `Plugin "<x>" not found in marketplace`.

Real examples: superpowers marketplace = `"source": "./"` single plugin at repo root with `version`+`author` on the entry. anthropics__skills = `"source":"./","strict":false,"skills":["./skills/xlsx",...]` (entry defines components, no plugin.json). trailofbits = `"source":"./plugins/<name>"` per plugin, `metadata.{version,description}`.

[CLI] Verified scratch marketplace passes `claude plugin validate mk --strict` with: name, description, owner{name,email}, metadata{description,version,pluginRoot}, plugins[{name, source:"./plugins/ult", description, version, category, tags}] -> `√ Validation passed`.

Implication for Ultimatum: single-plugin repo can use `source: "./"` (repo root = plugin root, like superpowers) or `./plugins/ultimatum`. Root form risks the "plugin at marketplace root" submodule/whole-repo note and ships research/, evals results etc. into the plugin cache; prefer `./plugins/ultimatum` so research/ and dev tooling stay out of the installed copy (verify: cache copy contains whole plugin dir only).

## 2. Skill invocation, arguments, frontmatter, commands/

- Namespacing [DOC /skills]: "`my-plugin/skills/review/SKILL.md` -> `/my-plugin:review`". [CLI] confirmed: init showed `skills: ['ult:work']`, and `claude -p "/ult:work alpha beta"` ran. So Ultimatum: plugin `ultimatum`, dir `skills/work/` => `/ultimatum:work <task>`. The frontmatter `name` overrides the dir name part. Plugin and local skills never collide.
- Substitution [DOC + CLI verified]: `$ARGUMENTS` (all args), `$ARGUMENTS[N]`, `$N` (`$0` first, shell-quoted: `"hello world"` is one arg), `$name` via `arguments:` frontmatter. If SKILL.md contains no placeholder, args are appended as `ARGUMENTS: <value>`. [CLI] `Task: $ARGUMENTS` rendered `Task: alpha beta`; `$0` rendered `alpha`.
- `argument-hint` is autocomplete display only, e.g. `"<task>"`; it does not parse anything.
- Frontmatter [DOC /skills], all optional (description recommended): `name`, `description`, `when_to_use` (appended; combined description+when_to_use truncated at 1,536 chars in listing - key use case first), `argument-hint`, `arguments`, `disable-model-invocation` (true = only manual `/name`), `user-invocable` (false = hidden from `/` menu, Claude-only), `allowed-tools` (space/comma string or YAML list; grants no-prompt use for that turn; does NOT restrict), `disallowed-tools`, `model`, `effort` (low..max), `context: fork` + `agent` + `background`, `hooks`, `paths` (globs), `shell`, `metadata`/`license`/`compatibility` (accepted, not acted on). Skill body should be < 500 lines.
- `context: fork` runs skill text as the prompt of a fresh subagent (no conversation history; default type general-purpose; background by default unless `background: false`). Only for self-contained instructions; this loses the user's conversation, so the router skill for Ultimatum should NOT fork.
- commands/ not needed [DOC /skills]: "Custom commands have been merged into skills... Prefer a skill for new work." [DOC plugins-reference] `commands/` "Prefer `skills/` for new plugins". A `commands/` file would be a second `/ultimatum:x` entry; skip. Aliases: plugin manifest `commands` object map can add inline named commands (`"about"` -> `/plugin:about`) without files.
- `claude plugin init` scaffold [CLI]: writes to `~/.claude/skills/<name>/` (i.e. `$CLAUDE_CONFIG_DIR/skills/<name>/`), NOT cwd; manifest has `"skills": ["./"]`, root `SKILL.md` plus `skills/example/SKILL.md` and `agents/example.md`. Not a layout to copy; hand-write ours.

## 3. Progressive disclosure and variable expansion

- Loading [DOC /skills]: "Description always in context, full skill loads when invoked"; "a skill's body loads only when it's used"; supporting files are loaded only when Claude reads them (Read tool). Once invoked, rendered SKILL.md "enters the conversation as a single message and stays there"; after compaction re-attached skills share 25,000 tokens, first 5,000 per skill. So: keep SKILL.md router small (every token persists for the session and survives compaction); put references behind explicit "read X when Y".
- [CLI `claude plugin details`] gives projected cost: scratch plugin with 1 skill + 1 agent: `Always-on ~42 tok`; `work ~30 always-on / ~140 on-invoke`; agent `<20`. Use this as a budget gate in our tests (always-on per skill/agent is name+description only).
- Variable expansion [DOC plugins-reference "Where each variable resolves"]: "Skill, command, and agent content - Anywhere in the Markdown body" resolves `${CLAUDE_PLUGIN_ROOT}`/`${CLAUDE_PLUGIN_DATA}`/`${CLAUDE_PROJECT_DIR}`. "The variables aren't present in the environment of commands Claude runs through the Bash tool" - so `$CLAUDE_PLUGIN_ROOT` in a shell command typed by Claude will be EMPTY; only the pre-substituted text works. Hooks/MCP/LSP additionally get them as env vars.
- [DOC /skills] `${CLAUDE_SKILL_DIR}` = skill's own subdirectory ("For plugin skills, this is the skill's subdirectory within the plugin, not the plugin root"); `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_DATA}` "Substituted only in plugin skills"; also `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_PROJECT_DIR}`.
- [CLI verified, `claude -p`, installed marketplace plugin] SKILL.md body `Skill dir: ${CLAUDE_SKILL_DIR}` -> `<plugin>/skills/work`; `Plugin root: ${CLAUDE_PLUGIN_ROOT}` -> `<plugin>`; `Data: ${CLAUDE_PLUGIN_DATA}` -> `$CLAUDE_CONFIG_DIR/plugins/data/ult-ult-mk`. Same under `--plugin-dir`. For a local-path marketplace, the root is the source dir in place (not a cache copy) - `claude plugin list` shows `Read from: <source>`.
- Practical rule for SKILL.md: write commands as `python3 "${CLAUDE_SKILL_DIR}/scripts/x.py" ...` or `"${CLAUDE_PLUGIN_ROOT}/scripts/x.py"`; write Read targets as `${CLAUDE_SKILL_DIR}/references/y.md`. Absolute paths get baked into the transcript at load time, which is what Claude then executes. Quote paths (spaces). `allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/*)` form is documented (`Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)`). Not verified: whether substitution applies inside `allowed-tools` frontmatter in a plugin (docs example suggests yes). Test before relying on it.
- Referenced files (references/*.md, scripts/) must live under the plugin dir so they are copied into the cache on install; path outside plugin root is not shipped.

## 4. Plugin subagents

[DOC /sub-agents] Required: `name`, `description`. Fields (camelCase exact, unknown ignored silently): `tools` (inherits all if omitted; comma string or YAML list - [CLI scaffold uses a YAML list]), `disallowedTools`, `model` (`sonnet`, `opus`, `haiku`, `fable`, full model ID, or `inherit`), `maxTurns`, `effort`, `skills` (preload), `memory`, `background`, `omitClaudeMd`, `isolation: worktree`, `color`, `permissionMode`, `mcpServers`, `hooks`, `initialPrompt`, `autoCompactWindow`, `experimental.cacheTtl`.
- Plugin restriction: "plugin subagents don't support the `hooks`, `mcpServers`, or `permissionMode` frontmatter fields. These fields are ignored".
- Names cannot contain `:`. Namespacing: [CLI verified] stream-json init listed `agents: [..., 'ult:scout']` for `agents/scout.md`. Subfolder becomes part of id: `agents/review/security.md` -> `my-plugin:review:security`. Dispatch by `ultimatum:scout`. `claude --agent ultimatum:scout` works for main-thread use.
- Limits: nesting default up to 3 layers below main (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, 1 = off); 20 concurrent (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`); `Agent(x,y)` type allowlist only honoured for `--agent` main thread. Subagent result returns as one message to caller (context isolation = the token-saving mechanism for scouts).
- `claude plugin details` counts each agent at `<20` always-on tokens, so cheap to ship several.
- In evals, baseline arm cannot dispatch plugin agents (`Agent type 'x:y' not found` expected) [DOC plugin-evals].

## 5. `claude plugin validate` and `claude plugin eval` formats

### validate [CLI]
- Flags: `--json`, `--strict` (warnings => exit 1), `--profile directory` (also exit 1 on Anthropic-directory submission blockers: README missing, etc.). Accepts a plugin dir, a marketplace dir/file, or a dir of skills/agents/commands.
- Observed on scratch plugin and marketplace:
```
$ claude plugin validate mk --strict
Validating marketplace manifest: .../mk/.claude-plugin/marketplace.json
√ Validation passed                                  (rc=0)
$ claude plugin validate mk/plugins/ult --strict     -> √ Validation passed (rc=0), also prints advisory "Plugin directory checks" block
$ ... --profile directory  -> × README.md: README missing (README_MISSING)
   ‼ ICON_MISSING ... "Validation failed (--profile directory ...)" (rc=1)
```
`--json` shape: `{success, strict, target, manifest:{file,type,errors[],warnings[],notes[],gatingHooks[]}, contents[], advice[], directory:{profile, findings[{code,title,severity,blocking,...}]}}`. Use `claude plugin validate . --strict --json` in CI. Add README.md (>= 40 words) to plugin folder to satisfy directory profile; icon is a warning only (square PNG 512-2048px).

### eval [CLI help + DOC https://code.claude.com/docs/en/plugin-evals.md]
- Subcommand: `claude plugin eval init [name] [--bare] [--eval-dir d] [-i]`. There is no `schema` subcommand. `init` default is an interactive interview (spends tokens); `init --bare <name>` is free. [CLI] `--bare smoke` produced:
```
evals/smoke/prompt.md
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---
TODO: describe what the agent should do

evals/smoke/graders/criteria.md
---
type: llm
weight: 1
---
TODO: describe what a successful response looks like
```
- Layout [DOC]: `<evalDir>/<case>/prompt.md` (frontmatter = case fields, body = prompt), `<case>/graders/<name>.md` (frontmatter type+options, body = rubric for llm), optional `case.yaml`, `<evalDir>/mocks/<server>/<tool>.md`, `<evalDir>/results/<ts>/{aggregate-result.json,report.html}` (gitignore results/). A case without >= 1 grader fails to load ("invalid case.yaml ... graders"). Default eval dir `evals/`; override `experimental.evals` in plugin.json or `--eval-dir` (relative, no `..`).
- prompt.md frontmatter (unknown key = error): `schema_version` ("1.1", auto), `name` (default dir name), `description`, `tags[]`, `plugins` (set `["../.."]` if plugin not auto-detected), `runs` (default 3, 1-50), `expected_outcome`, `model`, `max_turns` (default 10, <=200), `timeout_seconds` (default 300, <=3600), `allowed_tools` (read-only set: Read Glob Grep NotebookRead Skill AskUserQuestion Agent TodoWrite Task*; Bash/Write/Edit/WebFetch need `--allow-tools`), `append_system_prompt`, `env` (keys must match `EVAL_[A-Z0-9_]*`).
- case.yaml (alternative/companion): requires `schema_version: "1.1"` and `name`; top-level `description, tags, plugins, runs, expected_outcome`; under `execution:` `model, max_turns, timeout_seconds, allowed_tools, append_system_prompt, env, prompt`; plus `context.scaffold_script` (bash, runs only with `--scaffold`, 120s, empty workspace, for fixture files/git), `context.history_file` (.jsonl to resume), `context.add_dirs`; `graders:` list (each item has `name` + same keys as grader frontmatter; llm rubric goes in `criteria`). prompt.md frontmatter overrides case.yaml fields. Example from docs:
```yaml
schema_version: "1.1"
name: changelog-from-diff
tags: [smoke]
context:
  scaffold_script: fixture.sh
  add_dirs: [resources]
```
- Graders (frontmatter `type`, `weight` default 1, `arm: with-only|both`): `regex` (`pattern`, `flags` (no inline `(?i)`), `match: not_contains | "count:N"`, `target`), `tool_used` (`tool`, `input_match` regex over JSON-encoded input, `min` default 1, `max`; min:0,max:0 = never used), `tool_order` (`before`,`after`), `file_exists` (`path` glob, `exists`; only files created in run), `llm` (`criteria`/body, `focus`; 2-of-3 judge votes, default judge haiku), `baseline` (`baseline_file` .jsonl). `target`/`focus`: `last_message` (default), `trace`, `files` (paths only), `{source: file, path: <p>}` (contents), `mock_calls`. "There are no custom-code graders." Free (no model call): regex, tool_used, tool_order, file_exists. Paid: llm, baseline.
- Skill-fired grader (doc): `type: tool_used`, `tool: Skill`, `input_match: '"skill"\s*:\s*"(?:[\w-]+:)?work"'`. Under default with-without ablation, `tool_used: Skill` graders are indicators only (not scored). Use `--ablation none` for deterministic iteration.
- Isolation [DOC]: run starts in empty workspace; no user settings/hooks/CLAUDE.md/other plugins/skills; only plugin under test loaded. Therefore evals cannot test "with upstream packs installed" - good for our no-upstream core guarantee. Scoring: runs per arm default 3; case passes when mean score >= `--threshold` (default 1.0). Cost ~ cases x runs x 2 arms.
- Key flags: `--runs`, `--case <glob>`, `--tag`, `-j 1-8`, `--model`, `--judge-model`, `--ablation none|with-without`, `--threshold`, `--max-cost-usd`, `--allow-tools "Bash(python3 *)"`, `--scaffold`, `--trust-plugin` (CI; else first-run trust prompt), `--json [path.json]` (put target BEFORE `--json`), `--no-publish`, `--report`, `--output-dir`, `--keep-temp`. Exit: 0 pass, 1 below threshold / load error / API-error runs, 2 cost ceiling hit with partial results.
- Cheap local pattern for us: `claude plugin eval plugins/ultimatum --trust-plugin --ablation none --runs 1 --max-cost-usd 1 --model haiku --no-publish --json out.json`. NOT run here.

## 6. Clean-install test procedure [CLI verified end to end]

`CLAUDE_CONFIG_DIR` is honoured by plugin commands and by `claude -p`: with `CLAUDE_CONFIG_DIR=$PWD/cfg3`, state went to `cfg3/{settings.json,plugins/installed_plugins.json,plugins/known_marketplaces.json,plugins/cache,plugins/marketplaces,plugins/data}`; `plugin init` wrote to `cfg/skills/<name>`. Auth still worked inside the isolated dir in this sandbox (credentials via env). Setting `HOME` to a scratch dir as well keeps `~/.claude` untouched.

```bash
export CLAUDE_CONFIG_DIR="$(mktemp -d)"            # isolated; also: export HOME to a scratch dir
claude plugin validate ./plugins/ultimatum --strict
claude plugin validate .   --strict                  # marketplace root (reads .claude-plugin/marketplace.json)
claude plugin marketplace add ./                     # -> "Successfully added marketplace: <name> (declared in user settings)"
claude plugin install ultimatum@<marketplace-name>   # -> "Successfully installed plugin: ultimatum@<mk> (scope: user)"
claude plugin list                                   # Version, "Read from:", Status: enabled
claude plugin details ultimatum                      # Component inventory + projected token cost
claude -p "/ultimatum:work <task>" --output-format json
claude plugin uninstall ultimatum@<mk>               # -> "Successfully uninstalled plugin"
claude plugin marketplace remove <mk>                # also uninstalls its plugins
```
Notes: `--scope user|project|local` on add/install (default user); `--json` on add/install gives one machine-readable last line; `-y` required if stdin/stdout not TTY and the marketplace declares a command source (not our case). Install id is `<entry name>@<marketplace name>`. A local-path (directory) marketplace is read IN PLACE ("Read from: <source dir>"), edits apply at next session or `/reload-plugins`; a git-hosted marketplace is copied to `plugins/cache` and re-fetched only when `version` changes (since `version` pins). This means a local-path test does not prove the packaged tree is self-sufficient. To test packaging faithfully: `git clone`/`cp -r` only the plugin dir (or `git archive`) to a temp dir and add THAT, or add by `file://` git URL after committing. Listing installed skills: `claude plugin details <name>` (component inventory + token cost); session-level list: the `system/init` event of `--output-format stream-json --verbose` has `skills`, `agents`, `plugins`, `slash_commands` arrays (saw `ult:work`, `ult:scout`); in a REPL, `/skills` and `/agents`.

## 7. Non-interactive use and usage fields

`claude --help` [CLI]: `-p/--print`, `--plugin-dir <path>` (directory or .zip; repeatable), `--output-format text|json|stream-json`, `--max-turns`, `--max-budget-usd` (print only), `--allowedTools`, `--disallowedTools`, `--permission-mode`, `--setting-sources`, `--bare` (minimal: skips hooks etc.; read `claude --help` for auth caveats), `--model`.

[CLI verified] Both work and expand the skill:
- Installed: `claude -p "/ult:work alpha beta" --model haiku --output-format json --max-turns 3 --max-budget-usd 0.3` -> result text contained substituted values.
- Dev: `claude -p "/ult:work x y" --plugin-dir mk/plugins/ult ...` -> plugin source shows `ult@inline`; skill present as `ult:work`. Slash command works in `-p` mode because skills are listed under `slash_commands`.

`--output-format json` result keys observed: `type:"result"`, `subtype:"success"`, `is_error`, `api_error_status`, `result` (final text), `session_id`, `uuid`, `stop_reason`, `terminal_reason`, `num_turns`, `duration_ms`, `duration_api_ms`, `ttft_ms`, `total_cost_usd`, `permission_denials[]`, `safety_stops`, `subagent_stats` (`spawned, requested, max_depth, completed, failed, by_type{}`), `modelUsage{<model>:{inputTokens, outputTokens, cacheReadInputTokens, cacheCreationInputTokens, webSearchRequests, costUSD, contextWindow, maxOutputTokens, thinkingTokens, ...}}`, and `usage{input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens, cache_creation{ephemeral_1h_input_tokens, ephemeral_5m_input_tokens}, output_tokens_details{thinking_tokens}, server_tool_use{web_search_requests, web_fetch_requests}, service_tier, iterations[...]}`. Example: `num_turns 1, total_cost_usd 0.0026, input_tokens 2, cache_creation 10665, cache_read 26220, output 441`. Note ~37k tokens of base context even for a trivial prompt (system prompt + built-in/other skills in this environment), so measure Ultimatum overhead as a DELTA against a baseline run (same prompt without `--plugin-dir`), not as absolute. For `stream-json` add `--verbose`; per-message usage and the `init` event are available there. `permission_denials` and `subagent_stats.by_type` are useful assertions (e.g. scout was spawned: `by_type` contains `ultimatum:scout`).

Caveats: `-p` run needs `--allowedTools`/`--permission-mode` for Bash/Write or the tool is denied (recorded in `permission_denials`). Keep model pinned (`--model`) for comparability; prompt cache makes cost vary between first and repeat runs.

## Recommended layout

```
Ultimatum/                                   # repo (marketplace root)
  .claude-plugin/marketplace.json            # name "ultimatum-dev"? (avoid reserved/impersonating names); plugins[0]: name "ultimatum", source "./plugins/ultimatum", version, description, category, tags
  research/ docs/ tools/ ...                 # NOT shipped: outside the plugin dir
  plugins/ultimatum/                         # plugin root = what gets installed
    .claude-plugin/plugin.json               # name, version, description, author{name}, homepage, repository, license, keywords (no component paths: defaults suffice)
    README.md                                # >= 40 words (satisfies --profile directory)
    LICENSE, NOTICE                          # upstream credits / recorded license decisions
    skills/work/
      SKILL.md                               # name: work; description (+when_to_use) <1.5k chars; argument-hint: "<task>"; body = compact router, < ~150 lines; uses $ARGUMENTS
      references/*.md                        # loaded on demand: "Read ${CLAUDE_SKILL_DIR}/references/x.md when <condition>"
      scripts/*.py                           # stdlib-only; invoked as python3 "${CLAUDE_SKILL_DIR}/scripts/x.py"
    agents/scout.md, ...                     # -> ultimatum:scout; tools: read-only list; model: haiku|sonnet|inherit; no hooks/mcpServers/permissionMode (ignored)
    evals/<case>/{prompt.md,graders/*.md}    # claude plugin eval; ship or keep dev-only (evals/results in .gitignore)
    fixtures/                                # test inputs for scripts
    tests/                                   # python unittest for scripts (plain stdlib)
    (no commands/, no hooks/, no .mcp.json in core)
```
Decisions:
1. Single entry skill `work`; do not add `commands/`. Slash is `/ultimatum:work <task>`. Optional extra skills (e.g. `user-invocable: false` reference skills) only if they pay for their always-on description cost; otherwise keep everything under `work/references/`.
2. Router SKILL.md must (a) state arguments (`$ARGUMENTS`), (b) give every script/reference as a `${CLAUDE_SKILL_DIR}`-prefixed path, (c) say which references to Read for which task type, (d) avoid `context: fork` (needs conversation).
3. Marketplace entry points at `./plugins/ultimatum` so dev material stays out of the install; keep entry `name` == plugin.json `name`; keep `version` in plugin.json only (entry version mismatch warns; plugin.json wins). Bump `version` per release or installs will not update.
4. CI gates (all offline unless noted): `claude plugin validate . --strict` (marketplace) and `claude plugin validate plugins/ultimatum --strict`; `claude plugin details ultimatum` token-budget check; stdlib unit tests for scripts; packaged-copy install test in an isolated `CLAUDE_CONFIG_DIR` (copy only the plugin dir, section 6); paid and optional: `claude plugin eval plugins/ultimatum --ablation none --runs 1 --max-cost-usd N --trust-plugin`; `claude -p` smoke with `--plugin-dir` reading `usage`/`total_cost_usd`/`num_turns`.
5. Core must work with no upstream packs: evals run in an isolation sandbox with only our plugin, which gives that test for free.
6. Open items to verify before depending on them: substitution inside `allowed-tools` frontmatter; whether a git-hosted install ships only the `./plugins/ultimatum` subtree (docs imply yes for relative source); `--bare` + `--plugin-dir` + auth behaviour in CI.
