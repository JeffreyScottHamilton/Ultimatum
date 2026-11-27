# Launch day: load, limits and spend

Read this before an app with accounts or data goes live, and again before any launch you expect to bring a spike (a post that might travel, a press day, a paid campaign). Each item says what to set, why, and how to show it is done. Vendor names, plans and numbers change: confirm each on the vendor's own docs and pricing page, and write down the number you found and the date.

Start with one figure: **expected peak**, in users per minute and requests per minute, from the owner's best guess (mailing list size, follower count, ad budget). Every limit below is checked against it.

## 1. Money stops, not just warns

1. **A spend limit that pauses.** An alert at 3 a.m. is read at 9 a.m. Set the host's hard limit so the project pauses when it is reached (Vercel: Spend Management; check which plans can pause and that "pause" is switched on, not only notifications). Do the same for the database (Supabase: the spend cap) and every metered API. Evidence: a screenshot or the settings page text with the amount.
2. **The host's attack protection on.** On Vercel, know where Attack Challenge Mode is and turn it on during an attack; check the firewall rules for your plan. Elsewhere, put the site behind Cloudflare with its DDoS protection. Rate-limit sign-up, login, password reset and any route that costs money per call. Evidence: a rate-limit rule listed, and one request over the limit answered with 429.
3. **Free plan limits against launch day.** For hosting, database, sign-in and storage, write a row: the limit (bandwidth, function time, database size, monthly active users, storage, egress), our launch-day estimate, and what happens when it is hit (paused, throttled, billed). Any row where the estimate passes half the limit: upgrade before launch or cut the load.

## 2. The database survives the spike

4. **Connections through a pooler.** Serverless functions open many short connections; Postgres allows few. Use the provider's pooler in transaction mode for serverless code (on Supabase, the pooler connection string for transaction mode; prepared statements are not supported there, so turn them off in the client). Keep session mode or a direct connection for migrations.
5. **Functions near the database.** Set the function region to the database region. Every query crosses that distance; a continent between them adds a tenth of a second or more per query. Evidence: both regions written down and equal.
6. **An index on every column we filter, join or sort by.** Run `explain analyze` on the five busiest queries with realistic row counts; a sequential scan on a large table is the fix list. Foreign keys are not indexed automatically in Postgres.
7. **Every list paginated.** No query without a limit. Supabase's Data API also caps rows per request (a "max rows" setting, 1,000 by default; confirm in the API settings), so a list that silently stops at that cap is a bug, not a feature. Use keyset pagination (`where created_at < $last order by created_at desc limit 20`) for feeds.
8. **No N+1 queries.** A list of 50 posts must not run 50 more queries for authors. Join (Supabase: select related rows in one call, `posts(*, author:profiles(name))`) or batch by id. Evidence: query count per page from the database logs or a counter in tests.

## 3. Less work per visit

9. **Static or cached at the CDN** for pages that look the same for everyone: home, pricing, blog, docs. Personal data never goes in a shared cache; set `Cache-Control: private` on anything per-user.
10. **Images resized, compressed and lazy-loaded.** Serve WebP or AVIF at the size shown, with `width` and `height` set, `loading="lazy"` below the fold and the hero image loaded eagerly. Evidence: the largest image under 200 KB on the home page.
11. **Uploads straight to storage with signed URLs**, not through a function: the browser gets a short-lived upload URL and sends the file directly; functions have small body limits and you pay for their time. See `supabase.md` for bucket policies.
12. **Slow work in a background queue:** emails, AI calls longer than a few seconds, exports, image processing. The request returns at once with "we're on it"; the job retries on failure and is safe to run twice.

## 4. Other people's limits

13. **AI provider rate limits and monthly cap** checked against launch traffic: requests per minute, tokens per minute, and the monthly spend limit set in the provider console. On a 429, show "We're busy, try again in a minute", wait and retry with backoff, and never charge the user's credits for a failed call.
14. **Sign-up and login emails through our own email provider** (custom SMTP). Built-in senders on hosted auth are rate-limited and meant for testing. Set SPF, DKIM and DMARC for the sending domain.
15. **The email plan's daily and monthly limits fit launch day:** sign-ups × (confirm + welcome) + resets, with room to spare.
16. **SMS only to countries we serve**, with the provider's fraud protection on (on Twilio: geographic permissions limited to our countries, and its SMS pumping protection; check the current product names). SMS sign-in is the classic target for paid-message fraud.
17. **Live connections fit launch day.** Realtime and websocket plans cap concurrent connections and messages. Estimate concurrent users at peak; when the cap is hit, fall back to polling every 10 to 30 seconds and say "live updates paused".

## 5. Proof and a way back

18. **A load test at 10× expected peak, on staging.** Never against the live site without the owner's yes, and never through paid third-party APIs (stub them, or the test becomes the bill). Watch error rate, p95 response time and database connections. A tool such as k6 or `oha` is fine; record the command and the numbers.
19. **Uptime alerts that reach a phone.** One check on the home page and one on a route that touches the database, every minute or two, alerting by push or SMS to the owner, not only by email.
20. **A one-click rollback to the last good deploy.** Know where it is before launch (Vercel: Instant Rollback; Netlify and Cloudflare Pages keep earlier deploys to restore) and try it once on a preview. A rollback restores code, not the database: migrations must be additive (add columns, don't drop or rename on launch week) so the previous build still works against the new schema.

## Record

Copy into the launch notes, one line each: item, setting or number, where it was checked, date. Anything left undone is named to the owner with what happens if launch day hits it.
