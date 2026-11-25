# Website guide (use with Coding)

- **Structure:** landmarks (header, nav, main, footer), one `h1`, headings in order, real links for navigation and buttons for actions.
- **Mobile first:** works at 375 px with no sideways scrolling; check 768 px and 1280 px too. Tap targets at least 44 px in new or redesigned parts; on a small fix, report short ones instead of resizing them.
- **Keyboard:** every action works with Tab, Enter and Space; focus is visible; Escape closes overlays and focus returns. Use the project's accessible primitives (or Radix) for dialogs, menus and tabs instead of hand-built ones.
- **Components:** reuse the project's own first. With shadcn/ui, add pieces the way the project already does; don't paste a second copy.
- **Styles:** use the project's tokens (CSS variables, Tailwind theme). New values go into the tokens, not inline.
- **Content and media:** copy from the brief; meaningful images get alt text, decoration gets `alt=""`; images have width and height and lazy-load below the fold.
- **Motion:** respect `prefers-reduced-motion`; details in `references/design/motion.md`.
- **Forms:** visible labels, errors tied to their fields, server-side validation kept.
- **Speed:** no layout shift on load, font fallbacks, no large unused bundles.
- **Done** when it builds and the brief's checks pass in a real browser (Review runs them).
