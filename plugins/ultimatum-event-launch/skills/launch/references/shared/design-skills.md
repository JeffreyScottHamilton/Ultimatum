# Design skills and Claude Design

For the Website and Motion Graphics teams. `ult website` and `ult motion` print a `design-skill:` line on visual jobs.

## An installed design skill

- **Found** (for example Anthropic's `frontend-design` for pages, or a renderer's own skill such as Remotion's for clips): read its SKILL.md before the three directions (or the storyboard) and again before the build. Use it for look, type, layout, motion and craft.
- **Where it conflicts with these guides:** the approval stops, the taste critic, the browser and media checks, licences and the user's brand file still win. The skill shapes the work; it never skips a gate.
- **None installed:** use the built-in design guide (core `design/SKILL.md`, `../website/craft.md`, `../website/design-rules.md`). Don't install anything. Mention once, at the end, that the user can add Anthropic's `frontend-design` plugin from the official marketplace.

## A design from Claude Design

If the user brings work from Claude Design (an exported page, a prototype link, a handoff bundle or a design system):

1. Treat it as a direction the user already likes, not as approved code. Save what they gave you under `design/` and note its source in the brief.
2. Take its colours, type, spacing and components as the brand's tokens; if `brand/brand.md` is missing, write it from them.
3. Screenshot it at 375, 768 and 1440 px and run the taste critic on it like any direction. Show the findings; the user still approves before production code.
4. Build from it with the coding guide. Rebuild in the project's stack rather than pasting an export whole, and keep its look.
5. Compare the build with the design in the browser check. Differences that are not on purpose are findings.

Claude Design is an Anthropic product the user runs; Ultimatum can't open their account. Ask them to export or share the design. **Check before relying** on its export formats, which change.
