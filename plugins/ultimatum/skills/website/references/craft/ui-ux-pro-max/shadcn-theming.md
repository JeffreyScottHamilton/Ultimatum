# shadcn/ui theming: colour roles, radius and dark mode

Read when setting a shadcn/ui project's colours, radius or dark mode, mapping a brand onto its theme, or adding a colour it does not have. Checked against https://ui.shadcn.com/docs/theming, https://ui.shadcn.com/docs/tailwind-v4 and https://ui.shadcn.com/docs/dark-mode/next. The general layer model is `token-architecture.md`; shadcn's theme is a ready-made semantic layer.

## How the theme is built

With `cssVariables: true` (the default), every component uses role classes such as `bg-primary` and `text-muted-foreground`, never palette colours. The roles are CSS variables in the global stylesheet, in background/foreground pairs:

| Role | Pair partner | Used by |
|---|---|---|
| `background` | `foreground` | page |
| `card` | `card-foreground` | Card |
| `popover` | `popover-foreground` | Popover, Dropdown Menu, Select content |
| `primary` | `primary-foreground` | default Button, focus accents |
| `secondary` | `secondary-foreground` | secondary Button |
| `muted` | `muted-foreground` | descriptions, placeholders, low-contrast grounds |
| `accent` | `accent-foreground` | hovered menu items, ghost Button hover |
| `destructive` | (text on it varies by version; check the stylesheet) | destructive Button, errors |
| `border`, `input`, `ring` | | dividers, field borders, focus ring |
| `chart-1` ... `chart-5` | | Chart colours |
| `sidebar` set | | Sidebar component |
| `radius` | | base corner radius |

Colours are written in OKLCH in current versions. The stylesheet has three parts: values on `:root`, dark values on `.dark`, and an `@theme inline` block that exposes each variable to Tailwind (`--color-primary: var(--primary);`), the same structure our generator writes (`token-templates.md` § Template 2: Tailwind CSS v4 theme).

## Putting a brand in

1. Start from the base colour closest to the brand's neutral (`neutral` is greyest; `stone` is warm; `zinc` is cool).
2. Set `--primary` (and `--ring`) to the brand's action colour, and `--primary-foreground` to the text colour that passes 4.5:1 on it.
3. Tint `--accent` and `--secondary` lightly toward the brand only if the brand asks for it; neutral is usually better.
4. Re-check every pair in both modes. Pale brand colours often need dark `primary-foreground`.
5. Set `--radius` once; the theme derives the smaller and larger steps from it (for example `--radius-sm: calc(var(--radius) * 0.6)` in current versions), so the whole set moves together.

If the project already has our generated tokens, point shadcn's roles at them instead of keeping two sets: `--primary: var(--color-moss-600);` in `:root`, and so on. Our starter uses the same role names on purpose.

Hex works as well as OKLCH in these variables. Use OKLCH when building ramps by hand (steady hue, even lightness steps); use whatever the brand guide records when copying values.

## Adding a colour role

The documented way: define the variable in `:root` and `.dark`, then expose it in `@theme inline`.

```css
:root  { --warning: oklch(0.80 0.15 75); --warning-foreground: oklch(0.21 0.01 75); }
.dark  { --warning: oklch(0.84 0.13 80); --warning-foreground: oklch(0.21 0.01 75); }

@theme inline {
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
}
```

Now `bg-warning text-warning-foreground` work, and the role can be used in a variant (`shadcn-components.md` § Variants). Check the new pair with a contrast tool, in both modes, before using it.

## Changing a component's look

In order of preference:

1. **Theme variable**, when the change should hold everywhere (all buttons rounder: change `--radius`).
2. **Variant**, when a new kind is needed (a success button): edit the cva map.
3. **Edit the copied component**, when the default itself is wrong for this project (taller inputs).
4. **`className`**, for a single instance.

Never override a role with a raw colour in one component (`bg-[#2f6b4f]`): the dark theme cannot reach it.

## Dark mode

shadcn/ui themes dark mode through the `.dark` class on `<html>`. For Next.js, the documented setup uses `next-themes` (https://ui.shadcn.com/docs/dark-mode/next):

```
pnpm add next-themes
```

```tsx
// app/app-theme.tsx (client component)
"use client";
import { ThemeProvider as Themes } from "next-themes";
export function AppTheme({ children, ...options }: React.ComponentProps<typeof Themes>) {
  return <Themes {...options}>{children}</Themes>;
}

// app/layout.tsx
<html suppressHydrationWarning lang="en">
  <body>
    <AppTheme defaultTheme="system" enableSystem attribute="class" disableTransitionOnChange>
      {children}
    </AppTheme>
  </body>
</html>
```

- `suppressHydrationWarning` is needed because the class is set before React hydrates.
- `defaultTheme="system"` with `enableSystem` follows the OS until the user picks.
- `disableTransitionOnChange` stops every colour transition firing at once on switch.
- The mode toggle offers light, dark and system; it is a button or menu with a text label or `aria-label`, not an unlabelled icon.

For Vite and other setups, the docs give a small provider that sets the class and stores the choice; the same three rules apply. In Tailwind v4 the stylesheet also needs the class variant: `@custom-variant dark (&:where(.dark, .dark *));` (https://tailwindcss.com/docs/dark-mode).

Dark mode design itself (surfaces, elevation, brand steps) is in `../hallmark/dark-mode.md`; a dark theme is not the light theme inverted.

## Several themes

For a second brand or a high-contrast theme, add another class with only role overrides (`.theme-forest { --primary: ...; }`) and, if Tailwind utilities must target it, a variant: `@custom-variant theme-forest (&:where(.theme-forest, .theme-forest *));` (https://tailwindcss.com/docs/adding-custom-styles). Keep the role names identical across themes; components never change.

## Checks before shipping a theme

- every foreground/background pair passes 4.5:1 in both modes; `ring` and `input` pass 3:1 against `background` (WCAG 2.2 SC 1.4.3 and 1.4.11);
- no raw colour classes in components (search for `bg-[#`, `text-[#` and palette names such as `bg-blue-`);
- `chart-1` to `chart-5` are distinguishable from each other, and charts do not rest on colour alone;
- the page has no flash of the wrong theme on load (check with a slow network profile).
