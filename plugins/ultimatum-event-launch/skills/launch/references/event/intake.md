# Event intake

Ask in rounds of 5-8 questions with AskUserQuestion, mostly multiple choice, recommended answer first. Skip anything the user's message, `brand/brand.md` or an existing brief already answers, and say where you took it from. Ask "why" questions one at a time, in plain chat, after the rounds.

## Round 1: the event

| # | Question | Options (recommended first) |
|---|---|---|
| 1 | What kind of event? | Workshop or class · talk or meetup · show or performance · opening or pop-up · webinar · fundraiser · small conference |
| 2 | Date and start time? | Free text; ask for the time zone if online |
| 3 | Where? | In person · online · hybrid |
| 4 | How many people can attend? | A number; "no limit" for online |
| 5 | Free or paid? | Paid, one price · free with sign-up · pay what you can or donation · paid with tiers |
| 6 | If paid, what price? | Free text; mark "(guess)" if not decided |
| 7 | Is this the first time you run it? | First time · run before (ask for last numbers) · a series |

If the event is a wedding, a private party or festival logistics, say in one line that the plugin covers public events, and offer help only with public-facing parts.

## Round 2: people and reach

| # | Question | Options (recommended first) |
|---|---|---|
| 1 | Who is it for? | Free text: who they are and what they want from it |
| 2 | Where do they gather already? | A local community or group · a social platform · an email list · a venue's regulars · a partner organisation |
| 3 | Do you have a list? | Email list (size) · social following (size) · past attendees · none yet |
| 4 | Budget for promotion? | None, organic only · small, with a fixed cap · a set amount |
| 5 | Venue status? | Booked and confirmed · held, not confirmed · still looking · online platform chosen |
| 6 | Speakers, hosts or performers? | Confirmed · some confirmed · none needed |
| 7 | What makes it a success? | A number of sign-ups · revenue · people who come back or buy after · press or partner interest |

## Round 3: practical (only what applies)

- Sign-up or ticketing tool already in use, if any.
- Website or event page already live, and who controls it.
- Photos or video from past events, and whether people in them agreed to their use.
- Accessibility at the venue: step-free access, seating, hearing support; captions online.
- Who helps on the day.

## "Why" questions (one at a time)

1. Why would someone give up an evening or a fee for this? What do they leave with?
2. Why now: what makes this date or this year the right time?
3. Why you: what does the host know or have that others do not?

Write the answers in the user's words; they become the headline and the first posts.

## Filling `## Build brief`

After the rounds, run `ult business --start-brief` and fill the section like this (fictional example):

```
## Build brief

- Event: Beginner wheel-throwing workshop, "First Bowl"
- Date: Saturday 14 March, 10:00-13:00 (in person)
- Place: Clayhouse Studio, confirmed
- Capacity: 10 wheels; waitlist after that
- Price: paid, one price (guess, owner to confirm)
- Audience: adults new to pottery who live nearby and want a screen-free weekend activity
- Where they gather: a local neighbourhood group, the studio's followers, a nearby cafe
- List: about 300 newsletter readers, 1,200 followers (owner's figures)
- Budget: organic only
- Hosts: studio owner, one assistant
- Goal: sell out 10 places; 3 people book the follow-up course
- Why: leave with a bowl you made and know whether the course is for you
- Lead time: 6 weeks (standard plan)
- Out of scope: none
- Open questions: refund policy; photo consent at the session
```

Show the brief, then stop and wait. Yes: `ult gate approve brief "<their words>"`. Changes: `ult gate revise brief "<their words>"`, edit, show again.
