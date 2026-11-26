# Comp before build: compose in pixels, then in CSS

Read only when an image generator is available and the user wants it (or has supplied mock-ups), at the step after the picks block. Otherwise skip; never block on it. Ultimatum's toolbelt has no network, so generation runs through the harness's own image tool, and any key stays in the user's environment, never in files. A comp shows mass, interval and alignment faster than prose.

## What a comp is

| A comp is | A comp is not |
|---|---|
| a layout proposal covering weight, spacing, alignment and the spot the eye reaches first | a design system; palette and type were fixed earlier in the picks block |
| the first viewport only, at its real size | a full page |
| a target to measure the build against | a texture or asset; nothing from it ships or is committed |

A comp cannot override the floor. Generators return eyebrows, violet gradients, glass cards and fake browser frames. Borrow the composition only; "it was in the comp" never justifies a waiver.

## The call

Two comps (three if the direction truly forks). Build the prompt from the picks block, not the user's prompt: the first viewport as planned, the idea in plain words, ground and accent as plain colours, the display class (not a face name), the page shape as a compositional instruction, then one clause naming what the category usually does and must not appear. Example prompt: a hero, first 1280x800 only, for a rowing club whose season is a single race timetable with the next race largest; pale ground, deep green ink, one yellow mark; heavy grotesk headline set left across five columns and the timetable across seven; flat and printed; avoid centring, cards, gradients and device frames.

Change only one axis between comps (the composition) and keep the system fixed.

## Approval

Lay both next to each other, add a line on what differs, and ask for a pick or a rejection. Building starts only after a pick. On rejection, shift the axis and generate again once; after two rounds, build with no comp and say that.

## Reproduction check

A model reliably believes its recreation matched when it did not. So:

1. Screenshot the build at exactly the comp's size (1280x800).
2. Put them side by side and answer, one line each: Mass (same place, same size?), Interval (same proportions between major elements?), Entry (same first thing seen?).
3. State the biggest difference and fix it, or explain why the build is better. Saying nothing is not an option.

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 800})
    pg.goto("file:///abs/path/index.html"); pg.screenshot(path="build-1280x800.png"); b.close()
```

Stamp it, for example `comp: two made, first chosen, matched at 1280x800`, or `comp: skipped`.

## Medium inventory

Before coding, write one line per region of the approved comp naming how it will be made:

| Medium | Right for |
|---|---|
| code (CSS, SVG) | rules, type, geometry, diagrams, anything that reacts or must reflow |
| raster (supplied or generated) | material, grain, cloth, paper, photography, painted surfaces |
| neither | a region the comp invented that the copy does not support; cut it now |

A CSS gradient does not stand in for a texture. Raster regions need a real source (the user's asset, a licensed library photo or a generated still); a region drawn as a photograph in the comp is never swapped for line art. Switching a region's medium mid-build must be announced.

## Generated stills

Only when the user asked for generated images or the subject is out of the library's reach. Prompt like a photographer: one concrete subject, place, light and lens, "no text, no people facing the camera". Inspect every result for extra fingers, doubled furniture, melted labels. Stamp `generated: <model>`. Never auto-fire. For a local business, generated stills must not pose as its real premises, staff or work; use the owner's photos.
