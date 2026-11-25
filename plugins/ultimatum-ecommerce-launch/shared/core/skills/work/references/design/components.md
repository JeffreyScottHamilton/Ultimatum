# Choosing a component library

Goal: the smallest dependency that gives accessible primitives in the project's own style. Read with `ui.md` and `react.md` §A.

## 1. Reuse first

- Search the project before anything else: `ult search` for `components/`, `ui/` and design-system folders; `package.json` for an installed kit.
- Use what is there, even if it is imperfect. Extend it.
- Never add a second primitive of a kind the project already has (two dialogs is a bug waiting to happen).

## 2. Look up

- Run `ult components "<need>" --stack react` (or `vue`, `svelte`, `any`). It prints at most three candidates with licence, maintenance and an install line. The lookup is offline, so confirm the current version on the package registry before installing.
- Describe the behaviour, not the look: "accessible date picker with typed entry" finds more than "fancy calendar".
- If nothing fits, build on an accessible headless primitive rather than writing every widget from scratch.

## 3. Licence

- Permissive licences (MIT, Apache-2.0, BSD, ISC) are fine by default.
- Restricted terms are never used by default: Commons Clause add-ons, source-available licences, no licence file, custom non-SPDX terms. `--all` shows them flagged. Use one only with the user's explicit agreement, after reading its terms yourself.
- Copy-paste sources carry their licence into your repo. Check it, and keep the notice with the copied code.

## 4. Maintenance

- Look for a release and a commit within roughly the last year, and open security advisories.
- If the README says the project is archived or unmaintained, do not add it. Use the successor the README names.
- Pin the major version. Read the changelog for breaking changes before any upgrade.

## 5. Bundle cost

- Measure the minified and gzipped size of what you import, not the package size. Use the analyzer named in `react.md` §D.
- Headless primitives suit a custom design; a full kit suits a look you want as is.
- Import per component. Avoid barrel imports from large libraries.
- Animation libraries are a separate cost; see `motion.md` §4.

## 6. Accessibility primitives

- Prefer components that implement the ARIA authoring pattern: focus trapped and returned in dialogs, arrow keys in menus and tabs, a labelled combobox.
- Check each one: reachable and operable by keyboard alone; focus visible; name and role announced; reduced motion respected.
- A library's accessibility claim is a claim. Confirm with `ult-browser` and a manual keyboard pass (`browser-verification.md` §4 and §7).
- Icon-only buttons need an accessible name.

## 7. Record the choice

- A new dependency needs the user's go-ahead. State the candidate, licence, last release and bundle cost in one line each.
- Record the decision and its reason in the spec, or with `ult note --kind decision`.
