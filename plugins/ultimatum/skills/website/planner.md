# Planner: brief, mockup prompt, approval

For a new site or a major redesign. The Manager does this itself; a separate Planner or Designer agent only on a large job where the work splits cleanly.

## 1. Brief (`.ultimatum/brief.md`)

Keep it to about one screen, with these sections:

- **For whom:** the visitors and what they came for.
- **First action:** the one thing a visitor should do first (call, book, order, sign up), and where it sits.
- **Pages and sections:** each page with its sections in order.
- **Mobile:** what a 375 px visitor sees first, how the menu works, what stacks or hides.
- **Design direction** (Designer, when a new look is needed): one idea in a sentence, palette roles, type pair, image style, layout rhythm. Pick one; don't offer a menu of styles.
- **Assumptions:** what you decided without asking.
- **Placeholders:** each missing business fact written as `[[PLACEHOLDER: what goes here]]`, e.g. `[[PLACEHOLDER: opening hours]]`.
- **Phases:** 2–4 build phases, each with the check that proves it done (e.g. "Hero and menu — at 375 px the call button is visible without scrolling").
- **Browser checks:** 3–6 checks for the Reviewer: main actions, 375 and 1280 px, a keyboard path, no console errors.

Ask the user only about gaps that would change the plan itself (e.g. online ordering or not, one page or several). Everything else gets a placeholder.

## 2. Mockup prompt

Write one prompt the user can paste into ChatGPT (or any image model). It should stand alone and name:

1. The page (usually the home page) and the frame: "desktop website mockup, 1440 px wide, full page" (add a phone view only if mobile is the main concern).
2. The layout from top to bottom, section by section.
3. The main action and where it sits.
4. The visual style: mood, palette with hex values, type feel, spacing.
5. Imagery: what the photos or illustrations show.
6. Copy: the user's exact words in quotes; otherwise short realistic placeholder text, and say that it is placeholder.
7. "Flat UI mockup, no device frame, no browser chrome, readable text."

When the layout itself is the open question (unusual structure, many sections, the user is unsure), first ask for a **grayscale wireframe** of the same layout: boxes, labels and real headings, no colour or photos. Do the styled mockup after the layout is approved.

## 3. Show it and stop

- An image tool in your tool list → generate **one** mockup from the prompt (it may use the user's credits; never retry a generation silently) and show it.
- No image tool → give the prompt in a code block and ask the user to paste it into ChatGPT and bring the image back.

Then explain the idea in 3–5 plain sentences (who it is for, what they see first, why this look), list any questions from step 1, and **end your turn**. No production code until the user approves the look. Asking for changes means revise the prompt (or brief) and show it again.

## 4. Record the approval

When the user approves (in words, or with an image they bring back), record what they approved, in their terms:

`ult website --approve "<what was approved: layout, colours, type, imagery, changes asked for>" [--image <path to the mockup if saved>]`

This writes an **Approved direction** section in the brief. The Builder builds from it and the Reviewer compares the real page with it. Then continue with Build.
