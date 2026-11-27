"use client";
import * as React from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { cn, focusRing } from "./cn";

export interface CopyButtonProps {
  /** Text placed on the clipboard. */
  value: string;
  /** Accessible name; defaults to "Copy". */
  label?: string;
  /** How long the tick stays, in ms. */
  resetAfter?: number;
  className?: string;
  onCopied?: (value: string) => void;
}

const swap = { type: "spring", duration: 0.3, bounce: 0 } as const;

/** Icon button that copies, swaps its icon for a tick, and announces the copy to screen readers. */
export function CopyButton({ value, label = "Copy", resetAfter = 1600, className, onCopied }: CopyButtonProps) {
  const [copied, setCopied] = React.useState(false);
  const [failed, setFailed] = React.useState(false);
  const reduce = useReducedMotion();
  React.useEffect(() => {
    if (!copied && !failed) return;
    const t = window.setTimeout(() => { setCopied(false); setFailed(false); }, resetAfter);
    return () => window.clearTimeout(t);
  }, [copied, failed, resetAfter]);

  async function copy() {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      onCopied?.(value);
    } catch {
      setFailed(true);
    }
  }

  const fade = reduce
    ? { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 } }
    : { initial: { scale: 0.8, opacity: 0, filter: "blur(2px)" }, animate: { scale: 1, opacity: 1, filter: "blur(0px)" },
        exit: { scale: 0.8, opacity: 0, filter: "blur(2px)" } };

  return (
    <button
      type="button"
      onClick={copy}
      aria-label={copied ? "Copied" : label}
      className={cn(
        "relative inline-grid size-10 place-items-center rounded-[var(--radius)] text-muted-foreground",
        "transition-colors hover:bg-muted hover:text-foreground active:scale-[0.96] motion-reduce:active:scale-100",
        focusRing, className,
      )}
    >
      <AnimatePresence initial={false} mode="popLayout">
        {copied ? (
          <motion.svg key="tick" viewBox="0 0 16 16" className="size-4 text-success" aria-hidden="true" transition={swap} {...fade}>
            <path d="M3.5 8.5l3 3 6-7" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </motion.svg>
        ) : (
          <motion.svg key="copy" viewBox="0 0 16 16" className="size-4" aria-hidden="true" transition={swap} {...fade}>
            <rect x="5.5" y="5.5" width="8" height="8" rx="1.5" fill="none" stroke="currentColor" strokeWidth="1.5" />
            <path d="M10.5 3.5v-.5A1.5 1.5 0 0 0 9 1.5H4A1.5 1.5 0 0 0 2.5 3v5A1.5 1.5 0 0 0 4 9.5h.5" fill="none" stroke="currentColor" strokeWidth="1.5" />
          </motion.svg>
        )}
      </AnimatePresence>
      <span className="sr-only" role="status">{copied ? "Copied to clipboard" : failed ? "Copy failed" : ""}</span>
    </button>
  );
}
