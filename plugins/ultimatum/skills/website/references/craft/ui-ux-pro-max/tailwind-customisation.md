# Tailwind customisation (v4): theme, utilities, variants, layers

Read when a Tailwind CSS v4 project needs its own theme values, its own utility or variant, component classes, a plugin, or a v3 config moved to v4. Using utilities is in `tailwind-utilities.md`; the token layers this theme should carry are in `token-architecture.md`, with a ready theme in `token-templates.md`. Checked against https://tailwindcss.com/docs/theme, https://tailwindcss.com/docs/adding-custom-styles and https://tailwindcss.com/docs/upgrade-guide.

## Configure in CSS

v4 is configured in the stylesheet. The minimum:

```css
@import "tailwindcss";
```

Everything else is added to the same file, in this order: `@import` lines, `@source` lines, `@custom-variant`, `@theme`, `:root`/`.dark` variables, `@theme inline`, `@layer base`, `@layer components`, `@utility`.

## Theme variables

Variables in `@theme` become CSS variables and generate utilities, by namespace:

| Namespace | Example | Makes |
|---|---|---|
| `--color-*` | `--color-moss-600: #2f6b4f;` | `bg-moss-600`, `text-moss-600`, `border-moss-600`, ... |
| `--font-*` | `--font-display: "Fraunces", serif;` | `font-display` |
| `--text-*` | `--text-display: 3.5rem;` | `text-display` |
| `--spacing` | `--spacing: 0.25rem;` | every spacing step (`p-4` = 4 x spacing) |
| `--radius-*` | `--radius-card: 0.75rem;` | `rounded-card` |
| `--shadow-*` | `--shadow-lift: ...;` | `shadow-lift` |
| `--breakpoint-*` | `--breakpoint-3xl: 120rem;` | `3xl:` |
| `--container-*` | `--container-narrow: 42rem;` | `@narrow:` container variant and `max-w-narrow` |
| `--ease-*`, `--animate-*` | `--ease-snappy: cubic-bezier(...)` | `ease-snappy`, `animate-*` |

Rules:

- **Replace, not add,** with `initial`: `--color-*: initial;` removes the default palette before defining ours; `--*: initial;` clears the whole default theme.
- **`@theme inline`** for variables that point at other variables (`--color-primary: var(--primary);`), so the utility uses the live value and runtime switches (dark mode, brand themes) work.
- **`:root`, not `@theme`,** for variables that should exist but not generate utilities.
- Values in rem, so user font settings scale the layout.

## Our own utility

`@utility` adds a class that works with every variant, replacing v3's `@layer utilities`:

```css
@utility content-auto {
  content-visibility: auto;
}

/* a functional utility that takes a theme value or a number */
@utility tab-* {
  tab-size: --value(integer);
}
```

`tab-4` now works, and so does `md:tab-8`. Add a utility only when the same declaration appears in many places and has no built-in equivalent; a one-off is an arbitrary property (`[content-visibility:auto]`).

## Our own variant

```css
/* match a theme set by a data attribute */
@custom-variant theme-forest (&:where([data-theme="forest"] *));

/* a state from our own attribute */
@custom-variant loading (&[aria-busy="true"]);
```

`theme-forest:bg-moss-700` and `loading:opacity-70` then work. Inside our own CSS, apply existing variants with `@variant`:

```css
.prose a {
  color: var(--primary);
  @variant hover { color: var(--primary-hover); }
}
```

## Base styles and component classes

```css
@layer base {
  html { color-scheme: light dark; }
  body { @apply bg-background text-foreground font-sans antialiased; }
  h1, h2, h3 { text-wrap: balance; }
}

@layer components {
  .prose-body { max-width: 65ch; line-height: 1.6; }
}
```

- `@layer base` for element defaults; `@layer components` for the few classes that are genuinely shared and where utilities in markup would repeat many times (long-form content styling, third-party widget overrides).
- Utilities beat components when both set a property, so `<div class="prose-body max-w-none">` works.
- `@apply` is for these layers, not a way to rebuild a component library in CSS. In React or a template language, a component is the reuse unit.

## Arbitrary values

For one-offs that are not worth a theme value (https://tailwindcss.com/docs/adding-custom-styles):

- a value: `top-[117px]`, `grid-cols-[1fr_2fr]` (underscores become spaces);
- a property: `[mask-type:luminance]`;
- a variable: `bg-(--brand-ground)`, typed when ambiguous: `text-(length:--fluid-size)`.

If the same arbitrary value appears three times, move it into the theme.

## Plugins and JavaScript config

- First-party plugins load in CSS: `@plugin "@tailwindcss/typography";`.
- An existing v3 JavaScript config can be loaded with `@config "./tailwind.config.js";` while migrating. Some v3 options are not supported (`corePlugins`, `safelist`, `separator`); use `@source inline(...)` for safelisting.
- Animation helpers for shadcn/ui: `@import "tw-animate-css";` (it replaced the `tailwindcss-animate` plugin).

## Moving a v3 config to v4

1. Replace the three `@tailwind` directives with `@import "tailwindcss";`. The official upgrade tool (`npx @tailwindcss/upgrade`) does most of this in a project with a clean git tree; review its diff.
2. Move `theme.extend` values into `@theme`, renaming keys into the namespaces above (`colors.brand.600` → `--color-brand-600`).
3. Move HSL triplets used with `hsl(var(--x))` to full colour values in the variables (`--primary: oklch(...)` or hex) and expose them with `@theme inline`; drop the `hsl()` wrappers in the config. Opacity modifiers (`bg-primary/50`) keep working.
4. Replace `@layer utilities` blocks with `@utility`.
5. Rename changed utilities: the shadow, blur and radius scales (`shadow-sm` → `shadow-xs`, `shadow` → `shadow-sm`), `outline-none` → `outline-hidden`, `ring` → `ring-3` for the old width.
6. Name a border colour wherever `border` is used (the default changed to `currentColor`).
7. Move `!` from prefix to suffix: `!p-0` → `p-0!`.
8. Check hover styles on touch devices: `hover:` now applies only where hover is possible.
9. Compile, then compare key pages before and after with screenshots.

## Keep the theme small

- The theme holds the system's values, not every value the design ever used.
- Remove the default palette (`--color-*: initial`) once the project has its own; it stops drift toward stock colours.
- Avoid one-off names (`--color-header-blue-2`); a colour without a role is a sign the semantic layer is missing (`token-architecture.md` § Layer 2: semantic roles).
- Run the anti-generic pass (`../../website/design-rules.md` § 2. Anti-generic lint) on the result: a Tailwind site with the default palette, default radius and default shadows looks like every other one.
