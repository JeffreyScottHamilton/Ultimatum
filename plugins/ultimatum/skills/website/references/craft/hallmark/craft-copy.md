# Craft: copy, opening a section and missing facts

Read before writing any words, when a section needs an opening, and whenever the prompt leaves a fact out. Longer copy rules for local sites are in `../../copy.md` and `../taste/copy.md`; this file adds the budgets, the opening moves and the slot rules.

## Copy

Write as the owner would say it across a counter: the prompt's own nouns, a real place, a number the user gave, the verb a customer uses.

- **Swap test:** a head that would work on a competitor's page gets a noun only this business has. "Software that works for you" fits anyone; "Invoices that chase themselves" fits one product.
- **Three tests per line:** can the reader picture it, could it be proven false, could only this business say it. Specific beats clever: the place, the hour, the material, the result. A pun is a second-draft move, once a page at most.
- **Subhead:** says what it is, for whom and the one difference, in twelve words or fewer.
- **Section heads:** say what the visitor will see or get ("Three loaves a morning"), never a category label (Features, Our story, Why us). One-word stage names are fine in a staged shape.
- **Rhythm:** a short line beside a longer one; verbs over adjectives; one idea per sentence; no adjective triads.
- **Budget (gate 58):** headline seven words or fewer; section heads six or fewer; intros one line; paragraphs two short sentences; lists of four items with a three-word label and a ten-word line (five for steps that cannot merge; past that, a table); tables five rows; a set the user gave keeps its true count; 450 visible words a page at most. Read only the headings and the hero: if they tell the story the rest is the right length.
- **Refuse the generated voice:** the buzzword list in gate 19, plus "Reimagine", "Whether you are X or Y", "It is not just X, it is Y", "Say goodbye to", "game-changer", "journey", a colon title, "Click here", "Enter your email below", a version string in marketing copy.
- **Buttons:** the verb of the action ("Book a fitting"); "Continue" only as a flow's second step. **Errors:** what happened, why if known, what to do; no "Oops", no exclamation marks. **Empty states:** what is empty, why it matters, one action. **Loading:** a spinner after 150–300ms, shown at least 300ms, beside the label; text past 2s.
- **Sample data** in a built product: `example.com`, the prompt's field names, and values that read as samples (round amounts, "Example Kitchen"), never a figure a visitor could take as a claim.
- **Punctuation:** curly quotes, a true ellipsis and apostrophe, no double hyphen, no em or en dash (use comma, colon, full stop or brackets), a non-breaking space before units. A full stop on standalone sentences, none on list items.

Merged with `../../copy.md` (button wording, swap tests) and `../../website/design-rules.md` § 2 (stock words, em dashes, fake stats); local-business additions (phone number, hours, "call us" verbs) stay in those files.

## Opening a section

The reflex is a small tracked-caps label above the heading, and that reflex is the tell (gate 54). Ask what the reader does not yet know. If nothing, open with nothing. If something, it rides on a fact, a destination or an identifier, never on a name for what comes next. Twelve ways in:

1. Nothing: air above, the heading flush.
2. The heading announces itself, subject in its first two words. Usually best.
3. A lead-in inside the paragraph in a heavier weight, never on its own line.
4. A drop cap, one per page, first paragraph only.
5. A rule that does more than rule: hairline, fleuron, double rule, colour edge or pure gap, varied seam to seam.
6. A numeral at graphic scale (`clamp(6rem, 16vw, 14rem)`), one per page and only when the number is real and the point (an issue, a year, the offer's price).
7. A real `<ol>` with CSS counters when the sequence is genuine.
8. A caption below the content instead of a label above.
9. Marginalia in the outer margin beside the body.
10. A change of paper: the band edge is the break.
11. A running head or folio, legal because it persists rather than announces.
12. Persistence: the heading stays in view as content scrolls under it.

Two moves can share a section; three is noise. Rotate against the log. Legal small type because it names something present: figcaption, `th`, `label`, `legend`, nav or tab labels, a byline or `time`, a unit after its figure, a real filename on a code block, a live `role="status"` chip, one linked announcement going somewhere real, a plan name.

## Missing facts

- **A fact the prompt did not give** (venue, date, price) becomes a text slot, never an invented value: a span with a `data-fill` name in the muted colour inside a dashed outline, so it reads as a blank and not as a link. Two per page at most, each in the handoff. When the job's anatomy wants more facts than were given, slot the two a visitor needs to act and leave the rest for the handoff. A row or line that would hold only a missing fact is cut.
- **A face the page is about** that the user has not supplied is a font slot: the display token names it first, a free face of the same build stands in with one caption, a waiver for gate 37 is stamped, and the handoff asks for the files.
- **A section the user named but gave nothing for:** its heading, one line on what will go there, one text slot, or merge it into a neighbour. Never a block of pending rows.
- **A link with no URL given** points to the section on this page that does most of the job (`#lookbook`); the handoff names the URL needed. Never an invented route.
- **A form with no endpoint** carries an empty `data-endpoint`, states plainly that nothing was sent, and never prints success (gate 70).
- For our local sites: a missing phone, address or opening hours is the first fact to ask for in `../../intake.md`, and if still absent it stays a slot, never a placeholder number.
