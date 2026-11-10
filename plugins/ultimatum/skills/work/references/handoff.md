# Handoff and resume

Goal: the next session can continue from the next step without rereading this conversation or redoing work that is already proven.

## Writing a handoff (end of session, "save progress", or before a risky pause)

1. Run the checks that prove the current state so that the evidence is fresh: `ult run -- <test cmd>`.
2. Write the file:
   ```
   ult handoff write \
     --goal "<one sentence: the user-visible outcome>" \
     --decision "<what> — <why>" --decision "..." \
     --next "<the single next action, concrete enough to start without thinking: file, function, failing test>" \
     --question "<only questions that block the next step>"
   ```
   The tool fills in the branch, HEAD, changed files (from `git status`), and recent `ult run` results with their log ids. It redacts secrets before writing. The output goes to `.ultimatum/handoff.md`, and a copy goes to `.ultimatum/handoffs/`.
3. Keep it short, around 15 to 40 lines. Reference artifacts by path or log id rather than pasting them. Good references include a spec, an ADR, a findings file, a PR URL, or `ult log <id>`.
4. Record decisions together with their reasons. A decision without a reason gets reopened.
5. If the project has its own convention (a `docs/` progress log, an issue tracker, `HANDOFF.md`, or a PR description), write there too, or write there instead when the user asks. Do not create new tracked files unprompted.

What does **not** belong in a handoff:
- a transcript summary
- the full plan
- secrets
- speculative to-do lists
- long logs

The log id is enough for logs.

## Resuming ("continue", "resume", "pick up where we left off")

1. Run `ult handoff show`. It prints the file and checks it against the repository: whether HEAD moved, whether referenced files are missing, and whether log ids are missing.
2. Treat the handoff as a claim, not as proof. Rerun the cheapest check that confirms the stated state (usually the test command in Evidence) **before** editing. If the state differs from the handoff, say so and go with what the repository shows.
3. Start with **Next unfinished step**. Do not re-plan or redo settled decisions unless the new evidence contradicts them. If it does, name the contradiction.
4. Answer the open questions from the code if you can. Ask the user only about questions that block the next step.
5. When you finish, update the handoff or delete it if the goal is complete. Then report as usual.

## Cross-session memory for longer efforts

- Use `ult note --kind decision|fact|finding --title ... --body ...` for durable facts you will search for later. Find them with `ult find <terms>` and read them back exactly with `ult get <ref>`.
- Use specs, requirements, and success checks for a feature. They live wherever the project keeps docs. See `feature-planning.md`.
- A long audit's coverage ledger and findings file live in `.ultimatum/security/`. See `security/full-audit.md`.
