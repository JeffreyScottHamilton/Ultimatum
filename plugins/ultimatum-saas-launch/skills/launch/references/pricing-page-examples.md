# Pricing page: worked examples

Use after the model is chosen in `pricing-and-billing.md`. The products, plan names and prices below are **made up** to show structure; they are not suggestions or market rates. Real prices come from the user, tested with buyers. Competitor prices go through the fact-finder and are marked observed or guessed.

## Build order

1. Write the plan table in plain text first (name, for whom, price, what is included, limit), and get the user's yes on it.
2. Write the FAQ from real questions (beta users, sales calls, support inbox); add the standard ones listed below.
3. Hand both to `ultimatum-launch:website` with the anatomy from `pricing-and-billing.md`.
4. Compliance review of every claim, then a check that each button goes to the right checkout or form, in test mode.
5. Wire the analytics event `visited_pricing` and the plan chosen at checkout.

## Example A: self-serve tool, tiered with a trial

A made-up invoicing tool for freelancers.

| | Starter | Pro (recommended) | Studio |
|---|---|---|---|
| For | One freelancer starting out | Freelancers billing every week | Small studios with a few people |
| Price | [price] / month | [price] / month | [price] / month |
| Includes | Up to [n] clients, invoices, reminders | Unlimited clients, recurring invoices, payment links | Everything in Pro, [n] team members, shared templates |
| Button | Start free trial | Start free trial | Start free trial |

Below the table: "[n]-day free trial. No card needed. Cancel any time in Settings." (only if each is true). Then the FAQ.

What makes it work: plan names say who it is for; the middle plan is marked as the one most people should choose; the limit that differs between plans is the value metric (clients, team members), not a long feature checklist.

## Example B: usage-based API

A made-up text-extraction API.

| | Free | Pay as you go | Volume |
|---|---|---|---|
| For | Trying it out | Production apps | High, steady volume |
| Price | [n] calls / month free | [price] per 1,000 calls | Talk to us |
| Limits | [n] requests / minute | [n] requests / minute, spending cap you set | Custom limits, support terms |
| Button | Get API key | Get API key | Contact sales |

Must also have: a cost calculator (calls per month in, monthly cost out), the spending cap or alert explained, what happens at the limit (requests rejected or billed as overage), and a link to rate limits in the docs.

## Example C: sales-led B2B

A made-up compliance tool for mid-size companies.

| | Team | Business | Enterprise |
|---|---|---|---|
| For | One department | Several departments | Company-wide, custom security review |
| Price | From [price] / year | From [price] / year | Custom |
| Button | Book a demo | Book a demo | Contact sales |

Showing a "from" price, even on sales-led pages, filters out buyers who could never afford it (rule of thumb). If the user will not show prices, say what the price depends on (number of seats, modules) so the call is not a surprise.

## FAQ questions most pricing pages need

- Can I change plans later? What happens to my data if I downgrade?
- How do I cancel, and do I get a refund? (Must match the terms page.)
- What payment methods do you accept? Can I pay by invoice?
- Are prices shown with or without tax?
- Is there a discount for annual billing, non-profits or students? (Only if true.)
- What happens when I hit a limit?
- Where is my data stored, and can I export it?

## Monthly / annual toggle

- Show the annual price as a per-month figure and the yearly total next to it, so nobody is surprised at checkout.
- State the saving in plain numbers ("2 months free" only if the maths says so).
- Default the toggle to the option the user wants most people on; say which, and test it.

## Beginner mistakes

| Mistake | Fix |
|---|---|
| Five or more plans | Two or three; move rare needs to "Contact us" |
| Feature checklist of forty rows | Show the five rows that differ; link to a full comparison below |
| Plan names that mean nothing (Basic, Plus, Premium) | Name for whom: Solo, Team, Company |
| "Unlimited" that is not | State the fair-use limit, or do not say unlimited |
| Price only after sign-up | Show it on the page; hidden prices lose trust |
| Annual price shown per month with no yearly total | Show both figures |
| Testimonials with no permission | Only quotes and logos the customer agreed to, logged |
| Changing price for existing customers without notice | Announce early and honour what they signed up for, as the terms say |
