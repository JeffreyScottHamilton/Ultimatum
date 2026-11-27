"use client";
import * as React from "react";
import { motion, useReducedMotion } from "motion/react";
import { cn } from "./cn";

export interface RatingProps {
  value: number;
  onChange: (value: number) => void;
  max?: number;
  label: string;
  className?: string;
}

/**
 * Star rating as a native radio group (arrow keys, one tab stop), with a hover preview and a
 * small pop on the chosen star. The radios are visually hidden but real, so forms and screen
 * readers get the value for free.
 */
export function Rating({ value, onChange, max = 5, label, className }: RatingProps) {
  const reduce = useReducedMotion();
  const name = React.useId();
  const [hover, setHover] = React.useState(0);
  const shown = hover || value;
  return (
    <fieldset className={cn("m-0 border-0 p-0", className)} onPointerLeave={() => setHover(0)}>
      <legend className="sr-only">{label}</legend>
      <div className="flex">
        {Array.from({ length: max }, (_, i) => {
          const n = i + 1, on = n <= shown;
          return (
            <label key={n} onPointerEnter={() => setHover(n)}
              className="relative grid size-10 cursor-pointer place-items-center rounded-[var(--radius)] has-[:focus-visible]:ring-2 has-[:focus-visible]:ring-ring">
              <input type="radio" name={name} value={n} checked={value === n} onChange={() => onChange(n)} className="sr-only" />
              <span className="sr-only">{n} of {max}</span>
              <motion.svg aria-hidden="true" viewBox="0 0 24 24" className={cn("size-6 transition-colors", on ? "text-warning" : "text-muted-foreground/40")}
                initial={false} animate={value === n && !reduce ? { scale: [1, 1.25, 1] } : { scale: 1 }} transition={{ duration: 0.3 }}
                fill="currentColor"><path d="m12 2.5 2.9 6 6.6.8-4.9 4.6 1.3 6.5L12 17.2l-5.9 3.2 1.3-6.5L2.5 9.3l6.6-.8Z" /></motion.svg>
            </label>
          );
        })}
      </div>
    </fieldset>
  );
}

export interface QuickFeedbackProps {
  question?: string;
  onSubmit: (vote: "up" | "down", note: string) => void;
  className?: string;
}

/**
 * "Was this helpful?" with two choices; choosing one opens an optional note field in place and
 * ends with a thank-you, all without moving the page around it.
 */
export function QuickFeedback({ question = "Was this helpful?", onSubmit, className }: QuickFeedbackProps) {
  const reduce = useReducedMotion();
  const [vote, setVote] = React.useState<"up" | "down" | null>(null);
  const [note, setNote] = React.useState("");
  const [sent, setSent] = React.useState(false);
  const btn = "inline-flex h-10 items-center gap-1.5 rounded-[var(--radius)] border border-border px-3 text-sm transition-colors hover:bg-muted outline-none focus-visible:ring-2 focus-visible:ring-ring aria-pressed:border-primary aria-pressed:bg-muted";
  return (
    <motion.div layout={!reduce} className={cn("rounded-[calc(var(--radius)*2)] border border-border bg-card p-4", className)}>
      {sent ? (
        <p role="status" className="m-0 text-sm text-foreground">Thanks, that helps.</p>
      ) : (
        <>
          <div className="flex flex-wrap items-center gap-2">
            <span className="mr-auto text-sm text-foreground">{question}</span>
            <button type="button" aria-pressed={vote === "up"} onClick={() => setVote("up")} className={btn}>Yes</button>
            <button type="button" aria-pressed={vote === "down"} onClick={() => setVote("down")} className={btn}>No</button>
          </div>
          {vote && (
            <motion.form initial={reduce ? false : { opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }}
              onSubmit={(e) => { e.preventDefault(); onSubmit(vote, note); setSent(true); }} className="mt-3 flex gap-2">
              <label className="sr-only" htmlFor="qf-note">Anything to add? (optional)</label>
              <input id="qf-note" value={note} onChange={(e) => setNote(e.target.value)} placeholder="Anything to add? (optional)"
                className="h-10 min-w-0 flex-1 rounded-[var(--radius)] border border-input bg-background px-3 text-sm text-foreground outline-none focus:border-ring focus:ring-2 focus:ring-ring/30" />
              <button type="submit" className="h-10 rounded-[var(--radius)] bg-primary px-4 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary-hover outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">Send</button>
            </motion.form>
          )}
        </>
      )}
    </motion.div>
  );
}
