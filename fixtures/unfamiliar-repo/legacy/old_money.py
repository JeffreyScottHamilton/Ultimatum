# DEPRECATED: do not use. Superseded by billing/money.py. Kept only for
# reference until the old batch scripts are retired.
# Known issues: floors instead of rounding, wrong for negatives, no thousands separator.

def fmt(amount, cur="USD"):
    return "%s%d.%d" % ("$" if cur == "USD" else cur, amount / 100, amount % 100)
