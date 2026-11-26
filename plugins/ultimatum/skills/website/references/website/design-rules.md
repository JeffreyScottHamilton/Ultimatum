# Design rules: plan, de-generic, lint, basics

Run this on every direction before the critic, and again on the built site. It leans on two ideas: commit to a clear point of view before styling, and treat generic output as a defect to remove, not a default to accept.

## 1. Plan, de-generic, remove one

1. **Plan (3 lines).** Write the purpose of the page, the one feeling it should leave, and the one thing a visitor will remember. If the third line could describe any site, rewrite it.
2. **Build** with a deliberate choice for type, colour, space and motion (`craft.md`). No default stack.
3. **De-generic pass.** Reread the page as a stranger. Wherever you can name "that is what every site like this does", change it to something specific to this business: its real photo, number, word or product.
4. **Remove one element** that does not earn its place. Decoration must carry information.

## 2. Anti-generic lint

Fail the direction on any of these unless the brand or a reference site truly asks for it (say why in the file's top comment). Most are fine once; the defect is the habit of reaching for them by default.

**Type**
- one font family for headings and body, at one weight
- the fashionable display serif of the moment (e.g. Instrument Serif) picked without a reason from the brand
- italics used for emphasis in most headings, or a single italic word in every title
- tight negative letter-spacing on every heading, not only the big display line
- monospace for text that is not code, numbers or data
- ALL CAPS subtitles, and a small uppercase "eyebrow" label above every heading
- a full stop at the end of headlines and section titles
- little middle dots (·) strung between words or links

**Layout and decoration**
- cards nested inside cards, a grid of identical rounded cards, or a bordered box around every block
- squircle corners on everything; pills and tag chips used as decoration, or a pill badge above the headline
- three icon cards in a row; a coloured left border on quotes, notes or cards
- an arrow (→) on every button and link, not only the one that moves you on
- a divider line between every section or list item
- fake 01 / 02 / 03 section numbering; three-step "how it works" boxes
- code-style labels as decoration (`~/about`, `// services`, `<section>`, breadcrumbs on a one-level site)
- a mocked-up app screen or diagram with more detail than anyone can read; show the real thing or simplify it

**Colour and effects**
- a cream or off-white background by default (with or without a terracotta or clay accent); near-black with one acid accent
- gradient backgrounds, gradient-blob or aurora heroes, a blurry glow behind the hero; purple-to-blue gradients
- many tints and opacities of one colour instead of a few chosen colours
- dithering, halftone grain or ASCII-art images as a style
- emoji or sparkle (✦) icons; an icon tile above every heading
- a pulsing green "live" dot when nothing is live
- sections that fade or slide in on scroll, the same way every time

**Words and photos**
- copy that says the same thing twice, or a paragraph where a sentence would do
- clipped two-word sentences used for rhythm ("Fast. Simple. Yours.")
- the stock words "quiet", "real", "crafted", "seamless", "elevate" where a plain, specific word fits
- numbers nobody can back up: every stat, rating and count comes from the owner and is checked
- lorem ipsum, or "Welcome to ..." as the headline
- stock photos of people at laptops

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
