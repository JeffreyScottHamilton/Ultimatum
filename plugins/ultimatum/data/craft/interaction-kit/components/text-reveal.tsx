"use client";
import { motion, useReducedMotion } from "motion/react";
import { cn } from "./cn";

export interface TextRevealProps {
  /** Plain text; split into words. */
  text: string;
  as?: "h1" | "h2" | "h3" | "p" | "span";
  /** Seconds between words. */
  stagger?: number;
  delay?: number;
  /** Play when scrolled into view (default) or on mount. */
  trigger?: "view" | "mount";
  className?: string;
}

/**
 * Words rise out of a mask one after another, each un-blurring as it lands. The full sentence
 * stays as one string for assistive tech, and reduced motion gets a single fade.
 */
export function TextReveal({ text, as = "h2", stagger = 0.06, delay = 0, trigger = "view", className }: TextRevealProps) {
  const reduce = useReducedMotion();
  const Tag = motion[as];
  const words = text.split(/\s+/).filter(Boolean);
  const play = trigger === "view" ? { whileInView: "shown", viewport: { once: true, margin: "-15% 0px" } } : { animate: "shown" };

  if (reduce) {
    return (
      <Tag className={className} initial={{ opacity: 0 }} {...(trigger === "view"
        ? { whileInView: { opacity: 1 }, viewport: { once: true } } : { animate: { opacity: 1 } })}>
        {text}
      </Tag>
    );
  }
  return (
    <Tag className={cn("text-balance", className)} aria-label={text} initial="hidden" {...play}
      transition={{ staggerChildren: stagger, delayChildren: delay }}>
      {words.map((w, i) => (
        <span key={i} aria-hidden="true" className="inline-block overflow-hidden pb-[0.12em] align-bottom">
          <motion.span
            className="inline-block will-change-transform"
            variants={{
              hidden: { y: "110%", opacity: 0, filter: "blur(6px)" },
              shown: { y: "0%", opacity: 1, filter: "blur(0px)", transition: { type: "spring", duration: 0.7, bounce: 0 } },
            }}
          >
            {w}
          </motion.span>
          {i < words.length - 1 ? " " : null}
        </span>
      ))}
    </Tag>
  );
}
