# Product scope review of a plan

Read when the user asks whether a plan is aiming at the right thing, wants it bigger or smaller, or a plan is about to commit weeks of work.

Different from `plan-eng-review.md`: that asks whether the plan is built well; this asks whether it should be built as drawn.

## 1. Pick a stance first

| Stance | Use when | What you do |
|---|---|---|
| grow | new product or greenfield area | look for the version users would tell others about |
| pick | the plan adds a capability | keep the core, offer a few additions one by one |
| hold | a fix or a narrow change | keep scope fixed; review for risk only |
| cut | more than ~15 files, or the plan sprawls | find the smallest version that still delivers the point |

State the stance and why in one line. Any change of scope, up or down, is the user's call: offer it, do not apply it.

## 2. Premise

- What problem does this solve, for whom? Is it the problem or a stand-in for it (a metric that tracks the goal loosely)?
- What happens if nothing is built? If the answer is "not much", say so.
- What already exists, in this repo or off the shelf?

## 3. Three horizons

Write one line each: where things are today, where this plan leaves them, where they should be in a year. If the plan moves away from the one-year line, flag it.

## 4. Alternatives

Name at least three: the current plan, the smallest version, and a larger one. For each: effort, main risk, what it reuses. Recommend one and name what would change your mind.

## 5. Additions, one at a time (grow and pick only)

List up to five candidate additions, each small and concrete. For each, the user chooses add, defer or skip. Deferred items go in the project's backlog file if it has one, else in the spec's open points.

## 6. Walk the build in time

Picture the build in rough blocks and note what decision each block will force:
- first hour: what must be settled before any code;
- next few hours: what the first working path will reveal;
- later: where integration or data questions will surface;
- last: what testing and rollout will need.
Decisions that surface late but could be made now go back into the spec.

## 7. Review sections for large plans

Run the ones that apply; skip with a line saying why.
1. **Errors**: the map in `error-rescue-map.md`.
2. **Security**: each new input, role or secret, with likelihood and impact; follow `../../security/secure-implementation.md`.
3. **Data flow**: every input traced through validation, transform, storage and output, with its empty, invalid, slow, conflicting and stale cases (`error-rescue-map.md` § 2).
4. **Edges in the UI**: double submit, back button, two tabs, slow network.
5. **Observability**: could someone rebuild a bug report from three weeks ago using only logs and metrics? If not, what is missing? Who gets paged, and is there a runbook line?
6. **Rollout**: can old and new code run at once during deploy? Migrations first, code second. What to watch in the first five minutes and the first hour (`../../release.md` § 7).
7. **Trajectory**: rate how hard this is to undo (1 easy to 5 permanent) and what it makes harder a year from now.

## 8. Hand back

Stance, premise verdict, recommended alternative, accepted additions, and a short list of risks with an owner each. Keep it to a page.
