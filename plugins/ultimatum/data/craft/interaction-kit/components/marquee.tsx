"use client";
import * as React from "react";
import { cn } from "./cn";

export interface MarqueeProps {
  children: React.ReactNode;
  /** Seconds for one full loop. */
  duration?: number;
  reverse?: boolean;
  /** Pause while hovered or focused. */
  pauseOnHover?: boolean;
  /** Accessible name; the moving copy is hidden from assistive tech. */
  label: string;
  className?: string;
}

/**
 * An endless row (logos, quotes) that loops with a pure CSS transform, edges faded with a mask.
 * The duplicate copy is aria-hidden, and with reduced motion the row stops and wraps instead.
 * `contain: inline-size` keeps the long track from widening a grid or flex parent.
 */
export function Marquee({ children, duration = 30, reverse = false, pauseOnHover = true, label, className }: MarqueeProps) {
  const style = { "--marquee-duration": `${duration}s` } as React.CSSProperties;
  const track = cn(
    "flex shrink-0 items-center gap-[var(--marquee-gap,3rem)] pr-[var(--marquee-gap,3rem)]",
    "animate-[ult-marquee_var(--marquee-duration)_linear_infinite] motion-reduce:animate-none",
    reverse && "[animation-direction:reverse]",
  );
  return (
    <div
      role="region"
      aria-label={label}
      style={style}
      className={cn(
        "group flex w-full overflow-hidden [contain:inline-size] [mask-image:linear-gradient(90deg,transparent,#000_8%,#000_92%,transparent)]",
        "motion-reduce:flex-wrap motion-reduce:[mask-image:none]",
        pauseOnHover && "[&:hover>*]:[animation-play-state:paused] [&:focus-within>*]:[animation-play-state:paused]",
        className,
      )}
    >
      <style>{"@keyframes ult-marquee{to{transform:translateX(-100%)}}"}</style>
      <div className={track}>{children}</div>
      <div className={cn(track, "motion-reduce:hidden")} aria-hidden="true" inert>{children}</div>
    </div>
  );
}
