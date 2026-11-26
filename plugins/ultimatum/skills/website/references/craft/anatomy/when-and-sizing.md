# Anatomy: when to draw a machine, and how big

Read when a page, app screen or docs article might need one explanatory figure, before agreeing to build it.

## What this craft is

An explainer figure shows an idea as a physical object drawn in isometric view, as SVG. The object is the explanation: a pool of connections becomes a manifold with valves, a rate limit becomes a hopper and a gate. The figure is solid (faces, shading, edges), true to a small model of the idea, and often live (it moves when the reader acts).

It is a feature figure, not a hero background and not decoration. One figure carries one idea.

## Use it when

- A concept is hard to say in a paragraph and the reader gains from seeing the parts move (how a queue backs up, how a booking slot is held, how a cache answers).
- A local business has a process that customers misjudge: how a repair, a fitting or a brewing step works. Draw the real process, with the owner's real numbers.
- An app or docs page needs an onboarding or concept figure that a screenshot cannot give.

## Do not use it when

- A photo of the real thing exists and is good. Show the photo (`../taste/photos.md`).
- The idea is a flat list or a comparison. A table or a plain diagram is clearer (`../taste/icons-and-diagrams.md`).
- The figure would be a mock-up with more detail than anyone can read. That is on the lint list in `../../website/design-rules.md` §2.
- The page already has a focal effect; a figure is a second focal point (`../taste/grounds-and-effects.md`).

## Size tiers

| Tier | Parts | Typical time | Use for |
|---|---|---|---|
| Figure | 40 to 80 | not quoted | an article or docs figure |
| Hero | 80 to 150 | a few hours | a landing-page centrepiece |
| Epic | past 150 | most of a working day or more | propose a Hero instead |

Quote no time for a Figure; for a Hero say it plainly and ask first. The standard to hold: it must look finished at 1x and still hold up at 4x close-up, so a part count that is too low reads as a toy.

## Before you start, settle

1. The one idea, in a sentence, and the true numbers behind it. Never invent figures; the owner or the brief gives them (`../taste/principles.md`).
2. Where it sits on the page and how wide, including a phone width.
3. Light or dark ground; the figure takes the page's tokens (`../taste/system.md`).
4. Whether it is live or still, and what the still version shows (reduced motion needs one, see `accessibility-and-limits.md`).
5. The weight budget: SVG size and script size (`../taste/performance.md`).

Next: `workflow.md`.
