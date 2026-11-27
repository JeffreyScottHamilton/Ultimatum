# Test seams: agree where tests go, and fakes shaped like the client

Read when starting test-first work on a feature with several possible test points, when a test suite is written all at once before any code, or when a fake for an external API needs branching logic to work.

The loop, behavior assertions, mock-at-boundaries and tautology rules are in (`../../tdd.md` § 1) and (`../../tdd.md` § 4). This file adds three things those leave out.

## Agree the seams before the first test

You cannot test everything. Before writing tests, list the seams you plan to test and get a yes from the user (or, working alone, write them in the plan). One line each, saying what the seam catches and what it misses:

```text
1. CLI `drafts export --format csv`: catches parsing, filtering, file output; misses nothing user-facing.
2. Function `render_row(draft)`: catches escaping edge cases fast; misses wiring to the CLI.
```

That list is where testing effort goes: critical paths and tricky logic, not every getter. A test at a seam nobody agreed to is a candidate for deletion in review. If the shape of the interface itself is in doubt, settle it first (`deep-modules.md`).

## Grow tests one at a time

Writing the whole suite first and then the code tests what you imagined, not what you learned. Such tests tend to check the shape of data instead of behavior, stay green through real changes, and lock in a structure before you know the problem.

Instead: one test, the code to pass it, then the next test, chosen by what the last cycle taught you. Each test is a thin probe through the whole path. Clean-up of the design can wait for review if the loop is going well; the base file's refactor step is for tidying what you just wrote, not redesigning.

## Fakes shaped like the client

When code talks to an external API, give it a client with one function per operation, not one generic `request(path, options)`:

```ts
type Order = { id: string; total: number };

type ShopClient = {
  getOrder(id: string): Promise<Order>;
  refund(id: string, amount: number): Promise<void>;
};

async function refundIfSmall(client: ShopClient, id: string): Promise<boolean> {
  const order = await client.getOrder(id);
  if (order.total > 50) return false;
  await client.refund(id, order.total);
  return true;
}

// The fake has no branching on paths: each function returns one shape.
const refunds: Array<[string, number]> = [];
const fake: ShopClient = {
  getOrder: async (id) => ({ id, total: 20 }),
  refund: async (id, amount) => { refunds.push([id, amount]); },
};

refundIfSmall(fake, "o1").then((done) => {
  if (!done || refunds.length !== 1 || refunds[0][1] !== 20) throw new Error("unexpected");
  console.log("refundIfSmall: ok");
});
```

Why it helps: each fake function returns one shape, so setup has no `if path === ...`; the types check every operation separately; and a reader sees at once which calls a test relies on. A generic fetch wrapper forces the fake to re-implement routing, and that routing then needs its own tests.

The assertion above checks the recorded refund (an observable effect at the boundary), not how often `getOrder` was called.
