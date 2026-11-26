# TypeScript habits: test data without casts, and package entry points

Read when TypeScript tests are full of `as` casts to build partial objects, or when you want each package's internals reachable only through its entry files.

## Test data without `as`

Casting a half-built object (`{ params: { id: "1" } } as Req`) hides real type errors, and the double cast (`as unknown as Req`) hides all of them. Two better options:

**A small local helper.** No dependency, and the intent is clear at the call site:

```ts
type DeepPartial<T> = { [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K] };

// Test-only: fills in nothing, so the test must only touch what it set.
export function partial<T>(value: DeepPartial<T>): T {
  return value as T;
}

type Req = { params: { id: string }; query: Record<string, string>; locale: string };
function getUserId(req: Req): string { return req.params.id; }

const id = getUserId(partial<Req>({ params: { id: "123" } }));
// partial<Req>({ params: { id: 123 } }); // error: number is not string
```

The cast lives in one reviewed place, and the argument is still checked against the shape: a wrong field type fails to compile.

**The shoehorn library.** `@total-typescript/shoehorn` (MIT) offers `fromPartial` for partial but well-typed data, `fromAny` for data that is wrong on purpose (testing error paths) while keeping autocomplete, and `fromExact` for a full object you may loosen later. Adding it is a new dev dependency, so ask first.

Either way: test code only. In production code a partial object is a bug waiting.

To find candidates, search test files for casts to a capitalised type, for example `ult search " as [A-Z]" --glob "*.test.ts"` (or `rg` with the same pattern). Then run the type check and the tests; quote both exit codes.

## Packages that expose only their entry files

Goal: outside code can import a package's root files (`index.ts`, `client.ts`), never its subfolders. Each package becomes a deep module (`deep-modules.md`) with a small public surface.

```text
src/packages/
  billing/
    index.ts      entry (public)
    client.ts     another entry; several small entries beat one big barrel
    lib/          private implementation, free to import each other
    tests/        private; import entries only
```

Rules worth enforcing, all as errors:

1. Code outside a package imports only its root files.
2. Files inside a package import each other freely.
3. Tests import entry files only, even their own package's, so they test what callers see.
4. No import cycles.

The usual enforcer is dependency-cruiser (`https://github.com/sverweij/dependency-cruiser`), which supports path rules with capture groups so one rule covers every package. ESLint's `no-restricted-imports` can cover simpler cases. Adding either is a new dependency and a change to the check command: ask first, and do not touch `tsconfig` paths to make it pass.

**Prove the rule bites.** A boundary check that never fails is decoration. After wiring it:

1. Run it on clean code: exit 0.
2. Add one deep import in a test (`import { x } from "../lib/impl"`): it must fail and name the rule.
3. Remove the deep import: exit 0 again.

Quote all three exit codes. If step 2 passes, the rule is not wired; fix it before calling the job done.

Then leave a one-line pointer in the repo's agent notes (`CLAUDE.md` or `AGENTS.md`, if present) to the short README that explains the layout, so the next agent finds the rule before tripping on it. Editing those files is a project-guidance change; mention it in the report.

`../../../../../data/craft/mattpocock/entry_imports.py` is a stdlib checker for rule 1 and 3 that runs without installing anything; use it to triage a repo before proposing the real enforcer.
