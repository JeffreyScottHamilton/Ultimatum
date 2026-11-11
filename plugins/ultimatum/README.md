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
  - `ultimatum:worker`: one owned slice of a larger task.
  - `ultimatum:reviewer`: a fresh review of the integrated diff.
  - `ultimatum:security-hunter`: hunts in one assigned area during an audit.
  - `ultimatum:security-verifier`: independently challenges serious findings.

## Defaults that respect your project

- No hooks, telemetry, MCP servers, proxies, or hosted model routing are installed.
- State is kept in `.ultimatum/` in your project. The directory ignores itself in git. Raw logs are mode 0600, and anything printed or written to summaries is secret-redacted.
- Optional tools such as Semgrep, Gitleaks, OSV-Scanner, Playwright, axe-core, Context7, Serena, the Sentry MCP, and Chrome DevTools MCP are used only when present, and Ultimatum names them before use. The core works without any of them.
- Security audits are read-only by default. Active testing only targets local fixtures or environments you explicitly authorize.

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
