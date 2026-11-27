# Feel bar

A launch site should feel alive and still respect people who turn motion off. Check each item before the site goes to review. The approved direction's motion personality sets the timing.

## What the site has

- **Smooth scroll:** Lenis (pinned version), synced with GSAP ScrollTrigger when both are used. Native scrolling stays for keyboard, anchor links and reduced motion.
- **Scroll reveals:** content enters as it comes into view, with a different move for each kind of content (type, images, numbers). Not one fade-up everywhere.
- **Micro-interactions:** hover, focus, press and success states on every button, link and form field. Visible focus rings, taps of 44 px or more. No `transition: all`.
- **A motion hero:** the first screen moves within the first second: animated type, a product loop, layered parallax, or a short video. It never blocks the first action.
- **Page transitions:** between pages, a short transition in the direction's personality (View Transitions API where supported, a GSAP fallback otherwise).
- **Reduced motion:** with `prefers-reduced-motion: reduce`, smooth scroll is off, reveals show instantly, loops pause, and nothing parallaxes. Check that the page itself calms down: JS or WebGL animation can ignore the CSS media query.

The page kind's effect cap (`design-rules.md`) comes first: a trust page keeps only calm micro-interactions and a gentle reveal, and skips smooth scroll, pinned scenes and page transitions. Use GSAP only for what this list calls for (scroll reveals, pinned scenes, sequenced hero); plain CSS handles hover, focus and simple fades.

GSAP is free for commercial sites, plugins included. If the product being built is itself a visual no-code site or animation builder, flag GSAP's licence before using it.

## How to check it

1. **Long animation frames.** In Chrome or Edge, scroll the page in steps and collect `long-animation-frame` entries with a `PerformanceObserver`. Any frame over 50 ms during scroll is a finding; over 100 ms is a blocker. Other browsers do not report these; say so if you could not run it.
2. **Reduced motion.** Re-run with reduced motion emulated (Playwright `reducedMotion: 'reduce'`) and confirm the list above.
3. **Scroll-through recording.** Where Playwright is installed, record a video of a slow scroll from top to bottom at 1440 and 375 px (`recordVideo` on the browser context). Give the user the file. Do not judge frame rate from the video in a headless run; trust the in-page timing.
4. **Effect cap.** At most one heavy effect (WebGL, video background, pinned scene) per screen, and WebGL only when the brand is tech, software or games.

No Playwright or no Chromium → run what you can with `ult-browser.mjs`, and list the checks you could not run.
