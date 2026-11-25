# Intake for a software product

Goal: enough to write a one-page brief the user signs off, in few turns.

## How to ask

- Rounds of 4 questions with AskUserQuestion (its limit per call), repeated until every brief field is filled; expect 4-6 rounds on a real launch. Each question: 2-3 options plus free text, your **recommended answer first** labelled "(recommended)", and a last option "Skip, use your pick" (record it as `(your pick)` in the brief). Group each round by topic; after each round, say in one line which fields are still empty.
- "Why" questions go one at a time in plain chat: why this, why now, why would someone switch to you. Wait for each answer.
- Vague answer: dig once with a concrete ask ("name one person who would pay tomorrow").
- Skip what the repo, README, site or earlier answers already say, and say where you took it.
- "I don't know": suggest an answer, mark it `(guess)` in the brief, move on.
- Prices, competitor facts and vendor terms you offer as options go through the fact-finder first.
- Brand voice, colours and fonts belong to Business after the brief. Do not ask them here.

## Batch 1: the product (choices)

1. **Who is it for?** Solo users or consumers / small teams / mid-size or enterprise companies / developers (recommended: whichever the user names first; ask for one named example).
2. **The job.** One sentence: "helps [who] do [what] without [pain]". Free text, one at a time if unclear.
3. **Stage.** Idea / waitlist open / private beta / live and quiet (recommended: be honest; the stage picks the launch path in `route.md`).
4. **How people buy.** Self-serve sign-up / sales-led demo call / both. Recommended: self-serve when one person can decide and pay with a card; sales-led when buyers need a security review, a contract or several approvers (rule of thumb).
5. **Pricing model.** Free / freemium / free trial / paid only; flat, tiered, per seat or usage. If unsure, recommend tiered with a trial and read `pricing-and-billing.md`.
6. **Platforms.** Web / iOS and Android / desktop / API only / browser extension.
7. **Integrations that must exist** at launch (sign-in with Google, Slack, Stripe, calendar, import from a competitor). Free text.

## Batch 2: risk and reach (choices)

1. **Data handled.** None personal / emails and names / business data / payments / health, children or finance (the last needs a careful legal look; recommend asking a professional).
2. **Launch channels.** Waitlist email / Product Hunt / Hacker News / communities and forums / founder social posts / paid ads / partners. Recommend two or three, not all.
3. **Date.** Fixed date or event / within a month / when it is good (recommended: a date, even a soft one).
4. **Budget.** Monthly ceiling for hosting, tools, ads and AI credits; tools already paid for (hosting, billing, database, email, analytics); company size (above 3 people changes some video tool licences, see the rows in `shared/licenses.md`).
5. **Evidence.** Real footage, screen recordings, customer quotes, logos allowed? Anyone willing to appear on camera?

## One at a time

- What does "it worked" mean in 90 days (sign-ups, paying accounts, MRR)?
- Who do users use today instead, and what makes them switch? Two or three competitor names or links.
- Three to five sites the user likes the look of, and one thing about each.

## Filling the brief

Run `ult business --start-brief`, then fill `## Build brief` so it fits one screen:

- **Audience**, **Offer** (plan names and prices, marked guess if so), **Main visitor action** (join waitlist, start trial, book demo), **Pages**.
- **Known business details**: job, stage, buying path, platforms, integrations, data handled, date, budget, company size.
- **Open questions**: every `(guess)` and anything missing.
- **Checks that show it works**: the 90-day number plus 2–4 launch checks (sign-up works, test payment works, privacy page live, demo video checked).
- Under it, your own lines: route and why, channels, competitors, references.

Show it in plain words and stop. The brief stays a draft until `ult gate approve brief "<their words>"`.
