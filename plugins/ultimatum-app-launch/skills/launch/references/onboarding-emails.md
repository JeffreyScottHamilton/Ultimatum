# Onboarding email sequence

Emails from sign-up to the end of the trial, built around the aha moment defined in `activation.md`. Timings are rules of thumb, not rules; adjust to how long the product takes to show value. Sending email is an action: the user approves the sequence before it is switched on, and each broadcast needs its own yes.

## Before writing

1. The aha sentence and the activation event (from `activation.md`).
2. The 3-5 steps between sign-up and aha, each with a direct link into the product.
3. A reply-to address a person reads.
4. The tool: the product's own email code (coding work, done in a coding session), or an email platform. Use events from the product to start and stop emails; a fixed timetable that ignores what the user did sends the wrong message.
5. Legal basics: transactional email (receipts, password resets) differs from marketing email; marketing needs consent where the law requires it, plus an unsubscribe link and a postal address in some places (check before relying: rules where the users are).

## The sequence (example for a 14-day trial)

| # | When | Sent to | Subject idea | Body (one job each) |
|---|---|---|---|---|
| 1 | Right after sign-up | Everyone | "Welcome to [product] – your first step" | One sentence of welcome, one link to the first step, the reply-to invite ("hit reply if you get stuck") |
| 2 | Day 1, if not activated | Not yet at aha | "The quickest way to [aha outcome]" | The single step most people miss, with a link straight to it; a 30-second screenshot or GIF |
| 3 | Day 3, if not activated | Not yet at aha | "Stuck on [step]? Here is a shortcut" | Offer a template, sample data or a short call; ask one question: what were you hoping to do? |
| 3b | When aha happens | Just activated | "Nice – you [did the thing]" | Congratulate in one line; show the next most useful feature |
| 4 | Day 7 | Activated users | "[Product] tip: [feature]" | One feature that deepens use, linked to a real example |
| 5 | 3 days before trial end | Everyone on trial | "Your trial ends on [date]" | What happens at the end (charged, or access stops), the price, how to choose a plan, how to cancel; no pressure language |
| 6 | Trial end day | Did not convert | "Your trial has ended" | What they keep (data kept for [period], if true), how to come back, one question: what was missing? |

Rules:
- Stop the "not activated" emails the moment the user activates.
- One link, one ask per email. Plain text or very light design; it should look like a person wrote it.
- The trial-end emails must match the pricing page and terms exactly: price, date, what happens to data.
- No fake urgency, no fake "only 2 spots left", no countdowns that reset.

## Example copy (email 2, made-up product)

> Subject: The quickest way to your first invoice
>
> Hi [first name],
>
> Most people get their first invoice out in under five minutes once they add a client. That is the step to do next: [Add your first client →]
>
> If something is in the way, reply to this email; it comes to me.
>
> [Name], [Product]

Rewrite in the brand voice from `brand/brand.md`; keep the shape.

## What to measure

| Measure | Read it as |
|---|---|
| Open rate | Weak signal; privacy features in mail apps distort it (check before relying) |
| Click to the linked step | Did the email send people to the right place? |
| Activation rate, with and without the email | The real test; compare cohorts by week |
| Replies | The richest source of onboarding fixes; read every one |
| Unsubscribes and spam complaints | Too many emails or the wrong audience |

Change one email at a time and compare a week of sign-ups before and after.

## Beginner mistakes

| Mistake | Fix |
|---|---|
| Same timetable for everyone | Branch on activation; stop nudges once they activate |
| Welcome email lists every feature | One step, one link |
| Sent from no-reply | Use a monitored reply-to address |
| Trial-end email that surprises with a charge | Send it before the end, state date and amount |
| Turning on marketing emails for people who never agreed | Check consent rules; transactional only until they opt in |
| Testing only in one mail app | Send each email to a few providers and read it on a phone |
| Links that go to the home page or log-in screen | Deep-link to the exact step; check it works after log-in |
