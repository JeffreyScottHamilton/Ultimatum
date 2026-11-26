# Route: website

For every size of site: small business and local service sites (restaurant or cafe, salon, clinic, trades, agency or consultant, coach, portfolio, creator, personal brand), content sites (blog, docs, many locations), and web apps with accounts, saved data or payments. Most small sites are static and aim at calls, bookings or enquiries. If the brief needs logins, saved data, members-only pages or payments, read `app/route.md` as well.

## Team

Brand (short: positioning and `brand/brand.md`), then the website (three directions, critic, build).

## Site size

Rules of thumb, not laws:

| Size | Fits | Pages |
|---|---|---|
| One page | One service or offer, a new business with little content, a portfolio, an event, a link-in-bio style creator page | Hero with the action, services, proof, about, contact or booking, all on one scroll |
| 4-6 pages | Several services, several towns, a clinic or salon with a menu of treatments, a consultant with case studies | Home, Services (or one page per main service), About, Proof (reviews, work), Contact or Booking; optional Blog or FAQ |
| 7+ pages | Many services or locations, each worth searching for | Add one page per service or town only when real, distinct content exists for it |
| Content site | A blog, guides or docs, a business with many locations, a members-info site | Page templates (article, location, category), search, a content source the owner can edit (a headless CMS, Markdown in Git, or a builder), redirects from old URLs |
| App | Accounts, saved data, a dashboard, subscriptions or a custom checkout | `app/route.md`: data model, sign-in, payments, and two extra approvals |

Recommend the smaller size unless the owner has content to fill more. A thin page is worse than none. Detail per page is in `pages-and-seo.md`.

## Hosting and builder

Prices, limits and terms change: check before relying, on the vendor's own page.

- **Static files on a static host** (for example Vercel, Netlify, Cloudflare Pages, GitHub Pages). Fits when Claude builds the site and the owner rarely edits it. Cheap, fast, preview before production. The owner needs a way to ask for changes.
- **The framework the project already uses.** Fits when a repo exists; do not rebuild it.
- **A website builder** (for example Squarespace, Wix, Webflow, WordPress hosting). Fits when the owner wants to edit text and photos alone, or needs built-in booking, forms or a shop add-on. Ultimatum can write the content, structure and design brief; the build then happens in the builder, and the owner does their own logins.
- **A booking tool's own page.** Fits as the first step for a solo trader who only needs a link; the main site can come later.

Forms: use the host's form feature or the booking tool's embed. A mailto link is a last resort because it fails on devices without a mail app. Check that enquiries reach a monitored inbox.

Motion: restrained. GSAP with ScrollTrigger and Lenis are options (see `website/feel-bar.md`); skip heavy motion on a local-service site, where speed on a phone matters more.

## Domain and email

- The owner buys and owns the domain in their own account; never ask for registrar passwords. Prefer a name matching the business name; a short, spellable one is better than a clever one (rule of thumb).
- Point DNS at the host as the host's guide says; HTTPS should be automatic on most hosts (verify on the live URL).
- Business email on the domain (via a mailbox provider such as Google Workspace, Microsoft 365 or the registrar's mailbox) looks more trustworthy than a free address. Prices: check before relying. Setting up mail records can break existing mail, so ask what mail already runs on the domain before touching DNS.

## Order

1. Brand file, then three directions, critic, user's pick.
2. Build in 2-3 phases (hero and action, content sections, contact or booking).
3. Browser check at 375, 768 and 1440 px; compliance review of claims (reviews, "best", prices, medical or legal wording).
4. `launch-checklist.md`, then deploy on the user's yes (`ult gate approve deploy "<words>"`).
