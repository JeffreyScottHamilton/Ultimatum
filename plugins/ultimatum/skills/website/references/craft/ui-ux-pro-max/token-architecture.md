# Token architecture: three layers, one source

Read when a site or app needs a design system it can theme (light and dark, or several brands), when colours and sizes are scattered as raw values across components, or before running `tools/build_tokens.py`. For the house token list a small marketing site starts from, `../taste/system.md` § Tokens is enough; this file is for when that list has to grow into a system.

## Why layers

A raw value written into a component (`#2f6b4f` in a button) has to be found and changed everywhere when the brand moves, and cannot switch for dark mode. Layers put one level of naming between the value and its use:

| Layer | Holds | Example name | Example value | Who uses it |
|---|---|---|---|---|
| 1. primitive | every raw value the system allows | `--color-moss-600` | `#2f6b4f` | only layer 2, and rare one-offs |
| 2. semantic | the job a value does | `--primary` | `var(--color-moss-600)` | components and page CSS |
| 3. component | one component's settings | `--button-bg` | `var(--primary)` | that component only |

The rule that makes it work: **each layer points only at the layer above it.** Components never name a primitive; the brand changes by editing primitives; dark mode changes only semantic roles.

Small projects can stop at two layers (primitives plus semantic roles). Add component tokens when a component is themed separately (a brand wants square buttons but round cards), or when the design system ships to more than one product.

## Layer 1: primitives

The full palette of allowed raw values. Nothing here says where a value is used.

- **Colour ramps.** One neutral family of 9-11 steps, one brand family, at most one accent family, and the four status colours (danger, warning, success, info) with a light and a dark step each. Steps are named 50 (lightest) to 950 (darkest). How to build a ramp: `brand-visual.md` § Colour: roles before values.
- **Spacing.** One base unit (`--spacing: 0.25rem`, so 4 px) and multiples of it. Tailwind v4 works the same way: `p-4` means `calc(var(--spacing) * 4)`.
- **Type.** Families with fallback stacks, a size scale from one ratio, and the weights loaded. The scale method is in `brand-visual.md` § Type: a short, loadable spec.
- **Radius.** One base (`--radius`) with steps derived from it, so one edit rounds or squares the whole system.
- **Shadow.** Two or three elevations at most, tinted with the darkest neutral rather than pure black.
- **Motion.** Durations (fast for hover and press, base for open and close, slow for page-level change) and one or two easing curves. Every animation honours `prefers-reduced-motion` (`../hallmark/craft-motion.md`).
- **Layers (z-index).** A short fixed list, not free numbers: base 0, sticky 10, dropdown 20, overlay 30, modal 40, toast 50. A new layer gets a name first.

## Layer 2: semantic roles

Name roles by job, never by look. `--primary` survives a rebrand from green to blue; `--green` does not.

A role set that covers most products, in foreground/background pairs (the same pairing shadcn/ui uses, so its components work unchanged; see `shadcn-theming.md`):

| Role | Pair | Used for |
|---|---|---|
| `background` / `foreground` | page | page ground and body text |
| `card` / `card-foreground` | raised surface | cards, panels, popovers |
| `muted` / `muted-foreground` | low emphasis | secondary text, subtle grounds, placeholders |
| `primary` / `primary-foreground` | main action | the one main button per view, links, selected state |
| `accent` / `accent-foreground` | emphasis | hover grounds in menus, highlights |
| `destructive` / `destructive-foreground` | danger | delete, errors |
| `warning`, `success`, `info` (each with `-foreground`) | status | banners, badges, field messages |
| `border`, `input`, `ring` | lines | dividers, field borders, the focus ring |

Rules:

- Every `-foreground` role is checked against its partner, and every text role against `background`. List the pairs in the token file; the generator refuses to build when one fails.
- Interaction states are roles too when they need their own value (`primary-hover`). Derive them from the ramp, one step darker in light mode, one step lighter in dark mode.
- `input` (field border) needs 3:1 against the page; a pale border that looks tidy usually fails WCAG 1.4.11.

## Layer 3: component tokens

One prefix per component, named `--<component>-<property>[-<state>]`: `--button-bg`, `--button-bg-hover`, `--field-border-invalid`, `--card-padding`. Values point at roles or at primitives for sizes:

```css
:root {
  --button-bg: var(--primary);
  --button-fg: var(--primary-foreground);
  --button-height: 2.75rem;               /* 44 px target */
  --button-radius: calc(var(--radius) - 2px);
}
.button { color: var(--button-fg); background: var(--button-bg); height: var(--button-height); }
```

A variant changes the component tokens locally instead of writing new rules (see `states-and-variants.md` § Variants by local tokens).

## Dark mode is a semantic override

Only layer 2 changes. Primitives stay fixed; components already point at roles, so they follow without edits:

```css
:root { --background: var(--color-ink-50);  --primary: var(--color-moss-600); }
.dark { --background: var(--color-ink-950); --primary: var(--color-moss-400); }
```

Do not invert the ramp mechanically. Dark grounds want a near-black that is not pure black, slightly lighter surfaces for raised cards (elevation is shown by lightness, not shadow), and brand colours a step or two lighter so they still pass on the dark ground. Re-check every pair in dark. The full method, including how to emit both modes and the OS setting, is in `../hallmark/dark-mode.md`.

## Naming and files

Names are lower case, words joined by hyphens, from general to specific: `--color-moss-600`, `--text-2xl`, `--duration-fast`, `--button-bg-hover`. Keep one meaning per name across the project.

Keep one source file and generate the rest:

```
design/tokens.json          # the source: edited by people
src/styles/tokens.css       # generated: plain custom properties
src/styles/theme.css        # generated: Tailwind v4 version (when the project uses Tailwind)
```

Our starter source is `../../../../../data/design-own/tokens/starter.tokens.json`. Its shape:

```json
{
  "primitive": { "color": { "moss": { "600": "#2f6b4f" } }, "spacing": "0.25rem" },
  "semantic":  { "primary": { "light": "{color.moss.600}", "dark": "{color.moss.400}" } },
  "pairs":     [["primary-foreground", "primary", 4.5]],
  "component": { "button": { "bg": "{primary}" } }
}
```

A `{color.moss.600}` reference points at a primitive (dotted path); `{primary}` points at a semantic role.

The W3C Design Tokens Community Group format (https://www.designtokens.org/) is the shared exchange format between design tools and code: tokens carry `$value` and `$type`, and references use the same curly-brace form. When a project already exports DTCG files from a design tool, keep that file as the source and convert it into our layout (or into CSS directly) rather than keeping two sources.

## Running the generator

```
python3 tools/build_tokens.py --in design/tokens.json --out-dir src/styles
python3 tools/build_tokens.py --in design/tokens.json --out-dir src/styles --check
```

It prints every pair with its ratio in both modes, stops with exit 1 on any fail or unknown reference, and writes `<name>.tokens.css` and `<name>.theme.css`. Run `--check` in CI so a hand edit to the CSS, or a JSON edit without a rebuild, fails the build. What the two outputs contain and how they were tested: `token-templates.md`.

## Moving a flat stylesheet to layers

1. **Collect.** List every colour, size, radius, shadow and duration the CSS uses (search for `#`, `rgb(`, `px`, `rem`, `ms`). Expect near-duplicates.
2. **Merge.** Snap near-duplicates to one value each; that list is the primitive layer. Every merge is a visible change, so note it.
3. **Name the jobs.** For each place a colour is used, decide its role. Most projects find 15-25 roles.
4. **Swap in passes.** Replace raw values with roles one component at a time, checking the page after each pass; screenshots before and after catch drift.
5. **Add dark mode last,** once every component uses roles only.
6. **Lock it.** Add a check that fails on raw colour values outside the token file (a simple search in CI is enough).
