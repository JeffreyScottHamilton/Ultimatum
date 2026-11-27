# Parked: things the source had that we do not do yet

Read when someone asks for a generated-image mockup, an outside model review, a shared review dashboard or a fixture-backed preview, or wants to know why a gstack feature is missing. Each item needs a tool or service Ultimatum does not ship.

| Item | Why it is parked | What we do instead |
|---|---|---|
| Design image generator (`$D`: generated pictures of variants) | needs a paid image-generation service | built HTML mockups on a local board with pick, ratings and feedback read back (`mockup-step.md`, `mockup_board.py`) |
| Outside model review through a separate CLI | needs a second model provider | `second-opinion.md` with the `taste-critic` agent in a fresh context |
| Fixture-backed preview server (a loopback server that serves a page with a `?as=` scenario switch to show states such as empty, loading, error) | a helper we have not written | the build loop's preflight and states pass (`build-loop.md`); a tiny local scenario page can be added as a script here later |
| Persistent browser daemon and sign-in cookie import (`$B`, Aside) | a separate resident tool | Playwright with headless Chromium; the owner switches accounts themselves (`qa-taxonomy.md`) |
| Review log and readiness dashboard across skills | needs a shared store | a log line in the plan or project notes (`plan-review-outputs.md`) |
| Learnings store and cross-session memory search | needs a memory service | none; the project notes carry decisions |
| DOM-dump detector engine for the 19 rule ids (the Impeccable engine) | a downloaded native engine | `design-audit-recipes.md` covers the checks that a script can measure, and `slop-tells.md` lists the rest for a human read |
| Harness preamble (update checks, telemetry prompts, session routing) | harness-specific boilerplate | not needed |
| Autoplan runner profile | needs the unattended runner | the interactive plan review |
| Per-skill duplicate `.tmpl` templates | they duplicate the built files | noted only |

## Picking one up

A fixture-backed preview is the most useful next step: a script under `scripts/` that serves a static page and flips a scenario from a query value, plus a short recipe here. It must stay local, bind to loopback only and have a test that proves it refuses other hosts.
