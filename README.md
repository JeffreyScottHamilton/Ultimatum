# Ultimatum

A free, open-source developer skill for Claude Code. You install it once and use one command:

```
/ultimatum:work <task>
/ultimatum:website <task>
/ultimatum:motion-graphics <task>
```

`/ultimatum:work` is the default for chat and coding. `/ultimatum:website` builds or fixes websites with a brief, an optional designer, a mockup you approve for new looks, a builder and a browser review. You can also just ask in plain chat: "Build me a website for my coffee shop" starts Website, "Fix the CSV export" starts Work, "Make a logo reveal video" starts Motion Graphics (it stops for storyboard approval before animating), and plain questions stay in normal chat. It covers the work developers actually do: understanding a new codebase, small fixes, features, hard bugs, CI and PR feedback, UI design, motion and components verified in a real browser, data and infrastructure changes, bounded optimization, releases, MCP servers and skills, architecture checks for refactors and reviews (cycles, duplication, oversized modules, drift), handoffs, and three security workflows (secure implementation, security review of a change, full audit and remediation). A local router picks the mode and loads only the guidance each task needs, and Ultimatum learns from your sessions on your own machine. See [`plugins/ultimatum/README.md`](plugins/ultimatum/README.md) for what ships.

## Try it locally

From a clone of this repository:

```bash
claude --plugin-dir ./plugins/ultimatum
```

Then, inside Claude Code:

```
/ultimatum:work slugify drops digits; fix it
```

Or install it through the local marketplace:

```bash
claude plugin marketplace add ./
```

```bash
claude plugin install ultimatum@ultimatum
```

Remove it with `claude plugin uninstall ultimatum@ultimatum`, then `claude plugin marketplace remove ultimatum`.

## Install from GitHub

```
/plugin marketplace add JeffreyScottHamilton/Ultimatum
/plugin install ultimatum@ultimatum
```

### Turn on auto-update (do this once per computer)

Claude Code keeps auto-update off for marketplaces added from GitHub, and a repository cannot turn it on for you. The easiest way: run `/ultimatum:setup` once; it backs up your settings and makes the change below. Or add `"autoUpdate": true` to the marketplace's entry in your user settings, `~/.claude/settings.json` (on Windows, `%USERPROFILE%\.claude\settings.json`):

```json
{
  "extraKnownMarketplaces": {
    "ultimatum": {
      "source": { "source": "github", "repo": "JeffreyScottHamilton/Ultimatum" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": { "ultimatum@ultimatum": true }
}
```

Merge this with what the file already has. Claude Code then updates the marketplace and the plugin when it starts, so restart it to pick up a new release. Claude Code reads this setting only from user settings, not from project settings. An update installs only when the version in `plugins/ultimatum/.claude-plugin/plugin.json` changes, and only from the default branch (`main`).

Cloud sessions: install from claude.ai/customize/plugins; each new session downloads the current version. In a session that is already running, `/reload-plugins` picks up an update. Fallback anywhere: `claude plugin update ultimatum@ultimatum`.

## Repository layout

| Path | What it is | Shipped in the plugin? |
|---|---|---|
| `.claude-plugin/marketplace.json` | Marketplace that lists the plugin | — |
| `plugins/ultimatum/` | **The plugin**: skill, references, agents, toolbelt, schemas, unit tests | yes |
| `fixtures/` | Nine small projects used to test Ultimatum, some with seeded bugs and vulnerabilities. Answer keys are in `fixtures/_answer-keys/` | no |
| `evals/live/` | Live A/B harness: Ultimatum vs. plain Claude Code on the fixtures, with deterministic graders | no |
| `plugins/ultimatum/evals/` | `claude plugin eval` routing cases | yes (dev only) |
| `research/` | Upstream research notes, revisions and licenses, and architecture decisions | no |
| `docs/` | Coverage map, credits, test report, routing test, and Ultimatum's own security review | no |

## Development checks

```bash
python3 -m unittest discover -s plugins/ultimatum/tests
```

```bash
claude plugin validate . --strict
```

```bash
claude plugin validate plugins/ultimatum --strict
```

```bash
python3 plugins/ultimatum/scripts/ult route --eval plugins/ultimatum/tests/data/routing_holdout.jsonl
```

```bash
python3 evals/live/run_live.py --arms vanilla,v041,v2 --max-total-usd 15 --dry-run
```

Live evals run real Claude sessions and cost money (drop `--dry-run`). Each run's cost is printed and recorded, and the run stops before `--max-total-usd` is exceeded.

## Documents

- [`CHANGELOG.md`](CHANGELOG.md): release notes
- [`research/ultimatum-2/OFFLINE-EVALS.md`](research/ultimatum-2/OFFLINE-EVALS.md): 2.0 offline measurements
- [`docs/TEST-REPORT.md`](docs/TEST-REPORT.md): what was tested live, results, and open gaps
- [`docs/COVERAGE-MAP.md`](docs/COVERAGE-MAP.md): every upstream capability and where Ultimatum covers it, or why it doesn't
- [`docs/CREDITS.md`](docs/CREDITS.md): upstream projects, revisions, and licenses
- [`docs/SECURITY.md`](docs/SECURITY.md): security review of Ultimatum itself
- [`research/ARCHITECTURE-DECISIONS.md`](research/ARCHITECTURE-DECISIONS.md)

License: MIT. This is original work; no upstream code or prose is redistributed.
