"""Helpers kept for the old CSV importer."""
import re


def clean_phone(raw: str) -> str:
    return re.sub(r"\D", "", raw)
