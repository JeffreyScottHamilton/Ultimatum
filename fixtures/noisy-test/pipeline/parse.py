"""Parsing of raw string fields."""
import re
from datetime import date

from .logutil import log, legacy


def parse_amount(raw):
    """Parse '$1,234.56', '1234.56', '-12', and European '1.234,56' to float."""
    s = raw.strip().replace("$", "").replace("€", "").replace(" ", "")
    neg = s.startswith("-") or (s.startswith("(") and s.endswith(")"))
    s = s.strip("-()")
    if "," in s and s.rfind(",") > s.rfind("."):
        # European style: '.' groups thousands, ',' is the decimal mark
        s = s.replace(".", "")
        whole, _, frac = s.partition(",")
        s = whole + "." + frac[:1]
    else:
        s = s.replace(",", "")
    log("parse", f"amount {raw!r} -> {s}")
    value = float(s)
    return -value if neg else value


def parse_int(raw):
    s = raw.strip().replace(",", "").replace("_", "")
    log("parse", f"int {raw!r}")
    return int(s)


def parse_date(raw):
    """Accepts YYYY-MM-DD and DD/MM/YYYY."""
    raw = raw.strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", raw)
    if m:
        y, mo, d = map(int, m.groups())
    else:
        m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", raw)
        if not m:
            raise ValueError(f"unrecognized date: {raw!r}")
        d, mo, y = map(int, m.groups())
    log("parse", f"date {raw!r}")
    return date(y, mo, d)


def parse_bool(raw):
    legacy("parse_bool")
    return raw.strip().lower() in {"1", "true", "yes", "y"}
