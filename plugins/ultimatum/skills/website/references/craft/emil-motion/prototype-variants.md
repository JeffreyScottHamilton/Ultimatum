# Prototype variants behind a picker

Read when the user asks to see several different versions of one piece of UI (a toast, a pricing card, a booking button, a hero) and pick one live. Works as a standalone HTML file or an isolated dev route. It sits beside the page-level directions in `../../website/directions.md`: that file picks a look for a whole site; this one explores one component.

## Posture

The value is divergence. Three tints of one idea teach nothing. Each variant is a direction you could ship alone, and each still meets the motion bar (`gate.md`, `easing-and-duration.md`, `performance.md`, `reduced-motion.md`). A sloppy variant loses on execution, not on idea.

## Rules

1. Production code stays untouched while exploring. Work on a separate surface and bring in only the winner, later.
2. Each variant differs along a stated axis (layout, density, personality, motion or interaction model). If one phrase cannot name the axis, the variant is a duplicate. Sharing the project's tokens is not convergence.
3. Every variant is complete: live interactions, live motion, copy that sounds like the product, believable figures. No lorem ipsum, no dead buttons. For local-business work use real-sounding service names and prices, not placeholders.
4. The picker is scaffolding rather than a candidate. Keep it plain and identical across projects.
5. After the choice, delete the prototype surface unless asked to keep it.

## Phases

1. Scope one thing. If asked for "the dashboard", pick the highest-leverage piece, say why, offer the rest as later runs. Restate the brief in a sentence.
2. Recon: stack and styling system, tokens (colour, radius, spacing, type, easing), personality (playful consumer or crisp tool), and context (background, neighbours, sizes). No project: neutral grey, one accent, system font.
3. Choose directions: default three, five at most. Name them for the direction ("Quiet", "Editorial", "Dense"), never "A, B, C". Two that differ only in accent colour or copy are one direction; replace one.
4. Build the harness: with a dev server, an isolated route plus one file per variant; without, one self-contained HTML file. Show a single variant at actual size in a believable setting: a toast with a page behind it, a card with neighbours. Thumbnails mislead. Switching is instant: it is a 100-times-a-session action, so no animation (`gate.md`).
5. Verify: render every variant, use every interaction, keep the console clean, screenshot each if tooling exists. Then present this table and stop:

| # | Variant | Axis | Right when | Cost |
|---|---|---|---|---|
| 1 | Calm | little motion, outlines instead of shadows | a tool opened all day | easiest to forget |
| 2 | Editorial | big type, roomy spacing | the moment should feel weighty | spends vertical space |

6. On the pick: integrate with the project's file layout and tokens, delete the surface. For another round, keep the harness and diverge around the favourite.

Do not pre-pick a favourite. If asked, answer from the product's personality and how often the piece is seen.

## Picker contract

Floating small pill at the bottom centre, with its own plain styling that does not adapt to the project theme (so it is never mistaken for design). Move it to the top only if a variant sits at the bottom centre (a toast stack, a dock).

- Keys: `1` to `N` and arrow left or right switch; `R` replays. Ignore keys while an input, textarea, select or contenteditable has focus, or a modifier is held.
- Exactly one item has `aria-current="true"`. Selection lives in the URL (`?v=2`), default 1, and survives reload.
- Switching re-mounts the variant so entrance motion reruns; replay re-mounts without switching.
- The active highlight may slide (about 250 ms ease-out); the previewed variant never animates the swap.
- Show a replay button only when some variant has entrance or state motion.
- The picker honours reduced motion too (`reduced-motion.md`).

## Minimal wiring (runnable)

```html
<nav class="pk" aria-label="Prototype variants"></nav>
<div id="stage"></div>
<script>
const variants = [{name:'Quiet', render: el => el.textContent = 'quiet'},
                  {name:'Editorial', render: el => el.textContent = 'editorial'}];
const pk = document.querySelector('.pk'), stage = document.getElementById('stage');
let cur = Math.min(Math.max((+new URLSearchParams(location.search).get('v') || 1) - 1, 0), variants.length - 1);
function mount() {
  stage.replaceChildren(); const el = document.createElement('div'); stage.append(el); variants[cur].render(el);
  [...pk.children].forEach((b, i) => i === cur ? b.setAttribute('aria-current', 'true') : b.removeAttribute('aria-current'));
  const u = new URL(location); u.searchParams.set('v', cur + 1); history.replaceState(null, '', u);
}
variants.forEach((v, i) => { const b = document.createElement('button'); b.textContent = v.name; b.onclick = () => { cur = i; mount(); }; pk.append(b); });
addEventListener('keydown', e => {
  if (e.metaKey || e.ctrlKey || e.altKey || e.target.closest('input,textarea,select,[contenteditable]')) return;
  const n = variants.length;
  if (/^[1-9]$/.test(e.key) && +e.key <= n) cur = +e.key - 1;
  else if (e.key === 'ArrowRight') cur = (cur + 1) % n;
  else if (e.key === 'ArrowLeft') cur = (cur + n - 1) % n;
  else if (e.key !== 'r') return;
  mount();
});
mount();
</script>
```

## Invocations

`<description>` runs the whole flow; add a count (up to five); "riff on <name>" starts a new round around that direction; "keep <name>" promotes it and deletes the surface; "keep <name>, leave the picker" promotes and keeps the surface.
