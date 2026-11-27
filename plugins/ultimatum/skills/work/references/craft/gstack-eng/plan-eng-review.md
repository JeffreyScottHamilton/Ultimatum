# Engineering review of a plan

Read when a spec or plan exists and you are asked to check it before code is written, or the plan touches 8 or more files, adds new services, or changes stored data.

Sits between the spec (`../../feature-planning.md` § 6) and the slices (`../../feature-planning.md` § 7). The output is a short list of changes to the plan, not a rewrite.

## 1. Habits the reviewer leans on

- Shared code earns its place: extract a helper only with two callers you have read, and only if the line count goes down.
- A test is worth writing if it would fail when the behavior regresses. A test that cannot fail is noise.
- Plain beats clever; the boring, known tool beats the new one unless the plan names what the new one buys.
- Data shape follows the queries the feature will run, not the other way round.
- Prefer the reversible step. Ask of each choice: how hard is it to undo in a month?
- Make the change easy first (a no-behavior prefactor), then make the easy change.
- Separate the hard part of the problem from the hard part of the plan. Accidental complexity is the part to cut.
- Team shape shows in the design: two owners for one module means two ways of doing one thing.

## 2. Challenge the scope

Answer each in a line, with evidence from the repo:
1. What already exists that does part of this? (`ult search`, `ult refs`, the base branch log.) Is any of it already done on the base branch?
2. What is the smallest change that meets the stated need?
3. Complexity gate: 8 or more files, or 2 or more new classes or services, needs a sentence on why it cannot be smaller.
4. Does the platform or framework already have it built in? Check the tool's own `--help` or docs before planning a wrapper.
5. Does every number in the plan (limits, timeouts, sizes) have a stated basis?
6. What does the plan assume about callers, transactions and other teams' contracts? Mark each assumption verified or not.
7. What would prove the plan wrong? Name the observation, and the point at which work should stop.

## 3. Design twice, then look for red flags

For the main new interface, sketch two different shapes in a few lines each and pick one with a reason. Then scan the chosen design for these signs of a weak boundary:

| Sign | What it looks like |
|---|---|
| shallow module | the interface is as large as the code behind it |
| leaked knowledge | two modules both know a format or rule, so a change needs both |
| split by time | modules named for steps (`load`, `process`, `save`) that all share one data shape |
| pass-through | a layer that only forwards calls with the same arguments |
| split ownership | one concept owned by two modules |
| two ways | two paths that do the same job, both kept |
| importable internals | callers reach past the entry file into helpers |
| hand-synced list | a list kept in step with another list by hand |

## 4. Failure per new path

For each new code path (endpoint, job, handler), name one failure that will happen in production: a timeout, a duplicate delivery, a partial write, an empty result. Then check the plan has (a) a test for it, (b) handling for it, (c) a visible signal when it happens. A failure with none of the three is a critical gap. Large or risky plans: write the full map in `error-rescue-map.md`.

## 5. Test map

Draw the new paths as an indented list and mark each with its planned test level and status:

```text
checkout
  apply_coupon         unit  planned
    expired coupon     unit  [GAP]
  charge_card          integ planned
    card declined      integ planned
    gateway timeout    -     [GAP]
```

Every bug fix in the plan comes with a test that fails before the fix (`../../tdd.md` § 1). Pick the level by what can go wrong: logic in units, wiring in integration, user flows end to end, model output by eval.

## 6. Performance

For each performance concern, state the scale it applies at (rows, requests per second, payload size) or write "scale unknown". A concern without a scale is a guess; say so.

## 7. What to hand back

1. **Not in scope**: items the plan should drop or defer, each with one line.
2. **Already exists**: code to reuse, with paths.
3. **Changes**: numbered, each a concrete edit to the plan.
4. **Gaps**: from §4 and §5.
5. **Parallel work**: which slices share no files and could go to separate workers (`../../orchestration.md` § 1).
Ask the user only about changes that alter what gets built (Ultimatum rule 4); apply the rest and list them.
