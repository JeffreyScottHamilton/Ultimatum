from datetime import date

from .dates import parse_due_date


def days_until(due_text: str, today: date) -> int:
    return (parse_due_date(due_text) - today).days
