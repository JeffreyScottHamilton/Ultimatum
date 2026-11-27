"use client";
import * as React from "react";
import { AnimatePresence, motion, useMotionValue, useReducedMotion, useTransform, type PanInfo } from "motion/react";
import { cn, focusRing } from "./cn";

export interface SwipeCard { id: string; content: React.ReactNode; label: string; }

export interface SwipeDeckProps {
  cards: SwipeCard[];
  onDecide: (card: SwipeCard, choice: "keep" | "skip") => void;
  className?: string;
}

function TopCard({ card, onDone, reduce }: { card: SwipeCard; onDone: (c: "keep" | "skip") => void; reduce: boolean }) {
  const x = useMotionValue(0);
  const rotate = useTransform(x, [-200, 200], [-12, 12]);
  const keepOp = useTransform(x, [20, 120], [0, 1]);
  const skipOp = useTransform(x, [-120, -20], [1, 0]);
  function end(_: unknown, info: PanInfo) {
    if (info.offset.x > 120 || info.velocity.x > 600) onDone("keep");
    else if (info.offset.x < -120 || info.velocity.x < -600) onDone("skip");
  }
  return (
    <motion.div
      drag={reduce ? false : "x"}
      dragSnapToOrigin
      onDragEnd={end}
      style={{ x, rotate: reduce ? 0 : rotate }}
      exit={reduce ? { opacity: 0 } : { x: x.get() >= 0 ? 400 : -400, opacity: 0, transition: { duration: 0.25 } }}
      className="absolute inset-0 cursor-grab touch-pan-y overflow-hidden rounded-[calc(var(--radius)*2)] border border-border bg-card shadow-[var(--shadow-md)] active:cursor-grabbing"
    >
      {card.content}
      <motion.span aria-hidden="true" style={{ opacity: keepOp }} className="absolute left-4 top-4 rounded-[var(--radius)] border-2 border-success px-2 py-0.5 text-sm font-semibold text-success">KEEP</motion.span>
      <motion.span aria-hidden="true" style={{ opacity: skipOp }} className="absolute right-4 top-4 rounded-[var(--radius)] border-2 border-destructive px-2 py-0.5 text-sm font-semibold text-destructive">SKIP</motion.span>
    </motion.div>
  );
}

/**
 * A stack of cards you flick right to keep or left to skip, with the tilt and stamp following
 * your finger. The same choices are always available as two buttons (and the arrow keys), so
 * nobody has to drag.
 */
export function SwipeDeck({ cards, onDecide, className }: SwipeDeckProps) {
  const reduce = useReducedMotion() ?? false;
  const [i, setI] = React.useState(0);
  const card = cards[i];
  const decide = (c: "keep" | "skip") => { if (!card) return; onDecide(card, c); setI((n) => n + 1); };
  const btn = cn("grid size-12 place-items-center rounded-full border border-border bg-background transition-colors hover:bg-muted", focusRing);

  return (
    <div className={className} onKeyDown={(e) => { if (e.key === "ArrowRight") decide("keep"); if (e.key === "ArrowLeft") decide("skip"); }}>
      <div className="relative aspect-[3/4] w-full">
        {cards[i + 1] && <div aria-hidden="true" className="absolute inset-0 translate-y-2 scale-[0.96] rounded-[calc(var(--radius)*2)] border border-border bg-card" />}
        <AnimatePresence initial={false}>
          {card ? <TopCard key={card.id} card={card} onDone={decide} reduce={reduce} />
            : <p className="absolute inset-0 m-0 grid place-items-center text-sm text-muted-foreground">All done</p>}
        </AnimatePresence>
      </div>
      <div className="mt-4 flex justify-center gap-4">
        <button type="button" disabled={!card} aria-label={card ? `Skip ${card.label}` : "Skip"} onClick={() => decide("skip")} className={cn(btn, "text-destructive")}>
          <svg aria-hidden="true" viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round"><path d="M18 6 6 18M6 6l12 12" /></svg>
        </button>
        <button type="button" disabled={!card} aria-label={card ? `Keep ${card.label}` : "Keep"} onClick={() => decide("keep")} className={cn(btn, "text-success")}>
          <svg aria-hidden="true" viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"><path d="M5 12.5 10 17 19 7" /></svg>
        </button>
      </div>
      <p className="sr-only" aria-live="polite">{card ? `${card.label}, ${cards.length - i} left` : "No cards left"}</p>
    </div>
  );
}
