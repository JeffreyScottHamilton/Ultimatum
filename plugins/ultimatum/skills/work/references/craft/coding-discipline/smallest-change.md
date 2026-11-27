# Smallest change: the least code that fully does the job

Read when writing new code, when a diff passes about 100 lines for a request that sounded small, or when you catch yourself adding a setting, a layer or a "for later" hook.

"Small" means no code the request does not need. It does not mean skipping validation at a real boundary, tests, or error handling for failures that can happen. The ladder of reuse (call what exists, extend the owner, then write new) is in `../caveman/task-stances.md` § The simplicity ladder; this file is about the shape of the new code itself.

## 1. Not yet

Leave these out until a second real use or the user asks:

- **Options and settings** nobody requested. A constant in one place is easy to promote later.
- **Abstractions with one implementation:** an interface, a factory, a plugin registry, a base class for one subclass.
- **Generality:** handling formats, locales or providers the project does not use.
- **Error handling for the impossible:** a `try` around code that cannot throw, a null check on a value the type system already rules out. Handle failures that can happen (network, user input, files, parsing) properly.
- **Copies of existing helpers** under a new name. Search before writing (`ult search`, `ult symbols`).

## 2. The size test

After the change works, read the diff as a reviewer who did not write it:

1. Could a teammate explain every new function in one sentence?
2. Is any new name used exactly once, by the next line? Inline it.
3. Is there a branch no test or caller reaches? Delete it, or write the test that shows why it exists.
4. Would the same behaviour fit in half the lines without becoming clever? Rewrite it that way.

If two answers point at trouble, rewrite before showing the diff. A rewrite at this point is cheap; review time on a bloated diff is not.

## 3. Worked example

Request: "Log a warning when an upload is larger than 20 MB."

Overbuilt (about 40 lines, sketched):

```python
class SizePolicy(Protocol):
    def check(self, size: int) -> PolicyResult: ...

class ThresholdPolicy:
    def __init__(self, limit_mb: float = 20.0, level: str = "warning", notify: Callable | None = None): ...

POLICIES: dict[str, SizePolicy] = {"default": ThresholdPolicy()}
```

Enough (3 lines, in the upload handler that already exists):

```python
WARN_BYTES = 20 * 1024 * 1024

if upload.size > WARN_BYTES:
    log.warning("large upload: %s bytes for %s", upload.size, upload.id)
```

Plus one test that a 21 MB upload logs the warning and a 19 MB one does not. If a second limit ever appears, that is the moment to give it a shape.

## 4. When bigger is right

Some requests need structure: a public API, a migration, a security boundary, a module many callers share. Size the code to the request, not to a line target, and say why it is the size it is in the report.
