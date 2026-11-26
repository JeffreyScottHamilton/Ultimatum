# Interface words: labels, errors and states

Read when the words inside an interface (buttons, fields, errors, empty and loading states, help text) are vague or inconsistent and need a rewrite.

Page copy for marketing sections, voice and the tells that give copy away are in `../taste/copy.md` and `../taste/voice.md`; the content checks in a design audit are in `../design-review-qa/checklist-behaviour.md` § 8. Content and microcopy. This file covers the words that drive a task.

## Find the problems first

Read every string in place and mark:
- nouns and verbs that could mean two things ("Submit", "Process", "Item");
- internal names and team jargon the user never learned;
- states and outcomes that are not said ("Done" for what?);
- missing consequences, timing or a way to undo;
- the same thing called two names, or capitalised two ways;
- headings, intros and helper text that repeat each other;
- strings that break at real widths or when translated;
- tone that ignores the moment: a joke on an error, a shrug on a payment.

## Order inside a message

1. What the user must know at this moment.
2. What they can do about it.
3. Context that changes the decision, and nothing else.
4. A tone that fits what is at stake.

## By function

**Actions and links.** Name the outcome with a verb and object: "Save draft", "Send invoice", "Delete 3 files". The confirm button in a dialog repeats the verb from the question, never "OK". Links say where they go.

**Fields.** A visible label that stays visible (placeholders vanish when you type). Show the format before the user gets it wrong ("DD/MM/YYYY"). Mark the rarer case: if most fields are required, mark the optional ones.

**Errors and permissions.** What failed, why when it helps, how to recover. "Card declined. Your bank refused the payment. Try another card or call your bank." Never blame the user, never show a raw code alone. The status-code table is in `harden.md` § Errors.

**Destructive steps.** Say what will be lost and whether it can be undone. Prefer undo after the fact to a confirm dialog before it, when undo is possible.

**Loading.** Say what is happening ("Loading your invoices"). For waits over a few seconds, give progress or an estimate.

**Empty.** Why it is empty, and the one action that fills it. A first-use empty state teaches; a "no results" state says what was searched and offers to widen it.

**Success.** Confirm the result and its location ("Saved to Drafts"). Match the size of the response to the effort: a small toast for a small save, more for a finished setup.

**Help text.** Put it at the point of use, short, and only where people get stuck. If a field needs a paragraph, the field is probably wrong.

## Language, access and translation

- Write full sentences with named slots (`{count} files moved to {folder}`) so translators can reorder them; never join fragments.
- Keep numbers and names as variables, not baked into strings.
- Leave room for expansion instead of abbreviating early.
- Alt text carries the image's meaning; decoration gets empty alt.
- The accessible name of a control starts with its visible label (WCAG 2.5.3 Label in Name).
- Never let colour, an icon or punctuation carry the message alone.

## Check

- Someone new to the product understands each string without help.
- Every error, empty state and decision point offers an action.
- Facts are correct and terms are the same everywhere.
- Strings still read at the narrowest width and at 200% zoom.
- Long names, translated text, plurals and live values fit.
- State changes are announced to screen readers (a polite live region for status; see <https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/status_role>).
- Ask the owner before changing any claim, price or legal wording; those are facts, not copy.
