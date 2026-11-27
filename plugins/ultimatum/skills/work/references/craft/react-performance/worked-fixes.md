# Worked fixes: React and Next.js performance, before and after

Read when applying a rule from `../../react.md` and you want the shape of the fix and the number that shows it worked.

Each fix: the smell, the change, and what to measure (`measuring.md`). Examples use TypeScript and the Next.js App Router; the ideas carry to Remix, Vite and React Native.

## 1. Serial awaits (react.md C1)

Before: three independent requests in a row; page time is the sum.

```tsx
const user = await getUser(id);
const orders = await getOrders(id);
const plans = await getPlans();
```

After: start all three, wait once; page time is the slowest.

```tsx
const [user, orders, plans] = await Promise.all([getUser(id), getOrders(id), getPlans()]);
```

When one depends on another, start the independent ones first and await late:

```tsx
const plansP = getPlans();                    // starts now
const user = await getUser(id);
const orders = await getOrders(user.accountId);
const plans = await plansP;
```

Measure: server timing for the route, before and after (`measuring.md` § 3). Expect the sum to drop to roughly the slowest call.

## 2. Await in a loop (react.md C1)

Before: one request per item, in series.

```ts
for (const id of ids) results.push(await fetchItem(id));
```

After: a batch endpoint if one exists (`fetchItems(ids)`), otherwise parallel with a cap so you do not flood the API:

```ts
async function mapLimit<T, R>(items: T[], limit: number, fn: (x: T) => Promise<R>): Promise<R[]> {
  const out: R[] = new Array(items.length);
  let next = 0;
  const workers = Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (next < items.length) { const i = next++; out[i] = await fn(items[i]); }
  });
  await Promise.all(workers);
  return out;
}
const results = await mapLimit(ids, 5, fetchItem);
```

Keep the loop serial when order of side effects matters (payments, writes that depend on each other).

## 3. Slow section blocks the page (react.md C5)

Before: the page awaits a slow recommendations call, so nothing shows until it returns.

After: the page renders at once; the slow part streams in.

```tsx
export default function Page() {
  return (
    <>
      <ProductDetails />
      <Suspense fallback={<RecsSkeleton />}>
        <Recommendations />   {/* async server component, awaits its own data */}
      </Suspense>
    </>
  );
}
```

Give the skeleton the same height as the loaded block so nothing jumps. Measure: time to first byte and Largest Contentful Paint on the route; the slow call no longer sits in front of either.

## 4. Client boundary too high (react.md B1, B2)

Before: `'use client'` at the top of `app/products/page.tsx` because one button needs `onClick`; the whole page and its imports ship as client JavaScript.

After: the page stays a server component; only the button is a client component.

```tsx
// app/products/add-to-cart.tsx
'use client';
export function AddToCart({ id }: { id: string }) {
  const [pending, start] = useTransition();
  return <button disabled={pending} onClick={() => start(() => addToCart(id))}>Add to cart</button>;
}
```

Pass only `id`, not the product record. Measure: the route's first-load JavaScript in the build output (`measuring.md` § 1).

## 5. Heavy, rarely used UI in the main bundle (react.md D2, D4)

```tsx
const Editor = dynamic(() => import('./rich-editor'), { loading: () => <div className="h-64" /> });
```

Start the download on intent so the click feels instant:

```tsx
<button onMouseEnter={() => import('./rich-editor')} onFocus={() => import('./rich-editor')} onClick={open}>Edit</button>
```

Measure: route first-load JS and the analyzer treemap; the editor's chunk should now load only after the click or hover.

## 6. State copied by an effect (react.md E1)

Before: two renders per change, and a moment where the values disagree.

```tsx
const [fullName, setFullName] = useState('');
useEffect(() => setFullName(`${first} ${last}`), [first, last]);
```

After: computed during render.

```tsx
const fullName = `${first} ${last}`;
```

If the computation is costly and a profile shows it, wrap it in `useMemo` (skip this when the React Compiler is on). Measure: render count in the Profiler for one keystroke.

## 7. Context value rebuilt every render (react.md E3)

Before: every consumer re-renders whenever the provider's parent renders, because the value is a new object.

```tsx
<CartContext.Provider value={{ items, add, remove }}>
```

After: a stable value, and split contexts when some readers need only the actions.

```tsx
const actions = useMemo(() => ({ add, remove }), [add, remove]);
<CartActions.Provider value={actions}>
  <CartItems.Provider value={items}>{children}</CartItems.Provider>
</CartActions.Provider>
```

Measure: Profiler "why did this render" on a component that only uses `add`.

## 8. Typing in a filter freezes a long list (react.md E7, E8)

```tsx
const [query, setQuery] = useState('');
const deferred = useDeferredValue(query);
const visible = useMemo(() => filterRows(rows, deferred), [rows, deferred]);
```

The input updates at once; the list catches up. Past a few hundred rows, render only what is on screen with a virtualizer. Measure: interaction to next paint (INP) on the filter input, in the Performance panel or field data.

## 9. Index as key in a list that changes order (react.md E8)

Before: `items.map((it, i) => <Row key={i} ... />)` keeps input state on the wrong row after a sort or delete.

After: `key={it.id}`. This is a correctness fix as much as a speed one; test it by typing into row 2, deleting row 1, and checking the text moved with its row.

## 10. Pointer position in state (react.md E10)

Before: `onPointerMove={e => setPos({ x: e.clientX, y: e.clientY })}` re-renders the tree at 60 to 120 times a second.

After: write to a ref and the DOM directly, batched to the next frame.

```tsx
const el = useRef<HTMLDivElement>(null);
const frame = useRef(0);
function onMove(e: React.PointerEvent) {
  cancelAnimationFrame(frame.current);
  frame.current = requestAnimationFrame(() => {
    el.current?.style.setProperty('transform', `translate(${e.clientX}px, ${e.clientY}px)`);
  });
}
```

Measure: the Performance panel shows no React commits while moving the pointer.
