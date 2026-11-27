# Interaction kit: choosing a part

Read before you add a moving part to a page or app. It decides whether anything should move, which part to use, and where its code comes from.

## 1. Earn the motion first

A part moves only when movement tells the user something:

- that their press landed,
- where a panel came from,
- what changed,
- or that something is still working.

If the honest answer is "it looks nice", use the still version. Pages that move everywhere feel slower and cheaper than pages that move in two places. `../emil-motion/gate.md` is the full test.

Every screen gets a budget: one showpiece at most (a text reveal, tilt, marquee or beam), and quiet feedback everywhere else (press, copy, toast). A dashboard gets no showpiece.

## 2. Match the moment to a part

| Moment | Use | Avoid |
|---|---|---|
| A main action with one or two variants | `SplitButton` | a row of three equal buttons |
| Copying a key, link or command | `CopyButton` | a toast for a copy that sits beside its button |
| Two to five views of one thing | `Tabs` | a segmented control that swaps whole pages |
| One setting with two to four values | `SegmentedControl` | a dropdown for three options |
| A destructive act that can't be undone | `HoldToConfirm`, or a dialog | a plain red button |
| A result that appears away from the pointer | `ToastProvider` | an alert box |
| Mobile actions, share targets, filters on phones | `Drawer` | a centred modal on a 390px screen |
| A preview that opens into detail | `ExpandableCards` | navigating away and back |
| A small menu or form attached to a trigger | `MorphPopover` | a full dialog |
| Many pages or actions in an app | `CommandPalette` | a deep sidebar only |
| A number that matters on a stats strip | `NumberTicker` | a counter on every number |
| One headline per page that should arrive | `TextReveal` | revealing body text |
| A long label row of logos or quotes | `Marquee` | a carousel that auto-advances |
| Swipeable cards or photos | `Carousel`, or `SwipeDeck` for pick-or-pass | autoplay |
| A fine numeric value (design tools, sizes) | `ScrubNumber` | a slider with no typed entry |
| Labels and filters people type | `TagInput` | a comma-separated text field |
| A sign-in code | `OtpInput` | six separate inputs |
| Order that people choose | `ReorderList` | drag with no keyboard path |
| Feedback at the end of help or docs | `QuickFeedback`, or `Rating` | a five-field survey |
| A multi-step flow | `Stepper` | a progress bar with no step names |
| App-like icon navigation | `Dock` | magnification on a phone (it turns off there anyway) |
| A theme switch | `ThemeToggle` | a checkbox labelled "dark" |
| A card that should feel physical on a showcase | `TiltCard` or `SpotlightCard` | either one on a form or a table |

`components.md` lists what each one takes.

## 3. Ours, theirs, or nothing

`data/craft/interaction-kit/catalog.csv` lists all 131 Watermelon UI components. Each row says what it does and when to use it, names the kit part that covers it (110 rows have one), and gives its install URL.

1. **A kit part covers it:** copy ours. Our version has theme tokens only, reduced motion, keyboard paths, labelled icons and live regions. It also passes `ult kitlint` and an axe run.
2. **No kit part, and it is domain-specific** (a crypto swap, a voice recorder, a map or a signature pad): you may install theirs with `npx shadcn@latest add <install URL>`. Use the `-base` variant where one exists, because it uses theme tokens. Their code is MIT, so keep their licence notice in the file. Then run `ult kitlint` on what landed and fix every failure before you ship it. The comparison in §4 says why.
3. **Neither fits:** build it from the closest kit part and the rules in `details.md`, then lint it.

Page sections (heroes, pricing, footers, auth screens) and full dashboards are in `blocks.csv`, with the same install pattern. Treat a block as a starting layout. Rewrite its copy and recolour it to the page's tokens before review (`../taste/index.md`).

## 4. Measured comparison

`ult kitlint` was run on every Watermelon component (both variants, 131 each) and on the kit (32 files), on 2026-11-27.

| Check | Watermelon (base variant) | Watermelon (original) | Kit |
|---|---|---|---|
| Files with at least one failure | 130 of 131 | 130 of 131 | 0 of 32 |
| Moves without checking reduced motion | 128 | 128 | 0 |
| Raw colour in source | 10 | 83 | 0 |
| `transition-all` | 47 | 47 | 0 |
| Icon-only button with no name | 51 | 51 | 0 |
| Clickable div or span with no keyboard path | 50 | 50 | 0 |
| Outline removed with no focus style | 22 | 23 | 0 |
| Press scale below 0.95 | 19 | 19 | 0 |

The kit also passes an axe run (WCAG 2.1 AA plus best practice) at phone and desktop sizes, with reduced motion, and in dark mode. That run found 0 violations. No equivalent browser run was done on Watermelon's components.

What Watermelon does better: many more domain parts (finance, voice, maps, scheduling), 189 page blocks, 12 dashboards and a one-command installer. The kit doesn't try to match that breadth. It covers the common interaction parts properly and points to theirs for the rest.
