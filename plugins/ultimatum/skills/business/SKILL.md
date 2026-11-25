---
name: business
description: "Ultimatum's Business workflow. Use it whenever the user asks, in plain chat or with /ultimatum:business, about customers, offers, pricing, competitors or conversions (\"what's stopping people from booking?\", \"who are my competitors?\"). It researches who the customer is, what they might buy and what gets in the way, separates observed facts from guesses, and returns advice, or during a launch a build brief for the Launch Manager. Advice only changes nothing."
argument-hint: "<the business question or goal>"
---

# Ultimatum · Business

Task: $ARGUMENTS (if empty, use the user's latest request)

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"` (pass it fully substituted to helpers). Skills: `${CLAUDE_PLUGIN_ROOT}/skills/`.

Read `shared/defaults.md` once. Run `ult business "<task>" --root .`: it prints the mode, the roles and what to hand back.

## Modes

- **advice** (the user only asked): report the recommendation in chat. Change no files, site, records or accounts.
- **launch** (a launch, or the Launch Manager sent you): fill the shared brief's `## Build brief` (`ult business --start-brief` adds the empty fields; see `business/brief.md`) and return it to the Launch Manager. It is a draft until the user approves it; never mark it approved yourself.
- **change** (the user already asked for a specific change): hand it to Website (`website/SKILL.md`) or Work, covering only that change.

## Roles (one person can do all three)

1. **Researcher:** who the customer is, what they are trying to get done, what they compare you with. Ideas from Customer Research and Competitor Profiling.
2. **Marketing planner:** what they might buy, the offer, its price and the one promise. Ideas from Product Marketing and Offers.
3. **Analyst:** what gets in the way on the path to the main action, and how to measure it. Ideas from Analytics and Conversion Tracking.

## Rules

- **Observed or guessed.** Label every point: *observed* (say where: the site, a review, their numbers, a page you read) or *guess* (say what would confirm it). Never present a guess as a finding.
- **Sources.** Use the user's files, their site and public pages. Use Composio or another connector only if the user authorized that app, read-only. If a connector or transcript is missing, say what you actually accessed and continue.
- **No secrets.** Never put credentials or customer personal data in the brief, prompts or logs.
- **One main action.** Every recommendation names the one thing a visitor should do (book, buy, call, sign up) and how you will know it worked.

## Report

Lead with the answer in plain words. Then: the top three blockers to the main action (observed or guess), what to try first and why, how to measure it, and what you could not check.
