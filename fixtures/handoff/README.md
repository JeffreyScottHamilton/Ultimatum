# ratelimit

Token-bucket rate limiter with per-key buckets.

    from ratelimit import Limiter
    lim = Limiter(rate=5, burst=10)       # 5 tokens/sec, burst 10
    lim.allow("user-1")                   # True / False

Configuration lives in `ratelimit/config.py`. Time is injectable (`clock=`)
so tests are deterministic.

Run tests: `python3 -m unittest`
