# Intake

Goal: enough to write a one-page brief the user signs off, in as few turns as possible.

## How to ask

- **Decisions in batches.** Rounds of 5–8 questions with AskUserQuestion: mostly multiple choice, 2–4 options plus free text, your **recommended answer first** and labelled "(recommended)" so picking it is a plain yes.
- **Why-questions one at a time**, in plain chat, never batched: why this, why now, why would someone pick you. Wait for each answer; it shapes the next.
- **Vague answer → dig once** with a concrete ask: "name one person who would buy tomorrow", "what number, per month?", "which site looks the way you mean?".
- **Skip what you know** from messages, files, `brand/brand.md` or the current site, and say where you took it from.
- **"I don't know"** → suggest an answer, mark it `(guess)` in the brief, move on. Guesses show again on the brief for correction.
- **Facts before the user sees them.** Prices, vendor terms and market claims you offer as options go through the fact-finder: sourced, marked observed or guessed.
- Ask dependent topics after their parents (route after "what", budget after route).

## Topics, in order

1. **What and why.** What is launching, in one sentence; why the user is doing it; what "it worked" means in 90 days (a number if possible).
2. **Customer.** Who buys first; what they use today instead; what makes them switch.
3. **Price.** Free, one-off, subscription or per item; a rough figure; any trial or deposit.
4. **Competitors.** 2–3 names or links; what the user does better; what they refuse to copy.
5. **Reference sites.** 3–5 sites the user likes the look or feel of (any industry) and one thing about each.
6. **Must-haves.** Pages, features and integrations without which it is not a launch (booking, checkout, login, blog, languages).
7. **Deadline.** A date, an event, or "when it's good".
8. **Budget for paid tools.** Monthly ceiling for hosting, apps and AI credits; whether the user already pays for any (Shopify, Stripe, Supabase, Vercel, ElevenLabs, Suno, Higgsfield, stock or music libraries); company size (more than 3 people changes video tool licences); whether there is real footage of customers, the team or the place, and anyone willing to be filmed (it decides Brand Film).

A first round usually covers 2, 3, 6, 7 and 8 as choices; 1 and 4 come as one-at-a-time why-questions; 5 is a free-text ask.

**Brand interview hand-off.** Intake stops at what, who, price, look and limits. Voice, values, story, fonts and colours are Business's brand interview (`business/SKILL.md`), run after the brief is approved. Pass it the answers and references you gathered so it asks only what is missing.

## The brief

`ult business --start-brief` creates `.ultimatum/brief.md` with an empty `## Build brief`. Fill it so it fits on one screen:

- **Audience**, **Offer** (with price), **Main visitor action**, **Pages**
- **Known business details**: what, why, deadline, budget, company size
- **Open questions**: every `(guess)` and anything still missing
- **Checks that show it works**: the 90-day number and 2–4 launch checks
- Under it, your own lines: route picked and why, the reference sites, must-haves, competitors

Show it in plain words, then stop. Record the user's answer with `ult gate approve brief "<their words>"` or `ult gate revise brief "<their words>"`. The brief is a draft until then.

## Picking the route

| Signal in the brief | Route |
|---|---|
| Portfolio, local business, event, landing page, no logins or payments beyond a link | small site (`route-small-site.md`) |
| Accounts, subscriptions, a web app, a dashboard | SaaS (`route-saas.md`) |
| Physical or digital products sold from a catalogue, a cart, shipping | e-commerce (`route-ecommerce.md`) |
| Two of the above | the main money path's route, plus the needed section of the other |

Tell the user which route you picked and why in one line; they can override it.
