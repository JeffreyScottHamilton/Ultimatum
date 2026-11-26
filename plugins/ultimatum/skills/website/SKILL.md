---
name: website
description: "Ultimatum's website builder: new sites, redesigns and fixes for small business, local service, portfolio and creator sites (cafe, salon, clinic, trades, consultant, coach), usually aimed at calls, bookings or enquiries. Use it in plain chat or with /ultimatum:website. It interviews the owner, writes a one-page brief they approve, shows three design directions, builds the picked one, checks it in a browser and goes live only on the user's yes."
argument-hint: "<what site you want built or changed>"
---

# Website builder

Task: $ARGUMENTS (if empty, use the user's latest request)

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"`. This skill's files: `${CLAUDE_PLUGIN_ROOT}/skills/website/references/`. You run the job; the user talks only to you. Read `${CLAUDE_PLUGIN_ROOT}/shared/defaults.md` once.

**Small fix or a change that keeps the current look?** Skip steps 1-3: run `ult website "<task>" --root . --cat` and take the short path in `references/website/guide.md`.

## Steps

1. **Intake.** Follow `references/intake.md`: rounds of 4 questions (AskUserQuestion's limit) until every brief field is filled; recommended answer first, plus "skip, use your pick"; "why" questions one at a time. Skip what files already say.
2. **Brief.** Write `.ultimatum/brief.md` as intake.md and `references/website/planner.md` show, show it, stop. Yes: `ult gate approve brief "<their words>"`. Changes: `ult gate revise brief "<their words>"`, fix, show again. Never approve for the user.
3. **Route.** Read `references/route.md` (site size, host, domain) and the matching section of `references/by-business-type.md` (main action, pages, proof, mistakes to avoid). Check any paid tool, licence or price on the vendor's own page. Fill `brand/brand.md` as intake.md says.
4. **Build.** Run `ult website "<task>" --root . --cat` and follow `references/website/guide.md`: three directions, the critic, the user's pick (`ult website --approve`), the build, the browser check. Use `references/pages-and-seo.md`, and draft copy with `references/copy.md`; the owner approves every claim. Design tables: `ult design system "<business type>"`.
5. **Review loop.** `ult loop`. Run `ultimatum:compliance-reviewer` on every public page and `ultimatum:taste-critic` on designs. Fix, recheck. Open blockers stop delivery.
6. **Go live.** Work through `references/launch-checklist.md`. Only on the user's yes: `ult gate approve publish "<words>" --link <checked live url>`, `ult gate check publish --need-link`, then `ult gate done publish`. Deploys: `ult gate approve deploy "<words>"` and follow `${CLAUDE_PLUGIN_ROOT}/skills/release/SKILL.md`.
7. **First 30 days.** The numbers from the checklist; bring them to the user to choose the next change.

Big site (many pages or weeks): `ult board show` and resume from its `resume:` card; decisions in `ult notes add`.

## Rules

- One brief: every change to an approved brief goes through the user.
- Shops, carts, accounts and apps are out of scope for now; say so and offer a simple site with a link to the owner's existing tool.
- **Ask before** spending, changing listings (e.g. a Google Business Profile), buying a domain or deploying. Each yes covers one action.
- Never put credentials in Git, prompts or logs; the owner does their own logins.
- Facts marked "check before relying" must be confirmed on the vendor's page first.

## Report

Plain words: what changed, how to open the preview, each check and its result, the critic's last score, what waits for the user, and the one next decision. Never claim more than you ran.
