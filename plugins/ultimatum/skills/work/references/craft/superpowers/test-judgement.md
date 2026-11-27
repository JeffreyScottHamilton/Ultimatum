# Judging whether a test earns its place

Read when you are deciding what to assert, whether to mock, or whether an existing test is worth keeping, after tdd (`../../tdd.md` § 4) and its smells section has not settled it. The cycle, red-green-revert and the basic smells are there; this file is the judgement calls around them.

## Name what it catches

Before writing a test, finish this sentence: "This test fails if someone ___." Good endings name a bug a user would hit ("drops the last row when the file has no trailing newline") or a decision someone could reverse by accident ("starts charging tax on gift cards"). If the only ending you can find is "changes this code", the test guards the code, not the behaviour, and will break on every refactor.

## Work out the expected value by hand

An expected value computed by the code under test (or a copy of its logic) cannot fail. Derive it yourself from the requirement:

```python
def test_total_with_discount():
    # 3 items at 4.00 = 12.00; 10 percent off = 10.80
    assert cart_total([4.00, 4.00, 4.00], discount=0.10) == 10.80
```

not `assert cart_total(items, d) == sum(items) * (1 - d)`, which repeats the implementation and inherits its bugs. Snapshot files are the same trap when nobody reads them before accepting them.

## Tests to delete, or never write

- **Change detectors.** They assert how the code is laid out (which private method is called, in what order, with what internal argument) rather than what it produces. They fail on every refactor and on no actual bug.
- **Text checks.** Asserting that the source contains a string, or that a docstring says something, tests your typing, not the behaviour.
- **Framework tests.** Checking that the ORM saves a row or that the router routes tests someone else's library. Test the rule you wrote on top of it.

## Mocks: when, where, how

**Prefer the actual parts.** Use actual components when they are fast and have no outside effects: in-memory databases, temp directories, a local server on a free port. Mock only what is slow, flaky, costly or outside your control (a payment API, the clock, randomness).

**A mock is not the subject.** If the assertion is "the mock was called" or "the mocked element is on the page", the test proves the stub works. Assert on what your code did with the mock's answer.

**Mock at the right depth.** Understand what the replaced method does before replacing it, including side effects your test relies on. Mocking a whole repository layer to test one validation rule usually removes the very write a later step reads. Mock one level further out, or not at all.

**Shape the double like the live answer.** A fake API response with only the two fields this test reads breaks the code path that reads a third field later, and the test still passes. Copy the full structure of a production response (from docs or a captured, scrubbed example), then change the fields you care about.

**When setup outweighs the test,** the design is telling you something: the unit has too many collaborators. An integration test with the actual parts is often shorter and catches more.

## No test-only methods in product code

A `reset_for_tests()` or `_debug_state()` on a production class means tests and production share code that production never needs and an attacker might reach. Put such helpers in the test utilities: a fixture that builds a fresh instance, a factory, or a context manager that cleans up.

```python
# tests/helpers.py
import contextlib

@contextlib.contextmanager
def fresh_registry():
    reg = Registry()
    try:
        yield reg
    finally:
        reg.close()
```

## Check that a test can fail

For each test you keep, break the code on purpose in the way the test claims to catch (flip a comparison, drop a branch, return early) and watch it go red. A test that stays green under that change catches nothing; fix it or remove it. This is the manual version of mutation testing; tools like mutmut or Stryker automate it when a suite is large.

## Signs a test is going wrong

| Sign | Likely problem |
|---|---|
| Asserts on mock call counts only | tests the stub, not your code |
| Expected value calls the function under test | mirror assertion |
| Breaks when you rename a private helper | change detector |
| Needs a method that only tests call | test-only code in production |
| Setup is three times the length of the test | too many collaborators; consider using the actual parts |
| Passes with the feature deleted | asserts nothing that matters (tdd.md § 6) |
