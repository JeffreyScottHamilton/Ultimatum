# First impression, trunk test and critique voice

Read at the start of every page audit, before measuring anything. The gut read comes first because it is the one thing measurement cannot recover.

## Step 1: the gut read

Take one full-page desktop screenshot (1440 wide) and one first-screen shot at 390 wide, then write four lines before opening devtools:

1. "This page says **[what]**": the message at a glance. Competence, play, confusion?
2. "I notice **[specific thing]**": what stands out, good or bad.
3. "My eye lands on **[1]**, then **[2]**, then **[3]**": is that the order the author meant? If not, the hierarchy is lying.
4. "In one word: **[word]**."

**Narration variant.** Write as a stranger in the first person, meeting the page cold: name every element, say where it sits and how much weight it carries. Anything you cannot name is filler.

**Area test.** Name the job of every clearly bounded area in two seconds each. List the ones you could not name; those areas are poorly defined.

## Five-second test

Without scrolling: what is it, who is it for, what is the one action? A local business also needs where, when and how to reach them (phone, address, hours, booking). An app needs the product shown working, not described.

## Trunk test (every page)

Imagine landing here from nowhere. Can you tell, immediately:

1. Which site this is.
2. Which page you are on.
3. The main sections of the site.
4. What you can do on this page.
5. Where you sit in the structure (breadcrumb, highlighted nav item).
6. How to search or find things (only when the site is big enough to need that).

All six: pass. Four or five: partial. Three or fewer: fail, which is a high-impact finding no matter how handsome the page is.

## Critique voice

Phrase each finding in one of four ways, tied to what the visitor is trying to do and ending with a concrete improvement:

- "I notice..." (an observation)
- "I wonder..." (a question the design leaves open)
- "What if..." (a suggestion)
- "I think... because..." (a reasoned opinion)

Never "feels off" without the principle it breaks. Each finding carries: impact (high, medium or polish), category (the ten in `checklist-visual.md` and `checklist-behaviour.md`), evidence (screenshot name or measured value), and a fix a developer can do.

## Quick wins list

At the end of the audit, list 3 to 5 fixes under half an hour each, ordered by gain. Typical sources: a missing focus ring, one overlong paragraph, a button label that says "Submit", an unthemed selection colour, a missing empty state.

## Where this overlaps the house rules

`../../website/design-rules.md` § 1 already asks for a three-line plan and a de-generic pass; the gut read and area test are the audit-side partners of that. Merge notes are in the coverage file.
