# Compressing a memory or instruction file

Read when a `CLAUDE.md`, `AGENTS.md`, notes file or task list is loaded every session and the user wants it shorter, so it costs fewer input tokens.

Session handoffs are in `../../handoff.md`; trimming the project's own skill files is in `../../skill-author.md`. This file is about rewriting one prose file in a shorter register without changing what it instructs.

## Before you start

- **Ask for a file path.** If the user pastes text, offer to save it to a file first; do not compress loose text in chat, because there is then nothing to diff against.
- **Say where the text goes.** Compressing in this session keeps the text in this conversation. A script that sends the file to another model provider moves it off the machine; get the user's yes for that, and never send a file that holds secrets.
- **Keep the original.** Save it as a backup outside any folder the agent loads automatically, or the backup gets loaded too and the saving is lost. A path under `.ultimatum/` (git-ignored) works.

## What to cut

The prose cuts from `terse-voice.md` § Cuts that are safe, plus:

- "You should", "make sure to", "remember to", "always try to": state the action.
- Bullets that say the same thing twice in different words: keep one.
- Several examples of one pattern: keep the clearest.
- Long words where short ones say the same: "use" for "utilize", "fix" for "implement a solution for".

## What must come through byte for byte

- Fenced and indented code blocks, including their comments, spacing and line order.
- Inline code in backticks.
- URLs and link targets, file paths, commands, environment variables.
- Version numbers, dates and every other number.
- Names of tools, libraries, people and projects.
- Every heading's text, the nesting of lists, the numbering of numbered lists, table structure (cell text may shrink), and any YAML front matter.
- Every negation and condition. "Never push to main unless asked" must not become "push to main when asked".

Treat code blocks as read-only regions: compress only the prose between them, and do not merge sections across a block.

## Check the result mechanically

Run `python3 ../../../../../data/craft/caveman/check_compressed.py ORIGINAL COMPRESSED`. It compares the two files and fails (exit 1) if any fenced block, inline code span, URL, heading, number or negation word from the original is missing in the compressed copy. It reads only the two files and writes nothing.

Then read the compressed file once as the agent would: does every rule still say who does what, and when? If the check fails, fix the specific lines it names; do not compress the whole file again, which tends to lose something new.

Report the size before and after (bytes from `wc -c`; tokens only if you counted them with the provider's counter) and the backup path.

## Example

Original line:
> It is important that you always remember to run every test we have before any of your changes get pushed to `main`, since that is how we catch problems early.

Compressed:
> Run every test before pushing to `main`; that catches problems early.

`main` survived as code, the condition ("before pushing") survived, and nothing new was added. The example pair in `../../../../../data/craft/caveman/examples/` passes the checker; a third file there drops a negation and fails it.
