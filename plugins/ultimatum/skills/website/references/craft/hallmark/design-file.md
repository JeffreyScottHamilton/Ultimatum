# Design file and token exports

Read when the user asks to lock the system ("give me a design.md", "make this portable", "extract the tokens"), when a redesign spans more than one page, or when tokens are wanted as Tailwind, DTCG or shadcn. One page never writes a design file unprompted; its token stylesheet is already portable. Ultimatum's own place for the project brief is `../../intake.md`; the design file records the visual system only.

## Rules

- Triggers are explicit asks, or a multi-page redesign. A single component is too small.
- Never overwrite. If `design.md` or `DESIGN.md` exists, refresh only its Exports section and say so in one line.
- Write it at the project root, about 45 lines, from the token stylesheet, not from the theme file. State the picks aloud first.
- Later runs read it first; every pick defers to it and pages share the system. A page that needs something else adds a Variants section.

## Template

````markdown
# Design: <project>

## System
- Genre: <editorial | modern-minimal | atmospheric | playful>
- First page shape: <macrostructure or app screen>
- Theme: <catalog name, or custom (vibe in 4-8 words)>
- Axes and posture: <paper band>/<display class>/<accent band>, <posture>

## Tokens
tokens.css is the source of truth; roles listed with values.

## Controls
- Primary: fill, radius, height. Secondary: outline or text, same radius and height.

## Motion
- Character: still | severe | brisk | calm. At most one reveal; reduced motion ends everything at once.

## Exports
tokens.css here; other formats added on request.
````

## Token families

| Family | Tokens |
|---|---|
| Colour | paper, paper-2, paper-3, ink, ink-2, muted, rule, accent, accent-ink, focus, error, success; field on committed pages; accent-2 where a theme has a second ink |
| Type | display, body and outlier faces; a 1.25 scale from 16px (xs to 3xl); display sizes; section, title and lead roles; display tracking |
| Space | ten steps from 2px to 144px; container, gutter, column gap, three section gaps |
| Shape | card radius, pill radius, hairline, card shadow |
| Motion | three easings; durations 120, 220, 420ms |
| Layers | base 1, raised 10, dropdown 100, sticky 200, sticky-nav 300, modal 400, toast 500, tooltip 600 |

Nothing downstream may use a token the stylesheet does not declare.

## Placing tokens in a project

Put the token file beside the entry stylesheet and import it after the last `@import`. CSS drops an `@import` that follows any rule, silently. If the project already names its tokens (`--background`, a Tailwind `@theme`), map roles onto those names instead of adding a parallel set.

## Tailwind v4

```css
@import "tailwindcss";
@import "./tokens.css";
@import "./base.css" layer(base);
```
```css
@theme static { --color-paper: oklch(96.5% 0.008 50); --font-display: "Fraunces", serif; --radius-card: 4px; }
:root { --space-lg: 24px; --dur-short: 220ms; --z-modal: 400; }
```

- Colour, font, text, tracking, radius, shadow and easing tokens go in `@theme static` so they become utilities and stay variables. The rest stays in `:root`.
- Never define `--spacing-<name>`: Tailwind sizes width, padding and gap from that namespace, so `--spacing-xl` changes `max-w-xl`. The 4px-multiple space scale already lines up with Tailwind's unit.
- Nine names collide with Tailwind (text xs, sm, lg, xl, 2xl, 3xl and the three easings). On a new project the swap is intended; on one page of an existing site, declare them on the page root instead.
- Base styles go in the base layer or they outrank utilities.
- Tailwind v3: one `:root` block above the directives, base file in a layer; utilities via `theme.extend` with `var()` values.
- Docs: https://tailwindcss.com/docs/theme

## DTCG tokens.json

For Style Dictionary or Tokens Studio. A `$type` on every token; OKLCH as strings (say so if converting to hex loses accuracy); fluid sizes export their maximum.

```json
{ "color": { "paper": { "$value": "oklch(96.5% 0.008 50)", "$type": "color" } },
  "space": { "lg": { "$value": "24px", "$type": "dimension" } } }
```

Spec: https://www.designtokens.org/

## shadcn/ui

Point its variables at ours: background to paper, foreground to ink, card and popover to paper-2, primary to accent with accent-ink as foreground, secondary to paper-3, muted-foreground to muted, destructive to error, border and input to rule, ring to focus, radius to card radius. Its own `accent` and `muted` mean a hover surface and a quiet background, which clash with our names; keep our two out of `@theme` and reach them through `var()`, or rename them and say so in the handoff. Docs: https://ui.shadcn.com/docs/theming
