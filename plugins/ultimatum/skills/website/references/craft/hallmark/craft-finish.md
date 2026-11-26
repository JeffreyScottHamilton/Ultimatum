# Craft: finish details for controls, forms, tables, nav and the document

Read in the last pass of a page or component, and when styling controls, inputs, pricing, tables or the nav. It is the last 2%; the F-checks in `gates.md` report most of it. Detailed state recipes are in `interaction-and-states.md`.

## Controls

- Only one filled primary button per page, with each dialog counted as its own page. Secondary buttons are outlined or plain text and never outshine it; actions in the nav stay quieter than the hero's.
- On marketing pages controls are 44–52px high; in app UI they are 32–40px with a 44px target (48px for coarse pointers). Use at most two button sizes, differing by 6px or more. An input matches the height of the button next to it. A delete button looks secondary unless deleting is the page's single purpose.

## Inputs

- Keep border width fixed. Draw the focus ring with `outline`, inset on inputs, and never by changing the border.
- Mark disabled controls with roughly 0.55 opacity, `cursor: not-allowed` and the native attribute, all three.
- Leave `min-height: 1lh` for helper text and use 16px type on mobile. Each field needs a `name`, an `autocomplete`, a correct `type` and `inputmode`, plus a `<label>` or `aria-label`. Pasting is always allowed. Submit stays enabled until a request begins, and after a failed submit focus moves to the first invalid field. Give every `<button>` an explicit `type`.
- A one-field form is around 20rem wide; the input and button never share a single border.

## Content blocks

- **Testimonials:** include them only when the user provided them. Align attributions at the bottom, show the real person's photo or none, and hang the quote marks.
- **Pricing:** highlight a tier through its button and a label, not a different card colour. Align the buttons along the bottom of every tier. Make a taller featured tier a grid sibling on explicit rows, and never use negative margins.
- **Tables:** full width, with heads in sentence case that never wrap, only horizontal rules, and no outer border or card. On a phone keep the naming column and the acting column in view: restack rows as labelled blocks or pin the first column.
- **Stats:** their titles never wrap and carry no icon. **Features and metadata** use a `<dl>` whose `<dt>` is one weight bolder. **Logo rows** split evenly, 3 + 3 rather than 5 + 1.
- **Images:** use `alt=""` if the subject is named beside the picture; give every `<img>` `width` and `height` and make sure the file exists; footer links keep body weight.

## Responsive

- Small UI near body text (meta, nav links, controls) runs larger on phones and shrinks at 60rem; body text itself stays at 16px or above.
- A desktop sidebar or filter column folds into a menu or disclosure; for a widget whose layout depends on the space it is given, use container queries (https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries). Wider rules in `responsive.md`.

## Nav

- A single line, 56–80px tall. If a sticky nav is taller than `scroll-padding-top`, raise that value.
- Text links hold one weight in all states and show state through colour or a soft background instead of a primary fill. Tabs scroll sideways and do not wrap; under 60rem the links that stop fitting go into a menu. The logo links to the homepage and has an `aria-label`.

## Document basics

- Set `lang`. Give a `<title>` in the page's own words and a meta description of one sentence (F23). Heading levels descend one step at a time (F21).
- Browser surfaces (F16): keep what the base styles theme: `::selection`, `caret-color`, `scrollbar-color`, the focus ring, link underline.
- Local sites: add the schema, title and description rules in `../../pages-and-seo.md`; they sit on top of this list.

## Overlap

Merged with `../taste/cards-and-ui.md` (cards, buttons), `../taste/accessibility.md` (focus, labels, targets, WCAG 2.2 AA) and `../../website/design-rules.md` § 7 (interface basics). New here: the 44–52 versus 32–40 split, the one-primary rule and the table-on-phone rule.
