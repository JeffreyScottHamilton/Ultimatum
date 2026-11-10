# Ultimatum self-review (security)

Scope: everything shipped in `plugins/ultimatum/`. That covers the manifest, the skill and references, the agents, `scripts/ult` with `scripts/ultlib/*.py`, `scripts/ult-browser.mjs`, the schemas, and the tests. Reviewed at the commit that adds this file.

## Surface inventory

| Surface | What it does | Controls |
|---|---|---|
| Hooks, MCP servers, `settings.json` | **None shipped.** The manifest has no `hooks`, `mcpServers`, or LSP entries (`claude plugin details`: Hooks 0, MCP 0). | Nothing runs unless the user invokes `/ultimatum:work` or the model calls the toolbelt. |
| `ult run` | Runs the command the agent asks for. | Uses `subprocess.Popen(argv)` with no shell. The `--shell` flag (`bash -c`) is an explicit opt-in. The command runs with the user's own permissions, the same as Claude's Bash tool, and is subject to the user's Claude Code permission rules. |
| Other subprocesses | `git` (read-only: `rev-parse`, `status`, `ls-files`, `diff`), `rg`, `node -e require.resolve(<constant>)`, and scanners in `ult scan` (`semgrep`, `gitleaks`, `osv-scanner`) when installed. | Argument lists only, never `shell=True`. Scanner invocations use offline-safe flags (`--metrics=off --disable-version-check` for semgrep, `--redact` for gitleaks), and `ult scan` prints each command it ran. |
| Network | The Python toolbelt opens **no** sockets. `ult-browser.mjs` loads only the target URL and aborts requests to other origins unless `--allow-external` is set. | Verified by grep (no `urllib`, `http.client`, `socket`, or `requests` imports in `ultlib`) and by the `test_browser` external-block test. |
| Files written | Everything goes under `<project>/.ultimatum/`: logs, `index.db`, `map.json`, `handoff.md`, `security/`, `browser/`. | The directory is created at 0700 and ignores itself (`.gitignore` = `*`). Files are written 0600 with `O_NOFOLLOW`. A symlinked `.ultimatum`, subdirectory, or target file is refused (see the finding below). |
| Secrets | Commands may print secrets. | Raw logs keep exact bytes locally (0600). All *printed* output, saved notes, handoffs, map entries, and findings pass through `redact()`, which keeps only the last four characters. `ult findings validate` rejects unredacted secrets. |
| Ids → paths | Log ids and store refs come from the model or the user. | `safe_id()` allows only `[A-Za-z0-9_.-]` and rejects `..`. Covered by a test of path traversal through `ult get log:../../x:1-1`. |
| Untrusted text | Repo files, issues, PR comments, web pages, tool output, a repo-supplied `.ultimatum/handoff.md`. | SKILL.md §1 rule 4 and every agent prompt treat this text as data. Hunters report agent-addressed text as a finding. `ult handoff show` checks a handoff's claims against git before use. Authorization stays with the main agent. |
| Subagents | scout, hunter, verifier, and reviewer are read-only by instruction. The worker edits only the files it owns. | Plugin agents cannot set `permissionMode` or hooks (`platform.md` §4). The user's permission rules still apply. Briefs are redacted. |
| Update path | Installed from the marketplace (`git` source). Updates arrive only via `claude plugin marketplace update`, and the version in `plugin.json` gates them. | No self-update code and no download at runtime. `ult doctor` reports tools and never installs them. |
| Dependencies | Python stdlib only. Node script uses the user's installed Playwright and, optionally, axe-core. | No `package.json` and no lockfile, so there is nothing to resolve at install time. |

## Findings from this review

1. **Fixed: writes followed planted symlinks (CWE-59).** A cloned repository could commit `.ultimatum/map.json`, `handoff.md`, or `index.db` as a symlink to a file outside the project. `ult map build` or `ult handoff write` would then have overwritten the target with the user's permissions. The fix is in `common.py`: `_refuse_symlink` is checked on the state dir, its subdirs, and each target file, and opens use `O_NOFOLLOW`. `store._db` refuses a symlinked `index.db`. Regression tests: `tests/test_common.py::TestSymlinkSafety` (two tests). Both fail on the pre-fix code, where the victim file was overwritten, and pass after the fix.
2. **Fixed: path traversal in `ult get log:<id>` and `ult log <id>`.** This was found by the independent toolbelt tester. `safe_id()` was added, and a test covers it.
3. **Fixed: missed redactions.** These were prefixed env names (`DB_PASSWORD=`) and unquoted `.env` lines, and the independent tester found them too. New patterns and tests were added.
4. **Accepted: `ult run` runs arbitrary commands.** This is by design. It is equivalent to the Bash tool and subject to the same permission prompts and rules. `--shell` is opt-in.
5. **Accepted, documented: raw logs contain unredacted output.** They are needed for exact evidence, kept local at 0600, and git-ignored. Delete `.ultimatum/logs/` to purge them.

## Not covered by this review

- Behavior of optional external tools (semgrep, gitleaks, osv-scanner, Playwright, MCP servers). Those are the user's installs.
- Model-level prompt-injection resistance. The instructions mitigate it, but nothing can guarantee it. The audit eval checks that hunters treat repository text as data, and no adversarial prompt-injection fixture has been run yet (see `TEST-REPORT.md` gaps).
