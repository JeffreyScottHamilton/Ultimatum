# Patterns: small code shapes that pass the gates

Read once before building controls, forms, a rail, a reveal, stats or any loop. Take the shape, never the names or copy. Each block was run in Chromium with Playwright against a scratch page (see the coverage file for what was asserted). Tokens such as `--color-ink` come from your own `:root` block (`craft-type-colour.md`).

## Button with all eight states

```css
.btn { display: inline-flex; align-items: center; justify-content: center; gap: var(--space-xs);
  min-height: 48px; padding-inline: var(--space-lg); border: 1px solid var(--color-ink); border-radius: var(--radius-control);
  background: var(--color-ink); color: var(--color-paper); font: 500 1rem/1 var(--font-body); white-space: nowrap; text-decoration: none; cursor: pointer;
  transition: background-color var(--dur-short) var(--ease-out), transform var(--dur-micro) var(--ease-out); }
.btn:hover { background: var(--color-ink-2); }
.btn:active { transform: translateY(1px); }
.btn:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; transition: none; }
.btn:disabled, .btn[aria-disabled="true"] { opacity: .55; cursor: not-allowed; transform: none; }
.btn[aria-busy="true"] { cursor: progress; }
.btn.quiet { background: transparent; color: var(--color-ink); border-color: var(--color-rule); }
@media (prefers-reduced-motion: reduce) { .btn { transition: none; } }
```

One filled primary per page. Error and success belong to the form, not the button.

## Photo in a slot, with a fact caption

```html
<figure class="photo" data-slot="hero" data-alt="Rows of trees in October light">
  <img src="orchard-1280.jpg" srcset="orchard-960.jpg 960w, orchard-1280.jpg 1280w" sizes="(min-width: 60rem) 45vw, 100vw"
       width="1280" height="1600" alt="Rows of apple trees in October light" fetchpriority="high">
  <figcaption>Picking runs from September to the first frost.</figcaption>
</figure>
```

```css
.photo { margin: 0; }
.photo img { aspect-ratio: 4/5; width: 100%; height: auto; min-height: 440px; object-fit: cover; border-radius: var(--radius-card);
  outline: 1px solid color-mix(in oklab, var(--color-ink) 8%, transparent); outline-offset: -1px; }
.photo figcaption { margin-top: var(--space-sm); font-size: .875rem; color: var(--color-ink-2); }
```

The caption is a fact from the prompt, outside the frame; the credit goes in the footer line.

## A choice among a few (segmented radios)

```html
<fieldset class="seg"><legend>Size</legend>
  <input type="radio" name="size" id="s1" checked><label for="s1">One box</label>
  <input type="radio" name="size" id="s2"><label for="s2">Two boxes</label>
</fieldset>
```

```css
.seg input { position: absolute; width: 1px; height: 1px; opacity: 0; }
.seg label { display: inline-flex; align-items: center; min-height: 44px; padding-inline: var(--space-md); border: 1px solid var(--color-rule); cursor: pointer; }
.seg input:checked + label { background: var(--color-ink); color: var(--color-paper); }
.seg input:focus-visible + label { outline: 2px solid var(--color-focus); outline-offset: 2px; }
```

The radios stay in the flow at one pixel (gate 53), the label carries state and ring.

## Rail and switcher

```html
<ul class="rail" tabindex="0" aria-label="Upcoming dates">
  <li><time datetime="2027-06-12">12 June</time> Whitby</li><!-- five or more; the next is cut by the edge -->
</ul>
```

```css
.rail { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(16rem, 22%); gap: var(--gap-columns);
  overflow-x: auto; scroll-snap-type: x mandatory; scroll-padding-inline: var(--gutter); padding-inline: var(--gutter); overscroll-behavior-x: contain; }
.rail > * { scroll-snap-align: start; }
.rail:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 4px; }
```

Scroll snap reference: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll_snap. A switcher is a tablist of buttons plus tabpanels; arrow keys move the selection (a few lines set `aria-selected`, `tabindex` and `hidden`), and without script every panel shows in order (ARIA pattern: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/). A pinned pair is `position: sticky; top: var(--space-2xl)` on the visual's column, released under 60rem.

## A fact the prompt did not give

```html
<p>Doors at <span class="fill" data-fill="time">time to be announced</span>.</p>
```

```css
.fill { padding-inline: .25em; border: 1px dashed color-mix(in oklch, var(--color-muted) 70%, transparent); border-radius: 3px; color: var(--color-muted); box-decoration-break: clone; }
```

Two per page at most, each named in the handoff.

## A form that posts nowhere yet

```html
<form id="signup" data-endpoint="" novalidate>
  <label for="email">Email address</label>
  <div class="row"><input id="email" name="email" type="email" autocomplete="email" required>
  <button class="btn" type="submit">Send me the date</button></div>
  <p id="help" aria-live="polite"></p>
</form>
<script>
  const form = document.getElementById('signup'), input = form.email, help = document.getElementById('help');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!input.checkValidity()) { input.setAttribute('aria-invalid', 'true'); help.textContent = 'That address looks incomplete. Write it with an at sign and a domain.'; input.focus(); return; }
    input.removeAttribute('aria-invalid');
    if (!form.dataset.endpoint) { help.textContent = 'Nothing was sent: this form is not connected yet.'; return; }
    try {
      const r = await fetch(form.dataset.endpoint, { method: 'POST', body: new FormData(form) });
      help.textContent = r.ok ? 'Thanks, it is on its way.' : 'That did not go through. Try again in a minute.';
    } catch { help.textContent = 'That did not go through. Try again in a minute.'; }
  });
</script>
```

```css
.row { display: flex; gap: var(--space-xs); }
.row input { flex: 1; min-width: 0; min-height: 48px; padding-inline: var(--space-md); border: 1px solid var(--color-muted); outline: 2px solid transparent; outline-offset: -3px; background: var(--color-paper); color: var(--color-ink); }
.row input:focus-visible { outline-color: var(--color-focus); }
.row input[aria-invalid] { border-color: var(--color-error); }
#help { min-height: 1lh; margin-top: var(--space-2xs); color: var(--color-muted); }
```

For a site we ship with a real backend (a Supabase insert or a form service), fill `data-endpoint` and keep the same four outcomes: invalid, not connected, sent, failed.

## One reveal that survives no script

Use the pattern in `craft-motion.md` § A reveal that survives no script, plus an observer that adds the `in` class once per element (https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserver). Stagger by setting `transition-delay: calc(var(--i, 0) * 40ms)`.

## Figures that compare

```css
.stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); }
.stats > * { padding-inline: var(--space-lg); border-left: 1px solid var(--color-rule); }
.stats > :first-child { padding-left: 0; border-left: 0; }
.stats b { display: block; font: 600 var(--text-3xl)/1 var(--font-display); font-variant-numeric: tabular-nums; }
@media (max-width: 60rem) { .stats { grid-template-columns: minmax(0, 1fr); }
  .stats > * { padding: var(--space-md) 0; border-left: 0; border-top: 1px solid var(--color-rule); } .stats > :first-child { border-top: 0; } }
```

Only figures the user gave, each with unit and what it counts.

## A loop that can pause

Anything moving for over five seconds (marquee, ambient loop, looping video) holds still until script runs, stops off-screen and under reduced motion, pauses on hover and focus, and has a visible pause button (WCAG 2.2.2).

```html
<figure data-loop><div class="marquee">…</div><button class="btn quiet" type="button" data-loop-toggle>Pause</button></figure>
```

```css
[data-loop]:not(.running) * { animation-play-state: paused !important; }
html:not(.js) [data-loop-toggle] { display: none; }
@media (prefers-reduced-motion: reduce) { [data-loop-toggle] { display: none; } }
```

```js
document.querySelectorAll('[data-loop]').forEach((el) => {
  const s = { seen: false, over: false, held: matchMedia('(prefers-reduced-motion: reduce)').matches };
  const btn = el.querySelector('[data-loop-toggle]');
  const sync = () => { el.classList.toggle('running', s.seen && !s.over && !s.held); btn.textContent = s.held ? 'Play' : 'Pause'; };
  btn.onclick = () => { s.held = !s.held; sync(); };
  for (const [ev, v] of [['pointerenter', true], ['focusin', true], ['pointerleave', false], ['focusout', false]]) el.addEventListener(ev, () => { s.over = v; sync(); });
  new IntersectionObserver(([e]) => { s.seen = e.isIntersecting; sync(); }).observe(el);
});
```

For looping video also call `pause()` and `play()` in `sync`.

## A way past the nav

```html
<a class="skip" href="#main">Skip to content</a>
```

```css
.skip { position: absolute; left: var(--space-md); top: -6rem; z-index: 600; padding: var(--space-xs) var(--space-md); background: var(--color-ink); color: var(--color-paper); }
.skip:focus-visible { top: var(--space-md); }
```
