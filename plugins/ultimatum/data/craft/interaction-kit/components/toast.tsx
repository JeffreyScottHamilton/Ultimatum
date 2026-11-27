"use client";
import * as React from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { cn, focusRing, lively } from "./cn";

export type ToastTone = "neutral" | "success" | "danger";
export interface Toast { id: number; title: string; body?: string; tone?: ToastTone; }

const Ctx = React.createContext<(t: Omit<Toast, "id">) => void>(() => {});
/** Call inside a ToastProvider: `const toast = useToast(); toast({ title: "Saved" })`. */
export const useToast = () => React.useContext(Ctx);

/**
 * A stack of toasts in the corner: newest in front, older ones tucked behind and scaled down,
 * fanning out on hover or focus. Each dismisses itself, pauses while hovered, and is announced
 * through a polite live region.
 */
export function ToastProvider({ children, duration = 4000 }: { children: React.ReactNode; duration?: number }) {
  const [items, setItems] = React.useState<Toast[]>([]);
  const [expanded, setExpanded] = React.useState(false);
  const reduce = useReducedMotion();
  const next = React.useRef(1);

  const push = React.useCallback((t: Omit<Toast, "id">) => {
    setItems((cur) => [{ ...t, id: next.current++ }, ...cur].slice(0, 5));
  }, []);
  const drop = (id: number) => setItems((cur) => cur.filter((t) => t.id !== id));

  React.useEffect(() => {
    if (expanded || !items.length) return;
    const oldest = items[items.length - 1];
    const timer = window.setTimeout(() => drop(oldest.id), duration);
    return () => window.clearTimeout(timer);
  }, [items, expanded, duration]);

  return (
    <Ctx.Provider value={push}>
      {children}
      <section
        aria-label="Notifications"
        aria-live="polite"
        onPointerEnter={() => setExpanded(true)}
        onPointerLeave={() => setExpanded(false)}
        onFocus={() => setExpanded(true)}
        onBlur={() => setExpanded(false)}
        className="pointer-events-none fixed bottom-4 right-4 z-50 w-[min(22rem,calc(100vw-2rem))]"
      >
        <ol className="relative m-0 list-none p-0">
          <AnimatePresence initial={false}>
            {items.map((t, i) => (
              <motion.li
                key={t.id}
                layout={!reduce}
                initial={reduce ? { opacity: 0 } : { opacity: 0, y: 24, scale: 0.96 }}
                animate={{
                  opacity: i > 2 ? 0 : 1,
                  y: expanded ? -i * 76 : -i * 10,
                  scale: expanded || reduce ? 1 : 1 - i * 0.05,
                }}
                exit={reduce ? { opacity: 0 } : { opacity: 0, x: 40, transition: { duration: 0.18 } }}
                transition={reduce ? { duration: 0 } : lively}
                style={{ zIndex: 10 - i }}
                className={cn(
                  "pointer-events-auto absolute bottom-0 right-0 flex w-full items-start gap-3 rounded-[var(--radius)] border border-border bg-card p-4 shadow-[var(--shadow-md)]",
                  i > 0 && !expanded && "[&>*]:opacity-0",
                )}
              >
                <span aria-hidden="true" className={cn("mt-1.5 size-2 shrink-0 rounded-full",
                  t.tone === "success" ? "bg-success" : t.tone === "danger" ? "bg-destructive" : "bg-primary")} />
                <div className="min-w-0 flex-1">
                  <p className="m-0 text-sm font-medium text-foreground">{t.title}</p>
                  {t.body && <p className="m-0 mt-0.5 text-sm text-muted-foreground">{t.body}</p>}
                </div>
                <button type="button" aria-label="Dismiss notification" onClick={() => drop(t.id)}
                  className={cn("-m-2 grid size-10 shrink-0 place-items-center rounded-[var(--radius)] text-muted-foreground transition-colors hover:text-foreground", focusRing)}>
                  <svg aria-hidden="true" viewBox="0 0 24 24" className="size-4" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round"><path d="M18 6 6 18M6 6l12 12" /></svg>
                </button>
              </motion.li>
            ))}
          </AnimatePresence>
        </ol>
      </section>
    </Ctx.Provider>
  );
}
