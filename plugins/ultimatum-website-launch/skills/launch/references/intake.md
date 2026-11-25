# Intake: website launch

Goal: enough for a one-page brief the owner signs off, in few turns.

## How to ask

- Rounds of 4 questions with AskUserQuestion (its limit per call), repeated until every brief field is filled; expect 4-6 rounds on a real launch. Each question: 2-3 options plus free text, your **recommended answer first** labelled "(recommended)", and a last option "Skip, use your pick" (record it as `(your pick)` in the brief). Group each round by topic; after each round, say in one line which fields are still empty.
- "Why" questions (why now, why would someone pick you) go one at a time in chat.
- Vague answer: dig once with a concrete ask ("what did your last three customers ask first?").
- Skip what you already know from files, the current site or earlier answers, and say where it came from.
- "I don't know": suggest an answer, mark it `(guess)` in the brief.
- Any price, fee or vendor term you offer as an option goes through the fact-finder first and is marked "check before relying" until read on the vendor's page.

## Round 1: the business and the goal

1. **Business type.** Local service or trades; restaurant or cafe; salon or clinic; agency, consultant or coach; portfolio or creator. (Recommended: whichever the owner names; it sets the page list.)
2. **The one action.** Call, book online, send an enquiry or quote request, visit in person, buy a service, or join a list. (Recommended: pick one primary action; a second is allowed but secondary.)
3. **Service area.** One address, a radius or list of towns, online only. (Recommended: list the towns; each can later get its own page.)
4. **Hours and response time.** Fixed hours, by appointment, seasonal; how fast the owner replies to an enquiry. (Recommended: show real hours and a real reply time.)
5. **Proof.** Reviews, before-and-after photos, credentials or licences, awards, client names, press. Ask which exist right now. (Recommended: three real reviews plus one credential beats long copy.)
6. **Existing assets.** Domain, current site, Google Business Profile, social pages, directory listings. (Recommended: keep the domain and the listings; replace only the site.)

## Round 2: tools, content, limits

7. **Booking tool.** None yet, a tool already paid for, a phone or email only flow. (Recommended: the simplest tool that sends the owner a confirmation. Plans and fees: check before relying.)
8. **Content the owner can supply.** Own photos, a logo, service list with prices, an about story, testimonials, a short phone video. (Recommended: owner photos of the real place and people over stock.)
9. **Date.** A fixed date (opening, season, event) or "when it is good". (Recommended: a date with a two-day buffer.)
10. **Budget.** Monthly ceiling for hosting, domain, booking tool and any AI or stock credits; who pays for them. (Recommended: start with free or low tiers; confirm current terms on vendor pages.)

After round 1, read the type's section in `by-business-type.md` and add its few specific asks (menu, treatment list, licences, case studies, timetable) to round 2.

Add one free-text ask: 3 sites the owner likes the look of, and one thing about each. Ask one-at-a-time in chat: "Why would a stranger pick you over the nearest alternative?" Also ask if there is real footage and anyone willing to be filmed; that decides the video style (see `route.md`).

## Brand interview

Voice, values, story, fonts and colours belong to the Business team after the brief is approved. Pass it what you gathered so it asks only what is missing.

## Filling the brief

`ult business --start-brief` creates `.ultimatum/brief.md`. Fill `## Build brief` so it fits on one screen:

| Brief line | From |
|---|---|
| Audience | business type, service area, who calls or books today |
| Offer (with price) | services list; prices marked "check before relying" if from memory |
| Main visitor action | question 2 |
| Pages | route.md size choice plus any service-area pages |
| Known business details | hours, area, booking tool, existing assets, date, budget |
| Open questions | every `(guess)` and missing proof or photo |
| Checks that show it works | a 30-day number (enquiries, bookings or calls) and 2-4 launch checks from `launch-checklist.md` |

Below it add your lines: route and size picked and why, reference sites, competitors, must-haves. Show it in plain words and stop. Record the answer with `ult gate approve brief "<their words>"` or `ult gate revise brief "<their words>"`.
