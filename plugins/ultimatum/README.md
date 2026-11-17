# Ultimatum

One skill for the software work a developer actually does in Claude Code. Install it once, then run one command:

```
/ultimatum:work <task>
```

Ultimatum reads the task and picks a workflow:

- a small fix
- codebase discovery
- an unclear or large feature
- a hard bug or failing test
- CI or PR feedback
- UI work verified in a real browser
- data or infrastructure changes
- a bounded optimization loop
- release readiness
- security review of a change
- a full security audit or remediation
- a session handoff or resume
- an efficiency review of Claude's own recent usage

It then loads only the guidance that workflow needs. A short security pass runs automatically whenever a change touches auth, permissions, tenant boundaries, money, data exposure, external input, secrets, or deploy settings.

## What you get

- **A compact router** (`skills/work/SKILL.md`) that loads focused references on demand (`skills/work/references/`).
- **A local toolbelt** (`scripts/ult`), written in the Python standard library with no network access:
  - `ult run -- <cmd>`: runs a noisy command and prints its exit code and the exact failure lines. The full raw log is kept and can be retrieved with `ult log <id>`.
  - `ult search | symbols | refs`: scoped, capped code search.
  - `ult map`: a repository map you query by section.
  - `ult note | find | get`: a local full-text evidence store.
  - `ult handoff write | show`: a short, checkable session handoff.
  - `ult scan`: wraps Semgrep, Gitleaks, and OSV-Scanner if they are installed, and falls back to built-in leads if they aren't.
  - `ult findings`: validates and renders security findings and a coverage ledger.
  - `ult doctor`: shows which optional integrations are present.
  - `ult usage report` and `ult improve`: the efficiency coach. It reviews your local Claude Code transcripts, finds avoidable token use, and tracks whether each change actually helped.
- **A browser check** (`scripts/ult-browser.mjs`): uses Playwright for viewports, real interactions, console errors, and accessibility checks. It runs axe-core if installed and built-in checks otherwise.
- **Five subagents**:
  - `ultimatum:scout`: fast, read-only searching.
  - `ultimatum:worker`: makes every edit, from a one-line fix to one owned slice of a larger task. The main session only orchestrates: it never edits files itself.
  - `ultimatum:reviewer`: a fresh review of the integrated diff.
  - `ultimatum:security-hunter`: hunts in one assigned area during an audit.
  - `ultimatum:security-verifier`: independently challenges serious findings.

## Defaults that respect your project

- No telemetry, MCP servers, proxies, or hosted model routing are installed. One local hook ships (`hooks/hooks.json`): after a compaction it prints the saved handoff back into the chat. It runs `ult handoff show`, reads only `.ultimatum/handoff.md`, and makes no network calls.
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

The effect on your own token use is unmeasured. Track it with the efficiency coach (`ult usage report`).

## It learns

When you correct Claude, or the same mistake happens twice in a task, Ultimatum adds the one-line rule that would have prevented it to the project's `CLAUDE.md` under `## Learned`, and tells you. Claude Code loads that file in every later session. For measured changes, ask for an "efficiency review" (`ult usage report`, `ult improve`).

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

This applies Ultimatum, and its extra cost (about 1.5–1.8x per task in our evals), to every coding task. Leave it out if you'd rather call `/ultimatum:work` only when you want it.

Requirements: Claude Code with plugin support and Python 3.9+ (unit tests pass on 3.9, 3.11, 3.12 and 3.13). Browser checks need Node and Playwright.

Credits: see `CREDITS.md`. License: MIT.
