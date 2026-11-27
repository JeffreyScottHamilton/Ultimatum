# Surgical diff: every changed line traces to the request

Read before committing or showing a diff, when an edit touched a file for a reason you cannot name, or when you are tempted to "tidy while you're in there".

A reviewer should be able to point at any changed line and find the sentence in the request that caused it. Unrelated edits hide the real change, break `git blame`, and cause merge conflicts for other people.

## 1. Rules

1. **Touch only what the request needs.** No reformatting, renaming, reordering imports or rewording comments in code you are not otherwise changing.
2. **Match the house style** of the file even where you would write it differently: quotes, naming, error style, test layout. Consistency in one file beats your preference.
3. **Clean up your own leftovers.** Imports, helpers, variables or files that your change made unused are removed in the same diff.
4. **Mention, don't delete, other dead code.** Pre-existing unused code, an odd pattern, a bug next door: one line in the report ("`old_export()` in `jobs.py` looks unused; left as is"). The owner decides.
5. **Refactors are separate.** If the change really needs a restructure first, do it as its own commit with no behaviour change and its tests passing, then the feature on top. Say so in the plan.
6. **Formatter churn is not your change.** If the project's formatter rewrites the whole file, format only the lines you touched, or ask before committing a format-everything diff.

## 2. Read your own diff

Before reporting: `git diff --stat`, then `git diff` file by file. For each hunk, name the request sentence it serves. A hunk with no answer is reverted. Watch for:

- a file in `--stat` you do not remember editing;
- whitespace-only, quote-only or comment-only hunks;
- the same lines removed and added in a new order;
- a test changed to match new behaviour without the request asking for that behaviour.

## 3. The checker

`diff_scope.py` reads a zero-context diff and flags hunks that look like drive-by edits. It reads only stdin, writes nothing and has no network access.

```bash
git diff -U0 | python3 ../../../../../data/craft/coding-discipline/diff_scope.py
git diff -U0 main | python3 ../../../../../data/craft/coding-discipline/diff_scope.py --allow 'src/billing/*' --allow 'tests/billing/*'
```

It prints `path:line kind` for each suspect hunk and exits 1 if there are any:

- `whitespace-only`: the removed and added lines differ only in spaces, tabs or blank lines;
- `quote-only`: they differ only in `'` versus `"`;
- `comment-only`: every changed line on both sides is a comment;
- `reorder-only`: the same lines, in a different order;
- `outside-scope`: the file matches none of the `--allow` patterns (only when `--allow` is given).

A flag is a question, not a verdict: a comment fix the user asked for is fine. Explain each one you keep.
