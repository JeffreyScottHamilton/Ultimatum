"""Unit price helpers."""
from .logutil import trace


def bulk_price(unit_cents: int, qty: int) -> int:
    trace(f"price {unit_cents} x {qty}")
    pct = 10 if qty >= 100 else 5 if qty >= 20 else 0
    return unit_cents * qty * (100 - pct) // 100
