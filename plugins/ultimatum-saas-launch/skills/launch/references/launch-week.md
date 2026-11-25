# Launch week, day by day

For a public launch (see `route.md` for waitlist and beta paths). Start only when `launch-checklist.md` is done. Every post, email send and ad spend needs the user's yes, one action each. Third-party launch sites have their own rules that change: **check before relying** on each site's current guidelines before planning around it.

## Two weeks before

- [ ] Launch date agreed with the user; avoid days when the team cannot be online (rule of thumb: a weekday early in the week gives time to fix things before the weekend).
- [ ] Assets ready and through compliance review: headline, one-paragraph description, 3-5 screenshots of the real product, a short demo video (`ultimatum-launch:motion-graphics`), founder photo if used.
- [ ] Waitlist told the date and what they will get (an early-user offer only if the user approves it).
- [ ] Beta users asked if they will share an honest comment or quote on launch day; quotes only with written permission.
- [ ] Launch-site listings drafted (Product Hunt, "Show HN" on Hacker News, relevant communities) and each site's rules read. No asking for votes; no fake accounts.
- [ ] Load check on sign-up and the most expensive endpoint; error tracking on; status page ready.

## Day by day

| Day | Product and support | Marketing (each send or post: user's yes) |
|---|---|---|
| Day -3 | Code freeze for anything not launch-critical; billing test-mode rehearsal once more | Final copy approved; posts and emails scheduled as drafts, not sent |
| Day -2 | Production deploy of the launch version (`ult gate approve deploy "<words>"`); smoke test sign-up, payment, cancel on production with a real card and refund (owner) | Website announcement banner and changelog entry ready |
| Day -1 | On-call rota written: who watches errors, inbox and community comments, and for which hours | Reply templates for likely questions: pricing, security, data export, roadmap |
| Day 0 morning | Watch error tracker and sign-up funnel live | Waitlist email first; launch-site post(s); founder post on the user's own accounts |
| Day 0 all day | Fix blockers immediately, log each with `ult loop add`; post status updates if anything is down | Reply to every comment personally and plainly; thank people; no arguing |
| Day 1 | First activation numbers: did launch sign-ups reach the aha? | Share one honest result or lesson; a short demo clip |
| Day 2 | Fix the top onboarding drop-off seen on day 0-1 | Post in one relevant community where self-promotion is allowed, leading with usefulness |
| Day 3 | Read every feedback answer; tag themes | Email new sign-ups who did not activate (from `onboarding-emails.md`) |
| Day 4 | Ship one visible fix from feedback; changelog entry | Post about the fix: "you asked, we shipped" |
| Day 5-7 | Weekly review with the user | Thank-you email to supporters; record numbers with `ult social --results "<numbers>"` |

## Numbers to read at the end of the week

Visits, sign-ups, activation rate, trials started, paid accounts, top traffic sources, top three feedback themes, open bugs. Compare to the brief's 90-day goal, not to other companies' launch stories.

## If launch day goes quiet

- It is common; many products grow from steady weeks after launch, not one day (rule of thumb).
- Look at the funnel first: no visits is a distribution problem; visits without sign-ups is a page problem; sign-ups without activation is an onboarding problem.
- Pick one channel that brought the best users and do more there; personally email the first 20 users and ask what nearly stopped them.

## If something breaks

1. Post on the status page or a pinned post: what is affected, that it is being worked on.
2. Roll back if a deploy caused it (deploy rollback still needs a yes for production changes unless the user has agreed a rollback rule in advance).
3. Fix, verify, and post that it is resolved.
4. Email affected users plainly if data or billing was touched; the owner decides the wording.

## Beginner mistakes

| Mistake | Fix |
|---|---|
| Launching on every site the same day with no one replying | Two or three channels the team can actually answer |
| Asking friends to upvote | Against most sites' rules; share the link with a plain "here is what we built" |
| Deploying new features on launch morning | Freeze two or three days before |
| Demo video showing features that are not live | Show only what a new user can do today |
| No one watching the sign-up funnel | A named person with the error tracker and analytics open |
| Treating launch day as the finish | Plan weeks 2-4 now: onboarding fixes, one channel, customer calls |
