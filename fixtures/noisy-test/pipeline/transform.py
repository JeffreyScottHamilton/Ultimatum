from . import clean, parse
from .logutil import log


def to_record(raw):
    log("transform", "to_record")
    rec = clean.normalize_keys(clean.drop_empty(clean.strip_fields(raw)))
    out = dict(rec)
    if "amount" in rec:
        out["amount"] = parse.parse_amount(rec["amount"])
    if "date" in rec:
        out["date"] = parse.parse_date(rec["date"])
    if "qty" in rec:
        out["qty"] = parse.parse_int(rec["qty"])
    return out


def total(records):
    log("transform", f"total of {len(records)}")
    return round(sum(r.get("amount", 0) * r.get("qty", 1) for r in records), 2)


def group_by(records, key):
    log("transform", f"group_by {key}")
    groups = {}
    for r in records:
        groups.setdefault(r.get(key), []).append(r)
    return groups
