# Claude Code platform capabilities (researched 2026-11-24)

Source: code.claude.com docs, read by a research subagent on 2026-11-24. "Inferred" marks a reading of an omission; "not documented" marks a gap. Condensed by the main session.

## Plugin updates (plugins/install.md, plugins/loading.md, plugins/cli-reference.md)
- Auto-update is per marketplace: `autoUpdate` on the `extraKnownMarketplaces` entry, or the `/plugin` > Marketplaces toggle.
- **Defaults:** on for official marketplaces and marketplaces added from claude.ai; **off for third-party marketplaces like Ultimatum's**. Users must turn it on once.
- Runs in interactive sessions after the first message, with a random delay of up to 10 min. Writes the new copy to disk; it takes effect after `/reload-plugins` or at the next launch.
- Kill switches: `DISABLE_UPDATES`, `DISABLE_AUTOUPDATER`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` (override with `FORCE_AUTOUPDATE_PLUGINS=1`).
- Manual: `claude plugin update <plugin>@<marketplace>`, or `/plugin` > Installed > Update now.
- Version: the manifest `version` wins. If it is unchanged, users stay on the cached copy even after new commits.
- Old version directories are deleted 14 days after being orphaned, so a rollback has a narrow native window.

## Skills (skills.md, plugins/measure.md)
- Startup loads only name + `description` (+ `when_to_use`, combined cap 1,536 chars). The listing budget is 1% of the context window.
- The SKILL.md body loads on invoke and stays in the chat. Supporting files load only when SKILL.md tells Claude to read them. Scripts are executed, not loaded.
- `disable-model-invocation: true` gives no listing entry and no startup cost; the user invokes it by slash command only.
- After compaction, invoked skill bodies are re-attached: up to 5k tokens per skill, 25k in total.

## Agents (sub-agents.md)
- Plugin agent descriptions are in context from startup (inferred from a 15k-token warning).
- `model: haiku` etc. are allowed in plugin agent frontmatter (inferred: not in the ignored list).
- The Agent tool takes a per-call `model` alias. For plugin agents, `hooks`, `mcpServers`, `permissionMode` and `initialPrompt` are ignored.

## Hooks (hooks.md)
- 33 events. SessionStart matchers: `startup|resume|clear|compact|fork`.
- Stdout enters context for SessionStart, UserPromptSubmit, UserPromptExpansion and PostModelSwitch. PreCompact stdout steers the compaction summary.
- Command timeout defaults to 600 s (30 s on UserPromptSubmit). Plugin hooks register whenever the plugin is enabled.

## Commands (plugins/components.md)
- `commands/` is legacy; skills supersede it. Each command or skill adds name + description to every session. So management commands such as `/ultimatum:status` should use `disable-model-invocation: true` to avoid that cost.

## Cloud sessions (claude-code-on-the-web.md, cloud-environments.md)
- Plugins come from the claude.ai account (claude.ai/customize/plugins) and download at session start. Local user-scope plugins are not available.
- Repo `extraKnownMarketplaces` is **not** applied in Anthropic-hosted sessions. Repo `.claude/settings.json` hooks do run.
- Setup scripts run before launch and are cached if they take under ~5 min. Network is Limited (default) or Full.
- The VM is reclaimed when idle; history restores, background work does not.

## Remote Control (remote-control.md)
- Runs on the user's machine, so local plugins apply (inferred). `/plugin` and `/reload-plugins` are not available over Remote Control.

## Measuring context (plugins/measure.md, headless.md)
- `claude plugin details <name>` gives the "Always-on" token estimate. Also `/context`, `/usage`, `/skill-doctor`.
- `claude -p --output-format json` gives cost and usage. The `stream-json` init event lists loaded plugins.
- `--bare` skips plugins, hooks, MCP and CLAUDE.md, for clean baselines.
