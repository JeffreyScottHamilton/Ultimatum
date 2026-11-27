---
name: website
description: "Ultimatum's website builder: new sites, redesigns and fixes, from small business, local service, portfolio and creator sites (cafe, salon, clinic, trades, consultant, coach) to content sites and web apps with accounts, a Supabase database and Stripe payments. Use it in plain chat or with /ultimatum:website. It interviews the owner, writes a one-page brief they approve, shows three design directions, builds the picked one, checks it in a browser and goes live only on the user's yes."
argument-hint: "<what site you want built or changed>"
---

# Website builder

Task: $ARGUMENTS (if empty, use the user's latest request)

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"`. This skill's files: `${CLAUDE_PLUGIN_ROOT}/skills/website/references/`. You run the job; the user talks only to you. Read `${CLAUDE_PLUGIN_ROOT}/shared/defaults.md` once.

**Small fix or a change that keeps the current look?** Skip steps 1-3: run `ult website "<task>" --root . --cat` and take the short path in `references/website/guide.md`.

## Steps

1. **Intake.** Follow `references/intake.md`: rounds of 4 questions (AskUserQuestion's limit) until every brief field is filled; recommended answer first, plus "skip, use your pick"; "why" questions one at a time. Skip what files already say.
2. **Brief.** Write `.ultimatum/brief.md` as intake.md and `references/website/planner.md` show, show it, stop. Yes: `ult gate approve brief "<their words>"`. Changes: `ult gate revise brief "<their words>"`, fix, show again. Never approve for the user.
3. **Route.** Read `references/route.md` (site size, host, domain); for accounts, saved data or payments also `references/app/route.md`, and the matching section of `references/by-business-type.md` (main action, pages, proof, mistakes to avoid). Check any paid tool, licence or price on the vendor's own page. Fill `brand/brand.md` as intake.md says.
   App: plan the data model in `references/app/supabase.md`; on the owner's yes `ult gate approve data-model "<words>" --file <migration>`. Sign-in: `references/app/auth.md`. Payments: `references/app/stripe.md`, test mode only.
4. **Build.** Run `ult website "<task>" --root . --cat` and follow `references/website/guide.md`: three directions, the critic, the user's pick (`ult website --approve`), the build, the browser check. Use `references/pages-and-seo.md`, and draft copy with `references/copy.md`; the owner approves every claim. Design tables: `ult design system "<business type>"`.
5. **Review loop.** `ult loop`. Run `ultimatum:compliance-reviewer` on every public page and `ultimatum:taste-critic` on designs. Fix, recheck. Open blockers stop delivery.
6. **Go live.** Work through `references/launch-checklist.md` (apps: also `references/app/checklist.md` and `references/app/legal-risk.md`). Only on the user's yes: `ult gate approve publish "<words>" --link <checked live url>`, `ult gate check publish --need-link`, then `ult gate done publish`. Deploys: `ult gate approve deploy "<words>"` and follow `${CLAUDE_PLUGIN_ROOT}/skills/release/SKILL.md`. Real payments: only after `ult gate approve live-payments "<words>"`.
7. **First 30 days.** The numbers from the checklist; bring them to the user to choose the next change.

Big site (many pages or weeks): `ult board show` and resume from its `resume:` card; decisions in `ult notes add`.

## Rules

- One brief: every change to an approved brief goes through the user.
- Offer the simplest fit first (a payment link, a hosted shop, the booking tool's members area); build an app only when the owner picks it (`references/app/route.md`).
- Sign-in, data access and payment changes get the security overlay: `${CLAUDE_PLUGIN_ROOT}/skills/work/references/security/secure-implementation.md`, plus a test that fails without each guard.
- **Ask before** spending, changing listings (e.g. a Google Business Profile), buying a domain or deploying. Each yes covers one action.
- Never put credentials in Git, prompts or logs; the owner does their own logins and pastes keys into the host. Secret keys never reach browser code.
- Facts marked "check before relying" must be confirmed on the vendor's page first.

## Report

Plain words: what changed, how to open the preview, each check and its result, the critic's last score, what waits for the user, and the one next decision. Never claim more than you ran.
