# Plan

Read once scope is settled, to build the calendar.

## Pillars (when running a channel)

Agree three or four recurring themes. Each names the audience question it answers and one example. A fictional bike repair shop:

| Pillar | Audience question | Example |
|---|---|---|
| How it is done | "Can I fix this myself?" | A 20-second chain clean |
| What is new | "What can I get this week?" | Carousel of the spring service deal |
| People | "Who will touch my bike?" | The mechanic answers one customer question |
| Proof | "Do other riders trust them?" | A customer quote, with their written permission |

Write the pillars into `brand/brand.md`.

## Cadence

Pick a rate the user can keep for a month: ask how many hours a week they have for making, checking and replying. Two or three posts a week on one channel is a common start (rule of thumb, not a benchmark). One post a day per channel at most to begin; a higher rate or a second channel needs its own yes. About one post in five tries a new format or hook type.

## The plan file

`social/plan.json` holds the scope and every post. One object per post:

```json
{"scope": {"job": "campaign", "channel": "instagram", "action": "book a service"},
 "posts": [
  {"date": "2026-12-01", "time": "18:30", "channel": "instagram", "format": "carousel",
   "pillar": "how it is done", "hook_type": "mistake",
   "caption": "Three chain mistakes that cost you a new cassette...",
   "link": "https://example.com/book?utm_source=instagram&utm_medium=social&utm_campaign=spring",
   "alt": "Close-up of a rusty chain next to a clean one", "files": ["social/out/chain-1.png"],
   "sponsored": false, "ai_generated": false, "status": "draft"}
 ]}
```

Channel names: the keys in `ult posts specs`, or `instagram`, `youtube`, `twitter`, `fb`. Optional fields: `next_step` (when there is no link), `paid_label` (the platform's paid-partnership label is on), `ai_label` (the platform's AI label is on), `pillar`, `status`.

## Four weeks at a time

Fill week one in full; leave weeks two to four as ideas, since the first results change them. Run `ult posts plan social/plan.json`, fix every blocker, then show week one and wait for a yes before drafting week two.

Hand-over files: `ult posts calendar social/plan.json` writes a CSV for a scheduler's bulk import (columns date, time, channel, format, hook_type, caption, link, file, status); `--to ics` writes a calendar file for the user's own calendar. Neither posts anything.
