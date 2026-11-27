"use client";
import * as React from "react";
import { cn } from "./cn";

export interface BorderBeamProps {
  children: React.ReactNode;
  /** Seconds per lap. */
  duration?: number;
  className?: string;
}

/**
 * A short streak of light that travels around the border, for the one card or input you want
 * noticed. Built from a rotating conic gradient behind a 1px mask; it stops under reduced motion.
 * Use once per screen at most.
 */
export function BorderBeam({ children, duration = 6, className }: BorderBeamProps) {
  return (
    <div className={cn("relative rounded-[calc(var(--radius)*2)] p-px", className)}
      style={{ "--beam-duration": `${duration}s` } as React.CSSProperties}>
      <style>{"@property --beam-angle{syntax:'<angle>';inherits:false;initial-value:0deg}@keyframes ult-beam{to{--beam-angle:360deg}}"}</style>
      <span
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 rounded-[inherit] animate-[ult-beam_var(--beam-duration)_linear_infinite] motion-reduce:animate-none"
        style={{ background: "conic-gradient(from var(--beam-angle), transparent 0 80%, var(--primary) 90%, transparent 100%), var(--border)" }}
      />
      <div className="relative rounded-[calc(var(--radius)*2-1px)] bg-card">{children}</div>
    </div>
  );
}

/** Text with a slow sheen passing over it; for a single label such as "New". Static when reduced. */
export function ShimmerText({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <span
      className={cn(
        "bg-[linear-gradient(110deg,var(--muted-foreground)_35%,var(--foreground)_50%,var(--muted-foreground)_65%)] bg-[length:250%_100%] bg-clip-text text-transparent",
        "animate-[ult-shimmer_2.4s_linear_infinite] motion-reduce:animate-none motion-reduce:text-foreground",
        className,
      )}
    >
      <style>{"@keyframes ult-shimmer{from{background-position:100% 0}to{background-position:-150% 0}}"}</style>
      {children}
    </span>
  );
}
