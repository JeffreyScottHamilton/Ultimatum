"""Stock level arithmetic."""
from .logutil import trace


def reorder_qty(on_hand: int, target: int, pack_size: int) -> int:
    """Units to order so stock reaches `target`, in whole packs."""
    need = target - on_hand
    if need <= 0:
        return 0
    packs = need // pack_size
    trace(f"reorder need={need} packs={packs}")
    return packs * pack_size


def apply_events(level: int, events) -> int:
    for kind, n in events:
        trace(f"event {kind} {n}")
        if kind == "in":
            level += n
        elif kind == "out":
            level = max(0, level - n)
    return level
