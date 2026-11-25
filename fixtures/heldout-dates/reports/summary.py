from .dates import parse_report_date


def in_range(day_text: str, start_text: str, end_text: str) -> bool:
    return parse_report_date(start_text) <= parse_report_date(day_text) <= parse_report_date(end_text)
