# Redesign and audit

Read when the user asks to redesign, restyle, polish or audit an existing site or app screen. A small edit to existing work is done as asked inside the project's own system and does not need this file. Source is the user's own code (a file, folder or dev-server route); a live URL with no source can only be audited.

## What a redesign keeps

- **Content.** Every fact, claim, name, price, date and quote. Carry figures, quotes and logos over as found and list them for the owner to verify, including any a gate doubts. Add nothing the page lacked, beyond what the user supplies and what a gate requires (a pause on a loop, a focus ring). A drawing made from the page's own facts is composition and allowed.
- **Wiring.** Links, forms, fields, handlers, routes, ids, test hooks, scripts, data and analytics calls. Edit markup inside its component; never move logic, rename a prop, or drop a `name`, `id`, `key`, `type`, `href` or `data-testid`. A state the screen has no logic for (failed load, undo) is listed for the owner, never built. For Stripe or Supabase screens, keep every price id, redirect and policy untouched.
- **Files.** No file deleted, route removed or component tree replaced without a file-level plan the user approved; no test edited to pass. Start from a clean git tree (ask the user to commit or stash; do not do it for them) so the work is one revertable diff.
- **Brand.** A logo, colour or face the project names, or the user states, stays at every depth, read from files not memory. A framework default or a look the gates name (purple-to-blue, stock indigo, Inter as display) is not a brand; replace it and say so.
- **Words,** unless a copy gate names them. Tighten failing lines from facts already on the page and list every change before and after. An eyebrow is never just deleted: where its heading is figurative, the plain label becomes the heading. Never reword terms, disclaimers or consent text. "Keep every word" turns copy gates into notes.

## Depth

| Depth | Stays | Changes | Only when asked with |
|---|---|---|---|
| full | content, wiring | system and composition | the verb itself |
| restyle | layout | colour, type, radius, shadow, motion, controls | "keep the layout", "reskin" |
| polish | system and layout | only what a gate names: tells, contrast, states, motion, tokens | "polish", "keep our look" |

Depths never blend. A polish that finds the concept wrong says so and recommends the full run. On an app screen, full depth recomposes inside the shell it has: what leads, how figures, tables and forms sit. "From scratch" is a build, not a depth.

## Before

1. Pre-flight, then list pages (route, file, page or app screen). In a framework project run the dev server and screenshot the routes; the bare shell HTML on disk is not the page. An unstamped page has no genre; infer it and say so.
2. Record the page as it stands: screenshots at the standard widths plus an inventory of every link, form, field, handler, test hook, script, heading and figure. Playwright does both (example below). Ultimatum's own checks: `ult` and the website audit in `../../website/guide.md`.
3. Look at the screenshots before weighing findings. Give a four-line read: what the page is for (audience, one action); what works and stays (at least one thing); what reads as generated (worst tells by gate); what is broken.

**Audit** stops here: walk the judged gates from the screenshots, report findings by tier with `file:line`, the read, the lightest depth that settles them, and what only a deeper one would. Change no files.

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
      links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')),
      fields: [...document.querySelectorAll('input,select,textarea')].map(f => f.name || f.id),
      forms: document.forms.length,
      headings: [...document.querySelectorAll('h1,h2,h3')].map(h => h.textContent.trim()),
      hooks: [...document.querySelectorAll('[data-testid]')].map(e => e.dataset.testid) })""")
    json.dump(inv, open(f"{out}/before.json", "w"), indent=1); b.close()
```

## The ask

One message replaces the first-pass ask (skip if answered): what must stay (say "keep the layout" for restyle), what is wrong in the user's words and the feeling wanted, and anything new to show (photos, numbers, a quote). Or "go ahead" for a full redesign.

## The plan

The picks block opens with four rows and nothing is deleted before the user sees Files:

```markdown
- **Redesign**: full, 3 pages (/, /pricing, /docs)
- **Before**: floor 14 failing, reflex 9; centred template in stock indigo; pricing table clear, stays
- **Keeps**: every link, field, handler; the green and brand face; the pricing table
- **Files**: edit app/page.tsx, app/globals.css; create app/tokens.css; delete none
```

Then the build rows the depth reaches: theme at restyle and full; shape, hero, signature and sections at full only. At polish the block stops after Files.

## Build

- **Polish:** run the sweep on the user's page: fix in place, single elements and tokens, never restructure; stamp `built: the project, redesign: polish`. Load gates, patterns, and the states file when there is a form.
- **Layout-bound gates** (hero, section rhythm, screen budget, spacing scale) report as notes at polish and restyle; the screen budget is a note at every depth because the words are the owner's.
- **Restyle and full:** write the token and base files beside the project's stylesheet, then shared components and chrome, then pages (most visited first), each swept before the next. Tailwind and shadcn names are in `design-file.md`.
- **More than one page:** lock the system once (`design-file.md`); pages share theme, type and accent and differ only in shape. Past three pages, give each to its own subagent, with the design file and this file.
- **Full depth** runs the hero stage and hero review; polish and restyle skip them. A kept section order in a new composition is waived on the record.

## After

1. Re-run the inventory against the before record. Anything missing is a failure (link, form, field, handler, hook, script) or a warning (heading, figure, image, id). Restore it or write it in the stamp with a reason, for example `dropped /blog, #team: the user is retiring them`, or `reworded "X" to "Y": gate 19 names the opener`. Offer a side-by-side before/after page.
2. Run the project's own checks (types, build, tests). A redesign that breaks one is not finished.
3. The finish review also sees the before screenshots and answers what the old page did better. A plain defect is fixed at any depth; a new composition joins layout findings; missing content goes to the owner.
4. Log `mode: redesign`, depth and scope (page, site, app).
5. Handoff, ahead of other asks:

```
Redesign: full, 3 pages
Before   floor 14 failing, reflex 9
After    floor 0, reflex 1 waived
Kept     14/14 links, 5/5 fields, 9/9 handlers, 11/11 headings
Changed  system and composition
Dropped  none
Yours    2 claims kept as found, 4 lines reworded (listed)
```
