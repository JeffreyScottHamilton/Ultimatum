# Context and token efficiency

Purpose: spend context on evidence that changes decisions, and keep evidence exact enough to rely on it.

## 1. What may be compressed and what may not

| Compress freely | Never compress, paraphrase, or "clean up" |
|---|---|
| Your own prose, status updates, plans | Code, diffs, patch anchors (the exact lines an Edit matches) |
| Repetitive passing-test noise, progress bars, download logs | Identifiers, paths, versions, config keys, CLI flags |
| Duplicate warnings (count them instead) | Error messages, assertion text, stack frames that point into project code |
| Summaries of files you have already read and won't edit | Security evidence: inputs, requests and responses, `file:line`, tool findings |
| | Exit codes, test counts, and the fact that something was **not** checked |

When you shorten output, say what was dropped and how to get it back. A gap in evidence that nobody mentioned is worse than a long log.

## 2. Terse voice (chat prose only)

- Put the answer first. Skip preamble, the restated question, and closing pleasantries.
- Prefer short sentences and fragments in status lines. Keep the technical terms precise.
- **Not terse.** Use full sentences for:
  - security warnings
  - destructive-action confirmations
  - irreversible steps
  - anything the user must decide
  - anything written into the repository (code, comments, docs, commit messages), which follows the project's style
- If the user asks for "caveman", "be brief", or "less tokens", go terser in prose. The table in §1 still applies.

## 3. Noisy commands: `ult run`

```
ult run -- <cmd> [args]          # e.g. ult run -- npm test ; ult run --name tests -- pytest -x
ult run --shell -- "a | b && c"  # only when pipes or && are genuinely needed
ult log <id|last> --grep 'RE'    # exact raw lines with context
ult log <id> --lines 800:860     # exact raw range
ult logs                         # recent runs with exit codes
```

What `ult run` guarantees:
- It returns the command's own exit code and prints it.
- It saves the raw output byte for byte in `.ultimatum/logs/<id>.log` with mode 0600.
- It prints these blocks verbatim with line numbers:
  - failure blocks (unittest `FAIL:`, pytest `___ test ___`, jest `●`, go `--- FAIL`, cargo `error[E…]`)
  - signal lines (tsc `error TS…`, eslint `l:c error`, npm `ERR!`)
  - summary lines
  - the tail
- It counts noise and does not print it.
- It never reports success for a non-zero exit. "Zero tests ran" is flagged as not a pass.
- Small outputs pass through unchanged.

Your duties when you use it:
- **Before claiming anything about the failure, read the printed block.** If the key line isn't shown, use `ult log <id> --grep`. Don't rerun the command just to see more.
- **Quote the exact failing line** in your reasoning and your report.
- **When you hand a failure to a worker, pass the log id and line range**, not a paraphrase.
- **Use plain Bash for short, quiet commands** (`git status`, `ls`, a single test). `ult run` is for output you expect to be long.

## 4. Search before you read

Narrow first, then confirm in source:
1. `ult symbols <Name>` finds definitions. `ult refs <Name>` finds usages. `ult search '<regex>' --path src --glob '*.ts'` finds patterns. Results are grouped per file and capped. Use `--path`/`--glob` to narrow rather than raising the caps.
2. Read only the relevant range of a file, using offset and limit, unless you are going to edit most of it.
3. For a new repo, run `ult map summary` once and then `ult map query routes|auth|data_stores|sinks|entry_points|<keyword>`. The map gives `file:line` leads built with regexes, so they are *guesses* until you open the source.
4. If a Serena or LSP MCP is in your tool list, prefer it for definitions, references, and symbol-level edits in large typed codebases. If a Graphify graph exists, query it narrowly and never load the whole graph.
5. For library or API questions, check the installed version first (lockfile, `node_modules/<pkg>/package.json`, `pip show`). Then read the installed source or types. Use Context7 MCP if it is present: one concept per query and at most ~3 calls. Label answers from memory as unverified when the version matters.

Stop searching once you have the anchor you need. Repeating the same broad search with different wording is a sign to read one file properly instead.

## 5. Store, then retrieve

- `ult note --kind decision|fact|finding --title T --body B` saves facts you will need later in this task or a later session. `ult find <terms>` returns refs and snippets. `ult get <ref>` returns exact text.
- Logs from `ult run` are indexed automatically, so `ult find "AssertionError parse_amount"` finds the right chunk of an old run.
- Store hits point back to the source, which you re-read before editing. The store does not replace the source.

## 6. Delegation economics

- Delegation costs context: the worker has to rebuild understanding, and you have to read its report. Delegate when that cost is clearly smaller than doing the work inline. Examples:
  - a broad scan across many files where you need only the conclusion (`ultimatum:scout`, fast model)
  - truly independent slices
  - an independent review or verification, where a fresh context is the point
- Give each worker the minimum it needs:
  - the goal
  - the exact anchors (`file:line`, log id)
  - the files it owns
  - the acceptance command
  - the reply format
- Leave out the conversation history, unrelated files, and secrets.
- Model by role: fast/cheap for read-only scouting, mid-tier for implementation slices and hunting, and inherit (the session model) for verification and final review.
- Spot-check any "no match" or "no issues" a worker reports before relying on it. Ask for the queries it ran.
- Any efficiency measurement counts every subagent's tokens, plus retries and cache reads. See `skill-evaluation.md`.

## 7. Don't do the same work twice

- One search pass, one review pass, one compression pass. If a reference or a worker already produced a result, reuse it.
- Read each reference once per task.
- Don't re-read a file you just edited to "verify" the edit. Run the check instead.
