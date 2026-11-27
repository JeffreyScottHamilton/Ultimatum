# shadcn/ui components: adding, choosing and changing them

Read when a React project uses (or should use) shadcn/ui: setting it up, picking the right component for a job, building forms, or changing a component's look. Theming is in `shadcn-theming.md`; keyboard and screen-reader behaviour in `shadcn-accessibility.md`. Facts here are checked against the official docs at https://ui.shadcn.com/docs; when they disagree, the docs win, because the project moves quickly.

## What it is, and what that means for us

shadcn/ui describes itself as "not a component library": the CLI copies each component's source into the project, where it is ours to read and edit (the docs call this "Open Code"). Consequences:

- There is no package to upgrade. A fix upstream reaches us only if we re-add or diff the component (`npx shadcn@latest add button --diff`).
- Edits are expected. Change the copied file rather than wrapping it in layers of overrides.
- Components are built on Radix primitives (or Base UI in newer setups) for behaviour and on Tailwind for looks. The current line targets Tailwind CSS v4 and React 19: `forwardRef` is gone, each part carries a `data-slot` attribute for styling, colours are OKLCH, the old toast is replaced by Sonner, and `tw-animate-css` replaces `tailwindcss-animate` (https://ui.shadcn.com/docs/tailwind-v4).

## Setting up

```
npx shadcn@latest init          # writes components.json, the theme CSS and the cn() helper
npx shadcn@latest add button card dialog
npx shadcn@latest add button --dry-run   # show what would change, write nothing
```

`init` asks for a base colour and writes CSS variables into the global stylesheet (https://ui.shadcn.com/docs/cli). `components.json` records the choices (https://ui.shadcn.com/docs/components-json):

| Field | Holds | Note |
|---|---|---|
| `style` | `new-york` | fixed after init; the old `default` style is deprecated |
| `tailwind.config` | empty for Tailwind v4 | v4 is configured in CSS |
| `tailwind.css` | path to the global CSS | where the theme variables live |
| `tailwind.baseColor` | neutral, stone, zinc, and others | the neutral ramp the theme starts from |
| `tailwind.cssVariables` | `true` (default) | keep it: theming depends on it |
| `tailwind.prefix` | optional class prefix | |
| `rsc`, `tsx` | React Server Components, TypeScript | `rsc` adds `"use client"` where needed |
| `aliases` | import paths for `components`, `ui`, `lib`, `hooks`, `utils` | must match the project's path aliases |

Before adding to an existing project, check that the aliases match `tsconfig.json` paths and that the CSS file named in `components.json` is the one the app actually imports.

## Choosing the component

| Job | Use | Not |
|---|---|---|
| start an action | Button | a styled `div` |
| go somewhere | a link (Button with `asChild` around the link, if it must look like a button) | Button with an `onClick` that navigates |
| one line of text | Input (with Label) | |
| several lines | Textarea | |
| pick one of a few (2-5), all visible | Radio Group | Select |
| pick one of many | Select; Combobox (Popover + Command) when the list needs search | Radio Group |
| yes/no that applies at once | Switch | Checkbox |
| yes/no submitted with a form, or many independent options | Checkbox | Switch |
| a date | Date Picker (Calendar inside Popover); a plain date Input when the date is far from today (birth dates) | |
| group content about one thing | Card | Card around every section |
| switch between views of one thing | Tabs | Tabs for steps of a process |
| show and hide sections | Accordion | Accordion for primary content people must read |
| site navigation with sub-menus | Navigation Menu | Dropdown Menu |
| actions on an item | Dropdown Menu | |
| a focused task that blocks the page | Dialog; Drawer or Sheet on phones | |
| confirm a destructive action | Alert Dialog | Dialog |
| a small floating panel tied to a control | Popover | Dialog |
| a hint on hover and focus | Tooltip (never the only place for essential text) | |
| command palette, searchable list | Command | |
| short-lived notice after an action | Sonner (toast) | an alert for errors that need action |
| status inside the page | Alert | a toast |
| progress of a known length | Progress | a spinner |
| loading placeholder | Skeleton sized like the content | |
| records to compare | Table (Data Table with TanStack Table for sorting and filters) | cards |
| a person | Avatar with a fallback of initials | |
| status or category label | Badge | Badge as a button |

The component specs (sizes, states, behaviour) we hold them to are in `component-specs.md`.

## Forms

shadcn/ui's form docs cover several form libraries, React Hook Form and TanStack Form among them, with a `Field` component family for label, control, description and error (https://ui.shadcn.com/docs/components/form). The pattern that stays the same whichever library is used:

1. Describe the data once with a schema (Zod is the usual choice) and derive both validation and the TypeScript type from it.
2. Each field: a visible label, the control, a description if needed, and the error message joined to the control (`aria-describedby`, `aria-invalid`). The shadcn field parts wire this when used as documented; check the rendered HTML once.
3. Validate on blur and submit, not on each keystroke; validate again on the server.
4. On submit failure, move focus to the first invalid field, or to an error summary at the top for long forms.
5. Keep the submit button enabled; say what is missing when pressed (`states-and-variants.md` § Each state has its attribute).

```tsx
const signup = z.object({ workEmail: z.string().email("Enter an email like name@example.com") });
// useForm({ resolver: zodResolver(signup) }) with React Hook Form,
// then render each field with the shadcn Field parts: Label, Input, description, error.
```

Write error messages that say what to do ("Enter a date after today"), not what is wrong in the abstract ("Invalid input"). Copy rules: `../taste/copy.md`.

## Variants

Components with variants (Button, Badge, Alert) define them with `class-variance-authority` (cva): a base class string plus a map of variant name to classes. To add a variant, edit the map in the copied file:

```tsx
const buttonVariants = cva("inline-flex gap-2 items-center justify-center font-medium text-sm rounded-md ...", {
  variants: {
    variant: {
      outline: "border border-input bg-background hover:text-accent-foreground hover:bg-accent",
      default: "text-primary-foreground bg-primary hover:bg-primary/90",
      success: "bg-success text-success-foreground hover:bg-success/90",   // ours, added
    },
    size: { default: "h-9 px-4", lg: "h-11 px-6", icon: "size-9" },
  },
  defaultVariants: { variant: "default", size: "default" },
});
```

A new colour variant needs its colour role first (`shadcn-theming.md` § Adding a colour role). The house rule on targets is 44 px (`../../website/design-rules.md` § 7. Interface basics), larger than the stock `default` size: raise the heights in the map, or extend the hit area.

## Changing one instance

- Pass `className`; the `cn()` helper merges classes and lets later Tailwind classes replace earlier conflicting ones, so `<Button className="w-full">` works as expected.
- Style a part through its slot: `[&_[data-slot=card-title]]:text-lg`, or `*:data-[slot=...]` selectors.
- For anything that will be reused, add a variant instead of repeating a long `className`.
- Do not wrap a component in another component only to change its colours; change the theme or the variant map.

## Keeping copies healthy

- Record in the project README which components were edited and why.
- When upgrading, `npx shadcn@latest add <name> --diff` shows the upstream changes against the local copy; merge by hand.
- Keep the copied files in `components/ui/`, and build page-level pieces in a separate folder, so it stays clear what came from the CLI.
