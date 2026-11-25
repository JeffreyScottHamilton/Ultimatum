from .logutil import log, legacy


def strip_fields(rec):
    log("clean", f"strip {len(rec)} fields")
    return {k: v.strip() if isinstance(v, str) else v for k, v in rec.items()}


def drop_empty(rec):
    log("clean", "drop empty")
    return {k: v for k, v in rec.items() if v not in ("", None)}


def normalize_keys(rec):
    log("clean", "normalize keys")
    return {k.strip().lower().replace(" ", "_"): v for k, v in rec.items()}


def squash_spaces(s):
    legacy("squash_spaces")
    return " ".join(s.split())
