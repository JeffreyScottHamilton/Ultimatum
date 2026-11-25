/*
 * Accessible modal dialog.
 *   Dialog.open({ title, message, confirmLabel, cancelLabel, danger, onConfirm, onCancel })
 * - role="dialog", aria-modal="true", labelled by its title
 * - focus moves into the dialog, is trapped with Tab/Shift+Tab
 * - Escape cancels; focus returns to the previously focused element on close
 */
(function () {
  var css =
    ".ui-dialog-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.45);display:flex;" +
    "align-items:center;justify-content:center;padding:var(--space-4);z-index:var(--z-dialog);}" +
    ".ui-dialog{background:var(--color-surface);color:var(--color-text);border-radius:var(--radius-2);" +
    "box-shadow:var(--shadow-2);padding:var(--space-6);width:100%;max-width:420px;}" +
    ".ui-dialog h2{margin:0 0 var(--space-3);font-size:var(--font-size-3);}" +
    ".ui-dialog p{margin:0 0 var(--space-6);color:var(--color-muted);overflow-wrap:anywhere;}" +
    ".ui-dialog-actions{display:flex;justify-content:flex-end;gap:var(--space-3);flex-wrap:wrap;}";
  var counter = 0;

  function injectStyles() {
    if (document.getElementById("ui-dialog-styles")) return;
    var s = document.createElement("style");
    s.id = "ui-dialog-styles";
    s.textContent = css;
    document.head.appendChild(s);
  }

  function focusables(root) {
    return Array.prototype.slice.call(
      root.querySelectorAll('button,[href],input,select,textarea,[tabindex]:not([tabindex="-1"])')
    ).filter(function (el) { return !el.disabled; });
  }

  function open(opts) {
    injectStyles();
    var previous = document.activeElement;
    var id = "ui-dialog-title-" + (++counter);

    var backdrop = document.createElement("div");
    backdrop.className = "ui-dialog-backdrop";
    var dlg = document.createElement("div");
    dlg.className = "ui-dialog";
    dlg.setAttribute("role", "dialog");
    dlg.setAttribute("aria-modal", "true");
    dlg.setAttribute("aria-labelledby", id);

    var h = document.createElement("h2");
    h.id = id;
    h.textContent = opts.title;
    var p = document.createElement("p");
    p.textContent = opts.message || "";
    var actions = document.createElement("div");
    actions.className = "ui-dialog-actions";

    function close() {
      document.removeEventListener("keydown", onKey, true);
      backdrop.remove();
      if (previous && previous.isConnected) previous.focus();
    }
    function cancel() { close(); if (opts.onCancel) opts.onCancel(); }
    function confirm() { close(); if (opts.onConfirm) opts.onConfirm(); }

    var cancelBtn = Button.create({ label: opts.cancelLabel || "Cancel", variant: "secondary", onClick: cancel });
    var okBtn = Button.create({ label: opts.confirmLabel || "OK", variant: opts.danger ? "danger" : "primary", onClick: confirm });
    actions.appendChild(cancelBtn);
    actions.appendChild(okBtn);
    dlg.appendChild(h);
    dlg.appendChild(p);
    dlg.appendChild(actions);
    backdrop.appendChild(dlg);
    document.body.appendChild(backdrop);

    function onKey(e) {
      if (e.key === "Escape") { e.preventDefault(); cancel(); return; }
      if (e.key !== "Tab") return;
      var items = focusables(dlg);
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      else if (!dlg.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
    }
    document.addEventListener("keydown", onKey, true);
    cancelBtn.focus();
    return { close: close };
  }

  window.Dialog = { open: open };
})();
