# marketingskills rebuild: coverage map

Source: coreyhaines31/marketingskills at commit 2bf95edb4ebd (MIT, Copyright (c) 2025 Corey Haines), read only. Its `tools/clis` partner API wrappers were not run.
Our files: `plugins/ultimatum/skills/website/references/craft/marketing/` (7 files) and `plugins/ultimatum/scripts/ultlib/market.py` (`ult market page|abtest|events`). Test: `plugins/ultimatum/tests/test_market.py`.

## Licence

MIT. We ship none of its text: `tools/copy_check.py` finds 0 shared runs of 8+ words between our guides and its `skills/` folder.

## Scope

Ultimatum builds sites for small businesses, so the set keeps what changes the site and its first emails, and leaves out ads, outreach, sales, PR and app-store work.
Counts: 22 done, 9 partial, 22 out of scope, of 53 upstream skills.

## Items

| Source skill | Status | Where |
|---|---|---|
| `ab-testing` | done | measure.md §4; `ult market abtest plan/read` (sample size, whole weeks, SRM) |
| `ad-creative` | out of scope | paid ads |
| `ads` | out of scope | paid ads |
| `ai-seo` | done | search.md §5 |
| `analytics` | done | measure.md §1–3; `ult market events` |
| `aso` | out of scope | app-store listings |
| `attribution` | partial | measure.md §3 (UTMs, source of the enquiry); multi-touch models left out |
| `churn-prevention` | out of scope | subscription retention, not site building |
| `co-marketing` | partial | launch-and-email.md §2–3 (borrowed reach with partners) |
| `cold-email` | out of scope | cold outreach |
| `community-marketing` | partial | launch-and-email.md §3 (local groups, ask the admin) |
| `competitor-profiling` | partial | offers-and-pricing.md §2 (three dated competitor prices); deep profiling left out |
| `competitors` | done | copy-and-proof.md (comparison page type) |
| `content-strategy` | partial | search.md §3 (one topic per page, tree before building) |
| `conversion-tracking` | done | measure.md §3 (fire on success, test conversion, no double counts) |
| `copy-editing` | done | copy-and-proof.md (six-pass edit); `ult copylint` |
| `copywriting` | done | copy-and-proof.md |
| `cro` | done | convert.md §1–2; `ult market page` |
| `customer-research` | done | copy-and-proof.md (mining customer words) |
| `directory-submissions` | partial | launch-and-email.md §1, §3 (listings match; only where buyers look) |
| `emails` | done | launch-and-email.md §4–5 |
| `events` | out of scope | event marketing; `Event` markup is in search.md §4 |
| `free-tools` | done | offers-and-pricing.md §5 |
| `image` | out of scope | image generation; the website skill's design flow covers visuals |
| `influencer-marketing` | out of scope | influencer deals |
| `launch` | done | launch-and-email.md §1–3 |
| `lead-magnets` | done | offers-and-pricing.md §5 |
| `link-building` | partial | search.md §1, §5 (mentions from local and trade sites); outreach campaigns left out |
| `marketing-council` | out of scope | multi-persona brainstorm; not a site task |
| `marketing-ideas` | out of scope | idea lists |
| `marketing-loops` | out of scope | growth-loop design |
| `marketing-plan` | partial | measure.md §5 (monthly report, one proposal) |
| `marketing-psychology` | partial | offers-and-pricing.md §1 (honest urgency); no list of biases on purpose |
| `offers` | done | offers-and-pricing.md §1 |
| `onboarding` | out of scope | in-product onboarding |
| `paywalls` | out of scope | in-app paywalls |
| `popups` | done | convert.md §4 |
| `pricing` | done | offers-and-pricing.md §2–4; `ult market page --kind pricing` |
| `product-marketing` | done | copy-and-proof.md §1 (message questions and sentence) |
| `programmatic-seo` | done | search.md §3 (many pages from a template) |
| `prospecting` | out of scope | sales |
| `public-relations` | out of scope | PR; one personal pitch is in launch-and-email.md §3 |
| `referrals` | out of scope | referral programmes |
| `reverse-engineer-marketing` | out of scope | competitor teardown |
| `revops` | out of scope | sales operations |
| `sales-enablement` | out of scope | sales teams |
| `schema` | done | search.md §4; `ult market page` checks required properties and dead rich results |
| `seo-audit` | done | search.md §1–2; `ult market page` across the site (duplicate titles) |
| `signup` | done | convert.md §3; form checks in `ult market page --kind signup` |
| `site-architecture` | done | search.md §3 |
| `sms` | out of scope | SMS |
| `social` | out of scope | social content lives with the social-media workflow, not this set |
| `video` | out of scope | video lives with motion-graphics |

## Where ours is ahead

- Upstream is prose only. Ours checks pages (title, description, h1, canonical, social tags, alt, labels, form length, JSON-LD parse and required properties, self-serving stars, dead FAQ and HowTo rich results), A/B maths (sample size with Bonferroni split, whole-week run length, p-value, interval, sample-ratio mismatch) and tracking plans (names, tense, duplicates, personal data).
- Dated facts are current to 2026-11 and marked "check before relying": INP in Core Web Vitals, FAQ and HowTo rich-result limits, bulk-sender email rules.
- One index routes to six files under 7 KB each, linked from the website skill's build step.

## Where upstream still wins

- Breadth: 22 skills we leave out on purpose (ads, outreach, sales, PR, app stores, paywalls, social, video). The index says so and points the owner elsewhere.
- Partner API wrappers for ad and analytics platforms; ours never calls a network service.
