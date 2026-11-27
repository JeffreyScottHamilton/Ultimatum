"use client";
import * as React from "react";
import { motion, useReducedMotion } from "motion/react";
import { cn, focusRing } from "./cn";

export interface HoldToConfirmProps {
  /** Runs once the hold completes. */
  onConfirm: () => void;
  children: React.ReactNode;
  /** Hold length in ms. */
  holdFor?: number;
  className?: string;
}

/**
 * For destructive actions: the user presses and holds (pointer, Space or Enter) while a fill
 * sweeps across. Letting go early cancels and the fill drains back. No confirm dialog needed.
 */
export function HoldToConfirm({ onConfirm, children, holdFor = 1200, className }: HoldToConfirmProps) {
  const [holding, setHolding] = React.useState(false);
  const timer = React.useRef<number | null>(null);
  const reduce = useReducedMotion();
  const hintId = React.useId();

  const stop = React.useCallback(() => {
    setHolding(false);
    if (timer.current !== null) window.clearTimeout(timer.current);
    timer.current = null;
  }, []);
  const start = () => {
    if (timer.current !== null) return;
    setHolding(true);
    timer.current = window.setTimeout(() => { timer.current = null; setHolding(false); onConfirm(); }, holdFor);
  };
  React.useEffect(() => stop, [stop]);

  return (
    <button
      type="button"
      aria-describedby={hintId}
      onPointerDown={(e) => { if (e.button === 0) start(); }}
      onPointerUp={stop}
      onPointerLeave={stop}
      onPointerCancel={stop}
      onKeyDown={(e) => { if ((e.key === " " || e.key === "Enter") && !e.repeat) { e.preventDefault(); start(); } }}
      onKeyUp={(e) => { if (e.key === " " || e.key === "Enter") stop(); }}
      onBlur={stop}
      onContextMenu={(e) => e.preventDefault()}
      className={cn(
        "relative isolate inline-flex h-10 select-none items-center justify-center overflow-hidden rounded-[var(--radius)]",
        "border border-destructive/40 px-4 text-sm font-medium text-destructive transition-colors hover:bg-destructive/5",
        focusRing, className,
      )}
    >
      <motion.span
        aria-hidden="true"
        className="absolute inset-0 -z-10 origin-left bg-destructive/15"
        initial={false}
        animate={{ scaleX: holding ? 1 : 0 }}
        transition={holding
          ? { duration: holdFor / 1000, ease: "linear" }
          : { duration: reduce ? 0 : 0.25, ease: [0.2, 0, 0, 1] }}
      />
      {children}
      <span id={hintId} className="sr-only">Press and hold to confirm</span>
    </button>
  );
}
