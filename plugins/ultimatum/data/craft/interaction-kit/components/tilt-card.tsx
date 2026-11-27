"use client";
import * as React from "react";
import { motion, useMotionTemplate, useMotionValue, useReducedMotion, useSpring, useTransform } from "motion/react";
import { cn } from "./cn";

export interface TiltCardProps {
  children: React.ReactNode;
  /** Maximum tilt in degrees. */
  max?: number;
  /** Show a soft light that follows the pointer. */
  glare?: boolean;
  className?: string;
}

/**
 * A card that tilts in 3D toward a fine pointer, with an optional moving highlight. Flat for touch
 * and reduced motion. Keep the content readable at full tilt; this is a garnish, not a layout.
 */
export function TiltCard({ children, max = 8, glare = true, className }: TiltCardProps) {
  const reduce = useReducedMotion();
  const px = useMotionValue(0.5);
  const py = useMotionValue(0.5);
  const spring = { stiffness: 180, damping: 20, mass: 0.5 };
  const rx = useSpring(useTransform(py, [0, 1], [max, -max]), spring);
  const ry = useSpring(useTransform(px, [0, 1], [-max, max]), spring);
  const gx = useTransform(px, (v) => `${v * 100}%`);
  const gy = useTransform(py, (v) => `${v * 100}%`);
  const light = useMotionTemplate`radial-gradient(28rem circle at ${gx} ${gy}, color-mix(in oklab, var(--foreground) 10%, transparent), transparent 60%)`;

  function move(e: React.PointerEvent<HTMLDivElement>) {
    if (reduce || e.pointerType !== "mouse") return;
    const r = e.currentTarget.getBoundingClientRect();
    px.set((e.clientX - r.left) / r.width);
    py.set((e.clientY - r.top) / r.height);
  }
  function leave() { px.set(0.5); py.set(0.5); }

  return (
    <div className="[perspective:900px]">
      <motion.div
        onPointerMove={move}
        onPointerLeave={leave}
        style={reduce ? undefined : { rotateX: rx, rotateY: ry, transformStyle: "preserve-3d" }}
        className={cn("relative overflow-hidden rounded-[calc(var(--radius)*2)] border border-border bg-card", className)}
      >
        {children}
        {glare && !reduce && (
          <motion.div aria-hidden="true" className="pointer-events-none absolute inset-0" style={{ background: light }} />
        )}
      </motion.div>
    </div>
  );
}
