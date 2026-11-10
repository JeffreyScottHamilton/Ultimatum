from .logutil import log


def require(rec, *fields):
    log("validate", f"require {fields}")
    missing = [f for f in fields if f not in rec]
    if missing:
        raise ValueError("missing: " + ", ".join(missing))
    return rec


def positive_amount(rec):
    log("validate", "positive_amount")
    if rec.get("amount", 0) <= 0:
        raise ValueError("amount must be positive")
    return rec


def in_range(value, lo, hi):
    log("validate", f"range {lo}..{hi}")
    return lo <= value <= hi
