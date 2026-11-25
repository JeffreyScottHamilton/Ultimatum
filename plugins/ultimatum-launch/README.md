# Ultimatum Launch

Launch teams for Claude Code: intake, business and brand, website, marketing and motion graphics. It needs the core `ultimatum` plugin, and every spend, post, publish and deploy waits for your yes.

## Install

```
/plugin marketplace add JeffreyScottHamilton/Ultimatum
/plugin install ultimatum@ultimatum
/plugin install ultimatum-launch@ultimatum
```

## Skills

| Say something like | Skill |
|---|---|
| "Help me launch my business" | `/ultimatum-launch:launch`: intake in rounds of 5 to 8 questions with recommended answers, a one-page brief you approve, then the right route (small site, SaaS, e-commerce) |
| "Who is my customer and what should I charge?" | `/ultimatum-launch:business`: positioning before visuals, saved to `brand/brand.md` |
| "Build me a website for my coffee shop" | `/ultimatum-launch:website`: three HTML directions screenshotted at 375, 768 and 1440 px, a taste critic that needs 8/10, your pick, then the build and a browser check |
| "Write a week of tiktok posts" | `/ultimatum-launch:social-media`: hook videos, posts, blog and SEO articles, scripts; results read after about 48 hours and judged by signups |
| "Make a 30 second launch video" | `/ultimatum-launch:motion-graphics`: storyboard you approve, audio sheet (voice and music), animation to the audio, sound effects, a loudness check |

Plain requests start the right skill through a small local prompt hook (`ULTIMATUM_AUTO=0` turns it off). Plain questions stay in chat, and a typed command always wins.

## Agents

- `taste-critic`: read-only. It screenshots pages and returns severity-sorted findings with a score out of 10.
- `compliance-reviewer`: read-only. It checks claims, AI disclosure and asset licences before anything is published.

## Approvals

The brief, mockup, storyboard, video, publish and deploy stops are recorded with `ult gate`. Each approval is fingerprinted, so a changed file asks again. Connectors such as Composio, ElevenLabs or a scheduler are used only if you have authorized them. Generating audio asks before spending credits.

## Licences and facts

Vendor terms, platform limits and licence notes are in `skills/launch/references/licenses.md`. Some of them come from search previews and are marked "check before relying". Sound-effect packs stay on your machine and are never committed.

## Toolbelt

`scripts/` is a copy of the core toolbelt (Python standard library, no network access), kept identical by `tools/sync_launch_toolbelt.py`. Edit the core copy, then run the sync.

MIT licence; see `LICENSE`.
