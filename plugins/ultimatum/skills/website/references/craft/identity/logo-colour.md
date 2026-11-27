# Logo colour

Read after `logo.md` §1-3, when choosing the mark's colours. Palettes for the whole site come from `ult design system "<business>"` (our `colors.csv`); this file is about the mark.

## Start in black

Design and approve the mark in black first. Colour is added afterwards, and the black version stays as the one-colour fallback for stamps, receipts, embroidery and faxed forms.

## Choosing the colour

- **Count:** one main colour, at most two. Every extra colour costs in print, embroidery and signage.
- **Meaning is local and learned.** Colour associations vary by culture and by trade, and they change. Use them as a starting question ("what do rivals here use?"), not as rules. Red can read as urgent, festive, lucky or dangerous depending on where and what.
- **Differ from rivals.** Look at the five nearest competitors. If they all use the same blue, a different hue is the cheapest way to be remembered.
- **Fit the trade's expectations where trust matters** (health, law, money): a calm, readable colour; save surprises for the type or the symbol.
- **Check it reproduces.** Very saturated screen colours (bright greens, oranges, purples) shift in print. If the logo will be printed, ask the printer for the nearest CMYK or spot colour and look at a physical proof.

## Harmony when using two colours

| Approach | What it means | Use for |
|---|---|---|
| One hue, two values | a light and a dark of the same hue | calm, premium, safe in any setting |
| Neighbours | two hues next to each other on the wheel | warm or natural brands |
| Opposites | hues across the wheel | energetic brands; keep one dominant, the other small |

## Contrast

- WCAG 2.2 does not require contrast for logos (the logotype exception in SC 1.4.3), but an unreadable logo is still a problem. Aim for at least 3:1 against the backgrounds it sits on, the level SC 1.4.11 asks of meaningful graphics.
- Text placed next to the logo (taglines, nav labels) is ordinary text and needs 4.5:1.
- Never rely on colour alone to tell two versions apart (for example a red and a green dot meaning different things).

Check a pair with `python3 -c` and the WCAG formula, or any contrast checker; record the ratios in the logo rules page.

```python
def channel(v):
    v /= 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

def lum(colour):
    r, g, b = bytes.fromhex(colour.lstrip("#"))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

def ratio(a, b):
    light, dark = max(lum(a), lum(b)), min(lum(a), lum(b))
    return round((light + 0.05) / (dark + 0.05), 2)

print(ratio("#1F5C4A", "#FFFFFF"))  # 7.81
```

## Versions to deliver

Full colour on light, full colour on dark (often with a lighter tint of the main colour), one colour black, one colour white. Write each colour as hex for screen and the printer's CMYK or spot reference for print.
