"use client";
import * as React from "react";
import { AnimatePresence, motion, useDragControls, useReducedMotion, type PanInfo } from "motion/react";
import { cn, focusRing, settle } from "./cn";

export interface DrawerProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  className?: string;
}

const FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),select,textarea,[tabindex]:not([tabindex="-1"])';

/**
 * A bottom sheet: slides up, can be flicked or dragged down to close, and behaves as a modal
 * dialog (focus moves in and is trapped, Escape closes, focus returns to the opener, the page
 * behind stops scrolling).
 */
export function Drawer({ open, onClose, title, children, className }: DrawerProps) {
  const reduce = useReducedMotion();
  const panel = React.useRef<HTMLDivElement>(null);
  const drag = useDragControls();
  const titleId = React.useId();

  React.useEffect(() => {
    if (!open) return;
    const opener = document.activeElement as HTMLElement | null;
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const t = window.setTimeout(() => panel.current?.querySelector<HTMLElement>(FOCUSABLE)?.focus() ?? panel.current?.focus(), 0);
    return () => { window.clearTimeout(t); document.body.style.overflow = prevOverflow; opener?.focus?.(); };
  }, [open]);

  function onKey(e: React.KeyboardEvent) {
    if (e.key === "Escape") { e.stopPropagation(); onClose(); return; }
    if (e.key !== "Tab" || !panel.current) return;
    const els = Array.from(panel.current.querySelectorAll<HTMLElement>(FOCUSABLE));
    if (!els.length) return;
    const first = els[0], last = els[els.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }
  function onDragEnd(_: unknown, info: PanInfo) {
    if (info.offset.y > 120 || info.velocity.y > 500) onClose();
  }

  return (
    <AnimatePresence initial={false}>
      {open && (
        <div className="fixed inset-0 z-50" onKeyDown={onKey}>
          <motion.div aria-hidden="true" className="absolute inset-0 bg-foreground/40"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            transition={{ duration: reduce ? 0 : 0.2 }} onClick={onClose} />
          <motion.div
            ref={panel}
            role="dialog"
            aria-modal="true"
            aria-labelledby={titleId}
            tabIndex={-1}
            drag={reduce ? false : "y"}
            dragListener={false}
            dragControls={drag}
            dragConstraints={{ top: 0, bottom: 0 }}
            dragElastic={{ top: 0.05, bottom: 0.8 }}
            onDragEnd={onDragEnd}
            initial={reduce ? { opacity: 0 } : { y: "100%" }}
            animate={reduce ? { opacity: 1 } : { y: 0 }}
            exit={reduce ? { opacity: 0 } : { y: "100%" }}
            transition={reduce ? { duration: 0.01 } : settle}
            className={cn(
              "absolute inset-x-0 bottom-0 mx-auto max-h-[85dvh] w-full max-w-lg overflow-auto rounded-t-[calc(var(--radius)*2)]",
              "bg-background pb-[max(1rem,env(safe-area-inset-bottom))] shadow-[var(--shadow-md)] outline-none",
              className,
            )}
          >
            <div onPointerDown={(e) => drag.start(e)} className="flex cursor-grab touch-none justify-center py-3 active:cursor-grabbing">
              <span aria-hidden="true" className="h-1.5 w-10 rounded-full bg-muted-foreground/30" />
            </div>
            <div className="flex items-center justify-between gap-4 px-5">
              <h2 id={titleId} className="m-0 text-base font-semibold text-foreground">{title}</h2>
              <button type="button" aria-label="Close" onClick={onClose}
                className={cn("grid size-10 place-items-center rounded-[var(--radius)] text-muted-foreground transition-colors hover:text-foreground", focusRing)}>
                <svg aria-hidden="true" viewBox="0 0 24 24" className="size-4" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round"><path d="M18 6 6 18M6 6l12 12" /></svg>
              </button>
            </div>
            <div className="px-5 pt-2">{children}</div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
