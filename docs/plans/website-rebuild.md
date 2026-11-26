# Plan: a full website builder and our own design knowledge

Status: outline for the user's review. Nothing here is built yet.

## 1. Scope: every kind of website

The website workflow grows from small local sites to full web apps. Nothing it does today is removed.

| Size | Examples | What the workflow adds |
|---|---|---|
| Small | cafe, salon, trades, portfolio | today's flow: intake, brief, three directions, build, browser check, go live |
| Content | blog, docs, multi-location business, membership info site | CMS choice, page templates, search, redirects, larger SEO plan |
| App | Supabase database, sign-in and accounts, Stripe payments and subscriptions, dashboards | data model, row-level security, auth flows, Stripe test mode, webhooks, a security review before go-live |

New for the app size:
- **Supabase:** schema planning, row-level security on every table, policies tested with a second user, migrations in Git, the service key never in the browser.
- **Sign-in:** email and password, magic links, OAuth (Google, Apple), password reset, sessions, roles, account deletion.
- **Stripe:** Checkout or Payment Element, products and prices, subscriptions and the customer portal, webhooks verified by signature, test mode until the owner says go, receipts and refunds.
- **Gates:** two new approvals, "data model" and "go live with real payments". Live keys and real charges only on the owner's yes.
- **Security:** the Work skill's security guides run on every auth, payment and data change, with a test that fails without each guard.

## 2. UI UX Pro Max: rebuilt in full, in our own words

Every part of their repo gets an Ultimatum version. Nothing is cut. Each one is written from primary sources (official docs, standards, font and icon projects' own metadata) and our lessons, never by rewording their rows. Their repo only tells us which topics to cover.

| Their part | Their size | Our version |
|---|---|---|
| products | 194 business types | 194 or more, plus local-service detail (booking, calls, quotes, trust signals) |
| styles | 89 | 89 or more, each with when to use, when not, and the slop habits it invites |
| colors | 194 palettes | 194 or more, every pair checked for WCAG contrast by our own script |
| typography | 74 pairs | 74 or more, with licence, weights and fallbacks checked against the foundry |
| google-fonts | 1,934 fonts | rebuilt from Google Fonts' own public metadata (family, category, weights, licence) |
| icons | 105 | 105 or more, from Lucide's and Phosphor's own metadata, licence per set |
| landing | 34 page patterns | 34 or more, plus app patterns (sign-up, pricing, dashboard, checkout) |
| ui-reasoning | 194 rules | 194 or more, merged with our anti-generic lint (both slop lists) |
| ux-guidelines | 141 | 141 or more, tied to WCAG 2.2 success criteria |
| app-interface | 32 | 32 or more |
| react-performance | 44 | 44 or more, tied to React and Next.js docs |
| charts | 25 | 25 or more |
| motion | 20 | 20 or more, plus our motion personalities and reduced-motion rules |
| stacks | 23 frameworks | all 23, our own guidelines and tested code examples, each linked to official docs |
| design-system skill | tokens, templates | our tokens and templates |
| brand skill | brand guide | merged into our `brand/brand.md` flow, expanded |
| design skill (logo, icon, corporate identity) | generators and data | our own logo, icon and identity guidance |
| ui-styling | component styling, canvas fonts | our styling guide; fonts linked, not bundled (they carry their own OFL licences) |
| slides | slide design | kept as our own slide guide |

New tables of our own: Supabase patterns, auth flows, Stripe flows, local trust signals, copy patterns, and the anti-generic lint as searchable rows.

## 3. How each table is made

1. A coverage test first: a few hundred real requests ("plumber site", "cafe palette", "focus ring in Next.js", "Stripe subscription page") that must return a good answer.
2. Write our rows from primary sources and our lessons. Code examples are ours and are run where possible. Links point to official docs and are checked.
3. A copy check compares our text with theirs and flags any sentence that matches.
4. The taste critic and the unit tests run.
5. Ours replaces theirs only when every coverage request passes and the copy check is clean. Then their data and MIT file come out.

## 4. The other website skills, after UI UX Pro Max

Same method, in this order: Taste, Impeccable, Hallmark, Anatomy, Emil's animation skill, anime.js, gstack's design review and QA. Each gets an in-depth study, an outline of what it knows, and our own expanded version. Coding skills come after.

## 5. Releases

One patch release per finished part (0.0.8 scope and app support, then one per table group), each with tests and a CHANGELOG entry, pushed to the feature branch only.
