# What `ult posts` checks

Read when `ult posts plan` or `ult posts check` prints a finding you need to explain or fix.

`ult posts plan social/plan.json [--json]` checks every post in the plan. Exit 0: no blockers. Exit 1: at least one blocker. Exit 2: the plan is not readable JSON or not a list of posts. It never posts, schedules or contacts anything.

| Code | Kind | Means | Fix |
|---|---|---|---|
| P01 | blocker | date or time is not `YYYY-MM-DD` / `HH:MM` | write a real date; time defaults to 09:00 |
| P02 | blocker | channel is not one the checks know | use a name from `ult posts specs` (or `instagram`, `youtube`, `twitter`, `fb`) |
| P03 | blocker / fix | caption over the platform limit (blocker), over the API or scheduler limit, a caption where the format shows none, or no caption (fix) | shorten; move words onto the image for stories |
| P04 | fix | no `hook_type` | name one; results compare by hook type |
| P05 | fix | a link with no `utm_source` / `utm_campaign`, or a source that does not name the channel | tag it as in `writing.md` |
| P06 | fix | more than one link | one destination per post |
| P07 | fix | image, carousel, story or pin with no `alt` | describe what is in it and why it matters |
| P08 | fix | a second post on the same channel and day | spread them out, or get the user's yes for the higher rate |
| P09 | fix | more hashtags than the platform's current cap or norm | keep a few specific ones |
| P10 | fix | first line longer than about 125 characters | put the hook first and short |
| P11 | blocker | `sponsored: true` with no disclosure in the caption and no `paid_label: true` | say "Ad" or "Paid partnership with ..." at the start, and turn on the platform label |
| P12 | blocker | `ai_generated: true` with no `ai_label: true` | turn on the platform's AI label |
| P13 | fix / blocker | a listed file is missing, or fails the file check below | export again at the right size |
| P14 | fix | the same caption twice on one channel | rewrite one; platforms push repeats down |
| P15 | fix | no link and no `next_step` | say the one action |

`ult posts check FILE... --platform P [--caption TEXT | --caption-file F] [--json]` checks finished files:

- Images (PNG, JPEG, WebP, read from the file header): wrong aspect ratio is a blocker (it will be cropped or letterboxed); smaller than the size is a fix; over 8 MB is a fix.
- Video (needs the local `ffprobe`; without it the check says so and blocks): longer than the platform allows is a blocker; over 1 GB is a blocker; no audio track is a fix; a codec other than H.264 or HEVC is a fix.
- Caption: the same caption rules as P03, P09 and P10.

The limits come from `ult posts specs`, dated; `platforms.md` says which were re-checked and how sure they are.
