# Ultimatum

**Build, check and launch with Claude Code.** Ask in plain chat and Ultimatum sends the job to the right team: code, business research, websites, social media, motion graphics or brand film. Every step passes a checker, and nothing is published, posted, deployed or paid for until you approve it.

![Ultimatum workflow map: Launch in the middle, Business and Website on the left, Motion graphics and Social media on the right, shared skills along the top](docs/images/workflow.png)

## Install

```
/plugin marketplace add JeffreyScottHamilton/Ultimatum
/plugin install ultimatum@ultimatum
/ultimatum:setup
```

Add the launch plugins you need. Each launch add-on requires `ultimatum-launch`.

```
/plugin install ultimatum-launch@ultimatum             # shared teams: business, website, social, video
/plugin install ultimatum-website-launch@ultimatum     # small business, local service and portfolio sites
/plugin install ultimatum-ecommerce-launch@ultimatum   # online stores
/plugin install ultimatum-app-launch@ultimatum         # web apps, mobile apps, subscriptions
```

| Plugin | For |
|---|---|
| `ultimatum` | Software work: coding, debugging, CI, interface work, security review, releases |
| `ultimatum-launch` | Shared launch teams used by every add-on below |
| `ultimatum-website-launch` | Launching a small business, local service, portfolio or creator site |
| `ultimatum-ecommerce-launch` | Launching an online store |
| `ultimatum-app-launch` | Launching a web app, mobile app or subscription product |

Upgrading from the earlier 1.0.0 build: it used the same version number, so run `/plugin uninstall ultimatum@ultimatum` and install again. See the [changelog](CHANGELOG.md).

## What you can ask

| Say something like | Team | Command |
|---|---|---|
| "Help me launch my business" | Launch runs Business, Website, Social and video together, and hands over to the matching add-on | `/ultimatum-launch:launch` |
| "What's stopping people from booking?" | Business: research, plan, build brief | `/ultimatum-launch:business` |
| "Build me a website for my coffee shop" | Website: brief, mockup you approve, build, browser check | `/ultimatum-launch:website` |
| "Make a logo reveal video" | Motion graphics: storyboard you approve, animate, timestamped review | `/ultimatum-launch:motion-graphics` |
| "Make an emotional film about our customers" | Brand film: story, sourcing, animatic and cut, each approved | `/ultimatum-launch:brand-film` |
| "Plan a week of posts" | Social media: channel, posts, checks, publish only after you approve | `/ultimatum-launch:social-media` |
| "Fix the CSV export" | Work: discovery, fixes, features, bugs, CI, security, releases | `/ultimatum:work` |

Every row except the last needs `ultimatum-launch`; the last is the core plugin. Plain questions stay in normal chat. A typed command always wins over the router's guess.

## How it stays honest

- **Checkers on every step.** A browser reviewer for sites, a timestamped reviewer for videos, a claims and links reviewer for posts. Findings are fixed and rechecked before you see the work.
- **Approval stops.** Brief, mockup, storyboard, story, sourcing, animatic, video, publish and deploy. Each approval is fingerprinted, so if the file changes afterwards you are asked again.
- **Evidence before claims.** No "fixed" or "passes" without a check run in the session.
- **Local first.** The toolbelt is Python standard library with no network access, and what Ultimatum learns stays on your machine unless you choose to share it.

See [`plugins/ultimatum/README.md`](plugins/ultimatum/README.md) and [`plugins/ultimatum-launch/README.md`](plugins/ultimatum-launch/README.md) for everything that ships.

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

## Auto-update

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

Merge this with what the file already has. Claude Code then updates the marketplace and the plugin when it starts, so restart it to pick up a new release. Claude Code reads this setting only from user settings, not from project settings. A plugin updates only when the version in its `.claude-plugin/plugin.json` changes, and only from the default branch (`main`).

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
- [`research/ultimatum-2/OFFLINE-EVALS.md`](research/ultimatum-2/OFFLINE-EVALS.md): 1.0 offline measurements
- [`docs/TEST-REPORT.md`](docs/TEST-REPORT.md): what was tested live, results, and open gaps
- [`docs/COVERAGE-MAP.md`](docs/COVERAGE-MAP.md): every upstream capability and where Ultimatum covers it, or why it doesn't
- [`docs/CREDITS.md`](docs/CREDITS.md): upstream projects, revisions, and licenses
- [`docs/SECURITY.md`](docs/SECURITY.md): security review of Ultimatum itself
- [`research/ARCHITECTURE-DECISIONS.md`](research/ARCHITECTURE-DECISIONS.md)

License: MIT. This is original work; no upstream code or prose is redistributed.
