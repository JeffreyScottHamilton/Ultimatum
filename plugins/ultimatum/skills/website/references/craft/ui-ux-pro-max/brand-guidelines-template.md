# Brand guidelines: a starter template

Read when writing a brand's guidelines file for the first time (step 2 of `brand-flow.md`). Copy the block below to `docs/brand-guidelines.md`, fill every `<...>` from the owner's facts, and delete any section the brand does not need. A gap stays visible as `GAP (owner): ...` rather than being filled with a guess.

## How to fill it

- Fill in the order of `brand-flow.md`: voice first, then visuals, assets, review.
- Each value appears once here and once in the token file; the token names in the tables are the link between them. After editing, regenerate tokens with `tools/build_tokens.py`.
- Keep it short. A guide people read is 3-8 printed pages; detail lives in the token file and the asset library.
- The summary card at the top is what most people will read. Keep it current.

## The template

````markdown
# <Brand name> brand guidelines

Version <n>; updated <yyyy-mm-dd>; owner: <name, role>; tokens: `<path to tokens file>`

## Summary card

| | |
|---|---|
| Promise | <one sentence> |
| Voice | <trait>, <trait>, <trait> |
| Brand colour | <name> `<hex>` (token `--color-<family>-<step>`) |
| Type | <display family> for headings, <text family> for body |
| Logo | full lockup above <n> px wide; symbol below |
| Never | <the one thing the brand must not look or sound like> |

## 1. Voice and messaging

Sliders (1-5): distance <n>, weight <n>, words <n>, energy <n>.

| Trait | Means here | Stop before | Sounds like | Does not sound like |
|---|---|---|---|---|
| <trait> | <meaning> | <fence> | "<real line>" | "<bad line>" |

Tone by moment:

| Moment | Reader feels | Tone |
|---|---|---|
| <moment> | <feeling> | <shift> |

Words: we say <word> (not <word>); product names <exact spellings>; we never say <words>.

Purpose: <sentence>
Promise: <sentence>
Positioning: <paragraph: for whom, in what situation, compared with what, why believe it>
Proof points: <claim — evidence>, ...
Pitch, one line: <...>; three sentences: <...>; one minute: <...>

## 2. Colour

| Role | Name | Hex | Token | Text on it | Ratio |
|---|---|---|---|---|---|
| brand | <name> | `<hex>` | `--color-<family>-<step>` | <white or dark> | <n>:1 |
| support | <name> | `<hex>` | `--color-<family>-<step>` | <...> | <n>:1 |
| neutral text | <name> | `<hex>` | `--color-<neutral>-<step>` | on background | <n>:1 |
| danger / warning / success / info | <names> | `<hex>` | `--color-<family>-<step>` | <...> | <n>:1 |

Semantic roles (light / dark): background, foreground, primary, primary-foreground, muted, muted-foreground, border, ring, destructive. Mapping lives in the token file.

Use: neutrals for most of the area; brand colour for the main action and key highlights only. Status colours carry meaning only, always with a word or icon.

## 3. Type

| Role | Family | Weights | Source and licence | Fallback |
|---|---|---|---|---|
| display | <family> | <weights> | <link>, <licence> | <stack> |
| text | <family> | <weights> | <link>, <licence> | <stack> |

| Token | Size | Line height | Weight | Use |
|---|---|---|---|---|
| `--text-base` | 16 px | <n> | 400 | body |
| <...> | | | | |

Body measure about 65 characters. Body never below 16 px on screens.

## 4. Logo

Versions: <full lockup, symbol, wordmark; colour, one-colour, reversed>, files in `brand/core/logo/`.
Clear space: <unit taken from the mark> on every side.
Minimum width: lockup <n> px / <n> mm; symbol <n> px / <n> mm.
Approved grounds: <white, darkest neutral, brand colour, photo with scrim>.
Never: stretch, rotate, recolour, add effects, rearrange, re-typeset, place on a failing ground.
Partners: <rule, or "none yet">.

## 5. Imagery and icons

Photo style: <subject, light, grade, framing, people>. Avoid: <...>.
Illustration: <style, or "none">.
Icons: <set name>, <stroke weight>, <size steps>.

## 6. Components in brief

Buttons, fields and cards follow the design system (`<path to component specs>`): main action uses `--primary`; corner radius `--radius` = <value>; spacing steps from `--spacing` = <value>.

## 7. Assets

Root: `<path or shared drive>`. Naming: `<kind>_<subject>_<variant>_<size>_<yyyymmdd>_v<n>.<ext>`. Rights recorded per asset.

## 8. Review

Every piece passes the approval gate before release; brand owner signs; legal signs for claims and regulated topics. Consistency audit every <quarter>.

## Change log

| Date | Change | Why | By |
|---|---|---|---|
| <yyyy-mm-dd> | first version | <...> | <name> |
````

## After filling it

- Check the summary card against the sections: one value, one place.
- Run the generator's contrast check and paste its result into the colour table's Ratio column.
- Send the list of GAP lines to the owner in one message.
