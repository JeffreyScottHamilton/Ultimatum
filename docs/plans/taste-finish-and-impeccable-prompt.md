You have two jobs in this session, in order: finish the Taste rebuild, then rebuild Impeccable. Repository: JeffreyScottHamilton/Ultimatum.

## Setup (once)

```bash
git fetch origin claude/affectionate-turing-qr3gau
git checkout -B claude/rebuild-taste-2 FETCH_HEAD
```

The base branch already has the merged Taste work, released as 0.0.12. It also has `tools/copy_check.py` (with `--skip`) and our own colour, font and style tables. Read `docs/plans/skill-rebuild-prompt.md` first. Its hard rules, "Don't touch shared files" list, checks and report format all apply to both jobs. Ignore its "pick a skill" section: your skills are named here.

Two rules from this repo's `CLAUDE.md` also apply:
- Don't change the version and don't write CHANGELOG entries: put a changelog fragment in `docs/plans/changelog-fragments/`.
- Claim only what you ran.

## Job 1: finish Taste (branch `claude/rebuild-taste-2`)

Taste's knowledge files are live in `plugins/ultimatum/skills/website/references/craft/taste/`. What's left is listed in its `later.md` and in `docs/plans/coverage/taste.md`. Re-clone the source to `/tmp/src/taste` at `f6b7657` (MIT) and read it only. Never run its code.

Do these in order. Write all code yourself, keep each piece small, and run it:

1. **Review the 129 coverage rows matched only by keyword.** Open each source item, confirm our file really covers it, and fix the row: covered, expanded, merged, or later. Write any rule that turns out to be missing.
2. **Page system:** one starter page plus a stylesheet (reset, tokens, layout, motion, with reduced motion and visible focus), in `plugins/ultimatum/data/craft/taste/kit/`. It must pass `design-rules.md` §2 and §7.
3. **CSS grounds:** our own CSS for each named ground in `grounds-and-effects.md`. Add a contrast check that screenshots text on each ground with the preinstalled Playwright and fails below 4.5:1. That check is a test-time tool in `tools/`, not part of the stdlib toolbelt.
4. **UI fragments:** the 19 interface fragments from `cards-and-ui.md` as plain HTML and CSS partials, each readable at 390 px. Add the CSS phone frame around a real screenshot slot.
5. **Copy lint:** a stdlib Python check, in the toolbelt style with no network, that flags the lint's banned words and habits in page copy. Wire it in only as a proposed diff, because `scripts/ult` is shared.
6. **Effects, effect parts, objects, diagrams, icons:** do what fits in the session, cheapest first: icons, then diagrams as an SVG generator from a small JSON spec, then at most 3 WebGL effects within the `performance.md` budget, each with a static fallback and a reduced-motion stop. Leave the rest in `later.md` with an honest note.
7. **Wrap up:** update `later.md`, the coverage map and the Taste tests. Add `docs/plans/changelog-fragments/taste-2.md`. Run every check in the base prompt, plus the copy check on the new kit folder. Commit and push to `claude/rebuild-taste-2`, then report.

If time runs short, stop after any finished step, commit it, and list what's left. Don't start Job 2 until Job 1 is pushed.

## Job 2: rebuild Impeccable (branch `claude/rebuild-impeccable`)

```bash
git fetch origin claude/affectionate-turing-qr3gau
git checkout -B claude/rebuild-impeccable FETCH_HEAD
```

Follow `docs/plans/skill-rebuild-prompt.md` steps 0 to 8 for the Impeccable row:
- source repo: `pbakaus/impeccable`
- commit: `3c5e75f`
- slug: `impeccable`
- licence: Apache-2.0, with a NOTICE file that adds MIT, MPL-2.0 and OFL-1.1 parts. Read that NOTICE and record which parts carry which licence.

**Never run its launcher, hooks or anything it downloads.** It fetches a native engine at run time. Read the text only.

Before writing anything, read the Taste folder you just finished. Where Impeccable and Taste overlap, extend Taste's file with a pointer, not a second copy. Put only what Impeccable adds in `references/craft/impeccable/`. Note every merge in `docs/plans/coverage/impeccable.md`.

## Report (plain words, short, one section per job)

For each job:
- licence and commit;
- counts: covered, expanded, merged, later;
- files added;
- each check command with its exit code;
- which examples you ran;
- proposed diffs to shared files (`craft.md`, `taste-critic.md`, `upstreams.json`, `CREDITS.md`, `scripts/ult`);
- what you couldn't verify.

No PR, no main, no release.
