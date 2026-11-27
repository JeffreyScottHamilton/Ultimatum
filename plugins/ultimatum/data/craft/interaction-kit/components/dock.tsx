"use client";
import * as React from "react";
import { motion, useMotionValue, useReducedMotion, useSpring, useTransform, type MotionValue } from "motion/react";
import { cn } from "./cn";

export interface DockItem { id: string; label: string; icon: React.ReactNode; href?: string; onSelect?: () => void; }

export interface DockProps { items: DockItem[]; label?: string; className?: string; }

function DockIcon({ item, mouseX, reduce }: { item: DockItem; mouseX: MotionValue<number>; reduce: boolean }) {
  const ref = React.useRef<HTMLElement>(null);
  const dist = useTransform(mouseX, (x) => {
    const r = ref.current?.getBoundingClientRect();
    return r ? x - (r.left + r.width / 2) : Infinity;
  });
  const size = useSpring(useTransform(dist, [-140, 0, 140], [44, 68, 44]), { stiffness: 260, damping: 22, mass: 0.3 });
  const cls = "group relative grid aspect-square place-items-center rounded-[calc(var(--radius)+4px)] bg-muted text-foreground transition-colors hover:bg-accent outline-none focus-visible:ring-2 focus-visible:ring-ring";
  const tip = (
    <span role="tooltip" className="pointer-events-none absolute -top-9 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-[var(--radius)] bg-foreground px-2 py-1 text-xs text-background opacity-0 transition-opacity group-hover:opacity-100 group-focus-visible:opacity-100">
      {item.label}
    </span>
  );
  const style = reduce ? { width: 48 } : { width: size };
  return item.href ? (
    <motion.a ref={ref as React.Ref<HTMLAnchorElement>} href={item.href} aria-label={item.label} style={style} className={cls}>
      <span aria-hidden="true" className="size-1/2">{item.icon}</span>{tip}
    </motion.a>
  ) : (
    <motion.button ref={ref as React.Ref<HTMLButtonElement>} type="button" aria-label={item.label} onClick={item.onSelect} style={style} className={cls}>
      <span aria-hidden="true" className="size-1/2">{item.icon}</span>{tip}
    </motion.button>
  );
}

/**
 * An app dock whose icons swell as a fine pointer passes over them, neighbours growing a little
 * less. Every item is a labelled link or button with a tooltip on hover and focus; touch,
 * keyboard and reduced motion get a steady row.
 */
export function Dock({ items, label = "Dock", className }: DockProps) {
  const reduce = useReducedMotion() ?? false;
  const mouseX = useMotionValue(Infinity);
  return (
    <nav aria-label={label}>
      <motion.ul
        onPointerMove={(e) => { if (e.pointerType === "mouse") mouseX.set(e.clientX); }}
        onPointerLeave={() => mouseX.set(Infinity)}
        className={cn("m-0 flex h-[4.5rem] list-none items-end gap-2 rounded-[calc(var(--radius)*2+4px)] border border-border bg-background/80 px-3 pb-2.5 backdrop-blur", className)}
      >
        {items.map((it) => <li key={it.id}><DockIcon item={it} mouseX={mouseX} reduce={reduce} /></li>)}
      </motion.ul>
    </nav>
  );
}
