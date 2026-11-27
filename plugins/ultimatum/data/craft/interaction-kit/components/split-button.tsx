"use client";
import * as React from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { cn, focusRing, settle } from "./cn";

export interface SplitAction { id: string; label: string; run: () => void; }

export interface SplitButtonProps {
  primary: SplitAction;
  more: SplitAction[];
  /** Accessible name of the menu button, e.g. "More save options". */
  moreLabel: string;
  className?: string;
}

/**
 * A main action with a joined menu of alternatives (Save / Save as draft, Merge / Squash).
 * The menu follows the ARIA menu button pattern: arrows move, Enter picks, Escape closes and
 * returns focus.
 */
export function SplitButton({ primary, more, moreLabel, className }: SplitButtonProps) {
  const reduce = useReducedMotion();
  const id = React.useId();
  const [open, setOpen] = React.useState(false);
  const [active, setActive] = React.useState(0);
  const toggle = React.useRef<HTMLButtonElement>(null);
  const items = React.useRef<Array<HTMLButtonElement | null>>([]);
  const wrap = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => { if (open) items.current[active]?.focus(); }, [open, active]);
  React.useEffect(() => {
    if (!open) return;
    const out = (e: PointerEvent) => { if (!wrap.current?.contains(e.target as Node)) setOpen(false); };
    document.addEventListener("pointerdown", out);
    return () => document.removeEventListener("pointerdown", out);
  }, [open]);
  const close = () => { setOpen(false); toggle.current?.focus(); };
  function onMenuKey(e: React.KeyboardEvent) {
    const n = more.length;
    if (e.key === "ArrowDown") { e.preventDefault(); setActive((a) => (a + 1) % n); }
    else if (e.key === "ArrowUp") { e.preventDefault(); setActive((a) => (a - 1 + n) % n); }
    else if (e.key === "Home") { e.preventDefault(); setActive(0); }
    else if (e.key === "End") { e.preventDefault(); setActive(n - 1); }
    else if (e.key === "Escape" || e.key === "Tab") { e.preventDefault(); close(); }
  }
  const seg = cn("inline-flex h-10 items-center bg-primary text-sm font-medium text-primary-foreground transition-colors hover:bg-primary-hover active:scale-[0.97] motion-reduce:active:scale-100", focusRing);

  return (
    <div ref={wrap} className={cn("relative inline-flex", className)}>
      <button type="button" onClick={primary.run} className={cn(seg, "rounded-l-[var(--radius)] px-4")}>{primary.label}</button>
      <button ref={toggle} type="button" aria-label={moreLabel} aria-haspopup="menu" aria-expanded={open} aria-controls={`${id}-menu`}
        onClick={() => { setActive(0); setOpen((o) => !o); }}
        onKeyDown={(e) => { if (e.key === "ArrowDown") { e.preventDefault(); setActive(0); setOpen(true); } }}
        className={cn(seg, "w-10 justify-center rounded-r-[var(--radius)] border-l border-primary-foreground/20")}>
        <motion.svg aria-hidden="true" viewBox="0 0 24 24" className="size-4" initial={false} animate={{ rotate: open ? 180 : 0 }} transition={reduce ? { duration: 0 } : settle}
          fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"><path d="m6 9 6 6 6-6" /></motion.svg>
      </button>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div id={`${id}-menu`} role="menu" aria-label={moreLabel} onKeyDown={onMenuKey}
            initial={reduce ? { opacity: 0 } : { opacity: 0, scale: 0.96, y: -4 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={reduce ? { opacity: 0 } : { opacity: 0, scale: 0.98, transition: { duration: 0.1 } }}
            transition={reduce ? { duration: 0 } : settle}
            className="absolute right-0 top-full z-20 mt-1.5 min-w-48 origin-top-right rounded-[var(--radius)] border border-border bg-card p-1 shadow-[var(--shadow-md)]">
            {more.map((a, i) => (
              <button key={a.id} ref={(el) => { items.current[i] = el; }} type="button" role="menuitem" tabIndex={i === active ? 0 : -1}
                onClick={() => { close(); a.run(); }}
                className="flex h-10 w-full items-center rounded-[calc(var(--radius)-2px)] px-3 text-left text-sm text-foreground transition-colors hover:bg-muted focus:bg-muted outline-none">
                {a.label}
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
