# Debugging moves beyond the base loop

Read when `../../debugging.md` has you narrowed to a layer but the cause sits further up the call chain, when a fix needs guarding at more than one layer, when a test waits on timing, or when one test leaves the suite dirty for the next. The loop, bisect, hypotheses, the three-failure stop and flaky-test triage stay in debugging.md.

## Trace the bad value back to where it was born

The place an error shows up is rarely where it was made. Work backwards one frame at a time:

1. Name the bad value at the crash site: "`os.makedirs('')` fails" or "the repo is created in the source tree".
2. Find who called this with that value. Then who called that caller.
3. At each frame, ask whether this frame created the bad value or only passed it on.
4. Stop at the first frame that created it. That is where the fix goes.

Example: a test run leaves a `.git` folder inside the package. The `git init` call ran with `cwd=""`; the empty string came from a helper that read `config.workdir`; the config was built at module import, before the test fixture set `workdir`. The cause is import-time evaluation, not `git init`. Fixing the `git init` call with a fallback would have hidden it.

When you cannot follow the chain by reading, add one log line **just before** the dangerous call (not after it fails), with the value, the working directory and the stack:

```python
import os
import sys
import traceback

def init_repo(path):
    print(f"DBG_17 init_repo path={path!r} cwd={os.getcwd()!r}", file=sys.stderr)
    traceback.print_stack(file=sys.stderr)
    ...
```

In tests, write to stderr; a logger may be silenced by the test setup. Tag it (`DBG_<id>`) so cleanup is one search, as debugging.md § 2 says.

## Guard more than one layer

After the root-cause fix, ask what else would have stopped this bad value, and add a check at each layer it crosses. One check can be bypassed by a new caller, a mock or a refactor; several rarely fail together.

| Layer | Check | Example |
|---|---|---|
| Entry (API, CLI, public function) | reject obviously bad input | `workdir` must be non-empty and absolute |
| Business logic | the value makes sense for this operation | the target is not inside the source tree |
| Environment guard | refuse dangerous work in the wrong context | in tests, refuse paths outside the temp dir |
| Debug evidence | log context before the risky call | the `DBG_` line above, kept behind a flag |

Test each layer on its own: bypass the one before it (call the inner function directly) and check that this layer still refuses. A guard that is only ever reached through another guard is untested. When the bad value is a path, a command or a query built from input, these checks are a security boundary: apply `../../security/secure-implementation.md` and write the negative test.

## Wait for the condition, not the clock

A test that sleeps a fixed time guesses how long work takes. It passes on your laptop and fails on a loaded CI runner. Instead, poll for the thing you need, with a timeout and a description of what you were waiting for:

```python
import time

def wait_until(check, timeout=5.0, interval=0.01, what="condition"):
    deadline = time.monotonic() + timeout
    while True:
        result = check()
        if result:
            return result
        if time.monotonic() >= deadline:
            raise TimeoutError(f"gave up after {timeout}s waiting for {what}")
        time.sleep(interval)
```

- Read fresh state inside `check` each time; a value captured before the loop never changes.
- Always set a timeout, and put what you waited for in the error so the failure explains itself.
- Poll every 10 ms or so; tighter loops burn CPU for nothing.
- A fixed sleep is right only when the behaviour under test is about time itself (a debounce of 200 ms, a tick every second). Then first wait for the start condition, sleep the documented amount, and write why next to it.

A runnable copy with a self-test is `../../../../../data/craft/superpowers/wait_until.py`.

## Find the test that leaves a mess

When a file, folder or global appears after the suite and you do not know which test makes it, run the tests one at a time and stop at the first one that creates it. `../../../../../data/craft/superpowers/find_polluter.py` does this: it takes the artifact path and the test command as separate arguments, runs one test file per invocation without a shell, and reports the first culprit. It refuses to start if the artifact already exists, so a leftover from an earlier run cannot blame the wrong test.

## Compare against code that works

When you have no strong hypothesis, look for something similar in the same codebase that does work: another endpoint, another parser, the same feature on another platform.

1. If you are copying a pattern or following a reference, read it through to the end before applying it. Skimming is how a required step gets dropped.
2. List every difference between the working and broken versions, however small: argument order, an await, a config key, an import path.
3. List what the working version depends on: settings, environment, initialisation order, assumptions about its input.
4. Test the differences one at a time, starting with the one your current hypothesis likes least; that is the one you are most likely to have skipped.

## When there is no root cause

Sometimes the evidence points outside the code you own: a timing problem in a dependency, a platform bug, an outside service. If a real investigation ends there:

1. Write down what you ruled out and how.
2. Handle the failure where it enters your code: a clear error, a bounded retry if the operation is safe to repeat, a fallback if one exists.
3. Add a log or metric that will tell you next time it happens, with enough context to resume.
4. Say plainly in the report that the cause is not found, and why you stopped.

Most "no root cause" verdicts are an investigation that stopped early, so check you did the steps in debugging.md first.

## When the user is telling you to slow down

These remarks usually mean you skipped a step; go back to evidence:

| They say | Usually means |
|---|---|
| "Is that actually happening?" | you assumed something without checking it |
| "Did you look at the log?" | the evidence was there and you guessed past it |
| "Stop guessing" | you proposed a fix before you could name the cause |
| "Think about it more" | question the design (debugging.md § 5) |
| "We're going in circles" | your last fixes failed; list what each assumed |
