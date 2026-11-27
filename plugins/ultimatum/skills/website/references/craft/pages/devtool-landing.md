# Landing pages for developer products, APIs and AI services

Read when the product is used through code: an API, an SDK, a command-line tool, a model gateway, a database or a hosting service. Start from `landing.md` for the order of questions and the first-screen test; this file adds what developers and their coding agents check.

## What a developer checks first

1. **What does one call look like?** Show real code in the hero, at a size that can be read, with a switch for each language or SDK that actually exists. Check every import, endpoint, parameter and response against the product's own docs before shipping; a broken snippet on the home page is the fastest way to lose this reader.
2. **What does it return?** Show the response next to the request, or a short run of real output.
3. **How do I get to a first success?** The path from account to key to first working request, visible and short. Docs and the quickstart are one click from the hero and in the top navigation.
4. **What does it cost at my scale?** The billing unit (per request, per token, per seat, per GB), what is included, the limits, any markup or extra fees, and a link to full pricing. If pricing is not decided, say so; never invent tiers or a free allowance.
5. **What exactly is supported?** When models, providers, regions or integrations are the product, list them with real names, what each can do, and filters. Keep "integrates with X" apart from "X is a customer". If the catalogue is partial, say what is coming and do not imply it is there.

## Coding agents are readers too

Many visitors now arrive through an agent working for them. Give it what it needs in plain text:

- A copy button for the quickstart that copies working install steps, the names of the environment variables, and the docs link; placeholders for keys, never a live credential.
- A plain-text or Markdown version of the docs at a stable address, if the product has docs.
- Try the copied text in a clean project before calling the button done.

## Proof that fits developers

- Numbers only when sourced and current, with units and scope (latency at which percentile, from where, measured when). Label example request data as made up; it shows a workflow, not uptime or speed.
- Trust comes from things a developer can check: the changelog, the status page, the limits page, open issues, the licence, the security page. Logos only with the customer's permission.
- Name only the controls the product really has (rate limits, keys per project, audit logs, data retention settings).

## Leave out

- Screenshots faked out of divs, or dashboards that do not exist in the product.
- Metrics, customers, quotes, badges or capabilities that cannot be backed up (`../hallmark/brand-truth.md`).
- Three identical feature cards with headings that could be swapped.
- Sparkle icons and a purple gradient standing for "AI", unless the brand has chosen them.
- Words like "seamless", "unified" or "intelligent" in place of saying what the call does and what the developer gets.
