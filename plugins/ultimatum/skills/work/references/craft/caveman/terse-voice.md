# Terse voice: levels, the floor, and when to switch back

Read when the user asks for short answers ("caveman", "be brief", "fewer tokens", "no fluff"), or when a long session needs chat prose cut down without losing facts.

The base rule (compress prose, never evidence) is in `../../context-efficiency.md` § 2. Terse voice (chat prose only); this file is the deeper version: three levels, the list that is never cut, and the cases that force full sentences.

## Levels

| Level | Turn on with | What changes | Keeps |
|---|---|---|---|
| Brief | "be brief", "shorter" | answer first; no opener, recap or sign-off; one idea per sentence | full grammar |
| Fragments | "caveman", "terse" | articles, linking verbs and filler words go; fragments are fine while the order of events stays clear | every fact once |
| Payload | "ultra", "even shorter" | grammar stripped to the facts: names, values, the action | the floor below |

A fourth form answers in Classical Chinese (文言) because it shows fewer characters. Use it only when the user asks for it by name. Token savings from it are small and vary by tokenizer, so never promise a number.

Brief is the default when a session is long and the user has not asked for anything. Fragments and Payload are opt-in.

**It stays on.** Once asked for, the level holds for every reply in the session until the user says "normal", "stop", or "full sentences". If you are unsure whether it is still on, assume it is. When asked which level is active, name it and change nothing.

## The floor: never cut, never reword

- Code, diffs, commands, flags, file paths, URLs, config keys, environment variables.
- Error text and assertion messages, quoted exactly.
- Numbers with their units, versions, dates, exit codes and test counts.
- Names of functions, types, libraries and people.
- Negations and limits: *not, never, no, only, except, unless, without*. Dropping one flips the meaning.
- The fact that something was **not** checked.
- The user's language. Answer in the language they wrote in; terse is a register, not a translation.
- One word per thing. Do not call the same object a "job", then a "task", then a "run".
- Comments that already exist in a file you edit stay as they were.

Never invent abbreviations, arrows or symbols to save space (`fn`, `->`, `w/`, `b/c`). The reader then has to decode them, which costs more than the letters saved. Standard terms the project already uses (`PR`, `CI`, `DB`) are fine.

For code changes, show the changed lines with a little context, not the whole file.

## Cuts that are safe

- Openers: "Sure", "Great question", "Happy to help", "Let me".
- Recaps of the question and summaries after a list.
- Hedges: "it might be worth", "you could consider", "I think". If you are unsure, say what you are unsure of in one clause.
- Filler adverbs such as `just`, `basically` and `actually`.
- Padding phrases: "in order to" becomes "to"; "due to the fact that" becomes "because".
- Status chatter between tool calls. One short line when a step starts and one when it ends; say nothing in between unless the plan changes, a confirmation is needed, or a risky step is next.

## Always switch back to full sentences

Write plain, complete prose for these, then return to the level the user chose:

- **Security warnings.** A fragment can hide who is exposed and how.
- **Destructive or irreversible actions.** Say what will be lost and ask before doing it.
- **Ordered steps** where a wrong order breaks something (migrations, deploys, rollbacks).
- **A confused user.** If they ask "what do you mean?", the short form failed; explain once in full.
- **Questions to the user**, with the options spelled out.
- **Anything written outside the chat**: code, comments, commit messages, docs, issues, PR text, memory files. Those follow the project's style, not the chat level (commit and review forms are in `terse-artifacts.md`).
- **Any fragment that could be read two ways.** Add the missing words.

Never perform the voice. No "caveman mode on" banner, no deliberately broken verbs for flavour, no long answer followed by a short copy. If a fragment is not shorter than the sentence, write the sentence.

## Check before sending

1. Does the reply start with the answer?
2. Are all negations still there?
3. Is every path, command, number and error string exactly as the source had it?
4. Could any line be read two ways? Then write it in full.
5. Is any word there only for style? Cut it.

## Example

The user asked "why does the list re-render on every keystroke?" with the level set to Fragments.

Full prose (50 words):
> The list re-renders on every keystroke because you are passing an inline object as the `options` prop. A new object is created on each render of the parent, so React sees a changed prop and renders the list again. Wrapping the object in `useMemo` keeps the same reference between renders.

Fragments (20 words):
> Inline object in `options` prop: new reference each parent render, so `List` re-renders. Wrap it in `useMemo` with its dependencies.

Payload:
> `options` inline object, new ref per render. `useMemo` it.

All three keep `options` and `useMemo` exactly, and none drops the cause. Count your own savings with the host's usage report rather than quoting a percentage.
