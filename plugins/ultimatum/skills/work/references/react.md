# React and Next.js

Read after `ui.md` when the project uses React or Next. Rules are ordered by usual payoff: fix the earlier ones before polishing the later ones. Measure before micro-optimizing; a rule is a prior, not a verdict.

## A. Composition

1. **Prefer composition to boolean flags.** A component with `isCompact`, `withIcon`, `isDanger`, `hasFooter` grows combinatorial states nobody tests. Use `children`/slots and a small `variant` union.
2. **Compound components for related parts** (`Dialog`, `Dialog.Trigger`, `Dialog.Content`) sharing state through context. Callers arrange the pieces; the parent owns behavior.
3. **Lift state only as far as needed.** State used by one subtree lives in that subtree. Context for state many distant components read; not for values that change every keystroke.
4. **Explicit variants beat clever props.** `<Button variant="destructive">` is greppable; computed class strings from three props are not.
5. **Controlled and uncontrolled both** for reusable inputs (`value`/`onChange` and `defaultValue`), so callers pick.
6. **Reuse before create.** Search `components/` and the design system first. Match the project's styling method (CSS modules, Tailwind, tokens).
7. **Forms:** native elements, labels, `name`s; server actions or form submit before bespoke fetch wiring.

## B. Server and client boundaries (App Router)

1. **Server Components by default.** Add `'use client'` only at the leaf that needs state, effects, refs or browser APIs. Marking a layout client-side drags its whole subtree into the bundle.
2. **Push the boundary down.** Keep the page a server component; extract the interactive piece (a button, a form). Pass server-rendered children into client components as props.
3. **Serialize little.** Props crossing the boundary are sent to the browser. Pass the fields needed, not the whole record (and never secrets or other users' fields).
4. **No server-only code in client files.** Use `server-only` imports for modules that touch secrets or the database so the build fails if one leaks.
5. **Server actions are public endpoints.** Authenticate and authorize inside each action; validate input; do not trust hidden fields. See `security/secure-implementation.md`.
6. **Dedupe per-request work** with `React.cache`; decide caching deliberately (what is shared across users must not contain user data).
7. **Hydration:** render the same output on server and client. Time, random, locale and `window` checks belong in effects or behind a mount flag.

## C. Data waterfalls (highest payoff)

1. **Start independent async work together.** `await a(); await b();` serializes; `await Promise.all([a(), b()])` does not.
2. **Start early, await late.** Kick off the promise at the top; await it where the value is first needed.
3. **Move the `await` into the branch that needs it.** Do not fetch what an early return throws away.
4. **Fetch where the data is used** in server components and let siblings run in parallel; avoid parent-awaits-then-child-fetches chains.
5. **Stream.** Wrap slow sections in `<Suspense fallback=...>` so the shell and fast parts arrive first; keep fallbacks the same size as the content (prevents layout shift).
6. **Client fetching:** use one data layer (SWR/React Query/loader) with request dedupe; do not fetch in an effect per component mount.

## D. Bundle size

1. **Import from the module, not a barrel** when the barrel re-exports a large library (`lucide-react/icons/x`, `lodash/debounce`) or check the package's tree-shaking support.
2. **Dynamically import heavy, rare UI** (editors, charts, maps, modals opened on click) with `next/dynamic` / `React.lazy`; give a stable-size fallback.
3. **Load analytics, chat widgets and A/B code after hydration or on idle**, not in the critical path.
4. **Preload on intent:** start the dynamic import on hover/focus of the trigger.
5. **Check, don't guess:** build with the analyzer (`@next/bundle-analyzer`, `vite-bundle-visualizer`); compare route sizes before and after.
6. Images through the framework image component with explicit sizes; fonts via the framework font loader (no layout shift, no render-blocking CSS import).

## E. Re-render cost

1. **Derive, don't sync.** Values computable from props/state are computed in render; an effect that sets state from other state is a bug magnet and a double render.
2. **Do not subscribe to what you only read in a handler.** Read from a ref or the store at event time.
3. **Subscribe to the smallest slice** (a derived boolean, one field) from stores/context, so unrelated updates skip you.
4. **Functional updates** (`setN(n => n + 1)`) keep callbacks stable; **lazy initial state** (`useState(() => expensive())`) avoids re-running setup work.
5. **Primitive effect dependencies**, one concern per effect; effects clean up what they start (listeners, timers, subscriptions, abort controllers).
6. **Interaction logic in event handlers**, not in effects reacting to state set by the handler.
7. **Mark non-urgent updates** with `startTransition` or `useDeferredValue` (filtering a big list while typing).
8. **Stable keys** from data ids, never array index for reorderable lists. Virtualize long lists (hundreds of rows).
9. **Memoize at measured hot spots** (`memo`, `useMemo`, `useCallback`) and only where a profile shows wasted renders. With the React Compiler enabled, avoid hand-memoizing and fix patterns the compiler reports.
10. **High-frequency values** (pointer position, scroll, drag, animation frames) go to refs and direct style writes, or the animation library, not `setState` per frame.

## F. Rendering

1. Hoist static JSX and constants out of components; avoid creating components inside components (they remount every render).
2. Use CSS for show/hide when state should survive (`hidden`, `display`); conditional render when it should reset.
3. `content-visibility: auto` with `contain-intrinsic-size` for long offscreen sections.
4. Do not animate layout properties (`width`, `top`); use `transform`/`opacity` (see `ui.md` section 5).
5. Prevent layout shift: reserve space for images, embeds, async content and web fonts.

## G. View transitions

Use the browser View Transitions API (or the framework flag, such as Next's `viewTransition` option, when your version has it and it is stable) for navigation and list reorders where continuity helps. Rules: give a unique `view-transition-name` only to elements that exist on both sides; keep durations short (under 300 ms); skip for keyboard-initiated high-frequency actions; wrap with a feature check so unsupported browsers update instantly; honor `prefers-reduced-motion` by disabling or reducing to a crossfade. Confirm the installed React/Next version supports the API you use in its types or release notes before relying on it.

## H. Testing and verification

- Test behavior through roles and labels (Testing Library `getByRole`); that doubles as an a11y check. 
- Run the browser pass from `browser-verification.md`: console must be clean of hydration warnings, `act` warnings are test bugs, not noise.
- After a performance change, show a before/after number (bundle KB, requests in series, render count from the Profiler), not an impression.

## I. React Native notes

- Lists: `FlatList`/`FlashList` with stable `keyExtractor`, memoized item components, no inline closures per row on large lists.
- Animate with the native-driver path (Reanimated worklets or `useNativeDriver`), not JS-thread state per frame.
- Touch targets 44 pt+, `accessibilityLabel`/`accessibilityRole` on pressables, safe-area insets, keyboard-avoiding views on forms.
- Test on a real or emulated device at two sizes; `ult-browser` does not cover native.
