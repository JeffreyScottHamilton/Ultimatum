"use client";
import * as React from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { cn, focusRing, settle } from "./cn";

export type PressState = "idle" | "busy" | "done" | "failed";

export interface PressButtonProps extends Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, "children"> {
  /** Label in the idle state. */
  children: React.ReactNode;
  /** Drive it from your request: idle, busy, done or failed. */
  state?: PressState;
  busyLabel?: string;
  doneLabel?: string;
  failedLabel?: string;
  variant?: "solid" | "outline";
}

const Spinner = () => (
  <svg viewBox="0 0 16 16" className="size-4 animate-spin motion-reduce:animate-none" aria-hidden="true">
    <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" strokeOpacity="0.25" strokeWidth="2" />
    <path d="M14 8a6 6 0 0 0-6-6" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
  </svg>
);

const Tick = () => (
  <svg viewBox="0 0 16 16" className="size-4" aria-hidden="true">
    <path d="M3.5 8.5l3 3 6-7" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

/**
 * A button that answers the press: it gives under the finger, then morphs through
 * busy, done or failed without changing width abruptly, and says the result aloud.
 */
export function PressButton({
  children, state = "idle", busyLabel = "Working", doneLabel = "Done", failedLabel = "Try again",
  variant = "solid", className, disabled, ...rest
}: PressButtonProps) {
  const reduce = useReducedMotion();
  const label = { idle: children, busy: busyLabel, done: doneLabel, failed: failedLabel }[state];
  const icon = state === "busy" ? <Spinner /> : state === "done" ? <Tick /> : null;
  return (
    <motion.button
      layout={!reduce}
      transition={settle}
      whileTap={reduce || disabled ? undefined : { scale: 0.96 }}
      aria-busy={state === "busy" || undefined}
      disabled={disabled || state === "busy"}
      className={cn(
        "relative inline-flex h-10 min-w-10 items-center justify-center gap-2 overflow-hidden rounded-[var(--radius)] px-4 text-sm font-medium",
        "transition-colors disabled:cursor-not-allowed disabled:opacity-60",
        variant === "solid"
          ? "bg-primary text-primary-foreground hover:bg-primary/90"
          : "border border-border bg-background text-foreground hover:bg-muted",
        state === "failed" && "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        focusRing, className,
      )}
      {...(rest as React.ComponentProps<typeof motion.button>)}
    >
      <AnimatePresence mode="popLayout" initial={false}>
        <motion.span
          key={state}
          className="inline-flex items-center gap-2"
          initial={reduce ? { opacity: 0 } : { opacity: 0, y: 8, filter: "blur(4px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          exit={reduce ? { opacity: 0 } : { opacity: 0, y: -8, filter: "blur(4px)" }}
          transition={settle}
        >
          {icon}
          {label}
        </motion.span>
      </AnimatePresence>
      <span className="sr-only" aria-live="polite">{state === "done" || state === "failed" ? String(label) : ""}</span>
    </motion.button>
  );
}
