# Slides: grid, type, layouts and colour

Read after `story.md` has a slide list. Every slide here assumes one message, stated in the headline.

## 1. The canvas

- Design at 1920×1080 (16:9). Use 4:3 only if the room's projector or the owner's template needs it.
- Keep a safe margin of about 80 px on every side for text and key images; projectors and video calls crop edges.
- Use a 12-column grid with gutters of 24–40 px so slides line up with each other. The headline sits in the same place on every content slide; the audience learns where to look.
- Number every slide except the title, small, in a corner, so people can say "go back to 7".

## 2. Type that reads across a room

At 1920×1080, as CSS pixels:

| Role | Presented in a room | Read on a screen or sent as PDF |
|---|---|---|
| Title slide headline | 96–140 | 72–110 |
| Slide headline | 56–72 | 44–56 |
| Body and bullets | 32–40 | 24–30 |
| Big number | 140–240 | 110–180 |
| Labels, captions, sources | 24–28 | 18–22 |

Nothing an audience must read goes below 24 px on a presented deck. Body line height 1.3–1.4, headlines 1.05–1.15. Two faces at most; one is often better. The display face has to hold up at 200 px.

Word budget for a presented slide: a headline of up to 15 words, plus up to about 30 words of support. More than that and people read instead of listening; move the rest to speaker notes.

## 3. Layouts most decks need

| Layout | Use for | Shape |
|---|---|---|
| Title | slide 1 | name and one-line description, lots of space, logo small |
| Statement | the point, a turn in the story | one sentence, very large, nothing else |
| Big number | one metric that matters | the number huge, a label, the comparison ("up from …"), the source |
| Number row | 3–4 metrics together | equal columns, same format for every number, one highlighted at most |
| Split | claim and evidence | headline and two or three lines on one side, image, screenshot or chart on the other |
| Full image | a moment, a user, a place | edge-to-edge photo, headline on a dark or light scrim with enough contrast |
| Screenshot | the product | the screen big, cropped to the part that matters, a callout or two |
| Chart | one trend or comparison | headline states the finding; chart takes two thirds of the slide; see `charts.md` |
| Three ideas | features, pillars, steps | three columns or rows; each a short heading and one line; an icon only if it helps tell them apart |
| Before and after | change, comparison | two halves with the same structure so the difference is obvious |
| Timeline | roadmap, history, plan | left to right, few points, dates aligned, "now" marked |
| Quote | customer proof | the words large, name and role, photo optional, nothing else |
| Team | who we are | faces at the same size and crop, name, role, one relevant fact |
| Table | competition, pricing | few rows and columns, your column highlighted, ticks only where honest |
| Ask | the last slide | the amount or decision, what it buys, contact, nothing to distract |

Vary layouts in a sequence so slides do not blur together, but keep the headline position and margins fixed. A statement slide every four to six slides resets attention.

## 4. Bullets

- Three to five bullets, one line each, no sub-bullets. If you need sub-bullets, you need another slide.
- Start each bullet with the important word. Parallel grammar: all verbs, or all nouns.
- Reveal bullets one at a time only when you will talk to each one; otherwise show them together.
- Ask whether the bullets should be a layout instead: three items side by side, a number row, a before and after.

## 5. Colour and backgrounds

- Build the palette from the brand or the site: one background, one text colour, one accent, one muted tone for labels and lines. The accent marks the one thing to look at on each slide, so use it sparingly.
- Light or dark: dark backgrounds suit dim rooms and screens; light backgrounds survive bright rooms, cheap projectors and printing. If unsure, light, and test on a projector if one is available.
- Contrast: body text at least 4.5:1 against its background, large text at least 3:1. Projectors wash out colour, so aim higher than the minimum.
- Photos behind text need a scrim (a solid or gradient overlay) or a calm area of the photo; check every slide where text sits on an image.
- Colour must not be the only way to tell things apart in a chart or table; add labels or patterns.

## 6. Images and screenshots

- Real product screenshots beat illustrations; crop to the part that matters and enlarge it until it reads.
- Photos of real people and places beat stock; when stock is used, check the licence (`../../shared/licenses.md`) and avoid the obvious handshake and laptop shots.
- One image per slide, large. A collage of small images says nothing.
- Every image has alt text in an HTML deck, and a short description in the notes for anyone reading the PDF with a screen reader.

## 7. Motion

Slides move only to show change: a number counting to its value, a bar growing, a before turning into an after. Keep transitions to a short fade or none. No spins, bounces or flying text. Respect reduced motion in HTML decks (`../emil-motion/index.md` for timing).
