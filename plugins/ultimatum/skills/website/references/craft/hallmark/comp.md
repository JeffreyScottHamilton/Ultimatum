# Comp before build: compose in pixels, then in CSS

Read only when an image generator is available and the user wants it (or has supplied mock-ups), at the step after the picks block. Otherwise skip; never block on it. Ultimatum's toolbelt has no network, so generation runs through the harness's own image tool, and any key stays in the user's environment, never in files. A comp shows mass, interval and alignment faster than prose.

## What a comp is

| It is | It is not |
|---|---|
| a composition proposal: mass, interval, alignment, where the eye lands first | a design system; palette and type were set in the picks block |
| the first viewport only, at its real size | a full page |
| a target to measure the build against | a texture or asset; nothing from it ships or is committed |

The comp has no vote on the floor. Generators hand back eyebrows, violet gradients, glass cards and fake browser frames. Take the composition, not the compliance; "the comp had it" is never a waiver reason.

## The call

Two comps (three if the direction truly forks). Build the prompt from the picks block, not the user's prompt: the first viewport as planned, the idea in plain words, ground and accent as plain colours, the display class (not a face name), the page shape as a compositional instruction, then one clause naming what the category usually does and must not appear. Example: "Web page hero, top 1280x800 only. A rowing club's season as one race timetable, the next race the largest line. White ground, deep green ink, one signal-yellow mark. Heavy grotesk headline flush left over five columns; timetable across seven. Flat, printed. Not centred, no cards, no gradient, no device mockup."

Vary the comps on one axis only (composition), holding the system fixed.

## Approval

Show both side by side with one line on how they differ and ask which, or neither. Do not build past an unchosen comp. If neither, change the axis and re-call once; two rounds is the limit, then build without a comp and say so.

## Reproduction check

A model reliably believes its recreation matched when it did not. So:

1. Screenshot the build at exactly the comp's size (1280x800).
2. Put them side by side and answer, one line each: Mass (same place, same size?), Interval (same proportions between major elements?), Entry (same first thing seen?).
3. Name the largest divergence and fix it, or say why the build is right. Silence is not allowed.

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 800})
    pg.goto("file:///abs/path/index.html"); pg.screenshot(path="build-1280x800.png"); b.close()
```

Stamp: `comp: 2 rendered, c1 approved, reproduced (checked at 1280x800)` or `comp: skipped`.

## Medium inventory

Before coding, write one line per region of the approved comp naming how it will be made:

| Medium | Right for |
|---|---|
| code (CSS, SVG) | rules, type, geometry, diagrams, anything that reacts or must reflow |
| raster (supplied or generated) | material, grain, cloth, paper, photography, painted surfaces |
| neither | a region the comp invented that the copy does not support; cut it now |

A CSS gradient is not a texture. A raster region needs a real source (user asset, library photo, or generated still), never a photo from memory, and a region painted as a picture never becomes a drawing. No silent medium changes mid-build.

## Generated stills

Only when the user asked for generated images or the subject is out of the library's reach. Prompt like a photographer: one concrete subject, place, light and lens, "no text, no people facing the camera". Inspect every result for extra fingers, doubled furniture, melted labels. Stamp `generated: <model>`. Never auto-fire. For a local business, generated stills must not pose as its real premises, staff or work; use the owner's photos.
