# React performance: not covered yet

Read when a React performance question is not answered by `../../react.md` or the files in this folder.

- Framework caching APIs in depth (Next.js `use cache`, `revalidateTag`, fetch cache options, Partial Prerendering). They change between major versions; read the docs for the version in `package.json`. The rule in react.md B6 (dedupe per request, decide caching deliberately) still applies.
- React Native profiling (Hermes profiler, Flipper replacements, FlashList tuning). react.md § I has the rules; measuring there needs device tools.
- Server load testing (k6, autocannon). That measures capacity, not page speed; use the tool's docs.
- Image and font pipelines. See the website skill's performance guides for `next/image`, font loading and LCP images.
- An AST-based scanner. `react_scan.py` uses patterns; for exact results use ESLint with `eslint-plugin-react-hooks`, `@next/eslint-plugin-next`, and the React Compiler's lint rules.
