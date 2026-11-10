"""Limiter configuration."""
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Config:
    rate: float = 5.0        # tokens added per second
    burst: int = 10          # default bucket capacity
    # Per-key burst overrides, e.g. {"vip-user": 50}
    burst_overrides: Dict[str, int] = field(default_factory=dict)

    # TODO(handoff): add override_for(key) lookup -> burst for that key
