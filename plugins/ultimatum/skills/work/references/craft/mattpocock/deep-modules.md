# Deep modules: interface, seam and depth

Read when designing or reshaping a module's interface, deciding where a seam goes, merging shallow modules, or comparing several interface designs before you commit.

The testing side (test at the highest seam, inject the clock or client instead of patching privates) is in (`../../tdd.md` § 4). This file gives the shared design words and the moves that use them.

## Words to use, and keep using

Pick these and stick to them in specs, reviews and briefs; switching between synonyms makes readers think there are two things.

| Word | Meaning here |
|---|---|
| module | anything that has an inside and an interface, at any size: one function up to a package or a cross-tier slice |
| interface | all a caller must know to use it: types, plus ordering rules, invariants, errors, config and cost |
| implementation | the code inside |
| depth | how much behavior a caller gets per unit of interface they must learn |
| seam | the place where behavior can be swapped without editing there; where the interface sits (term from Michael Feathers) |
| adapter | whatever fills the slot at a seam: the production client, the in-memory fake |
| payoff | what callers gain from depth: one implementation serves many call sites and tests |
| locality | what maintainers gain: a change or a bug lives in one place |

"Boundary" is avoided because domain modeling uses it for something else. Depth is not a line-count ratio; counting lines rewards padding.

## Three quick tests

- **Delete it in your head.** If the complexity disappears with it, the module was a pass-through. If the same logic would have to reappear in every caller, it earns its place.
- **Count the adapters.** One adapter at a seam is a guess about the future; two (usually production and test) make it a seam that pays. Do not add a port for one adapter.
- **Test through the interface.** Callers and tests should cross the same seam. A test that has to reach inside means the module is the wrong shape, not that the test needs a back door.

Internal seams are fine: a deep module may be built from small swappable parts that its own tests use. They stay out of the public interface.

## Deepening shallow modules: sort the dependencies first

Before merging a cluster of thin modules into one deeper one, sort what it depends on. The sort decides how the result is tested.

| Kind | Example | How to test the merged module |
|---|---|---|
| in-process | pure functions, in-memory state | merge and test the new interface directly; no adapter |
| local stand-in exists | SQLite or PGlite for Postgres, a temp directory | run the stand-in inside the suite; the seam stays internal |
| your own remote service | an internal HTTP or queue API | define a port; production gets the network adapter, tests an in-memory one |
| third party you do not control | payments, SMS, email | inject the port; tests supply a fake adapter |

Then replace the old tests instead of stacking new ones on top: once tests at the new interface cover the behavior, the unit tests on the old shallow pieces are dead weight. Delete them in the same change and say so in the report.

## Design it twice

From John Ousterhout's *A Philosophy of Software Design*: the first interface you think of is rarely the best. When the interface matters (many callers, hard to change later), draft several that differ on purpose.

1. Write a short problem frame for the user: constraints any design must meet, dependencies and their kind from the table above, and a rough sketch that makes the constraints concrete. It is not a proposal.
2. Produce three or more designs, each under a different pressure:
   - smallest interface: one to three entry points;
   - most flexible: many uses and extension points;
   - easiest common case: the usual call is one line;
   - ports and adapters, when dependencies cross a network.
3. For each design give: the interface (types, ordering rules, errors), a caller example, what it hides, how its dependencies are supplied, and where it is weak.
4. Compare in prose on depth, locality and seam placement, then recommend one, or a mix, with the reason. A strong pick helps more than a menu.

Helpers can draft the designs in parallel, one per pressure, each with a self-contained brief (`../../orchestration.md` § 3). Their output is input to your comparison; check each claim against the code before recommending.

## Small habits that keep modules testable

- Pass dependencies in; do not construct clients inside.
- Return results; do not mutate the caller's objects as a side effect.
- Fewer entry points and fewer parameters mean fewer tests and simpler setup.

A runnable Python sketch of the port idea, with an in-memory adapter:

```python
from typing import Protocol

class Mailer(Protocol):
    def send(self, to: str, body: str) -> None: ...

class MemoryMailer:
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []
    def send(self, to: str, body: str) -> None:
        self.sent.append((to, body))

def invite(user_id: str, mailer: Mailer) -> str:
    if not user_id.isalnum():
        raise ValueError("bad user id")
    mailer.send(user_id, "You are invited")
    return "invited"

fake = MemoryMailer()
assert invite("u42", fake) == "invited"
assert fake.sent == [("u42", "You are invited")]
```
