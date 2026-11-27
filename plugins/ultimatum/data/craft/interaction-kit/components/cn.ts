/** Join class names, skipping empty values. Small enough that no package is needed. */
export function cn(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

/** The focus ring every interactive part of the kit shares. */
export const focusRing =
  "outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background";

/** Spring used for layout and position changes: quick, no overshoot. */
export const settle = { type: "spring", duration: 0.35, bounce: 0 } as const;

/** Spring for small playful moves (a thumb, a pill) where a touch of overshoot reads as physical. */
export const lively = { type: "spring", duration: 0.45, bounce: 0.18 } as const;
