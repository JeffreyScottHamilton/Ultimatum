# Interaction kit: index

Read when a page or app needs a moving or tactile part (a press, copy, tab, toast, sheet, palette, counter, reveal or drag), or when you review someone's animated components. One line per file with the question it answers. The code is in `../../../../../data/craft/interaction-kit/` (see its README).

Written in our own words from the ideas in Watermelon UI (WatermelonCorp/watermelon-platform, MIT). None of its code or text is copied. Motion timing and springs in depth are in `../emil-motion/index.md`; this set is about ready parts and the details that make them feel finished.

- `choosing.md`: which part fits this moment, and when should I use ours, install theirs, or build nothing?
- `components.md`: what does each kit component do, what does it take, and how does it work with a keyboard and reduced motion?
- `details.md`: which small details separate a polished part from a cheap one, and what does `ult kitlint` check?

Quick path: pick in `choosing.md`, copy the files from the kit, run `ult kitlint` on them, then render the page once with reduced motion on and once in dark mode.
