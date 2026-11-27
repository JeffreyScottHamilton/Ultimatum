# Brand flow: from a vague brief to a guide and tokens

Read when the user asks for brand guidelines, a brand refresh, or "make it on-brand", before writing any brand file or token. This is the order of work; the other `brand-*.md` files hold the detail for each step.

## 0. Look before you write

A project often has a brand already, just scattered. Search before asking:

- a guidelines file (`docs/brand*.md`, `BRAND.md`, a PDF in `assets/`), a token file (`*.tokens.json`, `tokens.css`, `theme.css`), a Tailwind `@theme` block or a `tailwind.config.*`, a shadcn `components.json` with its CSS file;
- the logo files and their folder;
- the live site, if there is one.

If a token source already exists, **it is the truth**. Edit it in place; never start a parallel file that will drift. Say which file you treat as the source in your first reply.

For a real, named company, read its values from its own site or files by the protocol in `../hallmark/brand-truth.md`. Never write a hex value, typeface or logo from memory.

## 1. Gather what only the owner knows

Ask once, in one message, only for what changes the result:

| Need | Why | If missing |
|---|---|---|
| who buys, and what they are choosing between | voice and positioning depend on it | ask; do not guess an audience |
| three words the brand should feel like, and one it must never feel like | sets the voice traits | offer two contrasting sets to pick from |
| existing logo files | logo rules are written around the real mark | leave the logo section as a marked gap |
| colours or fonts already in use (print, signage, packaging) | the guide must match what customers have seen | derive from the logo, then confirm |
| legal or sector limits (claims, health, finance, alcohol) | approval checklist items | note "none stated" |

## 2. Write the guide in this order

1. **Voice and messaging** (`brand-voice.md`): who we are, how we sound, what we say first.
2. **Visual identity** (`brand-visual.md`): colour roles, type, logo use, imagery.
3. **Assets** (`brand-assets.md`): where files live and how they are named.
4. **Review** (`brand-review.md`): the consistency audit and the approval gate.

Fill the starter in `brand-guidelines-template.md`. Keep one guide per brand, as one Markdown file at `docs/brand-guidelines.md` unless the project already has a place for it.

Words come before colours because the voice decides how loud the palette and type can be; a sober law firm and a festival cannot share a contrast level or a type weight.

## 3. Turn the guide into tokens

The guide is for people; tokens are for code. Every colour, font, size and radius in the guide gets a token name, built in three layers (`token-architecture.md`):

- **primitive**: the raw brand values (`--color-moss-600: #2f6b4f`);
- **semantic**: what a value is for (`--primary: var(--color-moss-600)`);
- **component**: one part's choice (`--button-bg: var(--primary)`).

Write the values once in a token JSON file and generate the CSS from it with `tools/build_tokens.py` (stdlib only; the starter lives in `../../../../../data/design-own/tokens/`). The generator also checks every text and background pair against WCAG contrast, so a brand colour that fails on white is caught before review, not after launch.

If the project already uses a different pipeline (Style Dictionary, a design tool export), keep it and map our three layers onto it.

## 4. Check the sync both ways

After any brand change:

- every colour named in the guide exists as a primitive token, and no primitive is unused or undocumented;
- each semantic pair passes its contrast floor in light and in dark (text 4.5:1, large text and UI parts 3:1);
- the guide's type scale matches the font-size tokens;
- the guide and the token file carry the same date or version line.

## 5. Updating an existing brand

For "change our primary colour" or "add a dark mode": change the primitive (or add one), re-point the semantic token, regenerate, then run `brand-review.md` § Consistency audit on the pages that use it. Record what changed and why in a short change log at the end of the guide. A colour change is never only a find-and-replace on hex values: hover, focus and chart colours were derived from the old one.

## 6. Hand back

Report: the guide's path, the token file's path, the contrast result from the generator (pairs checked, any that failed and the fix), the gaps left for the owner (logo files, legal review), and the next step.
