"use client";
import * as React from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { cn, settle } from "./cn";

export interface TabItem { id: string; label: React.ReactNode; panel: React.ReactNode; }

export interface TabsProps {
  tabs: TabItem[];
  /** Controlled selection; leave out for uncontrolled. */
  value?: string;
  defaultValue?: string;
  onChange?: (id: string) => void;
  label: string;
  className?: string;
}

/**
 * ARIA tabs with an underline that slides between tabs and panels that cross-fade in the
 * direction of travel. Arrow keys, Home and End move between tabs (automatic activation).
 */
export function Tabs({ tabs, value, defaultValue, onChange, label, className }: TabsProps) {
  const base = React.useId();
  const reduce = useReducedMotion();
  const [inner, setInner] = React.useState(defaultValue ?? tabs[0]?.id);
  const selected = value ?? inner;
  const index = Math.max(0, tabs.findIndex((t) => t.id === selected));
  const prev = React.useRef(index);
  const dir = index >= prev.current ? 1 : -1;
  React.useEffect(() => { prev.current = index; }, [index]);
  const refs = React.useRef<Array<HTMLButtonElement | null>>([]);

  const pick = (i: number) => {
    const id = tabs[i].id;
    if (value === undefined) setInner(id);
    onChange?.(id);
    refs.current[i]?.focus();
  };
  function onKey(e: React.KeyboardEvent) {
    const map: Record<string, number> = { ArrowRight: index + 1, ArrowLeft: index - 1, Home: 0, End: tabs.length - 1 };
    if (!(e.key in map)) return;
    e.preventDefault();
    pick((map[e.key] + tabs.length) % tabs.length);
  }
  const tab = tabs[index];

  return (
    <div className={className}>
      <div role="tablist" aria-label={label} onKeyDown={onKey} className="relative flex gap-1 border-b border-border">
        {tabs.map((t, i) => (
          <button
            key={t.id}
            ref={(el) => { refs.current[i] = el; }}
            id={`${base}-tab-${t.id}`}
            role="tab"
            type="button"
            aria-selected={i === index}
            aria-controls={`${base}-panel`}
            tabIndex={i === index ? 0 : -1}
            onClick={() => pick(i)}
            className={cn(
              "relative h-10 px-3 text-sm font-medium transition-colors outline-none",
              "focus-visible:rounded-[var(--radius)] focus-visible:ring-2 focus-visible:ring-ring",
              i === index ? "text-foreground" : "text-muted-foreground hover:text-foreground",
            )}
          >
            {t.label}
            {i === index && (
              <motion.span layoutId={`${base}-line`} transition={reduce ? { duration: 0 } : settle}
                className="absolute inset-x-2 -bottom-px h-0.5 rounded-full bg-primary" />
            )}
          </button>
        ))}
      </div>
      <div className="relative overflow-hidden">
        <AnimatePresence mode="popLayout" initial={false} custom={dir}>
          <motion.div
            key={tab?.id}
            id={`${base}-panel`}
            role="tabpanel"
            tabIndex={0}
            aria-labelledby={`${base}-tab-${tab?.id}`}
            custom={dir}
            initial={reduce ? { opacity: 0 } : { opacity: 0, x: 24 * dir }}
            animate={{ opacity: 1, x: 0 }}
            exit={reduce ? { opacity: 0 } : { opacity: 0, x: -24 * dir }}
            transition={settle}
            className="pt-4 outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            {tab?.panel}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
