"use client";
import * as React from "react";
import { motion, useMotionValue, useReducedMotion, useSpring } from "motion/react";
import { cn } from "./cn";

export interface MagneticProps {
  children: React.ReactNode;
  /** How far the child follows the pointer, 0 to 1. */
  strength?: number;
  className?: string;
}

/**
 * Wrap a button or link so it leans toward a fine pointer near it. Off for touch,
 * keyboard and reduced motion, where following a cursor means nothing or distracts.
 */
export function Magnetic({ children, strength = 0.3, className }: MagneticProps) {
  const ref = React.useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();
  const x = useSpring(useMotionValue(0), { stiffness: 220, damping: 18, mass: 0.4 });
  const y = useSpring(useMotionValue(0), { stiffness: 220, damping: 18, mass: 0.4 });

  function move(e: React.PointerEvent<HTMLDivElement>) {
    if (reduce || e.pointerType !== "mouse" || !ref.current) return;
    const r = ref.current.getBoundingClientRect();
    x.set((e.clientX - (r.left + r.width / 2)) * strength);
    y.set((e.clientY - (r.top + r.height / 2)) * strength);
  }
  function leave() { x.set(0); y.set(0); }

  return (
    <motion.div
      ref={ref}
      onPointerMove={move}
      onPointerLeave={leave}
      style={reduce ? undefined : { x, y }}
      className={cn("inline-block p-3 -m-3", className)}
    >
      {children}
    </motion.div>
  );
}
