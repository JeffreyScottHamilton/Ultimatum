# Component libraries: registry facts

Verified 2026-11-24. Data is in `component-registry.json` (same folder).

Sources: npm registry `/latest` and full package docs (publish dates from `time`). GitHub API returned 403 for this session, so repo facts come from shallow `git clone --depth 1` of the default branch. Nothing fetched was executed. Categories and "use when" lines are brief groupings, not inventories.

## Summary

| Library | Package @ version | Released | License | Distribution | Framework | A11y basis | Styling | Last commit (clone) |
|---|---|---|---|---|---|---|---|---|
| shadcn/ui | shadcn @ 4.23.0 | 2026-10-27 | MIT | copy-paste (CLI) | React | Base UI or Radix (registry refs: 48 vs 1 file) | Tailwind | 2026-11-23 |
| Base UI | @base-ui/react @ 1.9.0 | 2026-10-09 | MIT | npm | React 17-19 | Headless, accessibility-focused (not audited) | Unstyled | 2026-11-24 |
| Radix UI | radix-ui @ 1.8.1 | 2026-10-12 | MIT | npm | React 16.8-19 | WAI-ARIA-oriented (repo claim) | Unstyled | 2026-10-14 |
| Sonner | sonner @ 2.0.8 | 2026-08-09 | MIT | npm | React 18-19 | not checked | Own stylesheet | 2026-08-10 |
| Vaul | vaul @ 1.1.2 | 2024-12-14 | MIT | npm | React 16.8-19 | via Radix Dialog | not checked | 2025-10-03 (unmaintained) |
| cmdk | cmdk @ 1.1.1 | 2025-03-14 | MIT | npm | React 18-19 | accessible combobox (README) | Unstyled | 2025-10-28 |
| NumberFlow | @number-flow/react @ 0.6.2 | 2026-07-18 | MIT | npm | React 18-19 | not checked | not checked | 2026-09-20 |
| Magic UI | magicui-cli @ 0.1.6 | 2024-07-08 | MIT | copy-paste (CLI, registry.json: 260 items) | React / Next.js | not checked | Tailwind | 2026-11-24 |
| Aceternity UI | aceternity-ui @ 0.2.2 | 2024-07-22 | MIT (npm field) | copy-paste (CLI) | not checked | not checked | not checked | repo not found |
| 21st.dev | @21st-dev/cli @ 1.18.1 | 2026-11-24 | MIT (npm field) | CLI, installs from catalog | not checked | not checked | not checked | repo not found |
| React Bits | no npm match (see below) | n/a | MIT + Commons Clause | copy-paste (shadcn, jsrepo) | React | not checked | Tailwind | 2026-11-24 |
| React Aria Components | react-aria-components @ 1.22.1 | 2026-10-09 | Apache-2.0 | npm | React 16.8-19 rc | React Aria hooks, WAI-ARIA | Unstyled | 2026-11-23 |
| Motion | motion @ 14.14.0 | 2026-11-13 | MIT | npm | React 18-19 | not checked | not checked | 2026-11-24 |
| framer-motion | framer-motion @ 14.14.0 | 2026-11-13 | MIT | npm (same repo as Motion) | React 18-19 | n/a | n/a | same repo |
| GSAP | gsap @ 3.15.1 | 2026-11-04 | GreenSock "no charge" (not SPDX) | npm | framework-agnostic | n/a | n/a | 2026-11-03 |
| RareUI | rareui @ 0.1.6 | 2025-12-09 | MIT + Commons Clause + Attribution | copy-paste (shadcn registry, CLI) | React / Next.js | not checked | Tailwind | 2026-11-22 |

"not checked" means the fact was not verified from the package or repo, so it is null in the JSON.

## Use and avoid, in short

- **shadcn/ui:** you want source you own, with Tailwind styling. Avoid it if you want versioned updates without copied code.
- **Base UI:** unstyled, accessible primitives under your own styling. Use `@base-ui/react`, since `@base-ui-components/react` is deprecated.
- **Radix:** unstyled primitives, and the base of shadcn's classic stack.
- **Sonner:** toasts only. Use it for transient notifications, not persistent alerts.
- **Vaul:** bottom drawers. Avoid it for new work, since its README says the repo is unmaintained.
- **cmdk:** command palettes and comboboxes.
- **NumberFlow:** animated number transitions.
- **Magic UI / RareUI / React Bits / Aceternity / 21st.dev:** copy-paste or catalog sources of visual components. Review the copied code, because accessibility is not established for most of them.
- **React Aria Components:** accessible, internationalized complex widgets such as date fields.
- **Motion and framer-motion:** React animations. Use `motion` for new projects; `framer-motion` is the same codebase under the older name.
- **GSAP:** timelines and scroll animation, framework-agnostic.

## License caveats

- **React Bits** is MIT with a Commons Clause. Per its LICENSE, you may use the software commercially, but you may not sell, sublicense, or redistribute the components, the tools, or the sounds on their own. Its exports may be used in paid products, but not sold as packs.
- **RareUI** is MIT with a Commons Clause and an attribution clause. The Commons Clause forbids selling the software.
- **GSAP** uses a GreenSock "Standard no charge" license, not an SPDX license. Its README says the full toolset, including former Club plugins, is free, including commercially. The repo has no LICENSE file, and the license text at gsap.com was not fetched, so confirm the terms there.
- **Aceternity UI and 21st.dev:** the npm packages declare MIT, but the npm field is what was checked. Their source repos were not found, so their license and origin are unconfirmed.
- Base UI's `@base-ui-components/react` is deprecated. Use `@base-ui/react`.

## Unresolved names

- **"Beautiful UI":** not identified. The npm package `beautiful-ui` @ 1.0.31 (MIT, 2022) is an Ant Design-based package with no repository. Search found other "beautiful UI" projects that were not clearly the intended one. Excluded from the JSON.
- **"RareUI":** identified as the `rareui` npm package and `Codewithswappy/rareui` repo (homepage rareui.in). Included.
- **React Bits:** the npm package `react-bits` is an unrelated 2017 React Native helper (dmiller9911/react-bits). The React Bits project is `DavidHDev/react-bits` (reactbits.dev). `package` is null in the JSON.
- **Aceternity UI:** the npm package `aceternity-ui` has no repository field, and no source repo could be cloned. Included with nulls.
- **21st.dev:** `@21st-dev/cli` has no repository field, and no `21st-dev/21st` repo could be cloned. Included with nulls.

## Not verified

- **YouTube video:** https://youtu.be/zsCGS-Yzjnw could not be accessed from this environment (YouTube is blocked). Any recommendations in it are unverified and are not reflected in this data.
- Accessibility claims and styling for most copy-paste libraries are from package descriptions and dependencies, not from testing.
- GitHub stars, issue counts, and contributor data were not collected.

## Permissive alternatives (verified 2026-11-24)

User decision: skip restricted or unlicensed libraries and use permissively licensed alternatives with similar capability. Each alternative below was checked with `npm view` (metadata only) and a `git clone --depth 1` whose LICENSE file was read. Nothing was installed or run. "Repo commit" is the date of the last commit in the clone.

| Replaces | Alternative | Licence (verified) | Latest release | Repo commit | Notes |
|---|---|---|---|---|---|
| React Bits, RareUI (Commons Clause) | Magic UI (`magicui-cli` 0.1.6) | MIT, LICENSE.md | 2024-07-08 (CLI) | 2026-11-24 | Copy-paste components; repo active, CLI release old |
| React Bits, RareUI (Commons Clause) | Motion Primitives (`motion-primitives` 0.1.0) | MIT, LICENCE.md | 2025-03-04 (npm) | 2026-09-28 | Copy-paste from docs; repo `package.json` is private |
| GSAP (non-SPDX) | Motion (`motion` 14.14.0) | MIT, LICENSE.md | 2026-11-13 | 2026-11-24 | React only; framer-motion is the same codebase |
| GSAP (non-SPDX) | Anime.js (`animejs` 4.5.0) | MIT, LICENSE.md | 2026-06-22 | 2026-08-09 | Framework-agnostic timelines; 5.x is beta |
| Vaul (unmaintained) | react-modal-sheet (`react-modal-sheet` 5.7.0) | MIT, LICENSE | 2026-11-07 | 2026-11-09 | Bottom sheets with snap points and gestures |
| Vaul (unmaintained) | Radix Dialog (`@radix-ui/react-dialog` 1.3.1) | MIT, LICENSE | 2026-10-12 | 2026-10-14 | Primitive only; you build the sheet on it |
| remotion (no licence) | Revideo (`@revideo/core` 0.11.0) | MIT, LICENSE | 2026-07-10 | 2026-07-15 | Code-driven video; ffmpeg needs were not checked |
| remotion (no licence) | Motion Canvas (`@motion-canvas/core` 3.17.2) | MIT, LICENSE | 2024-12-14 (npm) | 2026-07-02 | Code-driven video; npm release old, repo active |

Verified and not used as an alternative: shadcn (`shadcn` 4.23.0, MIT, LICENSE, repo commit 2026-11-23). It is a copy-paste CLI, not a drop-in for any restricted entry.

Caveats:
- "Maintained" here means a repo commit or npm release within 12 months of 2026-11-24. For Magic UI, Motion Primitives and Motion Canvas, the npm release is older than the repo commit, so the repo was used.
- Feature fit comes from package descriptions and READMEs. Accessibility, bundle size and API fit were not tested.
- Video alternatives were not tested for rendering, since that needs ffmpeg and a browser. Nothing was run.
- Machine-readable entries: `plugins/ultimatum/data/components.json` (`alternatives_to`) and `plugins/ultimatum/data/upstreams.json` (`kind: component-library`).
