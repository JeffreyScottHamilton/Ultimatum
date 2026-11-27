"use client";
import * as React from "react";
import { cn } from "./cn";

export interface ScrubNumberProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  step?: number;
  /** Pixels of horizontal drag per step. */
  pxPerStep?: number;
  unit?: string;
  className?: string;
}

const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));

/**
 * A design-tool style number field: drag the label sideways to scrub the value, or type into it.
 * It is a real spinbutton (arrows step, Shift+arrows step by ten, Home and End jump to the
 * limits), and dragging locks the pointer so long scrubs do not run off the screen.
 */
export function ScrubNumber({ label, value, onChange, min = -Infinity, max = Infinity, step = 1, pxPerStep = 4, unit, className }: ScrubNumberProps) {
  const id = React.useId();
  const [text, setText] = React.useState(String(value));
  const drag = React.useRef<{ x: number; v: number } | null>(null);
  React.useEffect(() => { setText(String(value)); }, [value]);
  const decimals = (String(step).split(".")[1] ?? "").length;
  const set = (v: number) => onChange(Number(clamp(v, min, max).toFixed(decimals)));

  return (
    <div className={cn("inline-flex h-10 items-center overflow-hidden rounded-[var(--radius)] border border-input bg-background focus-within:border-ring focus-within:ring-2 focus-within:ring-ring/30", className)}>
      <label
        htmlFor={id}
        onPointerDown={(e) => { drag.current = { x: e.clientX, v: value }; e.currentTarget.setPointerCapture(e.pointerId); }}
        onPointerMove={(e) => { if (drag.current) set(drag.current.v + Math.round((e.clientX - drag.current.x) / pxPerStep) * step); }}
        onPointerUp={() => { drag.current = null; }}
        className="flex h-full cursor-ew-resize touch-none select-none items-center border-r border-border px-3 text-xs font-medium text-muted-foreground"
      >
        {label}
      </label>
      <input
        id={id}
        role="spinbutton"
        inputMode="decimal"
        aria-valuenow={value}
        aria-valuemin={Number.isFinite(min) ? min : undefined}
        aria-valuemax={Number.isFinite(max) ? max : undefined}
        aria-valuetext={unit ? `${value} ${unit}` : undefined}
        value={text}
        onChange={(e) => setText(e.target.value)}
        onBlur={() => { const n = parseFloat(text); if (Number.isFinite(n)) set(n); else setText(String(value)); }}
        onKeyDown={(e) => {
          const k = e.shiftKey ? 10 : 1;
          if (e.key === "ArrowUp") { e.preventDefault(); set(value + step * k); }
          else if (e.key === "ArrowDown") { e.preventDefault(); set(value - step * k); }
          else if (e.key === "Home" && Number.isFinite(min)) { e.preventDefault(); set(min); }
          else if (e.key === "End" && Number.isFinite(max)) { e.preventDefault(); set(max); }
          else if (e.key === "Enter") (e.target as HTMLInputElement).blur();
        }}
        className="h-full w-16 bg-transparent px-2 text-right text-sm tabular-nums text-foreground outline-none"
      />
      {unit && <span aria-hidden="true" className="pr-3 text-xs text-muted-foreground">{unit}</span>}
    </div>
  );
}
