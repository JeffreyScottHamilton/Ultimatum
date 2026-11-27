"use client";
import * as React from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { settle } from "./cn";

export interface TagInputProps {
  value: string[];
  onChange: (tags: string[]) => void;
  label: string;
  placeholder?: string;
  max?: number;
  className?: string;
}

/**
 * Type and press Enter or comma to add a chip; Backspace on an empty field removes the last one.
 * Chips pop in and out with layout animation, each has its own labelled remove button, and
 * changes are announced politely.
 */
export function TagInput({ value, onChange, label, placeholder = "Add…", max, className }: TagInputProps) {
  const reduce = useReducedMotion();
  const [draft, setDraft] = React.useState("");
  const [said, setSaid] = React.useState("");
  const id = React.useId();

  const add = (raw: string) => {
    const t = raw.trim();
    if (!t || value.includes(t) || (max !== undefined && value.length >= max)) return;
    onChange([...value, t]); setSaid(`${t} added`);
  };
  const remove = (t: string) => { onChange(value.filter((x) => x !== t)); setSaid(`${t} removed`); };

  return (
    <div className={className}>
      <label htmlFor={id} className="mb-1.5 block text-sm font-medium text-foreground">{label}</label>
      <div className="flex min-h-11 flex-wrap items-center gap-1.5 rounded-[var(--radius)] border border-input bg-background p-1.5 transition-[border-color,box-shadow] focus-within:border-ring focus-within:ring-2 focus-within:ring-ring/30">
        <ul className="contents m-0 list-none p-0">
          <AnimatePresence initial={false} mode="popLayout">
            {value.map((t) => (
              <motion.li key={t} layout={!reduce}
                initial={reduce ? { opacity: 0 } : { opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={reduce ? { opacity: 0 } : { opacity: 0, scale: 0.8 }}
                transition={reduce ? { duration: 0 } : settle}
                className="flex h-8 items-center gap-1 rounded-[calc(var(--radius)-2px)] bg-muted pl-2.5 text-sm text-foreground">
                {t}
                <button type="button" aria-label={`Remove ${t}`} onClick={() => remove(t)}
                  className="grid size-8 place-items-center rounded-[calc(var(--radius)-2px)] text-muted-foreground transition-colors hover:text-foreground outline-none focus-visible:ring-2 focus-visible:ring-ring">
                  <svg aria-hidden="true" viewBox="0 0 24 24" className="size-3.5" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round"><path d="M18 6 6 18M6 6l12 12" /></svg>
                </button>
              </motion.li>
            ))}
          </AnimatePresence>
        </ul>
        <input
          id={id}
          value={draft}
          placeholder={placeholder}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === ",") { e.preventDefault(); add(draft); setDraft(""); }
            else if (e.key === "Backspace" && !draft && value.length) remove(value[value.length - 1]);
          }}
          onBlur={() => { if (draft) { add(draft); setDraft(""); } }}
          className="h-8 min-w-24 flex-1 bg-transparent px-1.5 text-sm text-foreground outline-none placeholder:text-muted-foreground"
        />
      </div>
      <p className="sr-only" aria-live="polite">{said}</p>
    </div>
  );
}
