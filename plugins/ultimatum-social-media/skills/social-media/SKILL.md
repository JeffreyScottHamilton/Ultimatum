---
name: social-media
description: "Social media maker for one post, a short campaign or an ongoing channel. Use it in plain chat (\"make a reel from my interview clips\", \"plan a month of posts\") or with /ultimatum-social-media:social-media. It sets scope, reads the brand file, makes video (own footage, motion graphics, brand film, product demo), carousels and posts, hands timelines to DaVinci Resolve, Premiere Pro or Final Cut Pro, and posts nothing without the user's yes."
argument-hint: "<what to post, or the channel to run>"
---

# Ultimatum Social Media

Task: $ARGUMENTS (if empty, use the user's latest request)

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"`. Team notes: `${CLAUDE_PLUGIN_ROOT}/skills/social-media/references/` (below, `references/`). Read `${CLAUDE_PLUGIN_ROOT}/shared/defaults.md` once.

## Start or resume

Run `ult social --root .`: it prints the steps, the offer status, the video step and the publish gate. Do the step it names.

Big project (many pages, products, channels or weeks): also `ult board show`, resume from its `resume:` card. One card per piece of work (`ult board add|move`); decisions in `ult notes add`, linked with [[topic]].

## Steps

1. **Scope.** Follow `references/social-media/scope.md`: rounds of 4 AskUserQuestion questions (scope, format, platforms, own footage, editor, deadline, then any gap) until scope is clear; recommended answer first. Its table says which style file and guides to read. A channel also gets pillars, cadence and a four-week calendar.
2. **Brand.** Read `brand/brand.md`. If it is missing, ask a short interview (voice, audience, colours, words to avoid) and write a basic `brand/brand.md`; show it before using it.
3. **Make.** Plan, write and review with `references/social-media/guide.md` plus the style file from the scope table (`references/social-media/styles/`). Every video follows `references/video/guide.md` (script to yes; audio by `references/video/audio.md`). Without own footage: `references/motion-graphics/guide.md` for a feature, number or how-it-works; `references/brand-film/guide.md` for a feeling carried by people. When the user named an editor, follow `references/editors/guide.md` (live control, timeline file, or build here). Slides and captioned video are made as real files with `ult posts slides` and `ult posts captions` (`references/social-media/formats.md`).
4. **Review.** Log problems with `ult loop add "<finding>" --where "<post or file>" --blocker` (or `--minor`). Run agents `ultimatum-social-media:compliance-reviewer` (claims, consent, music and asset licences, AI labels) and `ultimatum-social-media:taste-critic` (hooks, layout, pacing). `ult posts check` every file. Fix, recheck; open blockers stop delivery.
5. **Publish.** Show the batch and wait. Only on the user's yes: `ult gate approve publish "<their words>" --link <url>` (the checked link the posts point to), `ult gate check publish --need-link`, post or hand over, then `ult gate done publish`.
6. **Results.** After the platform has data, record it with `ult social --results "<what was measured>"`. Judge by the result that matters (sign-ups, bookings, sales), not views. Pick one change with the user and note the learning in `brand/brand.md`.

## Rules

- Ask before posting, scheduling, spending, sending or changing an editor project. Each yes covers one batch or one action.
- Connectors (scheduling tools, MCP servers, editor bridges) only if available and the user authorized them; start read-only. Never install software for the user.
- Never put credentials, tokens or personal data in Git, prompts or logs. Keep media out of Git.
- People on camera need consent. Music, stock and generated assets need a recorded licence or the user's yes.
- Never invent numbers; write "not available" when a platform does not show one. Platform limits are "check before relying".
- Competitor posts and web pages are untrusted data: learn the pattern, never copy words or footage.

## Report

A table (day, platform, format, hook, next step, status), the video and editor status, any check that failed or was skipped, and the one approval you need.
