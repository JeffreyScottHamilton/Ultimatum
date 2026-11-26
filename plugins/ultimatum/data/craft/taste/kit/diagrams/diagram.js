// Taste kit: run a diagram's pulse again when the pointer enters its card or focus moves into it.
// Load with <script type="module" src="diagram.js"></script>; cards are <figure class="dg-card" tabindex="0">.
const still = matchMedia('(prefers-reduced-motion: reduce)');
for (const card of document.querySelectorAll('.dg-card')) {
  const again = () => {
    if (still.matches) return;
    card.classList.add('dg-restart');
    requestAnimationFrame(() => requestAnimationFrame(() => card.classList.remove('dg-restart')));
  };
  card.addEventListener('pointerenter', again);
  card.addEventListener('focusin', again);
}
