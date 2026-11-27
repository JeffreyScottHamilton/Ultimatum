# Superpowers: a choice board for questions better seen than read

Read when, while shaping a request, the user has to choose between layouts, colours, diagrams or other things they would judge by looking, and a text sketch (`shaping-conversation.md` § Show it) is not enough.

## Seen or read

Decide question by question. Ask: would they answer faster from a picture? Picking between two page layouts, three accent colours or two flow diagrams: yes, build a board. Which features are in scope, which library, what a word means, a list of trade-offs: no, ask in the chat. A question about a screen is not automatically a visual question; "what should settings hold?" is words, "which of these settings pages?" is a picture.

`choice_board.py check` warns `visual` when a question shows nothing, which is that rule caught after the fact.

## The tool

`../../../../../data/craft/superpowers/choice_board.py` is standard-library Python. It writes one HTML file that needs no server, no open port, no network and no install. Each question is a group of cards the user clicks (one pick or many), with an optional note, and the page builds one answer line from what they picked. They copy that line and paste it into the chat. In a cloud session, where a local port is unreachable, the file still opens anywhere: send it to the user or publish it as a page.

```bash
python3 choice_board.py check spec.json
python3 choice_board.py build spec.json --out board.html
python3 choice_board.py read spec.json 'pick homepage-direction: layout=b; accents=moss,ink; note="warmer"'
```

Run these from `data/craft/superpowers/` in the installed plugin. `read` prints the picks, their labels, the note and any question left unanswered, as JSON. It exits 1 when the line names a question or option the spec lacks, gives two picks where one was asked, or came from a different board, so a mistyped or stale answer is caught rather than guessed at.

## The spec

```json
{"title": "Homepage direction", "intro": "Two quick picks before I build the page.",
 "questions": [
  {"id": "layout", "prompt": "Which layout reads best?", "options": [
    {"id": "a", "label": "Single column", "note": "One path down the page.", "show": "<svg ...>...</svg>"},
    {"id": "b", "label": "Split hero", "image": "mock-b.png", "alt": "Words left, product shot right"}]},
  {"id": "accents", "prompt": "Which accents could work?", "pick": "many", "options": [ ... ]}]}
```

- `show` is an inline SVG or HTML fragment; `image` is a local file, embedded into the page. Paths are relative to the spec.
- `pick` is `one` (default) or `many`. `note` under a question replaces the "Pick one." hint.
- `board` sets the name in the answer line; otherwise it comes from the title.

## Rules

`choice_board.py rules` prints these; `build` refuses to write while any error stands.

| Rule | Level | What it guards |
|---|---|---|
| `ids` | error | ids are short lower-case words with hyphens and unique, so the answer line is unambiguous |
| `label` | error | every question has a prompt and every option a label; screen readers and the answer line use them |
| `offline` | error | fragments carry no scripts, event handlers, frames, forms or remote URLs, so the page stays inert and private |
| `image` | error | images are local PNG, JPEG, GIF, WebP or SVG files of 2 MB or less |
| `too-many` | warn | a pick-one question has four options or fewer; beyond that the user reads instead of seeing |
| `visual` | warn | something is shown; a words-only question belongs in the chat |

The page sets a content policy that allows only its own script (by hash), inline styles and embedded images, so a fragment that slipped past `offline` still cannot run or call out. Inputs are real radio buttons and checkboxes inside labelled groups: keyboard and screen reader work without extra code, the focus ring shows, picked cards say "Picked" in words as well as colour, and the page follows the system's light or dark setting (`--theme` forces one).

## The loop

1. Ask in words first. Build a board only for the questions that pass the seen-or-read test.
2. Draw the options yourself: inline SVG wireframes or colour tiles are enough. Keep each option honest; a board is for choosing, not selling the option you prefer.
3. `check`, then `build`. Open it at phone width once (`../../../../website/references/craft/design-review-qa/render-check.md` covers a rendered check) before you send it.
4. Send or publish the file. Say in one line what is on it, and ask them to paste the answer line, or just tell you in words.
5. `read` what they paste. Their words in the chat win where they differ from the line.
6. If the answer changes the design, build the next board as a new file (`layout-2.html`), never over the old one, so the trail of choices stays.

## Where boards live

Build into the scratch directory or `.ultimatum/boards/`, which is ignored by git. A board is a working note for one decision; do not commit it unless the user asks. It can hold mock-ups of unreleased work, so publish it privately and only on the user's say.
