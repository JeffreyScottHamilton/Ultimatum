# Brand review: the consistency audit and the approval gate

Read before a branded piece ships (page, campaign, email, print), and on a fixed schedule for the whole brand. The approval gate checks one piece; the consistency audit checks that many pieces still look and sound like one brand. Accessibility items here are a brand-level summary; the full page checks are in `../taste/accessibility.md` and `../design-review-qa/index.md`.

## Approval gate

Run it on each piece before it goes out. Mark each line pass, fail or not relevant; a single fail in the first group blocks release.

### Blocks release

- [ ] Logo: an approved version, at or above its minimum size, with its clear space, on an approved ground (`brand-visual.md` § Logo use).
- [ ] Text contrast meets 4.5:1 (3:1 for large text and for meaningful icons and control borders), checked with a tool, not by eye.
- [ ] Every claim, number, price and date is checked against its source; testimonials and ratings are real and permitted.
- [ ] Rights are clear for every photo, illustration, font and music track, with credits where the licence asks.
- [ ] Sector rules met where they apply (health claims, financial promotions, alcohol, competitions, privacy notices).
- [ ] Links and calls to action go where they say.

### Must be fixed before release, or signed off as an exception

- [ ] Colours come from the palette tokens; no near-miss values.
- [ ] Type uses the guide's families, weights and scale.
- [ ] Photos and illustrations match the written style; one icon set.
- [ ] Copy matches the voice (slider positions, the three traits) and uses the brand's own word list.
- [ ] Main message and proof points agree with the messaging block in the guide.
- [ ] Images have alt text that says what matters; video has captions; meaning never rests on colour alone.
- [ ] File format, size and dimensions suit the channel; file named by `brand-assets.md` § Names that sort and explain.

### Notes only

- [ ] Spacing, alignment and crop details.
- [ ] Opportunities to reuse a library piece instead of a one-off.

### Sign-off record

Keep one line per piece in the guide's log or the asset manifest:

| Piece | Version | Reviewer | Role | Result | Date | Exceptions |
|---|---|---|---|---|---|---|
| open-day landing page | v3 | (name) | brand owner | approved | 2026-03-20 | none |

Who signs: the brand owner always; legal or compliance when a claim, offer or regulated topic is present; the person who knows the facts (the owner, the product lead) for numbers and dates. An agent may run the checks and fill the table; a person gives the approval.

### Frequent fails and their fixes

| Fail | Fix |
|---|---|
| brand colour text on white fails contrast | use the ramp step recorded for text, or put the text on a darker ground |
| logo crammed into a header | drop to the symbol below the lockup's minimum width |
| a colour picked from a screenshot | replace with the token; screenshots shift colour |
| a stray font weight | load only the guide's weights; remove the rest |
| a photo from a free site without checking the licence | replace, or record the licence and credit |
| copy louder than the voice (exclamation marks, superlatives) | rewrite to the tone-by-moment table |

After approval, move the files to `final/`, store the approved version in the manifest, and keep the review notes with the piece for a year at least.

## Consistency audit

Run on the whole brand: quarterly for an active brand, after any rebrand, and when a new channel opens.

### Look

- [ ] The same logo file (or its exact exports) on every channel; no outdated versions.
- [ ] The palette reads the same across site, social, email and print; neutral surfaces have not drifted warmer or cooler.
- [ ] Type is the same families on every channel, or the documented substitutes where a channel cannot load them (email clients, office documents).
- [ ] Photo style holds across channels; no stock look creeping into social.

### Sound

- [ ] Headlines on the site, social bios and email subject lines sound like one writer.
- [ ] Product and service names are spelled and capitalised one way.
- [ ] The main message is the same in the site's opening, the social bio and the sales pitch.
- [ ] Error messages, receipts and automatic emails have been written in the voice, not left as platform defaults.

### Channel sweep

| Channel | Check |
|---|---|
| website | header logo, favicon and app icons, link-preview image, footer details, the 404 and error pages |
| social | avatar crop of the symbol, banner art current, bio wording, pinned post |
| email | sender name, template header, signature blocks for every staff member |
| documents and print | letterhead, invoice template, slide template, signage, packaging |
| third-party listings | maps profile, directory entries, marketplace stores: name, logo, hours, photos |

### Write up the audit

List each drift found with the channel, a screenshot or link, the rule it breaks, its fix and who owns the fix. Fix blockers (wrong logo, failing contrast, wrong facts) at once; batch the rest. Add a one-line summary to the guide's change log so the next audit starts from it.
