# Anatomy: workflow from idea to finished figure

Read when you have agreed to build a figure and need the order of work.

## The order

1. **Truth first.** Write the model of the idea as plain code with no drawing in it: state, rules, and the numbers it yields. The figure only shows what this model says. Test the model with a few inputs before any art.
2. **Invent the object.** Pick a physical thing whose parts match the idea one for one. Test: could someone point at a part and say which rule it is? If a part has no rule behind it, it is decoration; keep it only if it makes the object believable.
3. **Parts list.** Write at least 40 named parts, grouped: base, structure, mechanism, controls, subject. The subject (the thing the idea is about) gets the brightest treatment, the base the quietest.
4. **Plan the world.** Use z as up. Default camera: azimuth 45 degrees, elevation 30 degrees. Fit the projection to the card so the object fills about 55 to 65 percent of it. Math and a runnable sketch: `iso-math.md`.
5. **Build geometry once.** Compute each part's polygons one time at load, not per frame. Moving parts transform stored geometry.
6. **Painter's order.** Draw far to near; fix ties by hand with an explicit order list. Wrong depth is the commonest visible fault.
7. **Frame as a card.** Figure number, title, one-line hint, a readout of the true numbers, legend keys for the controls, a caption. See `craft-card.md`.
8. **Make it live** if it should be. See `motion.md`.
9. **Verify like a critic.** Capture, close-ups, line checks, the audit. See `verify.md`.

## Rules for the plan

- Group by what the reader sees, not by what the code needs.
- Pipes, chutes and cables are planned as paths first, then drawn as tubes; see `craft-rules.md` §Pipes.
- One lit accent on the whole figure marks the thing to watch.
- Keep each file or module small enough that you can name its job in one line.

## Local-business and app notes

- A local business figure uses its real steps and numbers, in the language of its customers. No jargon labels on parts.
- An app figure matches the product's real states. Name states as the interface names them, so the figure and the screen agree.
- Alt text and the readout carry the idea for people who cannot see the drawing; write them at plan time, not at the end (`accessibility-and-limits.md`).
