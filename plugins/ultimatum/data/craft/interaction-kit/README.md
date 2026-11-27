# Interaction kit

Thirty-two React components for the moments that make an interface feel alive: presses, copies, tabs, toasts, sheets, palettes, counters, reveals, drags. Each one is a single file you copy into a project and own. The guides are in `skills/website/references/craft/interaction-kit/`.

## What is here

| Path | What it is |
|---|---|
| `components/*.tsx` | The components. `cn.ts` holds the class joiner, the focus ring and the two shared springs. |
| `catalog.csv` | All 131 Watermelon UI components: what each does and when to use it, in our words, the kit component that covers it (110 of them), and its registry URL. |
| `blocks.csv` | Pointers to Watermelon's 189 page blocks and 12 dashboards by category, with registry URLs. |
| `gallery/` | Every component on one page, plus a browser check (layout, keyboard, focus, axe). |

## Using a component

1. Copy `components/cn.ts` and the component file into the project (for example `src/components/kit/`).
2. Install the two dependencies: `react` (18 or 19) and `motion` (12 or later, imported as `motion/react`).
3. The project needs Tailwind CSS 4 and the theme tokens below. The starter theme in `data/design-own/tokens/starter.theme.css` defines all of them; a shadcn-style theme works once its names match.
4. Run `ult kitlint <folder>` on the copied files. It should report no findings.

Tokens used: `background`, `foreground`, `card`, `card-foreground`, `primary`, `primary-foreground`, `primary-hover`, `muted`, `muted-foreground`, `accent`, `accent-foreground`, `border`, `input`, `ring`, `destructive`, `success`, plus `--radius`, `--shadow-sm` and `--shadow-md`. Dark mode is a `.dark` class on the root.

## What every component promises

- Colour only from theme tokens. No hex or rgb in the source.
- Reduced motion honoured. Movement becomes a fade or an instant change, never a broken state.
- Named transition properties. Never `transition-all`.
- Real controls. Buttons are buttons, keyboard paths exist for every pointer path, and icon-only controls have names.
- A visible focus ring and hit areas of at least 40px.
- Live regions where something changes out of view (toasts, reorders, copies, ratings).
- Inline SVG icons, so there's no icon library to install.

`ult kitlint` checks the parts of this that a source scan can see. The gallery check covers the rest in a real browser.

## Running the gallery check

From `gallery/`:

```bash
npm install
npm run typecheck
npm run build
python3 -m http.server 8765
```

In a second shell, also from `gallery/`, run `node check.js`. It needs Playwright with Chromium.

It renders the page at phone and desktop sizes, with reduced motion, and in dark mode. In each one it checks for sideways overflow, tab keyboard moves, a toast, the drawer's focus trap and focus return, the Ctrl+K palette and the hold button. Then it runs axe with the WCAG 2.1 AA and best-practice rules, and saves screenshots to `gallery/shots/`. It exits 1 on any overflow, console error or axe violation.

## Credit and licence

The component ideas and the catalog of what exists come from Watermelon UI (github.com/WatermelonCorp/watermelon-platform, MIT, copyright 2026 Watermelon Platform Contributors). The code in `components/` and `gallery/`, and every description in the CSVs, are written new for Ultimatum. The names, slugs, categories and registry URLs in the CSVs are facts that point back to Watermelon. To install one of their components as they wrote it, run `npx shadcn@latest add <install URL>`. That pulls their MIT code under their licence.
