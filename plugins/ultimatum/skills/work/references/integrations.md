# Optional integrations

Run `ult doctor` to see the CLI tools that are present. For MCP tools, check your own tool list. Each optional tool adds depth, and a local path exists for every one. Name the tool before using it, and don't install anything or contact a hosted service unless the user asks.

| Need | Use if present | Local path otherwise |
|---|---|---|
| Library or API docs | Context7 MCP | Installed package source/types (`node_modules`, site-packages), lockfile version, `--help` |
| Symbol graph and edits | Serena or LSP MCP | `ult symbols` / `ult refs`, then read the source |
| Repo graph, blast radius, cycles | Graphify (`graphify-out/graph.json`; `ult arch` merges its EXTRACTED import edges) | `ult arch check`, `ult map` |
| Bounded file bundle for a reviewer | Repomix, with an explicit file list | Pass paths to the agent |
| Command output filtering | RTK (only if already set up) | `ult run`, which keeps raw output and the exit code |
| SAST, secrets, advisories | semgrep, gitleaks, osv-scanner | `ult scan` built-ins; advisories are reported as **not checked** |
| Browser | Playwright (node), Chrome DevTools MCP, axe-core | `node "${CLAUDE_PLUGIN_ROOT}/scripts/ult-browser.mjs"` (Playwright required for real interaction) |
| Production errors | Sentry MCP or `sentry-cli` | Logs or stack traces the user provides; reproduce locally |
| PR or CI | GitHub MCP or `gh` | Local test run plus a CI config read |
