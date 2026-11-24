from datetime import date, datetime

_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d %b %Y")


def parse_due_date(text: str) -> date:
    """Parse a due date typed by a user."""
    cleaned = " ".join(str(text).split())
    for fmt in _FORMATS:
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"unrecognised due date: {text!r}")
