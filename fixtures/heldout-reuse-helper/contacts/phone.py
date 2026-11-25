"""Phone number normalisation (E.164, default region US)."""
import re


def normalize_phone(raw: str, default_cc: str = "1") -> str:
    """Return the number as +<country><digits>; raise ValueError if it is not a plausible number."""
    text = raw.strip()
    digits = re.sub(r"\D", "", text)
    if text.startswith("+"):
        out = digits
    elif text.startswith("00"):
        out = digits[2:]
    elif len(digits) == 11 and digits.startswith(default_cc):
        out = digits
    else:
        out = default_cc + digits
    if not 8 <= len(out) <= 15:
        raise ValueError(f"not a plausible phone number: {raw!r}")
    return "+" + out
