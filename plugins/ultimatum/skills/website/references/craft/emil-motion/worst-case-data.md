# Worst-case data: break a component before users do

Read when a list row, card, table, profile, pricing tile or form looks right with demo data and must survive real data. Value catalogue: `../../../../../data/craft/emil-motion/worst-case.csv`. It applies to local-business pages too (a customer review with a very long name, a service with no price, a staff list with one person) and to app screens.

## Posture

Be the most awkward real user. The demo names fit on one line, counts never need a separator and every optional field is filled; undo that choice field by field. Two failures to avoid, the first worse: nonsense data (a 5,000-letter name; the designer rightly says "never happens"), and stopping at long text (the shipped bugs are the one-letter name, the missing avatar, "1 members", the empty list, the translated label).

## Rules

1. Believable or bounded. Use a value that real people produce, or the hard limit set by the form schema, the database column or the API type. When no limit exists, record it as "unbounded" and try a long value that is still plausible.
2. Alter the data, leave the component alone. Worst-case values arrive through the same fixture, mock or props that carry the demo data; markup edited by hand only tests your edit.
3. One dataset, many failures, mixed across rows (row 1 long name, row 2 long email, row 3 one-letter name). The first rows are the ones on screen.
4. The toggle is dev only. Gate it behind the dev environment or a prototype route.
5. Report first, then fix on request. Some breaks are decisions (truncate or wrap?).
6. Use `example.com`, `example.org` or `.test` for emails and URLs so fixtures never reach real inboxes.

## Phases

1. Map: table every rendered value with source, type, limit, optional or not. Include counts in headers, relative times, badges, labels from data, tooltips, avatar images and the list length. Where front and back limits differ (50 in the form, 255 in the column), note it.
2. Build: pick values from the CSV for each field; add Empty, One and Huge (1,000+ rows if unpaginated) as extra fixtures or toggle positions.
3. Toggle: a segmented control (Demo, Worst case, Empty, One, many rows) at the bottom centre, plain chrome, swapping data at the boundary, selection kept in the URL (for example `?data=worst`). With no project, one self-contained HTML file with both datasets inline.
4. Break it at the real container width, at 320 px, at the widest layout, at 200 % zoom, in dark mode and in RTL if supported. Screenshot if tooling allows; otherwise say which findings you inferred.
5. Report, then stop. 6. Fix what was chosen, then flip every state again, the demo too, so a fix does not regress it. Keep the fixture as a regression test.

## Failure signatures

| You see | Cause | Fix |
|---|---|---|
| Avatar or icon squashed to an oval | flex child shrinking | `flex-shrink: 0` |
| Text spills out of its box | a flex or grid child left at `min-width: auto` | give the text column `min-width: 0` (in grids the track becomes `minmax(0, 1fr)`) |
| An email or URL overruns the edge | the string has no break points | `overflow-wrap: anywhere` |
| Trailing action pushed off or clipped | the middle column claimed everything | the middle gets `min-width: 0`, the action `flex-shrink: 0` |
| Badge breaks onto two lines | badge may shrink | keep it on one line and unshrinkable; choose what gives way instead |
| Avatar floats beside a three-line name | centred alignment in rows of unequal height | align to the top once text can wrap |
| Last row cut mid-glyph | fixed height, no fade or scroll cue | scrollbar or fade mask |
| Heading breaks mid-word | `word-break: break-all` | `overflow-wrap: anywhere` |
| Wrong initials ("J", "CI", a broken emoji half) | `split(' ')[0][0]` code | graphemes via `Intl.Segmenter`, first and last word, icon fallback |
| A stray dash or blank line | a placeholder printed for an absent optional field | leave the line out, or keep its height deliberately |
| "1 members" | hardcoded plural | `Intl.PluralRules` |
| Numbers jitter, columns drift | proportional digits | `tabular-nums` |
| `1284`, `NaN`, `undefined`, long floats | raw number printed | `Intl.NumberFormat`, guard null |
| Long translated button overflows | fixed `width` | `min-width` with content-sized width |
| Accents or Thai marks cut off | small `line-height` combined with `overflow: hidden` | give text more line height and do not clip it |
| Broken image icon | no error fallback | initials fallback, `object-fit: cover` |
| Ellipsis with no way to read the rest | truncation only | `title` or tooltip, full value in a detail view |
| 1,000 rows stutter | all rendered | virtualise or paginate (`libraries-and-toasts.md`) |
| Literal `<b>`, `&amp;`, `**text**` on screen | escaping happens at the wrong layer | escape one time, when rendering; keep user data out of `dangerouslySetInnerHTML` |

## Truncate, wrap or clamp: decide per field

Wrap what must be read in full to identify (names, detail titles; two lines fine, four means a narrow column). Truncate the end for secondary text whose start matters, and pair it with a way to read all. Cut from the middle when items differ only at the tail (file names, emails on one domain, paths, hashes). Clamp (`line-clamp: 2`) for card previews so heights stay predictable. Numbers, amounts, dates and anything people compare are never cut.

## Report

One row per break, worst first: number, severity, field, value, what happens, fix. Severity levels: Broken (unreadable, unreachable, wrong data), Ugly (readable but plainly off), Fragile (works today, a realistic input away from failing, for instance no limit or no fallback). Say which rows you saw rendered and which you reasoned from the CSS.

Deeper: `../impeccable/harden.md` covers languages, scripts, error states by status and interrupted gestures.
