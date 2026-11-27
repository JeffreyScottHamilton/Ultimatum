"use client";
import * as React from "react";
import { animate, useInView, useReducedMotion } from "motion/react";
import { cn } from "./cn";

export interface NumberTickerProps {
  value: number;
  /** Intl options, e.g. { style: "currency", currency: "USD" }. */
  format?: Intl.NumberFormatOptions;
  locale?: string;
  /** Count up only once the number scrolls into view. */
  startOnView?: boolean;
  duration?: number;
  className?: string;
}

/**
 * A number that rolls to its value. Digits are tabular so the width never jumps, screen
 * readers get the final value only, and with reduced motion the value simply appears.
 */
export function NumberTicker({ value, format, locale, startOnView = true, duration = 1.1, className }: NumberTickerProps) {
  const ref = React.useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true, margin: "-10% 0px" });
  const reduce = useReducedMotion();
  const fmt = React.useMemo(() => new Intl.NumberFormat(locale, format), [locale, format]);
  const from = React.useRef(0);

  React.useEffect(() => {
    const el = ref.current;
    if (!el || (startOnView && !inView)) return;
    if (reduce) { el.textContent = fmt.format(value); from.current = value; return; }
    const controls = animate(from.current, value, {
      duration, ease: [0.16, 1, 0.3, 1],
      onUpdate: (v) => { el.textContent = fmt.format(v); },
    });
    from.current = value;
    return () => controls.stop();
  }, [value, inView, startOnView, reduce, fmt, duration]);

  return (
    <span className={cn("tabular-nums", className)}>
      <span ref={ref} aria-hidden="true">{fmt.format(startOnView ? 0 : value)}</span>
      <span className="sr-only">{fmt.format(value)}</span>
    </span>
  );
}
