"use client";
import * as React from "react";
import { cn } from "./cn";

export interface FloatingInputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "placeholder"> {
  label: string;
  /** Shown under the field; turns into the error when `error` is set. */
  hint?: string;
  error?: string;
}

/**
 * A text field whose label sits inside and floats up on focus or when filled. Pure CSS (peer
 * selectors), so it works without JavaScript; the label is a real <label>, and hint and error
 * are wired with aria-describedby and aria-invalid.
 */
export const FloatingInput = React.forwardRef<HTMLInputElement, FloatingInputProps>(function FloatingInput(
  { label, hint, error, id, className, ...props }, ref,
) {
  const auto = React.useId();
  const inputId = id ?? auto;
  const noteId = `${inputId}-note`;
  return (
    <div className={cn("relative", className)}>
      <input
        ref={ref}
        id={inputId}
        placeholder=" "
        aria-invalid={error ? true : undefined}
        aria-describedby={hint || error ? noteId : undefined}
        className={cn(
          "peer h-14 w-full rounded-[var(--radius)] border bg-background px-3 pb-2 pt-6 text-base text-foreground transition-[border-color,box-shadow]",
          "outline-none focus:border-ring focus:ring-2 focus:ring-ring/30",
          error ? "border-destructive" : "border-input",
        )}
        {...props}
      />
      <label
        htmlFor={inputId}
        className={cn(
          "pointer-events-none absolute left-3 top-1/2 origin-left -translate-y-1/2 text-base text-muted-foreground transition-[transform,top,color] duration-150 ease-out",
          "peer-focus:top-4 peer-focus:scale-75 peer-[:not(:placeholder-shown)]:top-4 peer-[:not(:placeholder-shown)]:scale-75",
          "motion-reduce:transition-none",
          error ? "peer-focus:text-destructive" : "peer-focus:text-foreground",
        )}
      >
        {label}
      </label>
      {(hint || error) && (
        <p id={noteId} role={error ? "alert" : undefined}
          className={cn("m-0 mt-1.5 text-sm", error ? "text-destructive" : "text-muted-foreground")}>
          {error ?? hint}
        </p>
      )}
    </div>
  );
});
