# Measure: tracking and tests

Read when setting up analytics on a new site, when numbers look wrong, when the owner asks "is this working?", or before running an A/B test. Tracking that nobody uses is a cost (page weight, consent banners, privacy risk), so start from the decisions.

## 1. Start from the decisions

Write down the three to five questions the owner will act on, then track only what answers them.

| Question | What to count |
|---|---|
| Is the site bringing enquiries? | form sent, call link tapped, booking finished, email link tapped |
| Where do customers come from? | the source and campaign of the visit that led to the enquiry |
| Which page loses people? | views of each step, then the action |
| Did the change help? | the same action rate before and after, same weeks of the year if possible |

A small-business site rarely needs more than 5 to 15 events. `ult market events` warns above 30.

## 2. The tracking plan

Keep it in the repository as `tracking-plan.csv` (or JSON) with the columns `event,properties,trigger`, and check it:

```bash
ult market events tracking-plan.csv
```

Rules it checks:

- **Names:** `object_action` in snake_case, action in the past tense: `quote_form_submitted`, `call_link_clicked`, `booking_completed`. It fails on other shapes and warns when the last word isn't past tense.
- **No duplicates.**
- **No personal data in properties.** Email, phone, names, addresses, IPs and dates of birth fail. Count that a form was sent, not who sent it.
- **Every event says exactly when it fires** ("after the server confirms the booking", not "on click").

Example rows:

```csv
event,properties,trigger
quote_form_submitted,service_type;page_path,server returned 200 for the quote form
call_link_clicked,page_path;link_location,tap on any tel: link
booking_completed,service_type;deposit_paid,booking tool redirected to /thanks with a booking id
```

Use the analytics tool's own names where they exist (GA4's recommended events such as `generate_lead`, `sign_up`, `purchase`) and map yours to them, so built-in reports work. Keep one list of property names and reuse them across events.

## 3. Prove the tracking works

Every conversion is counted once, on success, from every route that produces it.

- Fire on the confirmed result: the thank-you page with an id, or the server's success response. Clicks on "Send" overcount when the form fails.
- Test each event in the tool's debug view: send a real test enquiry, see it arrive with the right properties, then delete or mark it.
- Check no double counts: refresh the thank-you page and press back; the count must not rise.
- Mark the key events as conversions in the analytics tool and in any ad account, with the same name.
- Compare with the source of truth monthly: enquiries in the inbox or bookings in the booking tool against the event count. A gap over about 10 to 20% means something is broken or blocked (ad blockers and declined consent cause some gap; say so).
- Consent: where the law requires opt-in (much of Europe and the UK), analytics and ad tags wait for consent. Use the tool's consent mode if it has one. Check before relying on the rules for the owner's country.
- UTM tags on every link the owner controls outside the site (emails, social bios, print QR codes): `utm_source`, `utm_medium`, `utm_campaign`, lowercase, one agreed spelling.

Write down what was tested and when in the launch checklist. Never say tracking works without having sent a test conversion.

## 4. A/B tests

Only when a page gets enough actions: under about 100 conversions a month per page, a test won't finish in time; improve the page and watch the trend instead.

**Plan before starting:**

```bash
ult market abtest plan --base 0.04 --lift 0.15 --daily 900
```

`--base` is today's rate, `--lift` the smallest relative change worth acting on, `--daily` the visitors reaching the test each day. It prints the visitors each version needs (two-sided test of two proportions at alpha 0.05 and power 0.8 by default; more than two versions split alpha across the comparisons), and the days to run in whole weeks, at least two, so weekdays and weekends both count. Over eight weeks, it says to test a bigger change instead.

Write the plan before launch: the change, why it should work, the one main metric, a guard metric (refunds, bounces, call quality), the visitors needed and the end date. Test one idea at a time; several small edits that serve one idea are fine.

**Run it:** split visitors randomly and keep each person in their version. Don't change the page, the traffic sources or the split mid-test.

**Read it at the planned size, not before:**

```bash
ult market abtest read --a 96/2400 --b 131/2390 --planned 2300
```

It prints both rates, the lift, a p-value, a 95% interval for the difference and a verdict: `not finished` (below plan; peeking and stopping early makes false wins common), `B wins` / `A wins`, `no clear difference`, or `broken split`. A broken split (the sample-ratio check under 0.001) means the visitors didn't divide as set, usually a redirect, a bot filter or a caching bug; fix it and rerun, since no result from that test can be trusted. It exits 1 in that case.

A "win" with an interval that nearly touches zero is a small, uncertain gain; keep it only if the new version is no harder to maintain. A "no clear difference" is a result too: keep the simpler version and try a bolder idea.

## 5. Reporting to the owner

Monthly, one screen: enquiries by source, the top three pages people act from, what changed this month, and one proposal for next month. Same numbers, same definitions every month. If a number moved because tracking changed, say so next to it.
