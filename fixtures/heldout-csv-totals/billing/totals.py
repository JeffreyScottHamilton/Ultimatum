"""Line and invoice totals, in integer cents."""


def line_total_cents(unit_price: str, qty: int, tax_pct: str) -> int:
    net = float(unit_price) * int(qty)
    gross = net * (1 + float(tax_pct) / 100)
    return int(round(gross * 100))


def invoice_total_cents(rows) -> int:
    return sum(line_total_cents(r["unit_price"], r["qty"], r["tax_pct"]) for r in rows)
