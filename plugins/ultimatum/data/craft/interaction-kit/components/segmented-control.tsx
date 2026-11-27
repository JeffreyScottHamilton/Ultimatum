"use client";
import * as React from "react";
import { motion, useReducedMotion } from "motion/react";
import { cn, lively } from "./cn";

export interface SegmentOption<T extends string> { value: T; label: React.ReactNode; }

export interface SegmentedControlProps<T extends string> {
  options: SegmentOption<T>[];
  value: T;
  onChange: (value: T) => void;
  /** Accessible name for the group. */
  label: string;
  className?: string;
}

/**
 * A radio group drawn as one track with a sliding thumb. Arrow keys move and select,
 * as a native radio group does; the thumb is a shared layout element, so it glides.
 */
export function SegmentedControl<T extends string>({ options, value, onChange, label, className }: SegmentedControlProps<T>) {
  const id = React.useId();
  const reduce = useReducedMotion();
  const refs = React.useRef<Array<HTMLButtonElement | null>>([]);
  const current = Math.max(0, options.findIndex((o) => o.value === value));

  function onKey(e: React.KeyboardEvent) {
    const step = e.key === "ArrowRight" || e.key === "ArrowDown" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowUp" ? -1 : 0;
    const jump = e.key === "Home" ? 0 : e.key === "End" ? options.length - 1 : null;
    if (!step && jump === null) return;
    e.preventDefault();
    const next = jump ?? (current + step + options.length) % options.length;
    onChange(options[next].value);
    refs.current[next]?.focus();
  }

  return (
    <div role="radiogroup" aria-label={label} onKeyDown={onKey}
      className={cn("inline-flex rounded-[calc(var(--radius)+4px)] bg-muted p-1", className)}>
      {options.map((o, i) => {
        const on = i === current;
        return (
          <button
            key={o.value}
            ref={(el) => { refs.current[i] = el; }}
            type="button"
            role="radio"
            aria-checked={on}
            tabIndex={on ? 0 : -1}
            onClick={() => onChange(o.value)}
            className={cn(
              "relative h-9 min-w-10 rounded-[var(--radius)] px-3 text-sm font-medium transition-colors",
              "outline-none focus-visible:ring-2 focus-visible:ring-ring",
              on ? "text-foreground" : "text-muted-foreground hover:text-foreground",
            )}
          >
            {on && (
              <motion.span layoutId={`${id}-thumb`} transition={reduce ? { duration: 0 } : lively}
                className="absolute inset-0 rounded-[var(--radius)] bg-background shadow-[var(--shadow-sm)]" />
            )}
            <span className="relative">{o.label}</span>
          </button>
        );
      })}
    </div>
  );
}
