# Ultimatum's website packs: owners and collisions

Read when a website or web app task could load more than one of Ultimatum's own craft packs, or two of them seem to disagree.

## 1. Who owns what

The house rules (`../../../../website/references/website/design-rules.md`) are the base for every page and win over any pack's defaults, as each pack's index already says. Below them, one owner per topic:

| Topic | Owner | Notes |
|---|---|---|
| Direction, layout, type and colour for a marketing page | Taste (`../../../../website/references/craft/taste/index.md`) | the usual lead for a new page |
| A themed layer over a Taste page | Hallmark (`../../../../website/references/craft/hallmark/index.md`) | a support on top of Taste, not a second lead; it points to Taste where they overlap |
| Motion on a marketing page | Taste's motion file (`../../../../website/references/craft/taste/motion.md`) | its index says it wins on marketing pages |
| Motion in product UI, gestures, polish | Emil motion (`../../../../website/references/craft/emil-motion/index.md`) | deeper on screens people use every day |
| Explanatory isometric figures | Anatomy (`../../../../website/references/craft/anatomy/index.md`) | load only when a figure is planned |
| Review, audit and QA | Design review and QA (`../../../../website/references/craft/design-review-qa/index.md`) | the finish phase lead |

Other packs added later slot in by the same test: which single topic do they own, and what does their index say about the house rules?

## 2. A plan that fits the budget

A typical new marketing page: Direction (lead Taste, support Anatomy if a figure is planned), Build (lead Taste), Motion (lead Taste's motion file, Emil motion as support for interactive controls), Review (lead design review and QA). Check it with `load_budget.py plan` (`load-budget.md` § 5).

## 3. Usual collisions and default rulings

These are the disagreements that come up between page, motion and review rules in general. The ladder (`precedence.md` § 1) still applies first; these are the defaults when it does not decide.

| Collision | Default ruling |
|---|---|
| Long, showy motion on a page vs short, functional motion in controls | the page may stage its hero and scroll moments; buttons, menus, dialogs and toasts keep short timings and honour reduced motion |
| Which animation library | CSS first; then whatever the project already has; add a scroll library only for scroll-driven storytelling, a spring library only for gestures; never two in one component |
| A common default font vs "pick a distinctive face" | the brand or project wins; otherwise choose from the concept and language coverage, and allow the common face when the user asks or the product is dense and neutral |
| Centred hero | allowed when the first screen also shows something real from the product; centred text over a blank glow stays a tell |
| Monospace labels | for real code, identifiers and aligned numbers; not as decoration on nav, eyebrows or captions |
| Very dark grounds | a dark ground tied to the brand hue with a reason; untinted near-black as a default is not a direction; pure black when the world calls for it |
| Who writes the design file | one owner per project; other packs read it, and any pack that writes its own format uses its own file name so the main one is not overwritten |
| Critique of a design that has no code yet vs a built page | with code or a running page, the review pack owns it; a screenshot of a page that exists counts as built |
| Several reviewers on one page | one finish reviewer per page; add the motion review only when the change moves |
| Dashes and other writing tics in UI copy | apply the house writing rules to copy we write; never rewrite copy the user supplied |
