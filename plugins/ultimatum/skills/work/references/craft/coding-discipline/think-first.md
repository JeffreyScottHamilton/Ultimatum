# Think first: settle the question before the first edit

Read before editing when the request could mean more than one thing, when you are about to assume something about data, users or the environment, or when you notice you are confused.

Most wasted work in a coding session is a correct answer to the wrong question. Five minutes of reading and one sentence to the user cost less than a diff that has to be thrown away.

## 1. Write the assumptions down

Before the first edit, list what you are taking as true and could be wrong about, in one short block in your reply:

- **Data:** shape, size, whether it can be empty or null, units, time zone, encoding.
- **Callers:** who else calls the code you will change (`ult refs <symbol>`), and whether they rely on the current behaviour.
- **Environment:** versions, feature flags, which database or API the code talks to in each environment.
- **Intent:** what the user will do with the result, if it changes the design.

An assumption you can check in under a minute (read the file, run the query, grep the callers) is checked, not listed.

## 2. The two-readings test

Say the request back to yourself two different ways. If both readings are plausible and lead to different code, it is ambiguous.

| Request | Reading A | Reading B |
|---|---|---|
| "Make the export faster" | cut wall time for one big export | let many users export at once |
| "Add a delete button" | soft delete, restorable | hard delete with cascade |
| "Fix the date bug" | the off-by-one in the report | the time-zone shift in the email |

Then decide:

- **Ask** when the readings differ in something hard to undo (data loss, a public API, money, a schema), or when picking wrong costs more than a round trip. One question, with your recommended answer first.
- **Pick and say so** when the difference is cheap to reverse. Name the reading you chose and the one you did not, so the user can redirect in one line.

## 3. Say when a simpler route exists

If the request asks for a mechanism and a smaller one meets the goal, say so before building: "A nightly cron would do this without a queue; want that instead?" Offer it once, with the trade-off, then do what the user picks. Do not quietly build the smaller thing either.

## 4. Stop when confused

Confusion is information. If the code does not behave the way you expect, or two files contradict each other, stop adding code. Name what does not fit ("`getUser` returns null here but the caller never handles it; is that reachable?"), then read, reproduce or ask. Code written on top of a misunderstanding has to be found and removed later.

## 5. The check before the first edit

- [ ] I can say in one sentence what will be different when this is done.
- [ ] I know which reading of the request I am building, and said so if it was a choice.
- [ ] Assumptions I could check quickly are checked; the rest are written down.
- [ ] I know who calls the code I am about to change.
