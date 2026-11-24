"""Shelf label text."""
from .logutil import trace


def shelf_label(sku: str, qty: int) -> str:
    trace(f"label {sku}")
    return f"{sku.upper():<10}{qty:>5}"
