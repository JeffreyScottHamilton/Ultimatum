# Matt Pocock skills rebuild: coverage map

Source: mattpocock/skills at commit d653911 (MIT, LICENSE read at that commit). Ours: `plugins/ultimatum/skills/work/references/craft/mattpocock/` and `plugins/ultimatum/data/craft/mattpocock/`.

## How this map was made

- Items are the main sections of the in-scope skills (grilling, grill-me, to-questionnaire, to-spec, to-tickets, tdd with its tests and mocking files, codebase-design with deepening and design-it-twice, domain-modeling with its glossary and ADR formats, prototype with its logic and UI files, setup-ts-deep-modules, migrate-to-shoehorn), grouped where several sections carry one idea. Skills outside the brief share one row.
- Status: `covered` (same idea, our words, in a new file), `expanded` (we add to it: a runnable script or typechecked example, the untrusted-input rule, the user's yes for remote or dependency changes), `merged` (already in an existing reference, so not repeated), `later` (in `later.md`, not shipped).
- Much of the source was already merged into `feature-planning.md` and `tdd.md`; the new files hold only what goes deeper.
- Not verified: the source's external links were not followed; the shoehorn and dependency-cruiser libraries were not installed or run (only their documented function and rule names are cited).

## Items

| Source item | Status | Where |
|---|---|---|
| grilling: decisions as a tree | covered | question-rounds.md § Picture the decisions as a tree |
| grilling: rounds over the frontier | covered | question-rounds.md § One round |
| grilling: numbered questions with a recommended answer | covered | question-rounds.md § One round |
| grilling: word questions so yes accepts the pick | covered | question-rounds.md § One round |
| grilling: dependent questions wait a round | covered | question-rounds.md § Picture the decisions as a tree |
| grilling: facts are looked up, decisions go to the user | merged | feature-planning.md § 2; question-rounds.md § One round |
| grilling: lookups run without blocking the round | covered | question-rounds.md § One round |
| grilling: done when the frontier is empty, confirm before acting | expanded | question-rounds.md § When it ends (rulings log, rule 4) |
| grill-me alias | merged | question-rounds.md |
| to-questionnaire: ask only about the send | covered | question-rounds.md § When someone else holds the answers |
| to-questionnaire: recipient step | covered | question-rounds.md § When someone else holds the answers |
| to-questionnaire: what you need back | covered | question-rounds.md § When someone else holds the answers |
| to-questionnaire: document structure and ordering | covered | question-rounds.md § When someone else holds the answers |
| to-questionnaire: one idea per question, why-line only when needed | covered | question-rounds.md § When someone else holds the answers |
| to-questionnaire: closing catch-all | covered | question-rounds.md § When someone else holds the answers |
| to-questionnaire: answers as data | expanded | question-rounds.md § When someone else holds the answers (untrusted) |
| to-spec: synthesize, no new interview | covered | spec-and-tickets.md § Write the spec from what you already have |
| to-spec: explore the repo, use glossary and ADRs | merged | feature-planning.md § 2; spec-and-tickets.md |
| to-spec: sketch seams, prefer existing and highest, confirm | covered | spec-and-tickets.md § Write the spec from what you already have |
| to-spec: problem and solution | merged | feature-planning.md § 6 |
| to-spec: long user-story list | covered | spec-and-tickets.md § Write the spec from what you already have |
| to-spec: implementation decisions | merged | feature-planning.md § 6 (Interfaces) |
| to-spec: no paths or code, prototype snippet exception | expanded | feature-planning.md § 6; spec-and-tickets.md (snippet exception) |
| to-spec: testing decisions | covered | spec-and-tickets.md § Write the spec from what you already have |
| to-spec: out of scope, further notes | merged | feature-planning.md § 6 (Non-goals, Open points) |
| to-spec: publish with triage label | later | later.md (label vocabulary) |
| to-tickets: gather context, read referenced issue | merged | feature-planning.md § 2 |
| to-tickets: prefactor first | merged | feature-planning.md § 7 |
| to-tickets: vertical slice rules | merged | feature-planning.md § 7 |
| to-tickets: blocking edges | expanded | spec-and-tickets.md § Cut tickets as a graph (ticket_order.py) |
| to-tickets: wide refactor expand-migrate-contract | merged | feature-planning.md § 7 |
| to-tickets: batches by blast radius | covered | spec-and-tickets.md § Wide refactors that cannot stay green in one step |
| to-tickets: shared integration branch fallback | covered | spec-and-tickets.md § Wide refactors that cannot stay green in one step |
| to-tickets: quiz the user on granularity and edges | covered | spec-and-tickets.md § Cut tickets as a graph |
| to-tickets: local files, one per ticket, dependency numbering | covered | spec-and-tickets.md § Publish |
| to-tickets: tracker, blockers first, native links, sub-issues | expanded | spec-and-tickets.md § Publish (ask before remote) |
| to-tickets: work the frontier | covered | spec-and-tickets.md § Cut tickets as a graph |
| to-tickets: never close the parent | covered | spec-and-tickets.md § Publish |
| to-tickets: ticket and issue templates | covered | spec-and-tickets.md § Publish |
| tdd: good test reads like a spec | merged | tdd.md § 4 |
| tdd: glossary for test names | merged | tdd.md § 1; domain-language.md |
| tdd: seams, confirm before testing, one-line note each | covered | test-seams.md § Agree the seams before the first test |
| tdd: implementation-coupled anti-pattern | merged | tdd.md § 4 |
| tdd: tautological anti-pattern | merged | tdd.md § 4 |
| tdd: horizontal slicing anti-pattern | covered | test-seams.md § Grow tests one at a time |
| tdd: red before green, one slice at a time | merged | tdd.md § 1 |
| tdd: refactor outside the loop | covered | test-seams.md § Grow tests one at a time |
| tdd/tests: good and bad test examples | merged | tdd.md § 4 |
| tdd/tests: verify through the interface, not the DB | merged | tdd.md § 4 |
| tdd/mocking: mock only at system boundaries | merged | tdd.md § 4 |
| tdd/mocking: dependency injection | merged | tdd.md § 2; deep-modules.md § Small habits |
| tdd/mocking: SDK-style client over generic fetcher | expanded | test-seams.md § Fakes shaped like the client (runnable TS) |
| codebase-design: deep module aim | covered | deep-modules.md |
| codebase-design: glossary of design terms | covered | deep-modules.md § Words to use, and keep using |
| codebase-design: deep vs shallow | covered | deep-modules.md § Words to use, and keep using |
| codebase-design: depth belongs to the interface, internal seams | covered | deep-modules.md § Three quick tests |
| codebase-design: deletion test | covered | deep-modules.md § Three quick tests |
| codebase-design: interface is the test surface | covered | deep-modules.md § Three quick tests |
| codebase-design: one adapter vs two | covered | deep-modules.md § Three quick tests |
| codebase-design: designing for testability | expanded | deep-modules.md § Small habits (runnable Python port) |
| codebase-design: relationships | merged | deep-modules.md § Words to use, and keep using |
| codebase-design: rejected framings | covered | deep-modules.md § Words to use, and keep using |
| deepening: dependency categories | covered | deep-modules.md § Deepening shallow modules |
| deepening: seam discipline | covered | deep-modules.md § Three quick tests |
| deepening: replace, don't layer tests | covered | deep-modules.md § Deepening shallow modules |
| design-it-twice: frame the problem | covered | deep-modules.md § Design it twice |
| design-it-twice: parallel drafts under different pressures | expanded | deep-modules.md § Design it twice (check helper claims) |
| design-it-twice: what each design must give | covered | deep-modules.md § Design it twice |
| design-it-twice: compare and recommend | covered | deep-modules.md § Design it twice |
| domain-modeling: active vs passive use | covered | domain-language.md |
| domain-modeling: file layout, lazy creation | merged | feature-planning.md § 4; domain-language.md |
| domain-modeling: challenge against glossary | covered | domain-language.md § During the talk |
| domain-modeling: sharpen fuzzy terms | covered | domain-language.md § During the talk |
| domain-modeling: concrete scenarios | covered | domain-language.md § During the talk |
| domain-modeling: cross-check the code | covered | domain-language.md § During the talk |
| domain-modeling: update inline, no implementation details | covered | domain-language.md § A good glossary entry |
| domain-modeling: offer ADRs sparingly | covered | domain-language.md § When a decision earns a record |
| glossary-format: entry shape and avoid list | covered | domain-language.md § A good glossary entry |
| glossary-format: rules | covered | domain-language.md § A good glossary entry |
| glossary-format: single vs multi-context map | covered | domain-language.md § A good glossary entry |
| adr-format: location and numbering | covered | domain-language.md § A minimal record |
| adr-format: one-paragraph template, optional sections | covered | domain-language.md § A minimal record |
| adr-format: three conditions | covered | domain-language.md § When a decision earns a record |
| adr-format: what qualifies | covered | domain-language.md § When a decision earns a record |
| prototype: pick a branch by the question | covered | prototypes.md § Pick the shape from the question |
| prototype: rules for both shapes | merged | feature-planning.md § 5; prototypes.md |
| prototype: capture on a throwaway branch | expanded | prototypes.md § Afterwards (only with the user's yes) |
| prototype/logic: state the question visibly | covered | prototypes.md § The logic demo |
| prototype/logic: pure portable module | covered | prototypes.md § The logic demo |
| prototype/logic: page layout and guided scenarios | covered | prototypes.md § The logic demo |
| prototype/logic: anti-patterns | covered | prototypes.md § The logic demo |
| prototype/ui: host inside an existing page | covered | prototypes.md § Layout variants on one route |
| prototype/ui: variant count and structural difference | covered | prototypes.md § Layout variants on one route |
| prototype/ui: URL parameter switch | covered | prototypes.md § Layout variants on one route |
| prototype/ui: floating switcher, keys, hidden in production | covered | prototypes.md § Layout variants on one route |
| prototype/ui: hand over and mix | expanded | prototypes.md § Layout variants on one route (viewport check) |
| setup-ts-deep-modules: layout with root entries | covered | typescript-habits.md § Packages that expose only their entry files |
| setup-ts-deep-modules: four rules | covered | typescript-habits.md § Packages that expose only their entry files |
| setup-ts-deep-modules: entries over barrels | covered | typescript-habits.md § Packages that expose only their entry files |
| setup-ts-deep-modules: detect, install, config | later | later.md (install and config not run) |
| setup-ts-deep-modules: wire into the check command | covered | typescript-habits.md § Packages that expose only their entry files |
| setup-ts-deep-modules: prove the rule bites | expanded | typescript-habits.md (entry_imports.py) |
| setup-ts-deep-modules: README and agent-notes pointer | covered | typescript-habits.md § Packages that expose only their entry files |
| migrate-to-shoehorn: why avoid as in tests | covered | typescript-habits.md § Test data without as |
| migrate-to-shoehorn: fromPartial, fromAny, fromExact | covered | typescript-habits.md § Test data without as |
| migrate-to-shoehorn: test code only | covered | typescript-habits.md § Test data without as |
| migrate-to-shoehorn: install and migrate workflow | expanded | typescript-habits.md (dependency-free helper, typechecked) |
| out of scope: teach, writing-*, chief-of-staff, software-factory, loop-me, wayfinder, setup, hooks, scaffold, research, retro, review, PR, diagnose, handoff | later | later.md |

Totals: covered 71, expanded 12, merged 22, later 3 (108 items)
