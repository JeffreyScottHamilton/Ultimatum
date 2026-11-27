# Prototypes: a clickable logic demo, or variants on one page

Read when a design question is about a state model ("does this flow hold up?") or about how a screen should look ("which layout?"), and reading the code cannot answer it.

When to prototype at all, the throwaway label and "never grow it into the shipped code" are in (`../../feature-planning.md` § 5). This file covers the two shapes and how each is handed over.

## Pick the shape from the question

| Question | Shape | Lives |
|---|---|---|
| does this state model or rule set hold up? | one HTML file with buttons | next to the module it is for, or a scratch folder |
| what should this screen look like? | several layouts on one route, switched by a URL parameter | inside the existing page when one exists |

A wrong pick throws away all the work. When the question stays unclear and the user is away, choose by the code around it (a backend module means logic, a page means layout) and write that guess at the top of the prototype.

Both shapes: one obvious command or a double-click to start; state in memory only, unless storage is the question (then a scratch file named so nobody keeps it); no tests, no polish; show the full state after every action or switch.

## The logic demo

1. Put the question in a visible paragraph at the top of the page, so anyone can check later whether the demo answers it.
2. Write the logic as a small pure module inside one `<script>`: a reducer `(state, action) => state`, an explicit state machine when "which actions are legal now?" is part of the question, or plain functions over a data type. No DOM access in it; the page calls it, never the reverse. That module is the part worth keeping.
3. Lay the page out as: title and question, a readable state panel (labelled fields, not raw JSON), one button per action for free play, and tabs of guided scenarios. Each scenario resets to a fixed start and walks through its steps as buttons: the happy path, an awkward edge case, and an attempt at something that should be refused.
4. Keep it plain: readable type, room to breathe, one accent colour, no animation.
5. Hand over the file. The useful moments are "that should not be possible" and "I expected something else": those are flaws in the idea, found before any production code.

No framework, bundler or server: the recipient may not be a developer.

## Layout variants on one route

1. Prefer mounting the variants inside the page that will host the feature, with its actual header, data and density. An empty new route makes every variant look fine. Use a new route only when nothing could host it, follow the project's routing convention, and put "prototype" in the path.
2. Three variants by default, five at most. They must differ in structure (layout, hierarchy, main action), not in colour. If two come out alike, redo one with an explicit "not a card grid" style constraint.
3. Read the choice from a URL parameter such as `?variant=b` so a link reproduces it and reload keeps it. Keep data loading above the switch; only the rendered part changes.
4. Add a small switcher bar fixed at the bottom: previous, current label, next, plus arrow keys, ignored while a text field has focus. Make it look unlike the design under test, and render it only outside production builds.
5. Hand over the URL and the variant keys. Expect answers like "header from B, list from C": that mix is the design they want.

Check the layout variants at phone and desktop width before handing over (`../../browser-verification.md` § 2).

## Afterwards

Record the answer (the question, the verdict, the reason) in the spec or rulings log, fold the decided logic or the winning layout into the codebase through the normal slices, and remove the prototype from the working branch. If the user wants it kept as a reference, push it to a separate throwaway branch only with their yes, and link that branch from the ticket.
