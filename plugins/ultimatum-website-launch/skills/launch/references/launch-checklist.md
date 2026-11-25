# Launch checklist

Tick each item with evidence (a command, a screenshot or a live URL), not a guess. Owner-only steps (domain purchase, DNS and listing logins) stay with the owner.

## Before launch

- [ ] **Forms end to end.** Submit a real test enquiry on the live or preview URL; confirm the owner receives it, the visitor sees a confirmation, and spam is limited (honeypot or the host's filter).
- [ ] **Booking end to end.** Make a test booking, check the confirmation email and the calendar entry, then cancel it. Test on a phone.
- [ ] **Phone links.** Every number is a tap-to-call link; tap one on a phone.
- [ ] **Maps and address.** Map loads, pin is correct, directions link works, hours match the listing.
- [ ] **Mobile speed.** Run a Lighthouse or PageSpeed check on the home page at mobile settings; fix oversize images first. Targets are rules of thumb (for example, main content visible in about 2.5 seconds on mobile); check current Core Web Vitals thresholds before relying.
- [ ] **Browser check** at 375, 768 and 1440 px; no horizontal scroll, no cut-off buttons.
- [ ] **Analytics and events.** Page views plus events for call taps, booking clicks and form submits. Pick a tool and its tier by checking the vendor's page. Add a cookie or privacy notice if the tool needs one for the owner's country.
- [ ] **Domain, SSL, email.** Domain resolves with and without `www`, one redirects to the other; HTTPS valid; business email sends and receives; SPF/DKIM set if the domain sends mail (ask before changing DNS).
- [ ] **Basics.** Title, description and preview image per page; 404 page; favicon; sitemap; privacy note if anything is collected; schema validates.
- [ ] **Claims reviewed** by the `ultimatum-website-launch:compliance-reviewer` agent; no open blockers in `ult loop`.
- [ ] **Deploy approved** (`ult gate approve deploy`), `ult gate check deploy` passes, live URL checked.

## Launch week

Each outward action needs the user's yes (one yes per action).

1. **Tell existing customers.** A short email, text or message with the link and the main action; draft it, the owner sends it.
2. **Listings.** Update the website link and booking link on Google Business Profile, directories and social bios (owner's yes, owner's login).
3. **Social.** One announcement post and a pinned link; use the Social Media team's drafts.
4. **Review requests.** Ask five recent happy customers for a review with the direct link (no payment, no pressure).
5. **Local word of mouth.** A flyer or QR code, a nearby partner business, a community group the owner already belongs to.
6. **Watch.** Check the form inbox and booking tool daily; reply fast (rule of thumb: same day).

## First 30 days

Record weekly, plainly, in `.ultimatum/` notes or the Marketing results (`ult social --results`):

| Metric | Where | What it tells you |
|---|---|---|
| Enquiries | form inbox, tool | demand |
| Bookings | booking tool | real outcome |
| Calls | call-tap events, phone log | local intent |
| Visitors | analytics | reach |
| Conversion rate | (enquiries + bookings + calls) / visitors | whether the page works |
| Top sources | analytics, profile insights | where to spend effort |
| New reviews | profile | trust and local ranking |

Rule-of-thumb reading: few visitors means fix reach (listings, reviews, social); visitors but few actions means fix the page (headline, button position, proof, form length, speed); actions but few bookings means fix follow-up speed or the booking flow. Change one thing at a time, note the date, compare after two weeks. Small sites have small numbers, so do not over-read a week of data. Bring the table to the user and choose the next single test together.
