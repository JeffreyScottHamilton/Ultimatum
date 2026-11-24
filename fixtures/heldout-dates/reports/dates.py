from datetime import date, datetime

FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d %b %Y")


def parse_report_date(value: str) -> date:
    """Parse a report date typed by a user."""
    cleaned = " ".join(str(value).split())
    for fmt in FORMATS:
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"unrecognised report date: {value!r}")
