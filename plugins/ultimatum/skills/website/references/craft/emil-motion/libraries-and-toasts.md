# Choosing a library, and working with toasts

Read when a task smells like a solved problem (toast, command menu, dialog, long list, drag and drop, animated number, chart, theme switch) or when a toast misbehaves. Rows: `../../../../../data/craft/emil-motion/libraries.csv`. For which libraries Ultimatum already prefers on website builds, `../../website/libraries.md` comes first; where it disagrees with this list, that file wins.

## Choosing

1. Start from the job, not from the library name in the request. A dropdown is an accessible-primitives job whichever package was mentioned.
2. Read `package.json`. If a listed library is installed, use it. If a competitor is, flag the suggestion but do not churn the dependency.
3. Recommend one library, say in a sentence what it is for, and wire it if asked. No menus of five.
4. If the task is not in the list, say so and recommend from your own knowledge, marked as outside the list.
5. Plain CSS wins when it can: a hover or fade needs no animation library; reach for one when you need springs, layout animation, exit animation or gesture-driven values (`components.md`, `springs.md`).

## Mismatches to catch

- Hand-built toasts, or a modal library used as a toast: use a toast library.
- A div dropdown or dialog with hand-rolled focus: use an accessible primitive set (focus trap, dismissal, roles).
- A number animated by re-rendering text: use a digit-transition library, with `tabular-nums` fallback (`ui-details.md`).
- 1,000-plus rows rendered directly: virtualise before inventing pagination tricks.
- A web of props passed down for shared state: a small store.
- Three-deep class ternaries: a class joiner, or a variant helper when the component has real variants.

## Toasts

One `<Toaster />`, mounted once, near the root (in Next.js, the root layout). Never per page or conditionally. `toast()` is a client-side function: for server actions, send the outcome back and show the toast from client code.

| You want | Call |
|---|---|
| Plain message | `toast('Title')`, plus `{ description }` for a second line |
| Typed icon | `toast.success`, `.error`, `.info`, `.warning` |
| Spinner you manage | `toast.loading('...')` then update by id |
| Loading to success or error with a promise | `toast.promise(p, { loading, success, error })` |
| Button inside | `{ action: { label, onClick } }`; `cancel` is the quiet one; closes unless `onClick` calls `preventDefault()` |
| Custom JSX in the default shell | `toast(<jsx />)` |
| Custom JSX, no styles | `toast.custom(t => <jsx />)` |

Recipes: update by calling again with the same `id`; persist with `duration: Infinity`; dismiss with `toast.dismiss(id)` or no argument for all; several toasters need an `id` each and `toasterId` on the call. `onDismiss` (close button or swipe) and `onAutoClose` (timeout) are two hooks, and nothing fires for both.

Styling ladder, stop at the lowest rung that works: defaults with `richColors` or `invert`; inline `style`; `classNames` per part (needs `!important` unless unstyled); headless `toast.custom` inside your own wrapper function, which suits a design system. Theme defaults to light and does not follow the OS: pass `theme="system"` or your resolved theme.

| Symptom | Likely cause |
|---|---|
| Nothing shows | the Toaster was never mounted or got unmounted; or `toast()` ran on the server |
| Appears twice | two Toasters, or an effect firing twice in React StrictMode in dev; fire from the handler or pass a stable `id` |
| Your classes do nothing | default styles win; `!important` or unstyled |
| Completely unstyled (Astro, view transitions) | the injected stylesheet was lost; import the library's CSS in the layout |
| Behind a modal or clipped | an ancestor makes a stacking context (`transform`, `filter`, `overflow`); move the Toaster to the root |
| Dark mode ignored | theme default is light |
| Stays forever | `duration: Infinity`, not dismissible, or a promise that never settles |
| Swipe goes the wrong way | directions follow `position`; set `swipeDirections` |
| Too near the edge on a phone | `offset` and `mobileOffset` |

Toast motion rules (opacity plus height, asymmetric timing, stack behaviour) are in `components.md`. A toast that carries an error a person must act on needs `role="alert"` semantics and must not vanish on a timer (`reduced-motion.md`, WCAG 2.2.1).

## API reference

Options, defaults and types live in the library docs: https://sonner.emilkowal.ski and https://motion.dev. Check them at the version you install; the defaults above (four seconds, three visible, bottom right) can change.
