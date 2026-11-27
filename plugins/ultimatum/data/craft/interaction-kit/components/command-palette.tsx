"use client";
import * as React from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { settle } from "./cn";

export interface Command { id: string; label: string; group?: string; hint?: string; keywords?: string[]; run: () => void; }

export interface CommandPaletteProps {
  commands: Command[];
  open: boolean;
  onOpenChange: (open: boolean) => void;
  /** Bind Cmd/Ctrl+K globally to open it. */
  hotkey?: boolean;
  placeholder?: string;
}

function score(c: Command, q: string): number {
  if (!q) return 1;
  const hay = [c.label, ...(c.keywords ?? [])].join(" ").toLowerCase();
  const needle = q.toLowerCase();
  if (hay.startsWith(needle)) return 3;
  if (hay.includes(needle)) return 2;
  let i = 0;
  for (const ch of hay) if (ch === needle[i]) i++;
  return i === needle.length ? 1 : 0;
}

/**
 * A Cmd/Ctrl+K command menu: an ARIA combobox over a listbox with grouped results, a highlight
 * that slides between options, arrow-key and Enter control, and Escape to close. Focus returns
 * to wherever it was before opening.
 */
export function CommandPalette({ commands, open, onOpenChange, hotkey = true, placeholder = "Type a command or search…" }: CommandPaletteProps) {
  const reduce = useReducedMotion();
  const base = React.useId();
  const [q, setQ] = React.useState("");
  const [active, setActive] = React.useState(0);
  const input = React.useRef<HTMLInputElement>(null);

  React.useEffect(() => {
    if (!hotkey) return;
    const on = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); onOpenChange(!open); }
    };
    window.addEventListener("keydown", on);
    return () => window.removeEventListener("keydown", on);
  }, [hotkey, open, onOpenChange]);

  React.useEffect(() => {
    if (!open) return;
    const opener = document.activeElement as HTMLElement | null;
    setQ(""); setActive(0);
    const t = window.setTimeout(() => input.current?.focus(), 0);
    return () => { window.clearTimeout(t); opener?.focus?.(); };
  }, [open]);

  const results = React.useMemo(() => commands
    .map((c) => ({ c, s: score(c, q) })).filter((r) => r.s > 0)
    .sort((a, b) => b.s - a.s).map((r) => r.c), [commands, q]);
  const groups = React.useMemo(() => {
    const m = new Map<string, Command[]>();
    for (const c of results) { const g = c.group ?? "Commands"; m.set(g, [...(m.get(g) ?? []), c]); }
    return [...m.entries()];
  }, [results]);
  const flat = groups.flatMap(([, cs]) => cs);
  const current = flat[Math.min(active, flat.length - 1)];

  function onKey(e: React.KeyboardEvent) {
    if (e.key === "ArrowDown") { e.preventDefault(); setActive((a) => (a + 1) % Math.max(1, flat.length)); }
    else if (e.key === "ArrowUp") { e.preventDefault(); setActive((a) => (a - 1 + flat.length) % Math.max(1, flat.length)); }
    else if (e.key === "Enter" && current) { e.preventDefault(); onOpenChange(false); current.run(); }
    else if (e.key === "Escape") { e.preventDefault(); onOpenChange(false); }
  }

  return (
    <AnimatePresence initial={false}>
      {open && (
        <div className="fixed inset-0 z-50 grid place-items-start justify-center px-4 pt-[12vh]">
          <motion.div aria-hidden="true" className="absolute inset-0 bg-foreground/30"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            transition={{ duration: reduce ? 0 : 0.15 }} onClick={() => onOpenChange(false)} />
          <motion.div
            role="dialog" aria-modal="true" aria-label="Command menu"
            initial={reduce ? { opacity: 0 } : { opacity: 0, scale: 0.97, y: -8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={reduce ? { opacity: 0 } : { opacity: 0, scale: 0.98, transition: { duration: 0.12 } }}
            transition={reduce ? { duration: 0 } : settle}
            className="relative w-full max-w-lg origin-top overflow-hidden rounded-[calc(var(--radius)*2)] border border-border bg-card text-card-foreground shadow-[var(--shadow-md)]"
          >
            {/* kitlint-ok: focus-hidden the dialog keeps focus here; the caret is the indicator */}
            <input
              ref={input}
              role="combobox"
              aria-expanded="true"
              aria-controls={`${base}-list`}
              aria-activedescendant={current ? `${base}-${current.id}` : undefined}
              aria-autocomplete="list"
              value={q}
              onChange={(e) => { setQ(e.target.value); setActive(0); }}
              onKeyDown={onKey}
              placeholder={placeholder}
              className="h-12 w-full border-b border-border bg-transparent px-4 text-base text-foreground outline-none placeholder:text-muted-foreground"
            />
            <div id={`${base}-list`} role="listbox" aria-label="Results" className="max-h-80 overflow-auto p-1.5">
              {flat.length === 0 && <p className="m-0 px-3 py-6 text-center text-sm text-muted-foreground" role="status">No results</p>}
              {groups.map(([g, cs]) => (
                <div key={g} role="group" aria-label={g}>
                  <p aria-hidden="true" className="m-0 px-3 pb-1 pt-2 text-xs font-medium text-muted-foreground">{g}</p>
                  {cs.map((c) => {
                    const on = c === current;
                    return (
                      <div key={c.id} id={`${base}-${c.id}`} role="option" aria-selected={on}
                        onPointerMove={() => setActive(flat.indexOf(c))}
                        onClick={() => { onOpenChange(false); c.run(); }}
                        className="relative flex h-10 cursor-pointer items-center justify-between rounded-[var(--radius)] px-3 text-sm">
                        {on && <motion.span layoutId={`${base}-hl`} transition={reduce ? { duration: 0 } : { type: "spring", duration: 0.25, bounce: 0 }}
                          className="absolute inset-0 rounded-[var(--radius)] bg-muted" />}
                        <span className="relative">{c.label}</span>
                        {c.hint && <kbd className="relative font-sans text-xs text-muted-foreground">{c.hint}</kbd>}
                      </div>
                    );
                  })}
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
