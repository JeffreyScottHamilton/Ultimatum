# Redesign and audit

Read when the user asks to redesign, restyle, polish or audit an existing site or app screen. A small edit to existing work is done as asked inside the project's own system and does not need this file. Source is the user's own code (a file, folder or dev-server route); a live URL with no source can only be audited.

## What a redesign keeps

- **Content.** All facts, claims, names, prices, dates and quotes. Bring figures, quotes and logos across exactly as found and list them for the owner to verify, including any a gate questions. Add nothing the page lacked apart from what the owner supplies and what a gate demands (a pause control on a loop, a focus ring). A drawing assembled from the page's own facts counts as composition and is allowed.
- **Wiring.** Links, forms, fields, handlers, routes, ids, test hooks, scripts, data and analytics calls. Change markup within its component; never shift logic, rename a prop, or lose a `name`, `id`, `key`, `type`, `href` or `data-testid`. If the screen lacks logic for a state (failed load, undo), list it for the owner and do not build it. On Stripe or Supabase screens leave every price id, redirect and policy alone.
- **Files.** Do not delete a file, remove a route or swap a component tree unless the owner approved a file-level plan, and never edit a test to make it pass. Start from a clean git tree (ask the owner to commit or stash, and do not do it for them) so the work lands as a single diff that can be reverted.
- **Brand.** Keep any logo, colour or typeface that the project or the owner names, at every depth, reading it from the files and not from memory. Framework defaults and looks the gates name (purple-to-blue, stock indigo, Inter as display) are not brand: replace them and say so.
- **Words**, unless a copy gate covers them. Shorten failing lines using facts already on the page, and list each change as before and after. Never simply delete an eyebrow: if its heading is figurative, the plain label takes over as the heading. Do not reword terms, disclaimers or consent text. If the owner says "keep every word", copy gates become notes.

## Depth

| Depth | Stays | Changes | Only when asked with |
|---|---|---|---|
| full | content, wiring | system and composition | the verb itself |
| restyle | layout | colour, type, radius, shadow, motion, controls | "keep the layout", "reskin" |
| polish | system and layout | only items named by a gate (tells, contrast, states, motion, tokens) | the words "polish" or "keep our look" |

Depths do not mix. If a polish pass finds the concept itself wrong, it says so and recommends the full run. On an app screen, full depth recomposes within the shell already present (what leads, how figures, tables and forms are arranged). Starting "from scratch" is a new build, not a depth.

## Before

1. Pre-flight, then list the pages (route, file, page or app screen). In a framework project, run the dev server and screenshot the routes, because the bare shell HTML on disk is not the page. An unstamped page has no recorded genre, so infer one and say so.
2. Capture the page as it is now: screenshots at the standard widths plus an inventory of every link, form, field, handler, test hook, script, heading and figure. Playwright does both (example below). Ultimatum's own checks: `ult` and the website audit in `../../website/guide.md`.
3. Look at the screenshots before weighing findings, and give a four-line read: what the page is for (audience, one action); what is working and stays (at least one item); what reads as generated (the worst tells, ordered by gate); what is broken.

**Audit** ends here. Walk the judged gates from the screenshots and report findings by tier with `file:line`, then the read, the lightest depth that would fix them and what only a deeper depth would. Change no files.

```python
# before.py: record screenshots and a wiring inventory with Playwright (Python)
import json, sys
from playwright.sync_api import sync_playwright
url, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for w in (375, 768, 1440):
        pg.set_viewport_size({"width": w, "height": 900}); pg.goto(url)
        pg.screenshot(path=f"{out}/before-{w}.png", full_page=True)
    inv = pg.evaluate("""() => ({
      links: Array.from(document.querySelectorAll('a[href]'), a => a.getAttribute('href')),
      fields: [...document.querySelectorAll('input,select,textarea')].map(f => f.name || f.id),
      forms: document.forms.length,
      headings: Array.from(document.querySelectorAll('h1,h2,h3'), h => h.textContent.trim()),
      hooks: [...document.querySelectorAll('[data-testid]')].map(e => e.dataset.testid) })""")
    json.dump(inv, open(f"{out}/before.json", "w"), indent=1); b.close()
```

## The ask

One message replaces the first-pass ask (skip if answered): what must stay (say "keep the layout" for restyle), what is wrong in the user's words and the feeling wanted, and anything new to show (photos, numbers, a quote). Or "go ahead" for a full redesign.

## The plan

Open the picks block with four rows. Nothing is removed before the owner has read the Files row:

```markdown
- **Redesign**: full depth, 3 pages (/, /pricing, /docs)
- **Before**: 14 floor failures and 9 reflex failures; centred template in stock indigo; pricing table clear, keep it
- **Keeps**: links, fields, handlers; brand green; brand face; the pricing table
- **Files**: edits to app/page.tsx and app/globals.css; new app/tokens.css; nothing deleted
```

After those come the build rows that the depth reaches: theme for restyle and full; shape, hero, signature and sections for full only. A polish block ends at Files.

## Build

- **Polish:** sweep the owner's page, repairing single elements and tokens in place without restructuring; stamp `built: the project, redesign: polish`. Load gates and patterns, and the states file when a form is present.
- **Layout-bound gates** (hero, section rhythm, screen budget, spacing scale) report as notes at polish and restyle; the screen budget is a note at every depth because the words are the owner's.
- **Restyle and full:** write the token and base files next to the project's stylesheet, then shared components and chrome, then pages starting with the most visited, sweeping each page before starting the next. Tailwind and shadcn naming is in `design-file.md`.
- **Several pages:** fix the system once (`design-file.md`). Theme, type and accent are shared across pages; only the shape differs. Beyond three pages, hand each to its own subagent along with the design file and this file.
- **Full depth** includes the hero stage and hero review, which polish and restyle skip. If the old section order survives inside a new composition, record a waiver.

## After

1. Re-run the inventory against the before record. Anything missing is a failure (link, form, field, handler, hook, script) or a warning (heading, figure, image, id). Restore it or write it in the stamp with a reason, for example `dropped /blog, #team: the user is retiring them`, or `reworded "X" to "Y": gate 19 names the opener`. Offer a side-by-side before/after page.
2. Run the project's own checks (types, build, tests). A redesign that breaks one is unfinished.
3. The finish review also receives the before screenshots and says what the old page did better. Fix a plain defect at any depth; fold a new composition into the layout findings; send missing content back to the owner.
4. Log `mode: redesign`, depth and scope (page, site, app).
5. Handoff, ahead of other asks:

```
Redesign: full, 3 pages
Before   14 floor failures, 9 reflex
After    0 floor, 1 reflex waived
Kept     links 14/14, fields 5/5, handlers 9/9, headings 11/11
Changed  system and composition
Dropped  nothing
Yours    2 claims kept as found, 4 lines reworded (listed)
```
