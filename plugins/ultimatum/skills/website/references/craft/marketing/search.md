# Search and AI answers

Read when the site doesn't show up for searches it should, traffic dropped, the owner asks about SEO or about being mentioned by AI assistants, or you're planning the page structure of a new site. Local basics (Business Profile, NAP, reviews) are in `../../pages-and-seo.md`; this file adds the audit, structure, markup and AI answers. Search engines change their rules; anything marked "check before relying" must be confirmed on the engine's own documentation.

## 1. Diagnose in this order

1. **Can it be found at all?** Search `site:example.com`. Nothing: check `robots.txt` isn't blocking, pages aren't `noindex`, the domain is verified in Google Search Console and Bing Webmaster Tools (the owner verifies), and a sitemap is submitted.
2. **Are the right pages indexed?** Search Console's page indexing report: look for "Crawled, currently not indexed" (often thin or duplicate pages) and "Duplicate without user-selected canonical".
3. **Does each page target one thing?** One main topic per page, said in the title, h1 and first paragraph in the words people search.
4. **Is it fast and usable on a phone?** §2.
5. **Does it earn trust?** Real business details, reviews, links from local and trade sites.
6. **Did something change?** For a drop: compare dates against site changes (redesign, new URLs, removed pages), tracking changes, and announced search updates. Most drops after a redesign are lost redirects.

Report each issue with the URL, the evidence (a screenshot or report row), the fix and its priority: blocking indexing, then wrong targeting, then speed, then nice-to-have.

## 2. Technical checks

Run `ult market page site/` for the per-page basics. It checks the title (15 to 60 characters), meta description (70 to 160), one h1, `lang`, viewport, a full https canonical, Open Graph tags, image alt, and repeated titles or descriptions across pages.

Beyond that:

- **HTTPS everywhere,** one host (with or without `www`), the other redirecting with a 301.
- **Clean URLs:** lowercase, hyphens, short, no dates unless it's news. `/services/boiler-repair`, not `/page?id=7`.
- **Redirects on any URL change:** old URL → new URL, one hop, 301. Keep a list when redesigning; check it after launch.
- **Sitemap** listing only canonical, indexable pages; **robots.txt** not blocking CSS, JS or images.
- **Speed (Core Web Vitals, at the 75th percentile of real visits):** Largest Contentful Paint 2.5 s or less, Interaction to Next Paint 200 ms or less, Cumulative Layout Shift 0.1 or less. Measure with PageSpeed Insights or the Search Console report; fix large hero images, web-font blocking and layout jumps first.
- **Mobile:** content the same as desktop, text readable without zoom, nothing covering the main content.
- **Languages:** separate URLs per language with `hreflang` pairs that point back to each other, including `x-default`.

## 3. Structure the site

- Every important page within three clicks of the home page, and linked from at least one other page in the body text, not only the menu.
- Group by what customers look for: `/services/<service>`, `/areas/<town>` only with real local content, `/work/<project>`.
- Header navigation: 5 to 7 items, in the customer's words. Put the main action as a button at the end.
- Footer: contact details, hours, the service list, legal pages.
- Breadcrumbs on deeper pages, with `BreadcrumbList` markup.
- Before building, sketch the tree for the owner: each page, its one topic and its parent. A page with no unique topic doesn't need to exist.

**Many pages from a template** (one per town, per product, per integration): only when each page has something no other page has, such as local photos, local reviews, a real price for that area, or specific data. Swapping the town name into the same text makes thin pages that can drag the whole site down. Start with 5 to 10, check they get indexed and visited, then add more.

## 4. Structured data (JSON-LD)

Mark up only what the page shows, with true values. `ult market page` parses every JSON-LD block, fails on parse errors, a missing `@context` and missing required properties, and warns on markup that earns nothing.

| Page | Type | Must have (checked) | Good to add |
|---|---|---|---|
| Home or contact (local) | `LocalBusiness` or a subtype (`Plumber`, `Dentist`, `Restaurant`…) | name, address | telephone, openingHoursSpecification, geo, url, image, sameAs, priceRange |
| Home (non-local) | `Organization` | name, url | logo, sameAs, contactPoint |
| Whole site | `WebSite` | name, url | - |
| Service page | `Service` | name | provider, areaServed, offers |
| Product | `Product` | name, plus offers or review | image, description, brand |
| Product price | `Offer` | price, priceCurrency | availability, url |
| Blog post | `BlogPosting` or `Article` | headline | datePublished, author, image |
| Event | `Event` | name, startDate, location | offers, eventStatus |
| Deeper pages | `BreadcrumbList` | itemListElement | - |

Known limits (check before relying): since 2023 Google shows FAQ rich results only for well-known government and health sites, and has retired HowTo rich results; review stars a business puts on its own `LocalBusiness` or `Organization` are not shown. Keep FAQs for readers; put real reviews on the page as text. Validate with Google's Rich Results Test and the Schema.org validator before launch.

## 5. AI answers and assistants

AI assistants and AI search summaries build answers from pages they can fetch and from what many sources agree on. What helps, as far as is publicly known (check before relying; this moves fast):

- **Be fetchable.** Important text in the HTML, not only drawn by JavaScript or in images. Don't block the crawlers the owner wants to be found by in `robots.txt`; blocking is the owner's choice, so ask.
- **Answer plainly.** Under each question-style heading, put a one- or two-sentence direct answer first, then the detail. Use tables for prices, hours and comparisons.
- **Say the facts once, the same everywhere.** Name, services, area, prices and hours must match across the site, the Business Profile, directories and social profiles. Assistants repeat what sources agree on.
- **Be mentioned elsewhere.** Local press, trade directories, review sites and community pages that name the business count more than anything on the site itself.
- **Date and source your numbers.** Pages with specific, dated facts are easier to cite.
- **Check what they say.** Ask two or three assistants the questions a customer would ("best emergency plumber in Northgate open Sunday"). Record the answers with the date. If facts are wrong, fix the sources they likely used; there's no form to submit.

Don't promise rankings or AI mentions. Report what was changed and when, then compare search impressions and the assistant answers a month later.
