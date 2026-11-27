"use client";
import * as React from "react";
import { motion, useReducedMotion } from "motion/react";
import { cn } from "./cn";

export interface OtpInputProps {
  length?: number;
  value: string;
  onChange: (value: string) => void;
  /** Called once every box is filled. */
  onComplete?: (value: string) => void;
  label?: string;
  invalid?: boolean;
  className?: string;
}

/**
 * One-time-code boxes built on a single hidden-in-plain-sight input, so paste, autofill
 * (autocomplete="one-time-code"), backspace and screen readers all work natively. The boxes are
 * drawn from the value; the active one shows a blinking caret, and an error shakes the row once.
 */
export function OtpInput({ length = 6, value, onChange, onComplete, label = "Verification code", invalid, className }: OtpInputProps) {
  const reduce = useReducedMotion();
  const [focused, setFocused] = React.useState(false);
  const ref = React.useRef<HTMLInputElement>(null);
  const active = Math.min(value.length, length - 1);

  return (
    <motion.label
      className={cn("relative inline-flex gap-2", className)}
      animate={invalid && !reduce ? { x: [0, -6, 6, -4, 4, 0] } : { x: 0 }}
      transition={{ duration: 0.36 }}
    >
      <input
        ref={ref}
        aria-label={label}
        aria-invalid={invalid || undefined}
        inputMode="numeric"
        autoComplete="one-time-code"
        pattern="[0-9]*"
        maxLength={length}
        value={value}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        onChange={(e) => {
          const v = e.target.value.replace(/\D/g, "").slice(0, length);
          onChange(v);
          if (v.length === length) onComplete?.(v);
        }}
        className="absolute inset-0 z-10 h-full w-full cursor-text opacity-0 outline-none [caret-color:transparent]"
      />
      {Array.from({ length }, (_, i) => {
        const ch = value[i];
        const on = focused && i === active;
        return (
          <div key={i} aria-hidden="true"
            className={cn(
              "relative grid h-12 w-10 place-items-center rounded-[var(--radius)] border bg-background text-lg font-medium tabular-nums text-foreground transition-[border-color,box-shadow]",
              invalid ? "border-destructive" : on ? "border-ring ring-2 ring-ring/30" : "border-input",
            )}>
            {ch ? (
              <motion.span initial={reduce ? false : { y: 6, opacity: 0 }} animate={{ y: 0, opacity: 1 }}
                transition={{ type: "spring", duration: 0.25, bounce: 0 }}>{ch}</motion.span>
            ) : on ? (
              <span className="h-5 w-px bg-foreground animate-pulse motion-reduce:animate-none" />
            ) : null}
          </div>
        );
      })}
    </motion.label>
  );
}
