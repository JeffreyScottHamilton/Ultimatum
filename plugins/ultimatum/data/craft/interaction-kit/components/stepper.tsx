"use client";
import { motion, useReducedMotion } from "motion/react";
import { cn, settle } from "./cn";

export interface StepperProps {
  steps: string[];
  /** Zero-based index of the current step. */
  current: number;
  className?: string;
}

/**
 * Progress through a multi-step flow. Finished steps show a drawn tick, the connector fills as
 * you advance, and the list is an ordered list with aria-current="step", so it reads correctly
 * without the visuals.
 */
export function Stepper({ steps, current, className }: StepperProps) {
  const reduce = useReducedMotion();
  return (
    <ol className={cn("m-0 flex list-none items-center gap-0 p-0", className)}>
      {steps.map((s, i) => {
        const done = i < current, here = i === current;
        return (
          <li key={s} aria-current={here ? "step" : undefined} className={cn("flex items-center", i < steps.length - 1 && "flex-1")}>
            <div className="flex flex-col items-center gap-1.5">
              <motion.span
                initial={false}
                animate={{ scale: here && !reduce ? 1.08 : 1 }}
                transition={settle}
                className={cn(
                  "grid size-8 place-items-center rounded-full border text-sm font-medium tabular-nums transition-colors",
                  done ? "border-primary bg-primary text-primary-foreground"
                    : here ? "border-primary text-foreground" : "border-border text-muted-foreground",
                )}
              >
                {done ? (
                  <svg aria-hidden="true" viewBox="0 0 24 24" className="size-4" fill="none" stroke="currentColor" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round">
                    <motion.path d="M5 12.5 10 17 19 7" initial={reduce ? false : { pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 0.3, ease: "easeOut" }} />
                  </svg>
                ) : i + 1}
              </motion.span>
              <span className={cn("text-xs", here ? "font-medium text-foreground" : "text-muted-foreground")}>
                {s}<span className="sr-only">{done ? " (done)" : here ? " (current)" : ""}</span>
              </span>
            </div>
            {i < steps.length - 1 && (
              <span aria-hidden="true" className="relative mx-2 mb-5 h-0.5 flex-1 overflow-hidden rounded-full bg-border">
                <motion.span className="absolute inset-0 origin-left bg-primary" initial={false}
                  animate={{ scaleX: done ? 1 : 0 }} transition={reduce ? { duration: 0 } : { duration: 0.4, ease: [0.2, 0, 0, 1] }} />
              </span>
            )}
          </li>
        );
      })}
    </ol>
  );
}
