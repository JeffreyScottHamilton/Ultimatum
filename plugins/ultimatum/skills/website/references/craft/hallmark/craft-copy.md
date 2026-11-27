# Craft: copy, opening a section and missing facts

Read before writing any words, when a section needs an opening, and whenever the prompt leaves a fact out. Longer copy rules for local sites are in `../../copy.md` and `../taste/copy.md`; this file adds the budgets, the opening moves and the slot rules.

## Voice and budgets

Write the way the owner would speak across a counter: draw on the brief's nouns, name a real place, quote a number the owner gave, and choose the verb a customer would use.

- **Swap test.** If a headline would work on a rival's page, add a noun only this business has. "Software that works for you" fits everyone; "Invoices that chase late payers" fits one product.
- **Three questions per line.** Test each line: a reader should be able to picture it, it should be falsifiable, and no other business could say it. Concrete beats clever: name the place, the hour, the material or the result. A pun is a second-draft move and appears once a page at most.
- **Subheads** state what the thing is, who it serves and the one difference, in a dozen words at most. **Section heads** tell the visitor what they will see or get ("Fresh rye every morning") and never use a category label such as Features, Our story or Why us. One-word stage names are fine in a staged shape.
- **Rhythm.** Pair a short line with a longer one, prefer verbs to adjectives, give each sentence one idea, and skip triads of adjectives.
- **Budget (gate 58).** Headline: at most 7 words. Section heads: at most 6. Intros: one line. Paragraphs: two brief sentences. Lists: four items, each with a label of three words and a line of ten (five when steps cannot be merged, and a table beyond that). Tables: up to five rows. A set the owner supplied keeps its real count. No more than 450 visible words a page. Test: read the headings and hero alone, and if they tell the story, the length is right.
- **Refuse the generated voice.** Gate 19's buzzword list, plus "Reimagine", "Whether you are X or Y", "It is not just X, it is Y", "Say goodbye to", "game-changer", "journey", titles built on a colon, "Click here", "Enter your email below", and version strings in marketing copy.
- **Buttons** name the action's verb ("Book a fitting"); "Continue" is only for the second step of a flow. **Errors** say what happened, why if known, and what to do, with no "Oops" and no exclamation marks. **Empty states** say what is empty, why it matters and offer one action. **Loading** shows a spinner after 150–300ms, held for at least 300ms and placed beside the label, switching to text after 2s.
- **Sample data** in a built product uses `example.com`, field names from the brief and values that read as samples (round amounts, "Example Kitchen"). Never include a figure a visitor could mistake for a claim.
- **Punctuation.** Curly quotes, a true ellipsis and apostrophe, no double hyphen and no em or en dash (use a comma, colon, full stop or brackets), and a non-breaking space ahead of units. Put a full stop after standalone sentences but not after list items.

Merged with `../../copy.md` (button wording, swap tests) and `../../website/design-rules.md` § 2 (stock words, em dashes, fake stats); local-business additions (phone number, hours, "call us" verbs) stay in those files.

## Opening a section

Writers habitually put a small tracked-caps label over the heading, and that habit gives the page away (gate 54). Ask what the reader still lacks. When the answer is nothing, open with nothing. When there is something, anchor it to a fact, an identifier or a destination, and not to a name for what follows. There are twelve ways in:

1. Nothing: space above and the heading flush.
2. A heading that announces itself, with its subject in the first two words. Usually the best option.
3. A lead-in set in a heavier weight inside the paragraph, never on a line of its own.
4. A drop cap on the first paragraph, once a page.
5. A rule with a bigger job than dividing: hairline, fleuron, double rule, coloured edge or plain gap, varied from seam to seam.
6. A graphic-scale numeral (`clamp(6rem, 16vw, 14rem)`), once a page and only if the number is real and central (an issue, a year, the offer's price).
7. A real `<ol>` with CSS counters, when the order is genuine.
8. A caption underneath the content in place of a label above.
9. Marginalia in the outer margin next to the body.
10. A switch of paper, so the band edge does the breaking.
11. A running head or a folio; it passes because it stays put and never announces.
12. A sticky heading that remains visible as content scrolls under it.

A section may combine two moves, but three is noise, so rotate against the log. Small type is legitimate when it names something that is actually there: figcaption, `th`, `label`, `legend`, nav or tab labels, a byline or `time`, a unit following its figure, a genuine filename on a code block, a live `role="status"` chip, an announcement that links somewhere real, or a plan name.

## Missing facts

- **A fact the brief omitted** (venue, date, price) turns into a text slot and never an invented value: a span with a `data-fill` name, in the muted colour, inside a dashed outline, so it looks like a blank and not a link. Allow two per page at most and list each in the handoff. When the anatomy asks for more facts than the owner gave, slot only the two a visitor needs in order to act and leave the others to the handoff. Remove any row or line whose only content would be a missing fact.
- **A typeface the page is about** that the owner has not supplied is treated as a font slot. Name it first in the display token, a free face with the same build stands in under a single caption, a waiver for gate 37 goes in the stamp, and the handoff requests the files.
- **A section the owner named but supplied nothing for** gets its heading, one line on what is coming, and one text slot; or merge it into a neighbouring section. Never fill it with rows of pending items.
- **A link with no URL given** points to the section on this page that does most of the job (`#lookbook`); the handoff names the URL needed. Never an invented route.
- **A form with no endpoint** carries an empty `data-endpoint`, says clearly that nothing was submitted, and never shows a success message (gate 70).
- For our local sites: a missing phone, address or opening hours is the first fact to ask for in `../../intake.md`, and if still absent it stays a slot, never a placeholder number.
