/*
 * Toast notifications.
 *   Toast.show(message, { type: "info"|"success"|"error", duration: 3500 })
 * Rendered in an aria-live="polite" region at the bottom of the viewport.
 */
(function () {
  var css =
    ".ui-toast-region{position:fixed;left:var(--space-4);right:var(--space-4);bottom:var(--space-4);" +
    "display:flex;flex-direction:column;align-items:center;gap:var(--space-2);z-index:var(--z-toast);pointer-events:none;}" +
    ".ui-toast{background:var(--color-text);color:var(--color-surface);padding:var(--space-3) var(--space-4);" +
    "border-radius:var(--radius-1);box-shadow:var(--shadow-2);font-size:var(--font-size-1);max-width:100%;overflow-wrap:anywhere;}" +
    ".ui-toast--success{border-left:6px solid #2e9e5b;}" +
    ".ui-toast--error{border-left:6px solid var(--color-danger);}";
  var region;

  function ensureRegion() {
    if (region) return region;
    var s = document.createElement("style");
    s.textContent = css;
    document.head.appendChild(s);
    region = document.createElement("div");
    region.className = "ui-toast-region";
    region.setAttribute("aria-live", "polite");
    document.body.appendChild(region);
    return region;
  }

  function show(message, opts) {
    opts = opts || {};
    var t = document.createElement("div");
    t.className = "ui-toast ui-toast--" + (opts.type || "info");
    t.textContent = message;
    ensureRegion().appendChild(t);
    setTimeout(function () { t.remove(); }, opts.duration || 3500);
    return t;
  }

  window.Toast = { show: show };
})();
