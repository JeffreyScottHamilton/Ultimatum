# Design rules: plan, de-generic, lint, basics

Run this on every direction before the critic, and again on the built site. It leans on two ideas: commit to a clear point of view before styling, and treat generic output as a defect to remove, not a default to accept.

## 1. Plan, de-generic, remove one

1. **Plan (3 lines).** Write the purpose of the page, the one feeling it should leave, and the one thing a visitor will remember. If the third line could describe any site, rewrite it.
2. **Build** with a deliberate choice for type, colour, space and motion. No default stack.
3. **De-generic pass.** Reread the page as a stranger. Wherever you can name "that is what every site like this does", change it to something specific to this business: its real photo, number, word or product.
4. **Remove one element** that does not earn its place. Decoration must carry information.

## 2. Anti-generic lint

Fail the direction on any of these unless the brand or a reference site truly asks for it (say why in the file's top comment):

- one font family for headings and body, at one weight
- cards nested inside cards, or a grid of identical rounded cards
- the stock cream background with terracotta or clay accent
- gradient-blob or aurora heroes; purple-to-blue gradients
- emoji used as icons; an icon tile above every heading
- the same fade-up on every section; fake 01 / 02 / 03 numbering
- pill badge above the headline; three-step "how it works" boxes
- near-black with one acid accent; stock photos of people at laptops
- lorem ipsum, or "Welcome to ..." as the headline

## 3. Page kind and effect caps

Classify first; the kind sets how much the page may move.

| Kind | Examples | Effects allowed |
|---|---|---|
| **Trust** | law, medical, finance, trades | calm: hover and focus states, one gentle reveal; no pinned scenes, no video background |
| **Local / service** | cafe, salon, studio | light: reveals, one soft hero move |
| **Portfolio / editorial** | designer, agency, studio | expressive: type moves, one pinned scene |
| **Launch / product** | app, SaaS, game, event | full: motion hero, product demo, scroll scenes (still one heavy effect per screen) |

## 4. Dealt, not picked

Before any mockup, deal each direction a **palette, a type pair and a layout** from different families, and write them as a short line at the top of the file. Do not let a direction fall back on the same trio as another. At most **3 revision rounds** per direction; after that, show it with the remaining issues named.

## 5. Revision verbs

After the user picks, these are named moves: **bolder** (larger type, stronger contrast, fewer elements), **quieter** (less motion, more space, softer colour), **tighter** (less padding, shorter copy, denser grid), **looser** (more space, bigger type steps), **simpler** (cut or merge a section), **warmer** / **cooler** (palette and photos), **sharper** (crisper corners, rules and contrast). Apply one at a time, then re-run the lint and the critic after a big move.

## 6. Critic severities

- **blocker:** breaks the main action, unreadable, or fails accessibility (no focus ring, tiny taps, contrast).
- **major:** a lint hit, a section that confuses, mobile layout broken.
- **minor:** spacing, hierarchy or motion that is off but usable.
- **nit:** taste notes. Fix after the rest.

Blockers and majors must be fixed before the user sees the three; list minors and nits in the notes.

## 7. Interface basics

- Visible focus ring on every link, button and field (`:focus-visible`), never `outline: none` without a replacement.
- Tap targets at least 44 x 44 px, with space between neighbours.
- Never `transition: all`; list the properties. Animate `transform` and `opacity`.
- Respect `prefers-reduced-motion` in CSS and in any JS animation.
- Real `<button>` and `<a>`, one `<h1>`, labels on form fields, alt text on meaningful images, text contrast at WCAG AA.
- Images have width and height set; body text at least 16 px; no horizontal scroll at 375 px.

## 8. Components

For a ready piece (counter, marquee, tabs, carousel), run `ult components "<need>" --stack any` and check its licence line before using it. Prefer plain HTML and CSS when the piece is simple.
