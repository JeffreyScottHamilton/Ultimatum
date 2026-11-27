"use client";
import * as React from "react";
import { cn, focusRing } from "./cn";

export interface CarouselProps {
  slides: React.ReactNode[];
  label: string;
  /** Width of each slide, any CSS length. */
  slideWidth?: string;
  className?: string;
}

/**
 * A swipeable row built on native scroll snapping (so momentum, trackpads and touch feel right)
 * with previous/next buttons that disable at the ends and dots that track the visible slide.
 * Follows the ARIA carousel pattern: region, slide groups with "n of m" labels, no autoplay.
 */
export function Carousel({ slides, label, slideWidth = "min(85%, 22rem)", className }: CarouselProps) {
  const track = React.useRef<HTMLDivElement>(null);
  const [index, setIndex] = React.useState(0);

  React.useEffect(() => {
    const el = track.current;
    if (!el) return;
    const io = new IntersectionObserver((entries) => {
      for (const en of entries) if (en.isIntersecting) setIndex(Number((en.target as HTMLElement).dataset.i));
    }, { root: el, threshold: 0.6 });
    el.querySelectorAll("[data-i]").forEach((li) => io.observe(li));
    return () => io.disconnect();
  }, [slides.length]);

  const go = (i: number) => {
    const li = track.current?.children[i] as HTMLElement | undefined;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    li?.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "nearest", inline: "start" });
  };
  const arrow = cn("grid size-10 place-items-center rounded-full border border-border bg-background text-foreground transition-[background-color,opacity] hover:bg-muted disabled:opacity-40", focusRing);

  return (
    <section aria-roledescription="carousel" aria-label={label} className={cn("w-full [contain:inline-size]", className)}>
      <div ref={track} tabIndex={0} aria-label={`${label}, scrollable`} className="flex snap-x snap-mandatory gap-4 overflow-x-auto overscroll-x-contain scroll-smooth p-0 pb-2 [scrollbar-width:none] outline-none focus-visible:ring-2 focus-visible:ring-ring motion-reduce:scroll-auto">
        {slides.map((s, i) => (
          <div key={i} data-i={i} role="group" aria-roledescription="slide" aria-label={`${i + 1} of ${slides.length}`}
            className="shrink-0 snap-start" style={{ width: slideWidth }}>{s}</div>
        ))}
      </div>
      <div className="mt-3 flex items-center gap-2">
        <button type="button" aria-label="Previous slide" disabled={index === 0} onClick={() => go(index - 1)} className={arrow}>
          <svg aria-hidden="true" viewBox="0 0 24 24" className="size-4" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"><path d="m15 18-6-6 6-6" /></svg>
        </button>
        <button type="button" aria-label="Next slide" disabled={index === slides.length - 1} onClick={() => go(index + 1)} className={arrow}>
          <svg aria-hidden="true" viewBox="0 0 24 24" className="size-4" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"><path d="m9 18 6-6-6-6" /></svg>
        </button>
        <div className="ml-auto flex gap-1" aria-hidden="true">
          {slides.map((_, i) => (
            <span key={i} className={cn("h-1.5 rounded-full transition-[width,background-color] duration-300 motion-reduce:transition-none", i === index ? "w-5 bg-foreground" : "w-1.5 bg-border")} />
          ))}
        </div>
        <p className="sr-only" aria-live="polite">Slide {index + 1} of {slides.length}</p>
      </div>
    </section>
  );
}
