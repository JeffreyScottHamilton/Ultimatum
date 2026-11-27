"use client";
import * as React from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { cn, focusRing, settle } from "./cn";

export interface ExpandableItem { id: string; title: string; subtitle?: string; media?: React.ReactNode; body: React.ReactNode; }

export interface ExpandableCardsProps { items: ExpandableItem[]; className?: string; }

/**
 * A grid of cards where the chosen one grows into a centred panel through a shared-layout
 * transition (title and media fly to their new place). The open panel is a modal dialog:
 * Escape or the backdrop closes it and focus goes back to the card.
 */
export function ExpandableCards({ items, className }: ExpandableCardsProps) {
  const reduce = useReducedMotion();
  const base = React.useId();
  const [openId, setOpenId] = React.useState<string | null>(null);
  const openers = React.useRef<Record<string, HTMLButtonElement | null>>({});
  const closeBtn = React.useRef<HTMLButtonElement>(null);
  const item = items.find((i) => i.id === openId);
  const t = reduce ? { duration: 0 } : settle;

  React.useEffect(() => {
    if (!openId) return;
    const id = openId;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const f = window.setTimeout(() => closeBtn.current?.focus(), 0);
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") setOpenId(null); };
    window.addEventListener("keydown", esc);
    return () => { window.clearTimeout(f); document.body.style.overflow = prev; window.removeEventListener("keydown", esc); openers.current[id]?.focus(); };
  }, [openId]);

  return (
    <>
      <ul className={cn("m-0 grid list-none gap-4 p-0 sm:grid-cols-2 lg:grid-cols-3", className)}>
        {items.map((it) => (
          <li key={it.id}>
            <motion.button
              ref={(el) => { openers.current[it.id] = el; }}
              type="button"
              layoutId={`${base}-card-${it.id}`}
              transition={t}
              onClick={() => setOpenId(it.id)}
              aria-haspopup="dialog"
              className={cn("w-full overflow-hidden rounded-[calc(var(--radius)*2)] border border-border bg-card text-left transition-colors hover:bg-muted/40", focusRing)}
            >
              {it.media && <motion.div layoutId={`${base}-media-${it.id}`} transition={t} className="aspect-video overflow-hidden">{it.media}</motion.div>}
              <div className="p-4">
                <motion.h3 layoutId={`${base}-title-${it.id}`} transition={t} className="m-0 text-base font-semibold text-foreground">{it.title}</motion.h3>
                {it.subtitle && <p className="m-0 mt-1 text-sm text-muted-foreground">{it.subtitle}</p>}
              </div>
            </motion.button>
          </li>
        ))}
      </ul>
      <AnimatePresence initial={false}>
        {item && (
          <div className="fixed inset-0 z-50 grid place-items-center p-4">
            <motion.div aria-hidden="true" className="absolute inset-0 bg-foreground/40" onClick={() => setOpenId(null)}
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: reduce ? 0 : 0.2 }} />
            <motion.div
              role="dialog" aria-modal="true" aria-labelledby={`${base}-dt`}
              layoutId={`${base}-card-${item.id}`} transition={t}
              className="relative max-h-[90dvh] w-full max-w-xl overflow-auto rounded-[calc(var(--radius)*2)] border border-border bg-card"
            >
              {item.media && <motion.div layoutId={`${base}-media-${item.id}`} transition={t} className="aspect-video overflow-hidden">{item.media}</motion.div>}
              <div className="p-5">
                <motion.h3 id={`${base}-dt`} layoutId={`${base}-title-${item.id}`} transition={t} className="m-0 text-lg font-semibold text-foreground">{item.title}</motion.h3>
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1, transition: { delay: reduce ? 0 : 0.12 } }} exit={{ opacity: 0, transition: { duration: 0.05 } }}
                  className="mt-2 text-sm text-muted-foreground text-pretty">{item.body}</motion.div>
              </div>
              <button ref={closeBtn} type="button" aria-label="Close" onClick={() => setOpenId(null)}
                className={cn("absolute right-2 top-2 grid size-10 place-items-center rounded-full bg-background/80 text-foreground backdrop-blur transition-colors hover:bg-background", focusRing)}>
                <svg aria-hidden="true" viewBox="0 0 24 24" className="size-4" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round"><path d="M18 6 6 18M6 6l12 12" /></svg>
              </button>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}
