/*
 * Button component.
 *   Button.create({ label, variant, onClick, ariaLabel }) -> <button>
 * variant: "primary" (default) | "secondary" | "danger"
 * Styles are injected once and use tokens.css custom properties.
 */
(function () {
  var css =
    ".ui-btn{font:inherit;font-size:var(--font-size-1);padding:var(--space-2) var(--space-4);" +
    "border-radius:var(--radius-1);border:1px solid transparent;cursor:pointer;min-height:40px;}" +
    ".ui-btn:focus-visible{outline:3px solid var(--color-focus);outline-offset:2px;}" +
    ".ui-btn--primary{background:var(--color-primary);color:var(--color-primary-text);}" +
    ".ui-btn--secondary{background:var(--color-surface);color:var(--color-text);border-color:var(--color-border);}" +
    ".ui-btn--danger{background:var(--color-danger);color:var(--color-danger-text);}";

  function injectStyles() {
    if (document.getElementById("ui-btn-styles")) return;
    var s = document.createElement("style");
    s.id = "ui-btn-styles";
    s.textContent = css;
    document.head.appendChild(s);
  }

  function create(opts) {
    injectStyles();
    var b = document.createElement("button");
    b.type = "button";
    b.className = "ui-btn ui-btn--" + (opts.variant || "primary");
    b.textContent = opts.label;
    if (opts.ariaLabel) b.setAttribute("aria-label", opts.ariaLabel);
    if (opts.onClick) b.addEventListener("click", opts.onClick);
    return b;
  }

  window.Button = { create: create };
})();
