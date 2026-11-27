"use client";
import * as React from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { cn, settle } from "./cn";

export interface AccordionItem { id: string; title: React.ReactNode; body: React.ReactNode; }

export interface AccordionProps {
  items: AccordionItem[];
  /** Allow more than one section open at a time. */
  multiple?: boolean;
  defaultOpen?: string[];
  className?: string;
}

/**
 * Disclosure sections whose height animates to its real size, with the chevron turning in step.
 * Each header is a real button with aria-expanded and aria-controls; Up, Down, Home and End
 * move between headers.
 */
export function Accordion({ items, multiple = false, defaultOpen = [], className }: AccordionProps) {
  const base = React.useId();
  const reduce = useReducedMotion();
  const [open, setOpen] = React.useState<string[]>(defaultOpen);
  const refs = React.useRef<Array<HTMLButtonElement | null>>([]);

  const toggle = (id: string) =>
    setOpen((cur) => cur.includes(id) ? cur.filter((x) => x !== id) : multiple ? [...cur, id] : [id]);
  function onKey(e: React.KeyboardEvent, i: number) {
    const n = items.length;
    const to = e.key === "ArrowDown" ? (i + 1) % n : e.key === "ArrowUp" ? (i - 1 + n) % n
      : e.key === "Home" ? 0 : e.key === "End" ? n - 1 : -1;
    if (to < 0) return;
    e.preventDefault();
    refs.current[to]?.focus();
  }

  return (
    <div className={cn("divide-y divide-border rounded-[var(--radius)] border border-border", className)}>
      {items.map((it, i) => {
        const isOpen = open.includes(it.id);
        return (
          <div key={it.id}>
            <h3 className="m-0">
              <button
                ref={(el) => { refs.current[i] = el; }}
                type="button"
                id={`${base}-h-${it.id}`}
                aria-expanded={isOpen}
                aria-controls={`${base}-p-${it.id}`}
                onClick={() => toggle(it.id)}
                onKeyDown={(e) => onKey(e, i)}
                className="flex min-h-12 w-full items-center justify-between gap-4 px-4 text-left text-sm font-medium transition-colors hover:bg-muted/60 outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-ring"
              >
                {it.title}
                <motion.svg aria-hidden="true" viewBox="0 0 24 24" className="size-4 shrink-0 text-muted-foreground"
                  initial={false} animate={{ rotate: isOpen ? 180 : 0 }} transition={reduce ? { duration: 0 } : settle}
                  fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
                  <path d="m6 9 6 6 6-6" />
                </motion.svg>
              </button>
            </h3>
            <AnimatePresence initial={false}>
              {isOpen && (
                <motion.div
                  id={`${base}-p-${it.id}`}
                  role="region"
                  aria-labelledby={`${base}-h-${it.id}`}
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={reduce ? { duration: 0 } : settle}
                  className="overflow-hidden"
                >
                  <div className="px-4 pb-4 text-sm text-muted-foreground text-pretty">{it.body}</div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        );
      })}
    </div>
  );
}
