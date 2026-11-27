# Frontend budget: index

Read when several skills or craft packs could all claim one UI task and you need to decide what to load and which rule wins. One line per file, with the question it answers. Rebuilt in our own words from the MIT-licensed frontend-stack plugin (JaimeJunr/claude-code-frontend-skills, commit 7177def). The script is in `../../../../../data/craft/frontend-budget/load_budget.py`.

- `load-budget.md`: how many skills may load at once, when to load them, and how to measure what they cost?
- `precedence.md`: when two loaded skills disagree, which one wins, and how is the ruling recorded?
- `phase-routing.md`: how do I classify a UI request, split it into phases, and handle a vague complaint?
- `house-packs.md`: which of Ultimatum's own website packs owns what, and how are their usual collisions settled?

Not rebuilt, with reasons: `later.md`. Base rules this folder builds on: rulings log (`../../feature-planning.md` § 8), size budgets (`../../skill-author.md` § 5), token habits (`../../context-efficiency.md`).
