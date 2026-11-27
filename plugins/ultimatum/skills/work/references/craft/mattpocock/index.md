# Matt Pocock craft: deeper notes on planning, design and tests

Read when planning or test-first work needs more than the base files give: long question rounds, a spec and ticket graph, deep-module design, domain language, prototypes, test seams, or TypeScript test and package habits.

Rebuilt from the ideas in mattpocock/skills at commit d653911 (MIT). All wording and code here are ours. The base rules live in `../../feature-planning.md` and `../../tdd.md`; these files only add what those leave out.

- `question-rounds.md`: settling many linked decisions in rounds by frontier, facts versus decisions, and a questionnaire for an expert who is not in the chat.
- `spec-and-tickets.md`: writing the spec from a settled talk, agreeing test seams, tickets with blocking edges, wide refactors by blast radius, and publishing locally or to a tracker.
- `deep-modules.md`: the design words (module, interface, seam, depth, adapter), three quick tests, deepening by dependency kind, and designing an interface twice.
- `domain-language.md`: challenging terms during a talk, what a glossary entry holds, and the three-part bar for a decision record.
- `prototypes.md`: a one-file logic demo with guided scenarios, or layout variants on one route behind a URL parameter.
- `test-seams.md`: agreeing seams before the first test, growing tests one at a time, and fakes shaped like the client.
- `typescript-habits.md`: partial test data without `as` casts, and packages reachable only through their entry files, with a check that must be seen to fail.

Scripts: `../../../../../data/craft/mattpocock/` (`ticket_order.py`, `entry_imports.py`).

Not rebuilt, with reasons: `later.md`.
