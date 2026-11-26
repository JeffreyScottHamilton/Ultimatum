# Social media: scope

Settle the scope before drafting anything. Ask the opening questions in rounds of 4 with AskUserQuestion (its limit per call), recommended answer first in each list plus a "Skip, use your pick" option, and keep going with any gaps until the scope is clear. Skip any question the brand file, the build brief or the user's message already answers, and say which answers you took from where.

## Opening questions (rounds of 4)

| # | Question | Options (recommended first) | Why it matters |
|---|---|---|---|
| 1 | How big is the job? | A short campaign (one to two weeks) · one post · running a channel week to week | Sets the plan length and whether a results loop is needed |
| 2 | What format? | Short vertical video · carousel · single photo · text post | Picks the style file below |
| 3 | Which platforms? (multi-select) | The one where the audience already is · Instagram · TikTok · YouTube Shorts · LinkedIn · Facebook · other | One platform first is easier to read; more can follow |
| 4 | Do you have your own footage or photos? | Yes, raw clips or a recording · some, mixed quality · none | Own footage changes the video style and the editing path |
| 5 | Which editor do you use, if any? | None, build it here · DaVinci Resolve · Premiere Pro · Final Cut Pro | Decides whether the editors guide applies |
| 6 | When does the first piece need to go out? | In one to two weeks · this week · a fixed date (say which) | Sets how much is drafted before the first approval |

Recommend a short campaign on one platform when the user has no strong view: it gives enough posts to learn from without committing to a schedule nobody keeps.

If the format answer is video and the user is unsure about style, ask one follow-up: "Is the message a feeling carried by people, or a feature, a number or a how-it-works?" The first points to brand film or own footage, the second to motion graphics or a product demo.

## What to read next

| Answers | Style file | Video team guide | Editors guide |
|---|---|---|---|
| Video, someone talking to camera (tips, opinions, podcast or stream clips) | `styles/own-footage.md` | `creator-cut/guide.md` | Yes, when they named an editor |
| Video, own footage (event, behind the scenes) | `styles/own-footage.md` | `brand-film/guide.md` only if the user wants a produced story cut | Yes, when they named an editor |
| Video, screen recording or software walkthrough | `styles/product-demo.md` | `motion-graphics/guide.md` for titles, callouts and the end card | Yes, when they named an editor |
| Video, no footage, feature or number to explain | none | `motion-graphics/guide.md` | Only if they want to finish it in their editor |
| Video, no footage, feeling or story to carry | none | `brand-film/guide.md` | Only if they want to finish it in their editor |
| Carousel or single photo | `styles/carousel-and-stills.md` | none | No |
| Text post | none (follow `guide.md`) | none | No |

Every row also uses `guide.md` for planning, writing, review and approval. When the editors guide applies, read `editors/guide.md` first; it picks between live control, a timeline file and building the cut here.

## Running a channel

When the answer to question 1 is "running a channel", add these steps after the opening rounds.

### Content pillars

Agree three or four pillars: recurring themes the account returns to. Each pillar names the audience question it answers and one example post. A fictional bakery might use:

| Pillar | Audience question | Example |
|---|---|---|
| How it is made | "Is this worth the price?" | Shaping the morning loaves, 20 seconds |
| What is new | "What can I get this week?" | Carousel of the weekend specials |
| People | "Who runs this place?" | The baker answers one customer question |
| Proof | "Do other people like it?" | A regular's quote, with their written permission |

Write the pillars into `brand/brand.md` so later sessions keep to them.

### Cadence

Pick a posting rate the user can keep up for a month, not the highest one they can imagine. Ask how many hours a week they can give to filming, reviewing and replying. Two or three posts a week on one platform is a common starting point (rule of thumb, not a benchmark). Raising the rate later needs its own yes.

### Four-week calendar

Draft a calendar in a table: week, day, platform, pillar, format, hook line, the one next step the post asks for, and status (idea, drafted, approved, posted). Fill week one in full and leave weeks two to four as ideas; they change after the first results review. Show the calendar and wait for the user's yes before drafting week two.

### Weekly results review

Once a week, with the user:

1. Pull the numbers for each post from the platform's own analytics: reach or views, the share who watched past the opening, saves and shares, profile visits, link clicks, and the result that matters (sign-ups, bookings, sales). Write "not available" for anything the platform does not show; never estimate it.
2. Record the week with `ult social --results "<what was measured>"`.
3. Compare the top three and bottom three posts. Look for one difference: the hook, the format, the pillar, the length or the posting time.
4. Choose one change for next week and write down what it should move. Keep everything else the same so the change can be read.
5. Note the learning in `brand/brand.md`.

### What to change, and when

| What you see | Likely cause | One change to try |
|---|---|---|
| Few views on every post | Weak opening or the wrong platform | Rewrite the first line and first frame; test one post on the second platform |
| Views but no one watches past the opening | Hook promises something the video does not deliver early | Show the result in the first two seconds |
| Watched, but no clicks or sign-ups | The next step is missing or vague | One clear next step, said and shown, with a tracked link |
| One pillar beats the others for three weeks | The audience wants that topic | Give it an extra slot; keep the others alive at a lower rate |
| Comments ask the same question | Content gap | Make the answer a post |
| User cannot keep the cadence | Plan too heavy | Drop a post a week before quality slips |

Give a change at least a week before judging it, longer when numbers are small.
