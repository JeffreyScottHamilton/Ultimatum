"use client";
import * as React from "react";
import { Reorder, useDragControls, useReducedMotion } from "motion/react";
import { cn } from "./cn";

export interface ReorderItem { id: string; label: React.ReactNode; }

export interface ReorderListProps {
  items: ReorderItem[];
  onReorder: (items: ReorderItem[]) => void;
  label: string;
  className?: string;
}

function Row({ item, index, count, move }: { item: ReorderItem; index: number; count: number; move: (from: number, to: number) => void }) {
  const controls = useDragControls();
  const reduce = useReducedMotion();
  return (
    <Reorder.Item value={item} dragListener={false} dragControls={controls}
      whileDrag={reduce ? undefined : { scale: 1.02, boxShadow: "var(--shadow-md)" }}
      className="flex items-center gap-2 rounded-[var(--radius)] border border-border bg-card pr-3 text-sm text-foreground">
      <button
        type="button"
        aria-label={`Move ${typeof item.label === "string" ? item.label : "item"}, position ${index + 1} of ${count}. Use arrow keys.`}
        onPointerDown={(e) => controls.start(e)}
        onKeyDown={(e) => {
          if (e.key === "ArrowUp" && index > 0) { e.preventDefault(); move(index, index - 1); }
          if (e.key === "ArrowDown" && index < count - 1) { e.preventDefault(); move(index, index + 1); }
        }}
        className="grid h-11 w-10 shrink-0 cursor-grab touch-none place-items-center rounded-[var(--radius)] text-muted-foreground active:cursor-grabbing outline-none focus-visible:ring-2 focus-visible:ring-ring"
      >
        <svg aria-hidden="true" viewBox="0 0 24 24" className="size-4" fill="currentColor">
          <circle cx="9" cy="6" r="1.5" /><circle cx="15" cy="6" r="1.5" /><circle cx="9" cy="12" r="1.5" /><circle cx="15" cy="12" r="1.5" /><circle cx="9" cy="18" r="1.5" /><circle cx="15" cy="18" r="1.5" />
        </svg>
      </button>
      <span className="flex-1">{item.label}</span>
    </Reorder.Item>
  );
}

/**
 * A list you reorder by dragging the grip, or by focusing the grip and pressing Up or Down
 * (drag-only lists lock out keyboard users). Moves are announced; neighbours glide aside.
 */
export function ReorderList({ items, onReorder, label, className }: ReorderListProps) {
  const [said, setSaid] = React.useState("");
  const move = (from: number, to: number) => {
    const next = [...items];
    const [it] = next.splice(from, 1);
    next.splice(to, 0, it);
    onReorder(next);
    setSaid(`Moved to position ${to + 1} of ${items.length}`);
    window.setTimeout(() => (document.querySelectorAll<HTMLButtonElement>(`[data-reorder="${label}"] li button`)[to])?.focus(), 0);
  };
  return (
    <div data-reorder={label}>
      <Reorder.Group axis="y" values={items} onReorder={onReorder} aria-label={label} className={cn("m-0 flex list-none flex-col gap-2 p-0", className)}>
        {items.map((it, i) => <Row key={it.id} item={it} index={i} count={items.length} move={move} />)}
      </Reorder.Group>
      <p className="sr-only" aria-live="assertive">{said}</p>
    </div>
  );
}
