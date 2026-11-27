# react_scan.py: a quick pattern scan for slow or fragile React code

Read when reviewing a React or Next.js change, or before a performance pass, to find likely problems fast; then confirm each with the code and a measurement (`measuring.md`).

## Run it

```
python3 ../../../../../data/craft/react-performance/react_scan.py src app
python3 .../react_scan.py app --only serial-await,await-in-loop
python3 .../react_scan.py app --json        # for a script or a report
python3 .../react_scan.py --rules           # list the rules
```

From the plugin root the path is `data/craft/react-performance/react_scan.py`. It skips `node_modules`, `.next`, `dist`, `build` and type declaration files. Exit 1 when it finds something, 0 when clean, 2 on an unknown rule name. Standard library only, no network.

## The rules

| Rule | What it flags | Fix | react.md |
|---|---|---|---|
| `serial-await` | `await` lines in a row where a later one uses nothing from the earlier ones | `Promise.all`, or start early and await late | C1, C2 |
| `await-in-loop` | `await` inside a `for` loop, or `forEach(async ...)` (which does not wait at all) | batch endpoint, or parallel with a cap | C1 |
| `barrel-import` | named import from lodash, MUI, icon packs and similar | per-module import, or `optimizePackageImports` in Next.js | D1 |
| `heavy-static-import` | editors, charts, maps, 3D, PDF and spreadsheet libraries imported at the top | `dynamic(() => import(...))` if not on first screen | D2 |
| `server-import-in-client` | database clients, `fs`, `child_process`, Stripe in a `'use client'` file | move to a server module; add `import 'server-only'` | B4 |
| `use-client-page` | `'use client'` on `page` or `layout` | keep the page on the server; mark only the interactive leaf | B1, B2 |
| `index-key` | `key={i}` or a key built from the index | `key={item.id}` | E8 |
| `effect-sets-state` | an effect whose whole body is `setX(...)` | compute the value during render | E1 |
| `inline-context-value` | `<X.Provider value={{ ... }}>` | `useMemo` the value, or split state and actions | E3 |
| `pointer-state` | `setX` inside `onPointerMove`, `onMouseMove`, `onScroll`, `onWheel` | ref plus direct DOM write per animation frame | E10 |
| `component-in-component` | a capitalised function or arrow defined inside another component | move it to module level and pass props | F1 |

Before-and-after code for most of these: `worked-fixes.md`.

## Reading the results

It reads lines, not a syntax tree, so expect both misses and false alarms:

- `serial-await` can fire when the second call depends on the first through a value it does not name (a shared cache, a session set by the first call), or when order matters (a write then a read). Keep those serial and say why in a comment.
- `heavy-static-import` is fine when the library is on the first screen (a dashboard whose main view is the chart).
- `use-client-page` is fine for a small page that is all interaction; check the route's first-load JS before moving anything.
- `index-key` is fine for a static list that never reorders, filters or holds input state.
- With the React Compiler on, `inline-context-value` and manual memo advice matter less; trust the Profiler.
- Multi-line patterns (an import split over lines, JSX props across lines) are missed. For exact results, add ESLint with `eslint-plugin-react-hooks` and `@next/eslint-plugin-next`.

Report each finding you keep as `file:line rule`, the fix, and the measurement that shows it helped.
