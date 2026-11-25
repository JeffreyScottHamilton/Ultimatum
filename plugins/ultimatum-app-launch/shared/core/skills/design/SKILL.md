---
name: design
description: Shared Design instructions (layout, colour, type) for the Designer role; used by Website when a site needs a new look.
disable-model-invocation: true
---

# Design

For the Designer, used only when the brief needs a new look. Refs: `${CLAUDE_PLUGIN_ROOT}/skills/work/references/` (read only the sections named).

1. **See what exists** (`ui.md` §1): current tokens, fonts, components and brand assets. Keep what the user wants kept.
2. **Direction card** (`ui.md` §3): purpose and audience, one clear visual idea, layout (grid, spacing scale), colour roles (background, surface, text, accent, states; text contrast at least 4.5:1), type (at most two families, one scale), motion stance.
3. **Skip generic defaults** (`ui.md` §6) unless the brief earns them.
4. **Write it as tokens** (CSS variables or the Tailwind theme) in the brief's Design section, so the Builder can use them directly.
5. **Check once it renders:** the craft floor (`ui.md` §4) and one bounded critique pass (`ui.md` §9). Use `design/design.md`, `design/motion.md` or `design/components.md` only when a choice needs them.

Hand back at most 10 lines: the direction in one sentence, the tokens added, and anything left open.
