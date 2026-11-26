# Craft: finish details for controls, forms, tables, nav and the document

Read in the last pass of a page or component, and when styling controls, inputs, pricing, tables or the nav. It is the last 2%; the F-checks in `gates.md` report most of it. Detailed state recipes are in `interaction-and-states.md`.

## Controls

- One filled primary per page (a dialog counts as its own page). Secondary buttons are outlined or typographic, never louder than the primary; nav actions quieter than the hero's.
- Marketing controls 44 to 52px tall; app UI 32 to 40px with a 44px hit area (48px on coarse pointers). Two button sizes at most, 6px or more apart. An input matches the button beside it. Delete takes a secondary style unless deleting is the page's one action.

## Inputs

- Constant border width. The focus ring is an `outline` (inset on inputs), never a border change.
- Disabled uses opacity about 0.55, `cursor: not-allowed` and the native attribute together.
- Reserve a line of height for helper text (`min-height: 1lh`), 16px type on mobile, a `name`, an `autocomplete`, the right `type` and `inputmode`, and a `<label>` or `aria-label` on every field. Never block paste. Keep submit enabled until the request starts; a failed submit focuses the first invalid field. Every `<button>` gets an explicit `type`.
- One-field form: about 20rem wide, never an input and a button sharing one border.

## Content blocks

- **Testimonials:** only if the user supplied them. Attribution bottom-aligned, the avatar the real person or nothing, hanging punctuation on pull quotes.
- **Pricing:** emphasise a tier with its button and a word, never a different card colour. Buttons align at the bottom across tiers. A taller featured tier is a grid sibling on explicit rows, never negative margins.
- **Tables:** sentence-case heads that never wrap, horizontal rules only, no outer border or card, full width. On a phone keep the naming column and the acting column in view: restack rows as labelled blocks or pin the first column.
- **Stats:** a title that never wraps, no icon. **Features and metadata** are a `<dl>` with the `<dt>` one weight heavier. **Logo rows** split evenly (3 + 3, never 5 + 1).
- **Images:** `alt=""` when the subject is named beside the picture; `width` and `height` on every `<img>`, and a file that exists; footer links at body weight.

## Responsive

- Body-adjacent UI (meta, nav links, controls) is larger on a phone and steps down at 60rem; body text never under 16px.
- Every desktop sidebar or filter column collapses into a menu or disclosure; use container queries for widgets whose layout depends on their own box (https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries). Wider rules in `responsive.md`.

## Nav

- One line, 56 to 80px. A sticky nav taller than the scaffold's `scroll-padding-top` raises it.
- Text links in one weight across states; state is a colour or soft background, never a primary fill. A tab row scrolls sideways rather than wrapping; under 60rem links that no longer fit go behind a menu. The logo links home with an `aria-label`.

## The document

- `lang`, a `<title>` in the page's own words, a one-sentence meta description (F23). Heading levels step one at a time (F21).
- Browser surfaces (F16): keep what the base styles theme: `::selection`, `caret-color`, `scrollbar-color`, the focus ring, link underline.
- Local sites: add the schema, title and description rules in `../../pages-and-seo.md`; they sit on top of this list.

## Overlap

Merged with `../taste/cards-and-ui.md` (cards, buttons), `../taste/accessibility.md` (focus, labels, targets, WCAG 2.2 AA) and `../../website/design-rules.md` § 7 (interface basics). New here: the 44 to 52 versus 32 to 40 split, the one-primary rule and the table-on-phone rule.
