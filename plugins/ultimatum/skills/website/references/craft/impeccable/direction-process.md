# Direction process: where truth lives and how a direction is chosen

Read when starting a new surface or a redesign and you need to know which document holds which truth, which questions to ask, and how to test a direction before building it.

The three-direction flow and approval are in `../../website/planner.md` and `../../website/directions.md`; a custom design is in `../hallmark/direction.md`; the font and look clusters to distrust are in `../design-review-qa/slop-tells.md` § Fonts and `../design-review-qa/page-modes.md` § Calibration: three looks to distrust. This file adds the parts those do not hold.

## Three places for truth

1. **Product facts**: what it is, who it is for, what it can prove. Owned by the user.
2. **The visual system**: tokens, type, components. Durable across surfaces.
3. **The surface brief**: what this one page or screen must do now.

Keep them apart. A design file is written after the build, from the build, not before as a wish. The direction's private contract (its name, its references, its banned moves) lives in the brief; it never ships in the source, the DOM, comments or data attributes.

## Starting state decides the work

| State | What it means | What to do |
|---|---|---|
| Redesign | an old look to replace | keep the facts and wiring, replace the look |
| Established world | a system that works | extend it; no concept round |
| Incomplete brand | a logo and a colour, little else | build the missing parts around what exists |
| None | nothing yet | full concept round |

A missing design file does not mean a blank slate: read the code and the live site first. A small addition to an existing surface inherits that surface; it never gets a new identity.

## Questions, two or three per round

Ask what you cannot read from the code or brief, and only what changes the build. One round is usually enough. Say what you think the answer is and invite correction, rather than asking open questions.

Always ask: what does success look like, what must not change, and what would feel wrong.

By page mode (modes are defined in `../design-review-qa/page-modes.md`):
- Persuade: who acts, what they must believe, what proof exists.
- Operate: the main task, the data, the states, how often it is used.
- Read: the question readers bring, the sources, how they find their place.
- Experience: what leads, and how much people may explore.

Never ask the user for CSS values. When settled, write the brief in seven parts: the job, the outcome, the direction, scope, states, interaction, constraints. Confirm it and stop; no code in the same turn.

## Finding a world for a new identity

1. Name the mechanism: how the product works, in one physical sentence.
2. Name the scene: who uses it, where, in what light. That sentence decides light or dark.
3. Name the category's rut (what every rival looks like) and its opposite.
4. Draw candidate visual systems from the audience's own culture (their tools, trades, print traditions), each with one line on why it fits and one on how it looks. Generate several, then keep three.
5. Present one committed direction with named choices: the world, the first viewport, the path through the page, the signature interaction, how far it reaches, and its risk.
6. Always also show the plain category standard as the safe option, without recommending it.

A borrowed reference lends discipline (a ruling grid, a measured shadow, a numbering habit), never its costume.

## Testing the direction

Rate it on two axes: would the audience see themselves in it, and is the product clear within seconds? A direction that wins one and loses the other needs another pass.

Model habits to watch: warm or bookish subjects drift toward cream paper and lamplight; tech subjects drift toward near-black with neon. Treat these as already spent unless the brief asks for them. Ban the device, not the energy: "no gradient text" is a useful rule, "no colour" is not.

## Colour strategy comes first

Choose one level before picking hues:
- **Restrained**: neutrals with one accent for actions and state. The default for tools and reading.
- **Committed**: one colour owns 30 to 60% of the surface.
- **Full palette**: three or four colours with fixed roles.
- **Drenched**: colour is the ground everywhere.

Apply colour at page scale (a region, a band, a ground), not as scattered small accents. Operate and Read surfaces lean restrained and code-led; Persuade and Experience may go further.

## Building to the direction

- A comp is a spatial contract, not artwork to trace; models over-trust their own recreations, so compare the build to the comp side by side.
- Build the named technique for real (canvas, WebGL, view transitions), not a picture of it.
- Use real, verified photos of the actual subject; check every image URL loads.
- Label sample data as sample. Claims come from the user (see `../design-review-qa/craft-audit.md` § 2. Claims come from the owner, never from you).
- Check widths from 320 px to wide desktop, including 1280 to 1600, with no fixed pixel grids.
- One screenshot round at desktop and phone (plus the user's own width), every state driven; at most two fix rounds before reporting.
- Report the verdict only for the scope you checked.

## Final review of a finished build

Give a fresh reviewer (a helper with no edit tools) the request, the user's answers, the files, the comp and the screenshots. It checks, in order: that the screenshots exist and show the right widths; that the brief and product facts were kept; the build against the comp, element by element (matches, adapted, missing, contradicted, added); what the chosen world could still give (frame, depth, lettering, motion) that the build left unused; each promise in the brief; that sample data is labelled and no claim was invented; and the floor in `../design-review-qa/slop-tells.md`. It returns one verdict word (recapture, rebuild, fix or ship) and an ordered list of fixes. After fixes it scores again rather than hunting for new problems.
