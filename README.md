# Ultimatum

**Build, check and launch with Claude Code.** Ask in plain chat and Ultimatum sends the job to the right team: code, business research, websites, social media, motion graphics or brand film. Every step passes a checker, and nothing is published, posted, deployed or paid for until you approve it.

![Ultimatum workflow map: Launch in the middle, Business and Website on the left, Motion graphics and Social media on the right, shared skills along the top](docs/images/workflow.png)

## Install

```
/plugin marketplace add JeffreyScottHamilton/Ultimatum
/plugin install ultimatum@ultimatum
/ultimatum:setup
```

Add the launch plugin for what you are launching, or Social Media on its own for posts and video. Each one stands alone: it ships its own team guides, reviewer agents and toolbelt, and needs no other plugin.

```
/plugin install ultimatum-website-launch@ultimatum     # small business, local service and portfolio sites
/plugin install ultimatum-ecommerce-launch@ultimatum   # online stores
/plugin install ultimatum-app-launch@ultimatum         # web apps, mobile apps, subscriptions
/plugin install ultimatum-event-launch@ultimatum       # workshops, classes, openings, ticketed events
/plugin install ultimatum-social-media@ultimatum       # posts, carousels and video for social
```

| Plugin | For |
|---|---|
| `ultimatum` | Software work: coding, debugging, CI, interface work, security review, releases |
| `ultimatum-website-launch` | Launching a small business, local service, portfolio or creator site |
| `ultimatum-ecommerce-launch` | Launching an online store |
| `ultimatum-app-launch` | Launching a web app, mobile app or subscription product |
| `ultimatum-event-launch` | Promoting a workshop, class, webinar, opening, fundraiser or ticketed show |
| `ultimatum-social-media` | Social posts, campaigns and video, with hand-off to DaVinci Resolve, Premiere Pro or Final Cut Pro |

Upgrading from the earlier 1.0.0 build: it used the same version number, so run `/plugin uninstall ultimatum@ultimatum` and install again. See the [changelog](CHANGELOG.md).

## What you can ask

| Say something like | What runs | Command |
|---|---|---|
| "Help me launch my coffee shop" | Website Launch: intake, brief, then its Business, Website, Social Media and video teams | `/ultimatum-website-launch:launch` |
| "Launch my online candle shop" | E-commerce Launch: the same teams with store guidance | `/ultimatum-ecommerce-launch:launch` |
| "Launch our SaaS invoicing app" | App Launch: the same teams with product guidance | `/ultimatum-app-launch:launch` |
| "Help me fill my workshop" | Event Launch: intake, ticketing, countdown promotion, run sheet and follow-up | `/ultimatum-event-launch:launch` |
| "Make a Reel for our new menu" | Social Media: posts and video in the style that fits | `/ultimatum-social-media:social-media` |
| "Fix the CSV export" | Work: discovery, fixes, features, bugs, CI, security, releases | `/ultimatum:work` |

Inside a launch, the manager reads each team's guide when that team's turn comes: Business (research, plan, build brief), Website (brief, mockup you approve, build, browser check), Social Media (posts, checks, publish only after you approve), Motion Graphics (storyboard you approve, animate, timestamped review) and Brand Film (story, sourcing, animatic and cut, each approved). Plain questions stay in normal chat. A typed command always wins.

## How it stays honest

- **Checkers on every step.** A browser reviewer for sites, a timestamped reviewer for videos, a claims and links reviewer for posts. Findings are fixed and rechecked before you see the work.
- **Approval stops.** Brief, mockup, storyboard, story, sourcing, animatic, video, publish and deploy. Each approval is fingerprinted, so if the file changes afterwards you are asked again.
- **Evidence before claims.** No "fixed" or "passes" without a check run in the session.
- **Local first.** The toolbelt is Python standard library with no network access, and what Ultimatum learns stays on your machine unless you choose to share it.

See [`plugins/ultimatum/README.md`](plugins/ultimatum/README.md) and the launch plugins' READMEs ([website](plugins/ultimatum-website-launch/README.md), [e-commerce](plugins/ultimatum-ecommerce-launch/README.md), [app](plugins/ultimatum-app-launch/README.md), [event](plugins/ultimatum-event-launch/README.md)) and [Social Media](plugins/ultimatum-social-media/README.md) for everything that ships.

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
| `.claude-plugin/marketplace.json` | Marketplace that lists the plugins | — |
| `plugins/ultimatum/` | **The core plugin**: skill, references, agents, toolbelt, schemas, unit tests | yes |
| `plugins/ultimatum-*-launch/` | **The launch plugins**: one head skill each, plus copies of the team guides, agents and toolbelt | yes |
| `plugins/ultimatum-social-media/` | **Social Media**: one head skill plus the same kind of copies | yes |
| `teams/` | Source of the team guides and reviewer agents; `tools/sync_plugins.py` copies them into each head | no (copied) |
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
python3 tools/sync_plugins.py --check
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
