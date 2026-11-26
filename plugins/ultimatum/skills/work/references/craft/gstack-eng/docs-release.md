# Docs after a change: what shipped versus what is written

Read when a branch is about to ship and its docs, changelog and backlog need to match what the code now does.

Used as step 3 of the ship order (`ship-pipeline.md` § 1), or on its own from a feature branch. Version rules: (`../../release.md` § 3). Release notes: (`../../release.md` § 6).

## 1. Read the diff

```bash
fork=$(git merge-base HEAD origin/main)
git log --oneline "$fork"..HEAD
git diff "$fork" HEAD --stat
```

Sort what changed into: new features, changed behavior, removed things, and infrastructure (build, tests, CI). Removed things are the ones docs most often keep.

## 2. Coverage map

List every public thing the diff adds, renames or removes: commands, flags, config keys, environment variables, endpoints, exported functions. For each, mark which kinds of doc cover it:

```text
item            reference  how-to  tutorial  explanation
--dry-run       README     -       -         -
SYNC_TIMEOUT    -          -       -         -
```

The four kinds: reference (what it is and its options), how-to (do one task), tutorial (first steps for a newcomer), explanation (why it works this way). No coverage at all is a gap to report; reference only is common and worth noting. Flag gaps; do not write new doc pages unless asked.

If a doc has a diagram (ASCII or Mermaid), check its names against the code. Report a renamed or removed box; do not redraw it yourself.

## 3. Edit without asking

Fix plain facts the diff settles: paths, counts, flag names, version numbers in prose, stale links, a row missing from a table, a backlog item now done.

## 4. Ask first

Rewrites of tone or rationale, removing sections, anything about security, a version bump, new backlog items, and two docs that disagree on intent rather than fact.

## 5. Changelog care

- Edit the changelog with exact string replacements, never by regenerating the file.
- Improve wording only; never drop or merge someone else's entry.
- Each line says what a user can now do or must change.

## 6. Report

One line per edited file with what changed, the coverage gaps, and any diagram drift. Every doc should be reachable from the README or the project's agent file; name any that are not.
