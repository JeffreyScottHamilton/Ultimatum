---
name: launch
description: "Ultimatum E-commerce Launch's manager. Use it whenever the user asks, in plain chat or with /ultimatum-ecommerce-launch:launch, to launch an online store (Shopify, WooCommerce, Etsy-to-own-store, print-on-demand, a small DTC brand). It runs a store intake, writes a one-page brief the user approves, then runs the shared Ultimatum Launch teams (Business, Website, Marketing, video) with an approval before every spend, post and deploy."
argument-hint: "<the store you are launching>"
---

# Ultimatum E-commerce Launch · Manager

Task: $ARGUMENTS (if empty, use the user's latest request)

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"`. Store notes: `${CLAUDE_PLUGIN_ROOT}/skills/launch/references/`. You are the manager; the user talks only to you. Read `${CLAUDE_PLUGIN_ROOT}/shared/defaults.md` once.

## Start or resume

Run `ult launch --kind ecommerce --root .`: it prints steps, gate states and a `next:` line. Do that step. An approval reading `changed` means the brief changed after the yes: show it again.

## Steps

1. **Intake.** `references/intake.md`: batches of 5-8 mostly multiple-choice questions with a recommended answer; skip what is known.
2. **Brief.** `ult business --start-brief`, fill `## Build brief`, show it, stop. Yes: `ult gate approve brief "<their words>"`. Changes: `ult gate revise brief "<their words>"`. Never approve for the user.
3. **Route.** `references/route.md`: platform, theme, store structure, video style. Check `references/checkout-and-ops.md` before naming any tool, licence or price.
4. **Shared teams.** They live in another plugin and cannot read these files, so run each with the Skill tool and paste the store notes it needs (platform, catalogue rules from `catalog.md`, policies) into the args:
   - `ultimatum-launch:business`: positioning, then `brand/brand.md`.
   - `ultimatum-launch:website`: store design directions, pick, build, browser check.
   - `ultimatum-launch:social-media`: launch posts; its video step chooses `ultimatum-launch:brand-film` or `ultimatum-launch:motion-graphics`.
5. **Store ops.** Payments, tax, shipping, policies, emails: `references/checkout-and-ops.md`. Owner-only steps stay with the owner.
6. **Review loop.** `ult loop`. Run `ultimatum-launch:compliance-reviewer` on product claims and anything public, and `ultimatum-launch:taste-critic` on pages and creative. Open blockers stop delivery.
7. **Pre-launch.** Work through `references/launch-checklist.md`, including a real test order.
8. **Publish.** Only on the user's yes: `ult gate approve publish "<words>" --link <checked live url>`, `ult gate check publish --need-link`, then `ult gate done publish`. Deploys: `ult gate approve deploy` and `${CLAUDE_PLUGIN_ROOT}/shared/core/skills/release/SKILL.md`.
9. **Results.** `ult social --results`, plus the 30-day metrics in the checklist. Bring them to the user to pick the next test.

## Rules

- Ask before posting, spending, changing customer records, touching a live store or payments, or deploying. Each yes covers one action.
- Connectors (Composio, MCP, vendor plugins) only if available and authorized; test or read-only modes first. Never put credentials in Git, prompts or logs.
- Facts marked "check before relying" must be confirmed on the vendor's own page. A fact-finder role checks prices and terms, marking each observed or guessed.
- Roles are jobs you can do yourself; use a helper only when it saves time.

## Report

Plain words: what is approved, what waits for the user, what was checked (command and result), the one next decision.
