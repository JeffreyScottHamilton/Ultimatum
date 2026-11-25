# Ultimatum Launch

Launch teams for Claude Code: intake, business and brand, website, marketing, motion graphics and emotional brand films. It needs the core `ultimatum` plugin, and every spend, post, publish and deploy needs your approval.

## Install

```
/plugin marketplace add JeffreyScottHamilton/Ultimatum
/plugin install ultimatum@ultimatum
/plugin install ultimatum-launch@ultimatum
```

## Launch kinds

This plugin is the shared base: the teams, the agents and a general manager for mixed or unsure launches. Each kind of launch also has its own plugin with a deeper manager that runs these same teams:

| Plugin | For |
|---|---|
| `ultimatum-website-launch` | small business, local service, portfolio and creator sites |
| `ultimatum-ecommerce-launch` | online stores |
| `ultimatum-app-launch` | web and mobile apps, software and subscriptions |

Install the ones you need (`/plugin install ultimatum-<kind>-launch@ultimatum`). The plain-chat hook names the right one when it is installed.

## Skills

| Say something like | Skill |
|---|---|
| "Help me launch my business" | `/ultimatum-launch:launch`: intake in rounds of 5 to 8 questions with recommended answers, a one-page brief you approve, then the kind of launch (website, e-commerce, app), handing over to that kind's plugin when installed; a fact-finder checks prices and terms first |
| "Who is my customer and what should I charge?" | `/ultimatum-launch:business`: positioning before visuals, saved to `brand/brand.md` |
| "Build me a website for my coffee shop" | `/ultimatum-launch:website`: three HTML directions screenshotted at 375, 768 and 1440 px, a taste critic that needs 8/10, your pick, then the build and a browser check |
| "Write a week of tiktok posts" | `/ultimatum-launch:social-media`: hook videos, posts, blog and SEO articles, scripts; results read after about 48 hours and judged by signups; its video step picks Brand Film or Motion Graphics |
| "Make a 30 second launch video" | `/ultimatum-launch:motion-graphics`: storyboard you approve, audio sheet (voice and music), animation to the audio, sound effects, a loudness check; for a feature, a number or frequent updates |
| "Make an emotional brand film for our launch" | `/ultimatum-launch:brand-film`: story you approve, then sourcing (footage, spend, consent), an animatic, and the video; `ult film "<task>"`, `ult film --check` for the footage manifest, `ult film --deliver FILE`; for a feeling people carry |

Plain requests start the right skill through a small local prompt hook (`ULTIMATUM_AUTO=0` turns it off). Plain questions stay in chat, and a typed command always wins.

## Agents

- `taste-critic`: read-only. Design mode screenshots pages and scores them out of 10; film mode scores a brand film's story and cut 1 to 5 and checks originality.
- `compliance-reviewer`: read-only. It checks claims, AI disclosure, releases, the footage manifest and asset licences before anything is published.

## Approvals

The brief, mockup, storyboard, publish and deploy stops, and for brand films the story, sourcing, animatic and video stops, are recorded with `ult gate` (for example `ult gate approve sourcing`). Each approval is fingerprinted, so a changed file asks again. Connectors such as Composio, ElevenLabs or a scheduler are used only if you have authorized them. Generating audio asks before spending credits.

## Licences and facts

Vendor terms, platform limits and licence notes are in `skills/launch/references/licenses.md`. Some of them come from search previews and are marked "check before relying". Footage, stock, AI video, music libraries, releases and AI labels (with C2PA) have rows there; prices and terms change, so confirm them on the vendor's page. Sound-effect packs and downloaded footage stay on your machine and are never committed; only the footage manifest is.

## Toolbelt

`scripts/` is a copy of the core toolbelt (Python standard library, no network access), kept identical by `tools/sync_launch_toolbelt.py`. Edit the core copy, then run the sync.

MIT licence; see `LICENSE`.
