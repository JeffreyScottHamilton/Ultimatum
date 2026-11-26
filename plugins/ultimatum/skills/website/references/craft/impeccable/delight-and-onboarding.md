# Delight, onboarding and the motion thesis

Read when a product needs personality at the right moments, a first-run experience, or a decision on which motions earn a place.

How motion is built (curves, durations, springs, reduced motion) is in `../emil-motion/index.md`; the one authored moment on a marketing page is in `../taste/moments-and-scenes.md`. This file decides where delight and motion go, and how first use teaches.

## Motion thesis

Before animating, write four lines:
- **Focal moment**: the one sequence that deserves authorship, if any.
- **Continuity**: which state, layout or navigation changes need explaining.
- **Feedback**: which actions need acknowledging.
- **Budget**: the costly effects allowed, and their frequency.

Each motion must do one job: acknowledge an action, make a change readable, keep continuity across a change, direct attention at a moment that matters, or carry the chosen look. Remove it and something should be lost.

Pick the material by meaning: shared-element or FLIP transforms for continuity; bounded blur, light or shadow for focus and depth; masks and clip paths for reveals; colour or texture shifts for energy when the look calls for it; the smallest visible change for feedback.

By mode: Persuade and Experience pages may let motion carry the voice in one rehearsed sequence. Operate and Read surfaces keep motion to feedback and continuity, fast and repeatable.

Use CSS for declared states, the Web Animations API or the project's existing library for interruption and sequencing, and View Transitions when continuity is the point. Do not add a dependency for what the stack already does.

## Delight

Look for moments that deserve it: effort worth recognising, a wait that can inform, a first-use or empty state, a recovery after an error, an action whose response can carry the brand, a useful capability people enjoy finding.

Write one delight idea for the product, tied to its world: a response to a meaningful action, product-specific wording that also clarifies, a transition with a recognisable material feel, or a detail from the product's own world.

By moment:
- **Success**: size the reaction to the work it rewards. A big milestone can expand; a routine save stays small.
- **Waiting**: show true progress or useful context. Never fake it.
- **Empty and first use**: the next action comes before personality.
- **Errors**: lead with the problem and the fix. Warmth can help; jokes usually do not.
- **Repeated use**: must still please on the hundredth time. Variety is optional; annoyance is not.
- **Discovery**: reward curiosity without hiding anything required.

Delight must never delay or block the task, override platform conventions or access, add claims, play sound without consent or against mute, become unskippable, or cost more than the moment is worth.

Check: could a rival product use it unchanged (then it is generic)? Does the interface still work fast and plainly without it? Do muted, keyboard, touch and translated paths still work?

## Onboarding

Start with the goal: what users are trying to do, where they get stuck, and the first moment they get value. Then: their experience level, motivation, and how much time they will give.

Principles:
- **Show, do not tell**: teach inside the real product with working examples, one thing at a time.
- **Optional where possible**: a visible skip; never block the product.
- **Value fast**: teach the few things that deliver most of the value; leave advanced features for later, in context.
- **In context**: teach a feature when it is first needed; empty states are the best teaching spot.
- **Respect the user**: short, plain, no explaining standard patterns.

Pieces:
- A welcome that says what the product is, what the user will do next, and how long setup takes.
- Account setup that asks for the minimum, says why each item is needed, and fills sensible defaults.
- A checklist for multi-step setup, with progress, that can be dismissed.
- Tooltips and hints at the point of use, one at a time, dismissible, never in a chain of ten.
- Sample or template content that the user can clear in one action.

Measure it by completion of the key first action and time to that action, not by how many tour steps were seen.
