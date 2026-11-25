# Ultimatum

One skill for the software work a developer actually does in Claude Code. Install it once, then run one command:

```
/ultimatum:work <task>        # chat and coding
```

You don't have to type it: once the plugin is enabled, a coding request such as "Fix the CSV export" starts `/ultimatum:work` through a small local prompt hook, with no line needed in your `CLAUDE.md`. Plain questions ("What is a closure?", "How does the export module work?") and writing help stay in normal chat. `ULTIMATUM_AUTO=0` turns the hook off, and typed commands always win.

Websites, business and brand, marketing, motion graphics and full launches live in the separate **Ultimatum Launch** plugin (`/ultimatum-launch:website`, `/ultimatum-launch:launch` and so on; see [`../ultimatum-launch/README.md`](../ultimatum-launch/README.md)). Since 1.1.0 the core plugin no longer has those commands.

A local router (`ult route`, no model call) reads the task and picks:

- **a mode:** FAST (clear, local edits: no references, no subagents), STANDARD, DEEP (large work: acceptance checks, a code map, optional helpers, one review), SECURITY (security review, audit or fix with the OWASP-informed guides) or RECOVERY (resume after a break or compaction). Start a task with `fast:` or `deep:` to force one.
- **one workflow:** small fix, discovery, feature, large change, bug, CI/PR, UI, data/infra, optimization, release, security review, audit or fix, handoff, efficiency review, skill evaluation, MCP server, or skill authoring.
- **up to two add-ons:** React, UI design, motion, components, production debugging, context efficiency, integrations.
- **the security overlay** whenever a change touches auth, permissions, tenants, money, personal data, external input, secrets or deploy settings.

It prints only the reference files that combination needs and their size, so Claude reads those and nothing else.

## What you get

- **A small entry skill** (`skills/work/SKILL.md`, about 1k tokens) plus the router and its registry (`skills/work/modules.json`), which load focused references on demand (`skills/work/references/`).
- **A local toolbelt** (`scripts/ult`), written in the Python standard library with no network access:
  - `ult run -- <cmd>`: runs a noisy command and prints its exit code and the exact failure lines. The full raw log is kept and can be retrieved with `ult log <id>`.
  - `ult search | symbols | refs`: scoped, capped code search.
  - `ult map`: a repository map you query by section.
  - `ult arch check [--changed] [--drift]`: the Architecture Guardian. It finds import cycles (merging Graphify's extracted edges if you have a graph), duplicated blocks, oversized files and functions, placeholders, naming outliers and untested changed modules. It runs only for structural work and reviews, never for small edits.
  - `ult note | find | get`: a local full-text evidence store.
  - `ult handoff write | show`: a short, checkable session handoff.
  - `ult scan`: wraps Semgrep, Gitleaks, and OSV-Scanner if they are installed, and falls back to built-in leads if they aren't.
  - `ult findings`: validates and renders security findings and a coverage ledger.
  - `ult doctor`: shows which optional integrations are present.
  - `ult retro`: lesson candidates from the current chat, run automatically at the end of a long task.
  - `ult website "<task>"`: the website plan (Designer yes or no, mockup gate, solo or helpers, files to read); `ult website --approve "…"` records the approved look in the brief. `ult style status|apply|remove`: the opt-in chat style.
  - `ult route`: the router above. `ult route --list` shows every module; `--eval FILE` scores it.
  - `ult components "<need>"`: suggests permissively licensed UI and animation libraries offline, with alternatives for restricted ones. `ult upstreams` lists the reviewed sources.
  - `ult learn`, `ult budget`, `ult sync`, `ult update`: local lessons and proposals, this chat's token use, copying lessons between machines, and update setup (see below).
  - `ult usage report` and `ult improve`: the efficiency coach. It reviews your local Claude Code transcripts, finds avoidable token use, and tracks whether each change actually helped.
- **A browser check** (`scripts/ult-browser.mjs`): uses Playwright for viewports, real interactions, console errors, and accessibility checks. It runs axe-core if installed and built-in checks otherwise.
- **Shared skills** read only when needed: `design`, `coding` (plus short guides such as `guides/website.md`), `review` and `release`. All workflows follow one set of shared defaults (`shared/defaults.md`). `/ultimatum:style` can copy those defaults into your own `CLAUDE.md` for normal chats; `ult style remove` undoes it exactly.
- **Management commands** that cost nothing until you type them: `/ultimatum:status`, `setup`, `sync`, `learn`, `skills`, `budget`, `eval`, `doctor`, `rollback`, `migrate`.
- **Five subagents**:
  - `ultimatum:scout`: fast, read-only searching.
  - `ultimatum:worker` (Haiku by default): one owned slice of large work, run in parallel with other slices. Small and medium changes are made directly in the main chat, which is cheaper than starting a new agent.
  - `ultimatum:reviewer`: a fresh review of the integrated diff.
  - `ultimatum:security-hunter`: hunts in one assigned area during an audit.
  - `ultimatum:security-verifier`: independently challenges serious findings.

## Defaults that respect your project

- No telemetry, MCP servers, proxies, or hosted model routing are installed. Local hooks ship in `hooks/hooks.json`. After a compaction one prints the saved handoff back into the chat (`ult handoff show`). At the end of each turn one records counts and categories (never prompts, code, paths or secrets) to `.ultimatum/observations.jsonl`; it prints nothing, so it adds no tokens, and `ULTIMATUM_OBSERVE=0` turns it off. The chat-size guard below does nothing unless you turn it on. None of them makes network calls.
- State is kept in `.ultimatum/` in your project. The directory ignores itself in git. Raw logs are mode 0600, and anything printed or written to summaries is secret-redacted.
- Optional tools such as Semgrep, Gitleaks, OSV-Scanner, Playwright, axe-core, Context7, Serena, the Sentry MCP, and Chrome DevTools MCP are used only when present, and Ultimatum names them before use. The core works without any of them.
- Security audits are read-only by default. Active testing only targets local fixtures or environments you explicitly authorize.

## One chat, compacted automatically at about 200k tokens

You should never need to start a new chat because the old one got long. Ultimatum is built to work through compaction: it saves a handoff at each milestone, the hook above prints it back after every compaction, and the skill tells Claude to re-check and keep going without asking you.

Claude Code compacts automatically; you only set where. On a 1M-token model the default is far too late (every turn re-reads the whole chat), so set the window to 200k once. A plugin can't change this setting for you:

- **Everywhere on your machine:** add to `~/.claude/settings.json`:
  ```json
  { "env": { "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "200000" } }
  ```
- **One project:** the same block in that project's `.claude/settings.json` (this repository ships one).
- **One run:** `claude --autocompact 200000`.
- **Cloud sessions (claude.ai/code):** add the environment variable `CLAUDE_CODE_AUTO_COMPACT_WINDOW=200000` in the environment's settings, or commit the project `.claude/settings.json` above.

Measured token use, so far: in the live A/B run (`evals/live/results/final`, 10 test tasks, one run each, made with a version before 0.3.0), Ultimatum cost 1.2× to 4.3× more per task than plain Claude Code and passed 9 of 10 tasks against 5 of 10. 1.0 has not been measured live yet. What has been measured offline is in `research/ultimatum-2/OFFLINE-EVALS.md`. Track your own use with `ult budget` and `ult usage report`.

## It learns, locally

- **Every turn** the observe hook above counts what went wrong (repeated failing commands, re-read files, oversized outputs, corrections). Nothing is sent anywhere.
- **After a long task** (or when you correct it) Claude records one lesson with `ult learn add`. Project lessons stay in `.ultimatum/` (git-ignored, never committed for you); lessons about how Claude works go to `~/.ultimatum/`. The router shows up to three relevant lessons with each task.
- **To improve Ultimatum itself**, run `/ultimatum:learn propose`. It writes a proposal from a fixed allow-list (plugin version, module, category, counts and one stock sentence), with no paths, code, your text, repository names, URLs or secrets. `/ultimatum:learn submit <id>` shows you the exact text and opens a pull request only after you say yes. A merged change ships as a new version.
- **Cloud sessions** start on a fresh machine. `/ultimatum:sync` copies your lessons to and from a private repository of your own, and asks before every push.

## Updates

Auto-update is off by default for third-party marketplaces like this one. Turn it on once:

- **Local CLI:** run `/ultimatum:setup`. It backs up `~/.claude/settings.json` and sets `autoUpdate` for the `ultimatum` marketplace. Or toggle it in `/plugin` > Marketplaces.
- **Cloud (claude.ai/code):** install and update from claude.ai/customize/plugins; sessions download the current version when they start.
- **A session that is already running:** `/reload-plugins` after an update lands, or restart.
- **Fallback:** `claude plugin update ultimatum@ultimatum`.

`/ultimatum:status` shows the running and available versions. `/ultimatum:rollback` explains how to go back to a cached earlier version (kept for 14 days). `/ultimatum:migrate` upgrades 0.4.x state; it changes nothing that already works.

## Optional: block prompts in chats that got too expensive

Use auto-compact (above) as the main control: it shrinks a chat in place, so nothing has to be re-learned. A new chat starts at roughly 78k tokens per turn and then re-reads files to catch up, so switching only pays off for very large chats. The guard is a safety net for those, which is why its limits sit well above the ~200k compaction point.

The chat-size guard is a `UserPromptSubmit` hook that ships with the plugin but is **off by default**. When on, before each prompt it runs a local script (no model call) that reads the current chat's transcript. If the last turn re-read more than 400k tokens, or the chat has been idle for more than 4 hours and re-reads more than 150k tokens, it:

1. blocks the prompt (exit code 2), so it never reaches the model and costs zero model tokens,
2. runs `ult handoff write --keep`, which keeps the existing goal, decisions, and next step and records the blocked prompt,
3. prints: `Chat too large. Start a new chat and type: /ultimatum:work resume`, and says you can send your message again to stay.

A small chat is never blocked for being idle: re-reading it once after the cache expires costs little. The guard blocks a chat once. If you send the same or any message again in that chat, it goes through, so you are never locked out.

When you then start a new chat in the same project (or type `/clear`), a `SessionStart` hook loads that handoff into the new chat once, so your first message can be anything, for example `continue`, and Claude picks up at the next unfinished step. Typing `/ultimatum:work resume` still works too. In cloud sessions, a new chat runs on a new machine without the old chat's `.ultimatum/` files, so use `/clear` in the same chat there instead.

To turn it on, set `ULTIMATUM_GUARD=1` in the environment Claude Code runs in, for example in `~/.claude/settings.json`:

```json
{ "env": { "ULTIMATUM_GUARD": "1" } }
```

For cloud sessions, add `ULTIMATUM_GUARD=1` to the environment's variables. Optional thresholds: `ULTIMATUM_GUARD_TOKENS` (default `400000`), `ULTIMATUM_GUARD_IDLE_MIN` (default `240`) and `ULTIMATUM_GUARD_IDLE_TOKENS` (default `150000`, the chat size below which idling never blocks). To turn it off, remove the variable. The guard needs `python3` on the PATH. If the transcript can't be read, it lets the prompt through.

## Install

```
/plugin install ultimatum --marketplace JeffreyScottHamilton/Ultimatum
```

Or add the marketplace first with `/plugin marketplace add JeffreyScottHamilton/Ultimatum`, then run `/plugin install ultimatum@ultimatum`. To try a local checkout: `claude --plugin-dir ./plugins/ultimatum`.

## Make Claude use it automatically

Claude does not pick a skill on its own for ordinary coding requests. In testing, it used Ultimatum unprompted in 0 of 3 tasks. Adding one instruction to your personal `~/.claude/CLAUDE.md` changed that to 3 of 3:

```
## Ultimatum
For any software task in a repository (fixing, building, debugging, reviewing, auditing,
testing, shipping, or explaining code), invoke the `ultimatum:work` skill first and follow it.
Skip it only for questions unrelated to a codebase.
```

This applies Ultimatum, and its extra cost (1.2× to 4.3× per task in the last live A/B run, before 0.4.0; 1.0 not yet measured live), to every coding task. Leave it out if you'd rather call `/ultimatum:work` only when you want it.

Requirements: Claude Code with plugin support and Python 3.9+ (unit tests pass on 3.9, 3.11, 3.12 and 3.13). Browser checks need Node and Playwright.

Credits: see `CREDITS.md`. License: MIT.
