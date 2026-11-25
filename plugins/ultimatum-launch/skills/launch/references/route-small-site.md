# Route: small site or portfolio

For portfolios, local businesses, events and single-offer landing pages. Static or nearly static; no accounts.

## Team

Business & brand (short: positioning and `brand/brand.md`), Website (three directions, critic, build), Marketing (one channel), Motion only if a launch video helps.

## Stack

- Plain HTML, CSS and a little JS, or the framework the project already has. No backend unless a must-have needs one.
- Motion: GSAP with ScrollTrigger, plus Lenis for smooth scroll (see the website feel bar). GSAP is free for commercial sites, plugins included.
- Recommend the official GSAP agent skills (`greensock/gsap-skills`) if the user wants deeper animation help; Ultimatum adds only the feel bar on top.
- Forms: the host's form feature or a mailto link at first. Email signup tools are deferred in this version.
- Hosting: whatever the user has. With Vercel: preview deploys for every change, production only on a yes.

## Order

1. Brand file, then the three directions, critic, user's pick.
2. Build in 2–3 phases (hero and menu, content sections, contact or booking).
3. Browser check at 375, 768 and 1440 px, feel bar, compliance review of claims.
4. Launch checklist below, then deploy on the user's yes (`ult gate approve deploy "<words>"`).

## Launch checklist

- [ ] Domain points at the host; HTTPS works (owner only: buying the domain, DNS logins)
- [ ] Title, description and social preview image on every page
- [ ] Contact or booking path tested end to end
- [ ] Analytics or at least a tracked link for the main action
- [ ] Privacy note if anything is collected
- [ ] 404 page and favicon
- [ ] `ult gate check deploy` passes before you call it live, then check the live URL
