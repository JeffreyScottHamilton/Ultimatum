# Design brief pass

Read when you build or reshape a user interface from a brief and want a short plan, checked against the brief, before writing code. The design rules themselves live in the website craft files; this one adds the plan-and-review step and a few points they leave out.

## 1. Where the rules already are

- Generated-page tells and how to grade them: `../../../../website/references/craft/design-review-qa/slop-tells.md`.
- Direction, type and layout principles: `../../../../website/references/craft/hallmark/principles.md` and `../../../../website/references/craft/taste/system.md`.
- Interface copy (button names, errors, empty states): `../../../../website/references/copy.md` and `../../../../website/references/craft/design-review-qa/checklist-behaviour.md`.
- Engineering-side UI checks: `../../ui.md` and `../../design/design.md`.

## 2. Ground the plan in the subject

If the brief does not say what the product is, who it is for and what the page must do, propose one answer to each and confirm it in one message. Distinct visual choices come from the subject's own world: its materials, its jargon, the objects its users handle. Use the brief's real content in the build; invented filler makes any layout look generic.

## 3. Two passes before code

1. **Plan** in a few lines:
   - colour: four to six named hex values;
   - type: the faces and the role of each;
   - layout: one sentence per section, plus a rough ASCII sketch when comparing two arrangements, and the alignment rule;
   - principles: two or three lines on what makes this page belong to this brief.
2. **Review the plan against the brief.** For each part, ask: would a similar brief from a different client get the same answer? If yes, it is a default, not a choice. Change it and write one line on what changed and why. Where the brief itself asks for a look, follow the brief, even when that look is a common one.

Only then write code, from the revised plan.

## 4. Points the other files leave out

- One loud element per page. Pick it, then keep everything around it plain.
- Numbered markers (01, 02, 03) only when the content is a real sequence (steps, a timeline).
- Motion the user did not ask for: one orchestrated moment at most. Motion that answers an action (open, expand, confirm) is welcome when it shows what changed.
- CSS: watch selector weight when a section class and an element class both set spacing; the heavier one wins silently and the gap between sections drifts. Check computed values in the browser rather than reading the stylesheet.
- One verb per action through the whole flow: the button that says "Publish" leads to a notice that says "Published".
- Errors say what happened and how to fix it, in the product's voice. An apology alone is not a message, and vague wording ("something went wrong") leaves the user stuck.
- Before calling it done, remove one decoration and see whether anything was lost. Then take a screenshot at phone and desktop width and read it back (`../../browser-verification.md` § 5).
