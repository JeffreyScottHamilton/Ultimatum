# Copy and proof

Read when writing or rewriting a page, or when the owner sends a draft to improve. The basics (headline patterns, button wording, service and about templates) are in `../../copy.md`; this file covers finding the message, editing in passes, and proof.

## 1. Find the message before writing

Answer these in one short block and show it to the owner before any page copy. If a line is blank, ask; don't guess.

| Question | Where the answer comes from |
|---|---|
| Who arrives on this page, and from where? | intake, search terms, the link they clicked |
| What were they trying to fix when they searched? | enquiry emails, reviews, the owner's "first question customers ask" |
| What do they fear will go wrong? | complaints about competitors, refund reasons, review worries ("turned up late", "hidden fees") |
| Why this business and not the next result? | a fact a customer would notice: hours, speed, guarantee, specialism, place |
| What one action do we want? | the brief's main action |
| What proof do we hold? | real reviews, counts, licences, photos, named clients with consent |

Write the message as one sentence: *For [who] who [situation], [business] [result] because [the reason to believe].* Every section of the page should support that sentence; cut sections that don't.

**Mine customer words.** Read 20 or more real reviews (the owner's and two competitors'), enquiry emails or call notes. Copy phrases that repeat, sorted into: the problem, the moment they decided, the worry, the result. Headlines built from those phrases beat ones written from the owner's point of view. Quote reviews only from the owner's own customers, and only on the owner's site with permission.

## 2. Draft

- Open with the result for the visitor, in their words. Then what is offered, then how it works, then who you are.
- One idea per section, each with its own heading a skimmer can follow down the page.
- Swap every feature for what it means: "open until 8pm" → "come after work"; then keep the feature too, since it is the proof.
- Specific beats big: a time, a place, a number, a name. "Most repairs in one visit" says more than "fast service".
- Answer the top three worries on the page itself, near the button, not only in an FAQ.
- Give the owner three headline options built from different angles (result, proof, situation). Never pick for them.

## 3. Edit in passes

Edit one concern at a time. A single pass that tries to fix everything misses most of it.

1. **Point.** Can you state each section's job in five words? If not, merge or cut it.
2. **Plain.** Replace words the customer wouldn't say. Run `ult copylint` for the filler list; it fails banned words and caps over-used devices.
3. **Proof.** Every claim gets a source next to it in your notes: review link, count, certificate. No source: soften it to a fact you hold, or flag it for the owner.
4. **Specific.** Circle every vague word (quality, solutions, professional, affordable). Replace each with the fact behind it or delete it.
5. **Risk.** Read as a nervous first-time buyer. Where would you stop? Add the missing answer: price, time, what happens after the click, how to cancel.
6. **Read aloud.** Anything you stumble on gets shorter.

Keep a short change log for the owner: line before, line after, why. They approve each change to a claim.

## 4. Proof that holds up

| Proof | Use it when | Rules |
|---|---|---|
| Review quote | always, near the button | exact words; trim only with "…"; first name and town or source as the reviewer allowed |
| Rating and count | the platform count is real today | name the platform; recheck on launch day |
| Count of jobs, years, clients | the owner can show records | round down, never up |
| Photos of real work | trades, food, places | the owner's own photos; say when a photo is illustrative |
| Licence, insurance, membership | regulated trades | number or link the visitor can check |
| Named client or logo | with written consent | no logos of companies that were only trial users |
| Guarantee | the owner will honour it | terms in plain words next to it (see `offers-and-pricing.md` §3) |

Never write fake reviews, buy them, offer rewards only for positive ones, or show only the good ones while claiming to show all. Health, legal and financial outcomes need careful wording; the `ultimatum:compliance-reviewer` agent checks every public page.

## 5. Page types beyond the basics

**Landing page for one offer.** No main navigation. Headline, the situation, the offer, proof, the worry answers, the button, repeated once lower down. One form or one booking link.

**Comparison page ("us vs them", "alternatives to X").** Only when the owner asks and only with facts dated and checked on the competitor's own pages. Say where the competitor is the better fit; readers trust a page that admits it. Put a "checked on [date]" line under any table of their prices or features. Never use their logo or imply partnership.

**FAQ.** Real questions from customers, short answers, each linking to the page that goes deeper. Don't pad it to look complete.

## 6. Before handing over

- [ ] The message sentence is on top of the copy doc and the owner agreed it.
- [ ] Each claim has its source or a flag.
- [ ] `ult copylint` passes on the built pages.
- [ ] `ult market page` shows no fails (titles, descriptions, link text).
- [ ] The change log is ready for the owner.
