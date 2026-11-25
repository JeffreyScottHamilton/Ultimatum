class TokenBucket:
    """Classic token bucket. `capacity` is the burst size."""

    def __init__(self, rate, capacity, clock):
        self.rate = rate
        self.capacity = capacity
        self.clock = clock
        self.tokens = float(capacity)
        self.updated = clock()

    def _refill(self):
        now = self.clock()
        self.tokens = min(self.capacity, self.tokens + (now - self.updated) * self.rate)
        self.updated = now

    def take(self, n=1):
        self._refill()
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False
