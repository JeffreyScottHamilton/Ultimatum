# Patterns: small code shapes that pass the gates

Read before building controls, forms, a rail, a reveal, figures or any loop.  Borrow the shape, not the names or the copy. The button, choice, loop and skip-link blocks were exercised in Chromium through Playwright, and the rest loaded without errors; the coverage file lists what was asserted. Custom properties such as `--ink` stand for tokens in your own `:root` block (`craft-type-colour.md`).

## Button with all eight states

```css
.action {
  display: inline-flex; gap: var(--s-1); align-items: center; justify-content: center;
  padding-inline: var(--s-4); min-height: 48px;
  font: 500 1rem/1 var(--body); cursor: pointer; white-space: nowrap; text-decoration: none;
  color: var(--paper); background: var(--ink);
  border: 1px solid var(--ink); border-radius: var(--r-control);
  transition: background-color var(--t-short) var(--ease), translate var(--t-micro) var(--ease);
}
.action:hover { background: var(--ink-soft); }
.action:active { translate: 0 1px; }
.action:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; transition: none; }
.action:disabled, .action[aria-disabled="true"] { opacity: .55; cursor: not-allowed; translate: none; }
.action[aria-busy="true"] { cursor: progress; }
.action.quiet { color: var(--ink); background: none; border-color: var(--hair); }
@media (prefers-reduced-motion: reduce) { .action { transition: none; } }
```

A page gets one filled primary. Errors and success belong to the form, not the button.

## Photo in a slot, with a factual caption

```html
<figure class="shot" data-slot="hero" data-alt="Rows of trees in autumn light">
  <img src="orchard-1280.jpg" srcset="orchard-960.jpg 960w, orchard-1280.jpg 1280w" sizes="(min-width: 60rem) 45vw, 100vw"
       width="1280" height="1600" alt="Rows of apple trees in autumn light" fetchpriority="high">
  <figcaption>Picking runs from September until the first frost.</figcaption>
</figure>
```

```css
.shot { margin: 0; }
.shot img {
  width: 100%; height: auto; min-height: 440px; aspect-ratio: 4 / 5; object-fit: cover;
  border-radius: var(--r-card);
  outline-offset: -1px; outline: solid 1px color-mix(in oklab, var(--ink) 8%, transparent);
}
.shot figcaption { margin-top: var(--s-2); font-size: .875rem; color: var(--ink-soft); }
```

The caption states a fact from the brief and sits outside the frame; credits go in the footer line.

## A choice among a few (segmented radios)

```html
<fieldset class="choice"><legend>Quantity</legend>
  <input id="box-1" type="radio" name="boxes" checked><label for="box-1">One box</label>
  <input id="box-2" type="radio" name="boxes"><label for="box-2">Two boxes</label>
</fieldset>
```

```css
.choice input { opacity: 0; position: absolute; height: 1px; width: 1px; }
.choice label {
  min-height: 44px; padding-inline: var(--s-3); cursor: pointer;
  display: inline-flex; align-items: center; border: 1px solid var(--hair);
}
.choice input:checked + label { color: var(--paper); background: var(--ink); }
.choice input:focus-visible + label { outline-offset: 2px; outline: 2px solid var(--ring); }
```

Keep the radios in the flow, one pixel square (gate 53); the label shows state and focus ring.

## Rail and switcher

```html
<ul class="strip" aria-label="Coming dates" tabindex="0">
  <li>Whitby, <time datetime="2027-06-12">Sat 12 June</time></li><!-- 5 or more, so the next is clipped by the edge -->
</ul>
```

```css
.strip {
  gap: var(--col-gap); display: grid; grid-auto-columns: minmax(16rem, 22%); grid-auto-flow: column;
  padding-inline: var(--gutter); scroll-padding-inline: var(--gutter);
  overflow-x: auto; overscroll-behavior-x: contain; scroll-snap-type: x mandatory;
}
.strip > * { scroll-snap-align: start; }
.strip:focus-visible { outline: 2px solid var(--ring); outline-offset: 4px; }
```

Scroll snap reference: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll_snap. A switcher is a row of tab buttons over tab panels. Arrow keys move the selection (a few lines flip `aria-selected`, `tabindex` and `hidden`), and with no script every panel stacks open (ARIA pattern: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/). For a pinned pair, put `position: sticky` and a `top` offset on the visual's column and release it below 60rem.

## A fact the brief left out

```html
<p>Doors open at <span class="tbd" data-gap="time">time to be confirmed</span>.</p>
```

```css
.tbd {
  padding-inline: .25em; color: var(--mute); border-radius: 3px;
  box-decoration-break: clone; border: 1px dashed color-mix(in srgb, var(--mute) 70%, transparent);
}
```

At most two per page, each listed in the handoff.

## A form wired to nothing yet

```html
<form data-endpoint="" id="join" novalidate>
  <label for="addr">Email address</label>
  <div class="line">
    <input id="addr" type="email" name="email" required autocomplete="email">
    <button type="submit" class="action">Tell me the date</button>
  </div>
  <p id="note" aria-live="polite"></p>
</form>
<script>
  const form = document.getElementById('join'), field = form.email, note = document.getElementById('note');
  const failed = 'It did not go through. Please try again shortly.';
  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    if (!field.checkValidity()) {
      field.setAttribute('aria-invalid', 'true');
      note.textContent = 'That address looks unfinished. It needs an @ sign and a domain.';
      field.focus(); return;
    }
    field.removeAttribute('aria-invalid');
    if (!form.dataset.endpoint) { note.textContent = 'Not connected yet, so nothing has been sent.'; return; }
    try {
      const res = await fetch(form.dataset.endpoint, { body: new FormData(form), method: 'POST' });
      note.textContent = res.ok ? 'Thanks, it is on its way.' : failed;
    } catch { note.textContent = failed; }
  });
</script>
```

```css
.line { display: flex; gap: var(--s-1); }
.line input {
  min-height: 48px; min-width: 0; flex: 1 1 0; padding-inline: var(--s-3);
  color: var(--ink); background: var(--paper);
  border: 1px solid var(--mute); outline: 2px solid transparent; outline-offset: -3px;
}
.line input:focus-visible { outline-color: var(--ring); }
.line input[aria-invalid] { border-color: var(--bad); }
#note { min-height: 1lh; margin-top: var(--s-half); color: var(--mute); }
```

On a site shipped with a real backend (a Supabase insert or a form service), fill `data-endpoint` and keep all four outcomes: invalid, not connected, sent, failed.

## One reveal that survives no script

Start from the reveal in `craft-motion.md` § A reveal that survives no script, then add an observer that sets the `in` class once per element (https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserver). Stagger with `transition-delay: calc(var(--i, 0) * 40ms)`.

## Figures side by side

```css
.figures { display: grid; grid-template: auto / repeat(3, 1fr); }
.figures > * { padding-inline: var(--s-4); border-left: 1px solid var(--hair); }
.figures > :first-child { padding-left: 0; border: 0; }
.figures b { font: 600 var(--size-3xl)/1 var(--display); font-variant-numeric: tabular-nums; display: block; }
@media (max-width: 60rem) {
  .figures { grid-template-columns: minmax(0, 1fr); }
  .figures > * { border-left: 0; padding: var(--s-3) 0; border-top: 1px solid var(--hair); }
  .figures > :first-child { border-top: 0; }
}
```

Use only figures the owner gave, each with a unit and a note saying what is counted.

## A loop with a pause control

Any motion lasting beyond five seconds (marquee, ambient loop, looping video) must start still, stop when off-screen and under reduced motion, pause while hovered or focused, and offer a visible pause button (WCAG success criterion 2.2.2).

```html
<figure data-motion>
  <div class="ticker">…</div>
  <button type="button" data-motion-toggle class="action quiet">Pause</button>
</figure>
```

```css
@media (prefers-reduced-motion: reduce) { [data-motion-toggle] { visibility: hidden; } }
[data-motion]:not(.running) * { animation-play-state: paused; }
html:not(.js) [data-motion-toggle] { visibility: hidden; }
```

```js
for (const box of document.querySelectorAll('[data-motion]')) {
  const on = { visible: false, hovered: false, paused: matchMedia('(prefers-reduced-motion: reduce)').matches };
  const toggle = box.querySelector('[data-motion-toggle]');
  const refresh = () => {
    box.classList.toggle('running', on.visible && !on.hovered && !on.paused);
    toggle.textContent = on.paused ? 'Play' : 'Pause';
  };
  toggle.onclick = () => { on.paused = !on.paused; refresh(); };
  for (const [type, value] of [['pointerleave', false], ['focusout', false], ['pointerenter', true], ['focusin', true]]) {
    box.addEventListener(type, () => { on.hovered = value; refresh(); });
  }
  new IntersectionObserver((entries) => { on.visible = entries[0].isIntersecting; refresh(); }).observe(box);
}
```

When the loop is a video, call `pause()` or `play()` inside `refresh`.

## Skipping the nav

```html
<a href="#main" class="jump">Skip to content</a>
```

```css
.jump {
  position: absolute; z-index: 600; top: -6rem; left: var(--s-3);
  padding: var(--s-1) var(--s-3); color: var(--paper); background: var(--ink);
}
.jump:focus-visible { top: var(--s-3); }
```
