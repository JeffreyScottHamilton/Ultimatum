# Launch checklist

Two gates: before announcing, and before opening sign-ups (often the same day). Work through each list with the organiser. Items marked **check locally** depend on where the event happens; this plugin does not say what any law requires. The organiser confirms them with the venue, the local authority or a professional.

## Before announcing

### The event is real

- [ ] Date, start and end time confirmed (and time zone for online events).
- [ ] Venue booked in writing, or the online platform chosen and tested.
- [ ] Speakers, hosts or performers confirmed in writing, including consent to use their name, photo and bio.
- [ ] Capacity agreed with the venue and the host.
- [ ] Price decided by the organiser.
- [ ] The brief is approved (`ult gate status brief`).

### Venue and legal items (check locally)

- [ ] Venue capacity and fire safety arrangements: check locally with the venue.
- [ ] Permits for the event type, signage or use of public space: check locally.
- [ ] Licences for music played or performed, and for any recording shown: check locally.
- [ ] Insurance for the event and for the organiser: check locally.
- [ ] Food served or sold: check locally (handling, labelling, allergens).
- [ ] Alcohol served or sold: check locally.
- [ ] Accessibility arrangements described accurately: confirm with the venue.
- [ ] Children attending, or working with children or vulnerable people: check locally.
- [ ] Fundraising, raffles or prize draws: check locally.

### The page

- [ ] Event page says what, when, where, who for, what you leave with, price, refund and transfer line, accessibility and a contact.
- [ ] One sign-up button, working, on desktop and phone.
- [ ] Details match everywhere: page, listings, posts, sign-up tool.
- [ ] Images are owned, licensed, or used with permission; people in them agreed.
- [ ] Compliance reviewer run on the page and the first posts; no open blockers (`ult loop status`).
- [ ] Taste critic run on the page and creative.

## Before opening sign-ups

- [ ] Sign-up tool set up: ticket types, prices, capacity, waitlist, dates for early-bird if used.
- [ ] Refund and transfer policy written in plain words and shown at checkout and in the confirmation.
- [ ] Form asks only what the event needs; marketing consent unticked by default.
- [ ] Confirmation and reminder messages written and scheduled (sending needs the organiser's yes).
- [ ] End-to-end test done (`tickets-and-signups.md`): sign-up, confirmation, list, capacity, refund.
- [ ] Payouts connected by the organiser; no account details shared here.
- [ ] Tracked links ready for each channel.
- [ ] Privacy: the organiser knows where attendee data is kept and who can see it; data protection rules are check locally.
- [ ] Announcement posts and the first email approved, each with its own yes.

## Publish

Only after the organiser's yes:

```
ult gate approve publish "<their words>" --link <checked live url>
ult gate check publish --need-link
ult gate done publish
```

Open the live page once more on a phone after publishing and complete one real sign-up path up to the payment step.

## If something is not ready

Do not announce with an open blocker. Tell the organiser which items are open, what each one risks, and whether the date still works. A short delay to the announcement is usually better than changing details after people have signed up.
