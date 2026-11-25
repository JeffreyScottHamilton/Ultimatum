---
name: business
description: "Ultimatum Launch's Business & Brand workflow. Use it whenever the user asks, in plain chat or with /ultimatum-launch:business, about customers, offers, pricing, competitors, positioning, naming, brand voice, colours and fonts, or why people don't buy or book (\"What's stopping people from booking?\"). It settles positioning before visuals and keeps one living brand file, brand/brand.md, that Website, Marketing and Motion read."
argument-hint: "<the business question or brand job>"
---

# Ultimatum Launch · Business & Brand

Task: $ARGUMENTS (if empty, use the user's latest request)

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"` (pass it substituted to helpers). Launch skills: `${CLAUDE_PLUGIN_ROOT}/skills/`.

Read `shared/defaults.md` once. Run `ult business "<task>" --root .`: it prints the mode, the roles and what to hand back.

## Modes

- **advice** (the user only asked): answer in chat. Change no files, site, records or accounts.
- **launch** (a launch, or the Launch Manager sent you): fill the shared brief's `## Build brief` (`ult business --start-brief`; see `business/brief.md`), then write or update `brand/brand.md`. Return both to the Launch Manager. The brief is a draft until the user approves it; never mark it approved yourself.
- **brand** (the user asked for a name, voice, colours, fonts or a brand file): write or update `brand/brand.md` and show the changes.
- **change** (a specific site change): hand it to Website (`website/SKILL.md`) or core's `ultimatum:work`, covering only that change.

## Positioning before visuals

Work in this order and don't skip ahead; each step uses the last one:

1. **Alternatives:** what the customer would do if this did not exist.
2. **What is different:** the two or three things only this offer has, and the proof for each.
3. **Who cares most:** the customer for whom those differences matter.
4. **Category:** the frame that makes the value obvious ("a Saturday baking class", not "an experience").
5. **Voice**, then **name** (only if one is needed), then **colours and fonts**.

The brand file layout is in `references/brand-file.md`. It is one living file: update sections in place, keep a dated line under "Changes", never fork a second brand file.

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
