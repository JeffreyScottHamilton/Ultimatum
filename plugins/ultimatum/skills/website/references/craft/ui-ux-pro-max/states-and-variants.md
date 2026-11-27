# States and variants: how a component changes, and in what order

Read when specifying or building an interactive component and deciding how its states combine, how variants are made, and which ARIA attribute goes with each state. The list of the eight states and how each should look is in `../hallmark/interaction-and-states.md` § The eight states; the focus ring and hit target rules are in the same file. This file covers what that one leaves out: precedence, the state attributes, and building variants from tokens.

## When states overlap, one wins

A button can be hovered, focused and loading at once. Decide the order once and apply it everywhere:

| Rank | State | Why it wins |
|---|---|---|
| 1 | disabled | nothing else may suggest it can be used |
| 2 | loading | the action is under way; pressing again must look pointless |
| 3 | error | the user has to see what went wrong before anything else |
| 4 | active (pressed) | instant feedback for the press itself |
| 5 | focus | always visible, and it **combines** with every state below it |
| 6 | hover | the weakest signal; pointer devices only |
| 7 | default | |

Focus is the exception to "one wins": the ring stays on top of hover, active and error, because a keyboard user must always know where they are. A disabled control that stays focusable (see below) keeps its ring too.

In CSS, write states in rank order from weakest to strongest, so later rules win on equal specificity, and gate hover on real pointers:

```css
.button { background: var(--button-bg); }
@media (hover: hover) { .button:hover { background: var(--button-bg-hover); } }
.button:active { transform: translateY(1px); }
.button:focus-visible { outline: var(--ring) solid 2px; outline-offset: 0.125rem; }
.button[aria-invalid="true"] { border-color: var(--destructive); }
.button[aria-busy="true"] { cursor: progress; }
.button:disabled, .button[aria-disabled="true"] { opacity: 0.55; cursor: not-allowed; }
```

Tailwind v4 already applies `hover:` only inside `@media (hover: hover)` (https://tailwindcss.com/docs/upgrade-guide).

## Each state has its attribute

Style from the attribute that tells assistive technology the same thing; then the look and the meaning cannot drift apart.

| State | Attribute | Notes |
|---|---|---|
| disabled, cannot be focused | `disabled` | native controls only; removed from tab order and not announced as actionable |
| disabled, must stay discoverable | `aria-disabled="true"` | stays in tab order, so the user can reach it and read why; the script must block the action itself |
| loading | `aria-busy="true"` on the updating region; keep the label | announce the result through a live region, not the spinner |
| error | `aria-invalid="true"` plus `aria-describedby` pointing at the message | the message says what to do, not only that it failed |
| pressed toggle | `aria-pressed="true"` / `"false"` | for a button that stays on |
| expanded | `aria-expanded` on the control that opens something | menus, accordions, disclosure |
| selected | `aria-selected` (tabs, options) or `aria-current="page"` (navigation) | not a class alone |
| checked | native `checked`, or `aria-checked` on a custom switch | prefer the native input |

Prefer `aria-disabled` over `disabled` when the reason for disabling matters (a submit button waiting for a required field): a disabled button that cannot be focused gives no clue why. Better still, leave the button enabled and say what is missing when it is pressed.

## Transitions

Animate only colour, opacity and transform, for 120-180 ms with an ease-out curve; never `transition: all` (`../../website/design-rules.md` § 7. Interface basics). Focus rings appear with no delay. Under `prefers-reduced-motion: reduce`, keep colour changes and drop movement.

## Loading without layout shift

- Keep the label and the width: put the spinner before the label, or overlay it and make the label transparent, so the button does not resize.
- Disable repeat presses during the request (`aria-busy`, and ignore clicks) but keep the button focusable.
- Under about 300 ms, show nothing; a flash of spinner reads as a glitch.
- For a region (a table, a card list), show a skeleton sized like the real content, and put `aria-busy="true"` on the region until it fills.

## Errors

The field's border takes the destructive colour, a message appears below it in text (never only red), and the message is linked with `aria-describedby`. Show errors after the user leaves the field or submits, not on each keystroke. Remove the error as soon as the value is valid. The full field anatomy is in `../hallmark/interaction-and-states.md` § The field (input, textarea, select, combobox).

## Variants by local tokens

A variant is a different set of component tokens, not a new set of rules. Override the tokens on the variant class and the base rules do the rest:

```css
.button {
  --button-bg: var(--primary); --button-fg: var(--primary-foreground);
  --button-bg-hover: var(--primary-hover); --button-border: transparent;
  color: var(--button-fg); background: var(--button-bg);
  border: 1px solid var(--button-border);
}
.button--secondary { --button-bg: var(--muted); --button-fg: var(--foreground); --button-bg-hover: var(--border); }
.button--outline   { --button-bg: transparent; --button-fg: var(--foreground); --button-border: var(--input); --button-bg-hover: var(--muted); }
.button--ghost     { --button-bg: transparent; --button-fg: var(--foreground); --button-bg-hover: var(--muted); }
.button--danger    { --button-bg: var(--destructive); --button-fg: var(--destructive-foreground); }
```

Sizes the same way: `.button--sm { --button-height: 2.25rem; }` (and enlarge the hit area invisibly to 44 px, as the hallmark file shows).

In React with Tailwind, the common way to express the same idea is a variant map (shadcn/ui uses `class-variance-authority`); see `shadcn-components.md` § Variants.

Keep the variant set small. One main (primary) button per view, a secondary for the alternative, outline or ghost for low-priority actions, and danger only for destroying data. More variants than that is usually a hierarchy problem, not a styling one.

## Check every variant in every state

For each variant, render the full grid (default, hover, focus, active, disabled, loading, error where it applies) in light and dark, and check:

- text on each ground meets 4.5:1; the border of an outline control and the focus ring meet 3:1 (WCAG 2.2 SC 1.4.3, 1.4.11);
- disabled still reads as text (a disabled label may fall below 4.5:1; WCAG exempts inactive controls, but it must still be readable);
- the focus ring is visible on every ground, including on the danger variant.
