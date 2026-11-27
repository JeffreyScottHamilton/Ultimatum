# Tailwind utilities and responsive layout (v4)

Read when writing markup with Tailwind CSS v4: picking utilities, building responsive layouts, using container queries, or fixing classes that do not apply. Changing the theme or adding utilities of our own is in `tailwind-customisation.md`. Checked against the official docs at https://tailwindcss.com/docs (pages cited per section). The house layout and breakpoint rules are in `../hallmark/responsive.md` and `../hallmark/layout.md`; this file is how to express them in Tailwind.

## How utilities work

- One class, one job: `flex`, `gap-4`, `text-lg`, `bg-primary`. Variants prefix it: `hover:`, `focus-visible:`, `md:`, `dark:`, and they stack (`dark:md:hover:bg-muted`).
- When two utilities set the same property, the one later **in the stylesheet** wins, not the one later in the class attribute. Do not put `p-2 p-4` on one element and expect `p-4`; remove the other, or use a merge helper such as `cn()` (https://tailwindcss.com/docs/styling-with-utility-classes).
- Reuse comes from components or template partials, not from long shared class strings or `@apply` everywhere.
- Important, when nothing else works: a `!` suffix (`bg-red-500!`); v3's prefix form changed in v4.

## Class names must be complete

Tailwind scans source files for class names as plain text. A class built at runtime is never generated (https://tailwindcss.com/docs/detecting-classes-in-source-files):

```tsx
// never generated: the scanner never sees "bg-red-600"
<div className={`bg-${tone}-600`} />

// generated: every full name appears in the source
const tones = { danger: "bg-destructive text-destructive-foreground", ok: "bg-success text-success-foreground" };
<div className={tones[tone]} />
```

Classes from a package in `node_modules` need `@source "../node_modules/<package>";`. A class that appears nowhere in source can be forced with `@source inline("underline");` (braces expand: `@source inline("{hover:,}underline");`).

## The utilities used most

| Need | Utilities | Notes |
|---|---|---|
| stack and row | `flex flex-col gap-4`, `flex items-center justify-between` | `gap-*` over margins between children |
| grid | `grid grid-cols-1 md:grid-cols-3 gap-6`, `grid-cols-[16rem_1fr]` | arbitrary tracks use underscores for spaces |
| auto-fit cards | `grid grid-cols-[repeat(auto-fill,minmax(16rem,1fr))] gap-6` | no breakpoints needed |
| spacing | `p-6`, `px-4`, `py-2`, `mt-8`, `space-y-4` | every step is `--spacing` x n, so `p-4` is 1 rem by default |
| size | `w-full`, `max-w-prose`, `size-10`, `min-h-dvh` | `size-*` sets width and height together |
| measure | `max-w-[65ch]` | body text line length |
| type | `text-base/7` (size with line height), `font-semibold`, `tracking-tight`, `text-balance` | `text-balance` for headings, `text-pretty` for paragraphs |
| colour | `bg-card`, `text-muted-foreground`, `border-border` | use role colours, not palette steps, in components |
| opacity of a colour | `bg-primary/90`, `bg-black/50` | the modifier works with role colours too |
| border and radius | `border`, `border-input`, `rounded-lg`, `divide-y` | in v4 the default border colour is `currentColor`; always name one |
| shadow | `shadow-sm` | v4 renamed the scale: v3 `shadow-sm` is now `shadow-xs`, v3 `shadow` is `shadow-sm` |
| focus | `outline-2 outline-offset-2 outline-ring`, each with the `focus-visible:` prefix | `outline-hidden` replaced v3's `outline-none` |
| position | `relative`, `absolute inset-0`, `sticky top-0` | |
| layer | `z-10`, or named values from the theme | see `token-architecture.md` § Layer 1: primitives |
| media | `aspect-video`, `object-cover` | set an aspect ratio on every image box |
| overflow | `overflow-x-auto` on a table wrapper, `truncate`, `line-clamp-3` | never on the page itself |
| state | `disabled:opacity-55`, `aria-invalid:border-destructive`, `data-[state=open]:bg-accent` | style from attributes, as in `states-and-variants.md` |
| motion | `transition-colors duration-150`, `motion-reduce:transition-none` | never `transition-all` |
| one-off | `top-[117px]`, `[mask-type:luminance]`, `bg-(--brand-ground)` | arbitrary values; a repeated one belongs in the theme |

Version traps when reading older examples (https://tailwindcss.com/docs/upgrade-guide): `@import "tailwindcss"` replaces the three `@tailwind` lines; `ring` is now 1 px (`ring-3` for the old width); blur, radius and drop-shadow scales shifted like shadows; `hover:` applies only on devices that can hover.

## Responsive: mobile first

Unprefixed utilities apply at every width; a prefix applies **from** that width up (https://tailwindcss.com/docs/responsive-design):

| Prefix | From |
|---|---|
| `sm:` | 40rem (640 px) |
| `md:` | 48rem (768 px) |
| `lg:` | 64rem (1024 px) |
| `xl:` | 80rem (1280 px) |
| `2xl:` | 96rem (1536 px) |

So write the phone layout first, then add what changes: `flex flex-col md:flex-row`. `sm:` does not mean "on small screens"; it means "from 640 px".

- Below a width: `max-md:hidden`. A range: `md:max-xl:grid-cols-2`.
- Custom breakpoints go in the theme, in rem: `@theme { --breakpoint-3xl: 120rem; }` makes `3xl:`. Pick breakpoints where the content breaks, not at device widths (`../hallmark/responsive.md` § Breakpoints).
- One-off: `min-[900px]:grid-cols-4`.

Common shapes:

```html
<!-- sidebar that drops below on phones -->
<div class="grid gap-8 lg:grid-cols-[16rem_1fr]">
  <aside>...</aside><main>...</main>
</div>

<!-- hero: stacked on phones, side by side from md -->
<section class="grid items-center gap-10 md:grid-cols-2">
  <div class="max-w-[38ch]"><h1 class="text-4xl md:text-5xl text-balance">...</h1></div>
  <img class="aspect-[4/3] w-full object-cover rounded-lg" src="..." alt="...">
</section>

<!-- navigation: menu button on phones, links from md -->
<nav class="flex items-center justify-between">
  <a href="/">...</a>
  <button class="md:hidden size-11" aria-expanded="false" aria-controls="menu">...</button>
  <ul id="menu" class="hidden md:flex gap-6">...</ul>
</nav>
```

Fluid type with `clamp()` avoids jumps between breakpoints: `text-[clamp(2rem,1.2rem+3vw,3.5rem)]`, or put the value in the theme as `--text-display`.

## Container queries

When a component's layout should depend on the space it is given, not on the window (a card used in a sidebar and in a wide grid), use container queries (https://tailwindcss.com/docs/responsive-design):

```html
<div class="@container">
  <article class="flex flex-col @md:flex-row gap-4">...</article>
</div>
```

- `@container` marks the parent; `@sm:`, `@md:` and up apply from that container width; `@max-md:` below it.
- Name containers when they nest: `@container/main` on the parent, `@lg/main:` on the child.
- Container sizes run from `@3xs` (16 rem) to `@7xl` (80 rem); one-offs with `@min-[475px]:`.

Prefer container queries for reusable components, and viewport breakpoints for the page frame.

## Checks at each width

- 320 px wide: nothing cut off, no sideways scroll on the page (WCAG 2.2 SC 1.4.10 Reflow);
- tap targets at least 44 px (`../../website/design-rules.md` § 7. Interface basics);
- body text 16 px or more, lines 45-75 characters;
- images keep their ratio and do not push the layout while loading;
- the menu opens, closes and traps nothing;
- the full check list by width is `../hallmark/responsive.md` § Check by eye at each width.
