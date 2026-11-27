"use client";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { cn, focusRing } from "./cn";

export interface ThemeToggleProps {
  theme: "light" | "dark";
  onToggle: () => void;
  className?: string;
}

/**
 * A sun/moon switch: the icon turns and swaps with a short blur. It is a real switch
 * (role="switch", aria-checked) with a stable label, so the state is announced, not guessed
 * from the icon.
 */
export function ThemeToggle({ theme, onToggle, className }: ThemeToggleProps) {
  const reduce = useReducedMotion();
  const dark = theme === "dark";
  const swap = reduce
    ? { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 } }
    : {
        initial: { opacity: 0, rotate: -90, scale: 0.5, filter: "blur(4px)" },
        animate: { opacity: 1, rotate: 0, scale: 1, filter: "blur(0px)" },
        exit: { opacity: 0, rotate: 90, scale: 0.5, filter: "blur(4px)" },
      };
  return (
    <button type="button" role="switch" aria-checked={dark} aria-label="Dark theme" onClick={onToggle}
      className={cn("grid size-10 place-items-center rounded-full text-foreground transition-colors hover:bg-muted active:scale-[0.96] motion-reduce:active:scale-100", focusRing, className)}>
      <AnimatePresence mode="popLayout" initial={false}>
        <motion.svg key={theme} aria-hidden="true" viewBox="0 0 24 24" className="size-5" {...swap}
          transition={{ type: "spring", duration: 0.35, bounce: 0 }}
          fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
          {dark
            ? <path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z" />
            : <><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" /></>}
        </motion.svg>
      </AnimatePresence>
    </button>
  );
}
