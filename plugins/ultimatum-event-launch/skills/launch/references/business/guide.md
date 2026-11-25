# Business and brand guide

Read by the plugin's head skill when the work needs this team. Files named here sit beside this guide; other teams sit in sibling folders (`../<team>/guide.md`).


`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"` (pass it substituted to helpers).

Read `shared/defaults.md` once. Run `ult business "<task>" --root .`: it prints the mode, the roles and what to hand back.

## Modes

- **advice** (the user only asked): answer in chat. Change no files, site, records or accounts.
- **launch** (a launch, sent by the head): fill the shared brief's `## Build brief` (`ult business --start-brief`; see `brief.md`), then write or update `brand/brand.md`. Return both to the head. The brief is a draft until the user approves it; never mark it approved yourself.
- **brand** (the user asked for a name, voice, colours, fonts or a brand file): write or update `brand/brand.md` and show the changes.
- **change** (a specific site change): hand it to Website (`../website/guide.md`) or a coding session, covering only that change.

## Interview and positioning

Brand or launch with no brand file: run the 10-question interview in `interview.md` (3 groups, ending in three adjectives), one group at a time. Then work in this order, each step using the last:

1. **Alternatives:** what the customer would do without this.
2. **Unique attributes:** what only this offer has, with proof.
3. **Value:** what those attributes give the customer.
4. **Best-fit customers:** who cares most.
5. **Category:** the frame that makes the value obvious ("a Saturday baking class").
6. Then **voice**, **name** (only if needed), **colours and fonts**.

**Brand phases:** interview, positioning, voice and name, look, then handoff. Tell the user which phase you are in.

`brand/brand.md` is the shared context file: every team (Website, Marketing, Motion) reads it first. Layout in `brand-file.md`. Update sections in place, add a dated line under "Changes", never fork a second brand file.

**Voice check.** When another team's draft (copy, ads, scripts) reaches you or is in view, read it against the Voice section and say what drifts.

**Startup numbers** (only when asked or it decides the answer): rough market size, a simple model, 3-5 metrics. See `numbers.md`.

## Roles (one person can do all of them)

1. **Researcher:** who the customer is, what they compare you with.
2. **Strategist:** positioning, offer, price and the one promise.
3. **Brand writer:** voice, name ideas, colours and fonts, written to the brand file.
4. **Analyst:** what blocks the main action and how to measure it.

## Rules

- **Observed or guessed.** Label every point *observed* (say where) or *guess* (say what would confirm it). Never present a guess as a finding.
- **Sources.** The user's files, their site and public pages. Use Composio or another connector only if the user authorized that app, read-only. Missing → say what you actually accessed and continue.
- **Names.** Suggest, never register. Say that a trademark and domain search is the user's job before they commit.
- **No secrets.** No credentials or customer personal data in the brief, the brand file, prompts or logs.
- **One main action.** Every recommendation names the one thing a visitor should do and how you will know it worked.

## Report

Lead with the answer. Then the top three blockers to the main action (observed or guess), what to try first and why, how to measure it, what changed in `brand/brand.md`, and what you could not check.
