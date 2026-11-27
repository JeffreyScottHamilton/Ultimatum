"use client";
import * as React from "react";
import { useInView, useReducedMotion } from "motion/react";
import { cn } from "./cn";

export interface ScrambleTextProps {
  text: string;
  /** Characters drawn while scrambling. */
  glyphs?: string;
  /** Total time in ms. */
  duration?: number;
  className?: string;
}

/**
 * Letters flicker through random glyphs and lock in left to right, like a terminal resolving.
 * Runs once on view, keeps width steady with a mono face, and reads as the real text to
 * screen readers. Reduced motion shows the text at once.
 */
export function ScrambleText({ text, glyphs = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#%&*+", duration = 900, className }: ScrambleTextProps) {
  const ref = React.useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true });
  const reduce = useReducedMotion();
  const [shown, setShown] = React.useState(text);

  React.useEffect(() => {
    if (!inView || reduce) { setShown(text); return; }
    let raf = 0;
    const t0 = performance.now();
    const tick = (now: number) => {
      const p = Math.min(1, (now - t0) / duration);
      const locked = Math.floor(p * text.length);
      setShown(text.split("").map((ch, i) =>
        i < locked || ch === " " ? ch : glyphs[Math.floor(Math.random() * glyphs.length)]).join(""));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [inView, reduce, text, glyphs, duration]);

  return (
    <span ref={ref} className={cn("font-mono tabular-nums", className)}>
      <span aria-hidden="true">{shown}</span>
      <span className="sr-only">{text}</span>
    </span>
  );
}
