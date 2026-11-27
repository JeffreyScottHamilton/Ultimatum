# Design file and token exports

Read when the user asks to lock the system ("give me a design.md", "make this portable", "extract the tokens"), when a redesign spans more than one page, or when tokens are wanted as Tailwind, DTCG or shadcn. One page never writes a design file unprompted; its token stylesheet is already portable. Ultimatum's own place for the project brief is `../../intake.md`; the design file records the visual system only.

## Rules

- Triggers are explicit asks, or a multi-page redesign. A single component is too small.
- Do not overwrite an existing `design.md` or `DESIGN.md`; refresh just its Exports section and mention it in one line.
- Write it at the project root, about 45 lines, from the token stylesheet, not from the theme file. State the picks aloud first.
- Later runs read it first; every pick defers to it and pages share the system. A page that needs something else adds a Variants section.

## Template

````markdown
# Design: <project>

## System
- Genre: <editorial | modern-minimal | atmospheric | playful>
- First-page shape: <named shape, or the app's first screen>
- Theme: <name from the catalog, or custom with a 4-8 word vibe>
- Axes: paper band, display class, accent band. Hero posture: <posture>

## Tokens
Source of truth: tokens.css. List each role with its value.

## Buttons
- Secondary: outline or text, sharing the primary's radius and height.
- Primary: fill, radius, height.

## Motion
- Character: calm | brisk | severe | still. At most one reveal; reduced motion ends everything at once.

## Exports
tokens.css here; other formats added on request.
````

## Token families

| Family | Tokens |
|---|---|
| Colour | paper in three steps, ink in two, muted, rule, accent with its ink, focus, error and success; a field colour on committed pages; a second accent where a theme has two inks |
| Type | display, body and outlier faces; a 1.25 scale from 16px (xs to 3xl); display sizes; section, title and lead roles; display tracking |
| Space | ten steps from 2px–144px; container, gutter, column gap, three section gaps |
| Shape | card radius, pill radius, hairline, card shadow |
| Motion | three easings; durations 120, 220, 420ms |
| Layers | z-index ladder: tooltip 600, toast 500, modal 400, nav 300, sticky 200, dropdown 100, raised 10, base 1 |

Nothing downstream may use a token the stylesheet does not declare.

## Placing tokens in a project

Place the token file next to the entry stylesheet and import it right after the final `@import`; CSS silently ignores an `@import` that comes after any other rule. Where the project already has token names (`--background`, a Tailwind `@theme`), map the roles onto them instead of adding a second set.

## Tailwind v4

```css
@import "tailwindcss";
@import "./base.css" layer(base);
@import "./tokens.css";
```
```css
@theme static {
  --font-display: "Fraunces", serif;
  --color-paper: oklch(96% 0.01 80);
  --radius-card: 6px;
}
:root { --z-modal: 400; --space-lg: 24px; --dur-short: 220ms; }
```

- Colour, font, text, tracking, radius, shadow and easing tokens go in `@theme static` so they become utilities and stay variables. The rest stays in `:root`.
- Do not declare `--spacing-<name>`. Tailwind derives width, padding and gap from that namespace, so a `--spacing-xl` would alter `max-w-xl`. Our space steps are 4px multiples and already match Tailwind's unit.
- Nine of our names clash with Tailwind's: six text sizes and the three easings. Overriding them suits a new project; on a single page inside an existing site, declare them on that page's root instead.
- Base styles go in the base layer or they outrank utilities.
- Tailwind v3: one `:root` block above the directives, base file in a layer; utilities via `theme.extend` with `var()` values.
- Docs: https://tailwindcss.com/docs/theme

## DTCG tokens.json

Export for Style Dictionary or Tokens Studio. A `$type` on every token; OKLCH as strings (say so if converting to hex loses accuracy); fluid sizes export their maximum.

```json
{
  "color": { "ink": { "$type": "color", "$value": "oklch(20% 0.02 260)" } },
  "space": { "md": { "$type": "dimension", "$value": "16px" } }
}
```

Spec: https://www.designtokens.org/

## shadcn/ui

Point its variables at ours: background to paper, foreground to ink, card and popover to paper-2, primary to accent with accent-ink as foreground, secondary to paper-3, muted-foreground to muted, destructive to error, border and input to rule, ring to focus, radius to card radius. Its own `accent` and `muted` mean a hover surface and a quiet background, which clash with our names; keep our two out of `@theme` and reach them through `var()`, or rename them and say so in the handoff. Docs: https://ui.shadcn.com/docs/theming
