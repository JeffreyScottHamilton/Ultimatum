"use client";
import * as React from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { cn, focusRing, settle } from "./cn";

export interface MorphPopoverProps {
  /** Label of the trigger button. */
  label: string;
  /** Content of the opened panel; receives a close function. */
  children: (close: () => void) => React.ReactNode;
  className?: string;
}

/**
 * A button that grows into its own panel (a shared layout box, not a separate popup flying in).
 * Escape, an outside click, or the close action shrink it back and return focus to the button.
 */
export function MorphPopover({ label, children, className }: MorphPopoverProps) {
  const reduce = useReducedMotion();
  const id = React.useId();
  const [open, setOpen] = React.useState(false);
  const root = React.useRef<HTMLDivElement>(null);
  const trigger = React.useRef<HTMLButtonElement>(null);
  const t = reduce ? { duration: 0 } : settle;
  const close = React.useCallback(() => { setOpen(false); window.setTimeout(() => trigger.current?.focus(), 0); }, []);

  React.useEffect(() => {
    if (!open) return;
    const onDown = (e: PointerEvent) => { if (!root.current?.contains(e.target as Node)) setOpen(false); };
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") close(); };
    document.addEventListener("pointerdown", onDown);
    document.addEventListener("keydown", onKey);
    const f = window.setTimeout(() => root.current?.querySelector<HTMLElement>("[data-autofocus],input,textarea,button")?.focus(), 0);
    return () => { document.removeEventListener("pointerdown", onDown); document.removeEventListener("keydown", onKey); window.clearTimeout(f); };
  }, [open, close]);

  return (
    <div ref={root} className={cn("relative inline-block", className)}>
      <AnimatePresence initial={false} mode="popLayout">
        {open ? (
          <motion.div key="panel" layoutId={`${id}-box`} transition={t} id={`${id}-panel`} role="dialog" aria-label={label}
            className="w-72 overflow-hidden rounded-[calc(var(--radius)*2)] border border-border bg-card p-3 text-card-foreground shadow-[var(--shadow-md)]">
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1, transition: { delay: reduce ? 0 : 0.08 } }} exit={{ opacity: 0, transition: { duration: 0.05 } }}>
              {children(close)}
            </motion.div>
          </motion.div>
        ) : (
          <motion.button key="trigger" ref={trigger} type="button" layoutId={`${id}-box`} transition={t}
            aria-expanded={false} aria-haspopup="dialog" onClick={() => setOpen(true)}
            className={cn("inline-flex h-10 items-center rounded-[var(--radius)] border border-border bg-card px-4 text-sm font-medium text-foreground transition-colors hover:bg-muted", focusRing)}>
            <motion.span layout="position">{label}</motion.span>
          </motion.button>
        )}
      </AnimatePresence>
    </div>
  );
}
