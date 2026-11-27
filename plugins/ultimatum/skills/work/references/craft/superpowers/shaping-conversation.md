# Shaping a request through conversation

Read when a request leaves something open that changes what gets built, and you need the user to tell you what they want before you design it. Sizing, reading before asking and the question budget are in feature planning (`../../feature-planning.md` § 1); this file is the conversation itself.

## Decide whether to talk at all

Ask yourself one thing first: does the request already hold everything that matters?

- **It does** ("rename the export button to Download"): do it and say what you did. No conversation.
- **Something that changes the result is missing**: start the conversation below.
- **The user opts out** ("just build it", "your call"): stop shaping. State each big how-it-gets-made choice in one plain line (platform, language, storage), then work as normal.

When the user did not ask for a design talk, end your first message with a one-line offer to skip it ("Or say go and I'll start with the defaults above."). When they asked for one, leave that line out.

## Read first, then speak

Before the first reply, read what the user pointed at (spec, issue, files, earlier messages) and the code it touches, until you can say how the affected parts work today. Never ask what the repo or their context already answers, and never reopen a choice they already made.

## The first message

Pick the shape that fits.

**They described what they want** (a spec, a detailed request). About 200 words:

1. Say the request back in your own words: what, for whom, and why, as far as they said.
2. Add what you found: how the relevant code works now and what the change would touch.
3. Name anything they may have missed that changes the request: a constraint, a conflict, a cheaper path.
4. One line inviting corrections.
5. Then one of:
   - they never said why: one open question about the why, in their words, with no options attached;
   - the why is known and one open point would change the build most: ask about that one point, sketching each choice with its trade-off and your pick;
   - nothing is open: sketch the chosen approach, note why the alternatives lost, and ask for a yes.

**They gave a one-liner** ("a page for our book club"). One open question about the biggest unknown, plus what the answer changes: "If it is mainly for members to see the next meeting, I'd put date and book first; signing up new members is a different page. What should a visitor be able to do there?"

## Questions during the talk

- Ask only when the answer changes the build and nothing on hand answers it. Otherwise state your call and the reason, as a proposal they can correct.
- One question per message, in the user's vocabulary. No process words ("acceptance criteria", "non-goals") unless they use them.
- Process steps are yours, not theirs: where files go, whether to look further, how to show something. Decide, then mention the decision in passing.
- **Open before options.** Until you know the why, ask open questions with no example answers; a menu steers them toward your guesses. Once the why is known, sketch named choices with trade-offs and a pick.
- **Build on the last answer.** Each question should follow from what they said or what you found, so it walks them into a case they skipped ("Two people can edit the same list. If both remove the same item, who wins?").
- **Read who owns the how.** Someone who asks about trade-offs wants options with your pick. Someone who talks only about outcomes has handed you the how: decide and state each call in a line. Build on what existing work already uses.
- "What do you think?" or "just guess": propose something concrete.

Ground worth covering over the talk (never read it out as a list): what kind of thing this is, why now and what success looks like, goals, non-goals and failure-even-if-it-works cases, examples they liked or hated, what exists today, the details they care about.

## Play it back as you go

As soon as one part is clear (who it serves, how one piece behaves), describe it back in 200 to 300 words and ask what is wrong or missing. Then go back to questions on the next part.

- Keep their words and your additions apart: mark each gap you closed as a proposal and give the reason.
- If the part is visual, a rough text sketch beside the description usually saves a round.

## Show it

When seeing beats reading, sketch in plain text: a few lines of what the screen or schedule would show. Keep sketches throwaway.

## Lay out the approaches

Once the what is clear, and before writing anything up, give the build options their own message:

1. Brainstorm widely, then cut: anything that works against the why, or that the current code makes awkward, goes.
2. Describe two or three survivors in terms of this project (which files, which libraries), with what each costs.
3. Name your pick and the reason, and ask for theirs. If they left the how to you, say you are going ahead with your pick.
4. When one option clearly wins, say why the rest fall short and move to the design next.

## A spike to learn something

When the open question is "would this feel right?" or "can this even work?", a few minutes of disposable code often answers it faster than talk. Offer one when that is the case; the prototype rules in feature planning apply (`../../feature-planning.md` § 5). Turning spike code into product code needs its own approval under the gate below.

## Write the design

With an approach picked, tell the user which size you think this is (they may disagree):

| Size | Design doc |
|---|---|
| Small change | a short note: what you agreed, a line or two per point |
| Project | the full design below |

Both sizes keep a short record of the options, their trade-offs, and the one chosen with its reason. Work that turns out bigger than first thought moves up to the full design, and you tell the user. Work that is really several projects gets an agreed order, and each is shaped separately.

The full design should let a competent builder write a plan with no further questions to the user. It covers: intent and why; goals, non-goals and failure cases; constraints; the approaches; the parts of the how the user decided, as they decided them; what is left to the builder. Put it where the project keeps design docs; otherwise `.ultimatum/specs/<slug>.md` (as in `../../feature-planning.md` § 6).

**Builder check (projects only).** Before handing over, ask a fresh read-only helper (`ultimatum:reviewer`) to read the design as the person who must plan from it and list every question it would have. Warn the user beforehand that this happens and may bring one more round of questions. Then put each question in one of three piles:

- **Answered already**, in the talk or the code: add the answer to the design.
- **Small**: any reasonable builder would land in the same place. Pick an answer, write it in, and flag it as your call.
- **For the user**: nobody else can answer it and it changes the result. Batch these into a single message, ordered by impact.

Revise the design, then send it with the list of calls you made on your own. The check gives at most that one extra round. With no helper available, do the builder's read yourself.

## The build gate

Nothing gets built until the user approves the design doc (the short one or the full one). Building means product code, scaffolding, installing packages, creating projects, or starting implementation. Reading and exploring are fine.

Exceptions: the user opted out of the talk, or approved a throwaway spike. "Sounds good" about an idea is not approval of a document they have not seen.

After approval, the next step is the plan (`plan-writing.md`).

## Traps

| Thought | Better |
|---|---|
| "A list of likely wants will speed this up" | Let them describe it first; your list narrows what they say. |
| "I'll fill in defaults quietly" | Say each default; one they never heard is one they could not refuse. |
| "Questions done, so I'll write the doc" | Send the approaches message first. |
| "Let me explain the process" | Ask the question; the process shows itself. |
| "The spike works, so build on it" | That needs approval like any other build. |
