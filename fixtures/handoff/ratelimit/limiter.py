import time

from .bucket import TokenBucket
from .config import Config


class Limiter:
    def __init__(self, rate=5.0, burst=10, clock=time.monotonic, config=None):
        self.config = config or Config(rate=rate, burst=burst)
        self.clock = clock
        self._buckets = {}

    def _bucket_for(self, key):
        b = self._buckets.get(key)
        if b is None:
            # TODO(handoff): use config.override_for(key) once it exists
            capacity = self.config.burst
            b = self._buckets[key] = TokenBucket(self.config.rate, capacity, self.clock)
        return b

    def allow(self, key, cost=1):
        return self._bucket_for(key).take(cost)
