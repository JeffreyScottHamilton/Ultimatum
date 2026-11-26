# Credits and license notes

Ultimatum is original work under the MIT License. It was designed after studying the projects below at the listed revisions. **No upstream source code, prose, or assets are copied or redistributed.** Ultimatum's instructions and scripts are written from scratch. Where a reference uses an identifier from a standard (OWASP ASVS requirement IDs, WSTG test IDs, CWE numbers), the identifier is cited, not the text.

Optional tools that Ultimatum can *invoke* when the user has installed them (Semgrep, Gitleaks, OSV-Scanner, Playwright, axe-core, Chrome DevTools MCP, Context7, Serena, Sentry, Supabase, Terraform) are not bundled. Their own licenses apply to their use.

Thank you to the authors and maintainers of these projects.

| Project | Revision inspected | License (at that revision) | What Ultimatum learned from it |
|---|---|---|---|
| [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | `6b056c848a98` | Apache-2.0 | Browser performance traces, network, console, and memory inspection (optional integration) |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | `96608e078b2d` | MIT | Reuse-first, minimal-diff implementation discipline |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | `5eedffa87476` | Apache-2.0 | Repository graphs with confidence-tagged edges, queried rather than dumped (`ult map`) |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | `3dc497a7f858` | Apache-2.0 | Terse voice that keeps every technical fact, command compression, role-based model routing |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | `f6b76575f949` | MIT | Deliberate visual direction, anti-generic design rules, bounded critique gates |
| [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | `1482e84` | MIT | Explanatory isometric figures: craft, shading, motion, WebGL, print and publishing (website craft references) |
| [OWASP/ASVS](https://github.com/OWASP/ASVS) | `62981c68fd06` | CC BY-SA 4.0 | Requirement chapters used as the security coverage model (IDs cited only) |
| [OWASP/wstg](https://github.com/OWASP/wstg) | `e493506b9cde` | CC BY-SA 4.0 | Test categories mapped to source-level questions (IDs cited only) |
| [anthropics/skills](https://github.com/anthropics/skills) | `2c5958ecac7c` | Apache-2.0 (skill-creator `LICENSE.txt`) | Skill evaluation: with/without-skill comparisons, discriminating assertions, trigger tests (skill-creator, Apache-2.0) |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | `c1c8a8c14710` | MIT | Coverage-driven audits, independent validation, three-verdict findings, ledgers |
| [dequelabs/axe-core](https://github.com/dequelabs/axe-core) | `c50bf8e8933e` | MPL-2.0 | Accessibility rule engine (optional), and the limits of automated a11y checks |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | `715c1807e08c` | MIT | Motion and interaction craft: purpose, duration, easing, interruptibility; website motion craft references (craft/emil-motion) |
| [garrytan/gstack](https://github.com/garrytan/gstack) | `7dace1fdeabc` | MIT | Ship, review, QA, release, and post-deploy workflows |
| [getsentry/plugin-claude](https://github.com/getsentry/plugin-claude) | `1b082a07d1a8` | MIT | Production issue investigation from error events (optional integration) |
| [getsentry/skills](https://github.com/getsentry/skills) | `e94f22214528` | Apache-2.0 | iterate-pr: CI failure and review-feedback loop with priority triage (Apache-2.0) |
| [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | `5f6ec56cfa6f` | MIT | Secret detection and redaction (optional integration; Ultimatum uses its own small pattern set) |
| [google/osv-scanner](https://github.com/google/osv-scanner) | `02f96a40691c` | Apache-2.0 | Dependency advisory checks (optional integration) |
| [hashicorp/agent-skills](https://github.com/hashicorp/agent-skills) | `5e30fa5c867b` | MPL-2.0 | Terraform module design and testing practices |
| [mattpocock/skills](https://github.com/mattpocock/skills) | `4ae2317ddb22` | MIT | Requirements interviews, domain modeling, prototyping, TDD, tickets, handoffs |
| [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | `9166133dd68a` | Apache-2.0 | Browser interaction, snapshots, sessions, screenshots |
| [mksglu/context-mode](https://github.com/mksglu/context-mode) | `3a3ef7d53c9a` | Elastic License 2.0 | Store-then-retrieve for large outputs with full-text search (ideas only; ELv2 code not used) |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | `2c606141936f` | MIT (stated in README) | Think before coding, simplicity, surgical changes, verifiable success criteria |
| [obra/superpowers](https://github.com/obra/superpowers) | `22f0b463e7a5` | MIT | Brainstorm/plan/execute flow, subagent-driven development, worktrees, systematic debugging, verification before completion |
| [oraios/serena](https://github.com/oraios/serena) | `6e5c3776d4e6` | MIT (SolidLSP) / GPL-3.0-or-later (app) | Symbol-aware search and editing (ideas and optional MCP; GPL application code not used) |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | `3c5e75fa07be` | Apache-2.0 | Design critique and audit vocabulary, craft floor, detector-style anti-patterns |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | `08a261a0d081` | Apache-2.0 | Command-specific output filtering with raw-output recovery and exit-code preservation |
| [semgrep/semgrep](https://github.com/semgrep/semgrep) | `692bfae4ca1b` | LGPL-2.1 | Static analysis (optional integration) |
| [shadcn-ui/ui](https://github.com/shadcn-ui/ui) | `8ab27715521c` | MIT | Registry-aware component reuse before building new components |
| [supabase/agent-skills](https://github.com/supabase/agent-skills) | `c9be0e931b79` | MIT | Postgres/RLS checks and query performance practices |
| [trailofbits/skills](https://github.com/trailofbits/skills) | `e4dd0bb5b155` | CC BY-SA 4.0 | False-positive checks, differential review, variant analysis, patch validation, property-based testing (ideas only; CC BY-SA text not copied) |
| [uditgoenka/autoresearch](https://github.com/uditgoenka/autoresearch) | `7bddd056dfd0` | MIT | Bounded optimization loops with a correctness guard |
| [upstash/context7](https://github.com/upstash/context7) | `6e68ffcbad0e` | MIT | Version-targeted library documentation lookup (optional integration) |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | `1a2c79d4e6c4` | MIT (stated in README) | React composition and performance priorities, web interface guidelines |
| [shadcn/ui skills docs](https://ui.shadcn.com/docs/skills) | docs page | MIT | See shadcn-ui/ui |

The full revision table and the license decisions are in `research/REVISIONS.md`. Capability-by-capability coverage is in `docs/COVERAGE-MAP.md`.

## Added for 2.0 (reviewed 2026-11-24; full list: `ult upstreams`)

| Project | Revision inspected | License | Use |
|---|---|---|---|
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `3442615` | MIT (ui-styling folder is Apache-2.0, not taken) | Design tables bundled in `data/design/` with their MIT licence and changes listed in `NOTICE.md`; read by `ult design`. Still recommended as an optional install |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | `89c8afa` | none | Reviewed and skipped (no licence); nothing used |
| [JaimeJunr/claude-code-frontend-skills](https://github.com/JaimeJunr/claude-code-frontend-skills) | `7177def` | MIT (bundled plugins are Apache-2.0 or MIT) | Ideas for the 2.0 design and component modules |
| [magicuidesign/magicui](https://github.com/magicuidesign/magicui) | `d13c610` | MIT | Recommended as an optional install by `ult components`; not bundled |
| [ibelick/motion-primitives](https://github.com/ibelick/motion-primitives) | `120f64f` | MIT | Recommended as an optional install by `ult components`; not bundled |
| [motiondivision/motion](https://github.com/motiondivision/motion) | `1fa0e14` | MIT | Recommended as an optional install by `ult components`; not bundled |
| [juliangarnier/anime](https://github.com/juliangarnier/anime) | `01b81be` | MIT | Recommended as an optional install by `ult components`; not bundled |
| [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | `7b91435` | MIT | Recommended as an optional install by `ult components`; not bundled |
| [midrender/revideo](https://github.com/midrender/revideo) | `b5de67a` | MIT | Recommended as an optional install by `ult components`; not bundled |
| [Temzasse/react-modal-sheet](https://github.com/Temzasse/react-modal-sheet) | `8cee295` | MIT | Recommended as an optional install by `ult components`; not bundled |
| [radix-ui/primitives](https://github.com/radix-ui/primitives) | `eb3a2b7` | MIT | Recommended as an optional install by `ult components`; not bundled |

## Where the 2.0 workflows draw ideas from

All wording in the skills and guides is original. This table only shows which listed project inspired which part; licences are as recorded above.

| Part | Inspired by |
|---|---|
| Shared defaults (`shared/defaults.md`) | Caveman (plain answers), Ponytail (reuse, simplest approach), Karpathy guidelines (plan to fit, check results) |
| DEEP mode | Superpowers, Matt Pocock's skills, Ponytail |
| Design skill | Taste, UI/UX Pro Max, Impeccable |
| Coding website guide | Ponytail, shadcn/ui, Radix |
| Review browser checks | gstack QA, Playwright, axe-core |
| Code-map escalation | Graphify |
