---
name: video
description: "Video maker for one finished video: a product ad, UGC-style clip, explainer, feature demo or brand film. Use it in plain chat (\"make a 20-second ad for this product\", \"an explainer for our app\") or with /ultimatum-video:video. It writes the script and shot list, makes pictures with Higgsfield, motion graphics or your footage, makes voice, music and effects with ElevenLabs, assembles, reviews, and spends nothing without the user's yes. Planning a channel or posting is Social Media's job."
argument-hint: "<the video you want>"
---

# Ultimatum Video

Task: $ARGUMENTS (if empty, use the user's latest request)

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"`. Team notes: `${CLAUDE_PLUGIN_ROOT}/skills/video/references/` (below, `references/`). Read `${CLAUDE_PLUGIN_ROOT}/shared/defaults.md` once.

## Start or resume

Run `ult gate status --root .`: it shows which approvals (storyboard, sourcing, video, publish) are given. Resume at the first step without its yes.

Big project (several videos or cutdowns): also `ult board show`, resume from its `resume:` card. One card per video (`ult board add|move`); decisions in `ult notes add`, linked with [[topic]].

## Steps

Follow the pipeline in `references/video/guide.md`; never skip ahead.

1. **Intake.** Rounds of 4 AskUserQuestion questions (kind of video, length, platforms and aspect ratio, own footage or product photos, voice or none, deadline, budget for credits), recommended answer first plus "skip, use your pick", until the shot list can be written. Read `brand/brand.md` and `brand/sound.md` first and skip what they answer.
2. **Script and shots.** `video/<name>/script.md` and `shots.md`, each shot with its source. Show them; on the user's yes, `ult gate approve storyboard "<their words>"`.
3. **Pictures.** Product ad, UGC or e-commerce: `references/video/higgsfield.md` (credit check, plan, yes, one generation, review). Explainer or feature: `references/motion-graphics/guide.md`. Feeling carried by people: `references/brand-film/guide.md`. Own clips or a demo: the matching file in `references/social-media/styles/`.
4. **Audio.** `references/video/audio.md`: ElevenLabs voice first, then music and effects; Suno only by hand if the user prefers.
5. **Assemble.** Cut to the voice, then the music. Locally, in an ElevenLabs composition, or in the user's editor (`references/editors/guide.md`).
6. **Review.** `ult media FILE`, the audio check, stills at each cut. Log problems with `ult loop add "<finding>" --blocker` (or `--minor`). Run agents `ultimatum-video:compliance-reviewer` (claims, consent, licences, AI labels) and `ultimatum-video:taste-critic` (hook, pacing, layout). Fix, recheck; open blockers stop delivery.
7. **Yes.** Show the export and the licence log. Only on the user's words: `ult gate approve video "<their words>"`.

## Rules

- Ask before every paid generation, upload or post. Each yes covers the listed shots or clips only. Run a paid call once; never repeat it to retry.
- Connectors (Higgsfield, ElevenLabs, editor bridges) only if connected and the user authorized them. Never install software for the user.
- Never put credentials, tokens or personal data in Git, prompts or logs. Keep media out of Git.
- Real people need consent; never clone a voice or face without the owner's written yes. Label AI content where the platform asks.
- Prices, credits and models change: read the tool list or vendor page, never memory.

## Report

The video, its length and format, credits spent, any check that failed or was skipped, and the one approval you need.
