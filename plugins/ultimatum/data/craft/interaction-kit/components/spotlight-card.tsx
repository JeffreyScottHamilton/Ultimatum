"use client";
import * as React from "react";
import { motion, useMotionTemplate, useMotionValue, useReducedMotion } from "motion/react";
import { cn } from "./cn";

export interface SpotlightCardProps { children: React.ReactNode; className?: string; }

/**
 * A card whose border lights up where the pointer is, as if a torch were held behind it. The
 * effect is CSS-only on the border (a masked gradient), so content and contrast never change.
 */
export function SpotlightCard({ children, className }: SpotlightCardProps) {
  const reduce = useReducedMotion();
  const x = useMotionValue(-999);
  const y = useMotionValue(-999);
  const ring = useMotionTemplate`radial-gradient(16rem circle at ${x}px ${y}px, var(--primary), transparent 70%)`;

  return (
    <div
      onPointerMove={(e) => {
        if (reduce || e.pointerType !== "mouse") return;
        const r = e.currentTarget.getBoundingClientRect();
        x.set(e.clientX - r.left); y.set(e.clientY - r.top);
      }}
      onPointerLeave={() => { x.set(-999); y.set(-999); }}
      className={cn("group relative rounded-[calc(var(--radius)*2)] border border-border bg-card", className)}
    >
      {!reduce && (
        <motion.div
          aria-hidden="true"
          className="pointer-events-none absolute -inset-px rounded-[inherit] p-px opacity-0 transition-opacity duration-300 group-hover:opacity-100"
          style={{
            background: ring,
            WebkitMask: "linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0)",
            WebkitMaskComposite: "xor",
            maskComposite: "exclude",
          }}
        />
      )}
      <div className="relative">{children}</div>
    </div>
  );
}
